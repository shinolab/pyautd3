#!/usr/bin/env python3


import argparse
import ast
import contextlib
import glob
import os
import pathlib
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import urllib.request
from typing import Optional


def err(msg: str):
    print("\033[91mERR \033[0m: " + msg)


def rm_f(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def onexc(func, path, exeption):
    import stat

    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


def rmtree_f(path):
    try:
        shutil.rmtree(path, onerror=onexc)
    except FileNotFoundError:
        pass


def glob_norm(path, recursive):
    return [os.path.normpath(p) for p in glob.glob(path, recursive=recursive)]


def rm_glob_f(path, exclude=None, recursive=True):
    if exclude is not None:
        for f in list(set(glob_norm(path, recursive=recursive)) - set(glob_norm(exclude, recursive=recursive))):
            rm_f(f)
    else:
        for f in glob.glob(path, recursive=recursive):
            rm_f(f)


def rmtree_glob_f(path, exclude=None, recursive=True):
    if exclude is not None:
        for f in list(set(glob_norm(path, recursive=recursive)) - set(glob_norm(exclude, recursive=recursive))):
            rmtree_f(f)
    else:
        for f in glob.glob(path, recursive=recursive):
            rmtree_f(f)


@contextlib.contextmanager
def working_dir(path):
    cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(cwd)


def fetch_submodule():
    if shutil.which("git") is not None:
        with working_dir(os.path.dirname(os.path.abspath(__file__))):
            subprocess.run(["git", "submodule", "update", "--init"]).check_returncode()
    else:
        err("git is not installed. Skip fetching submodules.")


def generate_wrapper():
    if shutil.which("cargo") is not None:
        with working_dir(os.path.dirname(os.path.abspath(__file__))):
            with working_dir("tools/wrapper-generator"):
                subprocess.run(
                    [
                        "cargo",
                        "run",
                    ],
                ).check_returncode()
    else:
        err("cargo is not installed. Skip generating wrapper.")


class PyiGenerator(ast.NodeVisitor):
    def __init__(self):
        self.class_defs = []
        self.has_builder_decorator = False

    def visit_ClassDef(self, node):  # noqa: N802
        has_builder_decorator = any(d.id == "builder" for d in node.decorator_list if isinstance(d, ast.Name))

        class_name = node.name
        base_classes = [self._get_type_annotation(base) for base in node.bases]
        attributes = []
        async_methods = []
        methods = []
        staticmethods = []
        classmethods = []
        properties = []

        for body_item in node.body:
            match body_item:
                case ast.AnnAssign(target=ast.Name(id=attr_name), annotation=annotation):
                    if not attr_name.startswith("_param_") and not attr_name.startswith("_prop_"):
                        attr_type = self._get_type_annotation(annotation)
                        attributes.append((attr_name, attr_type))
                case ast.AsyncFunctionDef(
                    name=method_name,
                    args=ast.arguments(args=args, defaults=defaults),
                    returns=returns,
                    decorator_list=decorators,
                ):
                    return_type = self._get_type_annotation(returns)
                    args = [(arg.arg, self._get_type_annotation(arg.annotation)) for arg in args[1:]]
                    defaults = [self._get_value_expr(d) for d in defaults]
                    async_methods.append((method_name, args, defaults, return_type))
                case ast.FunctionDef(
                    name=method_name,
                    args=ast.arguments(args=args, defaults=defaults),
                    returns=returns,
                    decorator_list=decorators,
                ):
                    if any(d.id == "property" for d in decorators if isinstance(d, ast.Name)):
                        return_type = self._get_type_annotation(returns)
                        properties.append((method_name, return_type))
                    elif any(d.id == "staticmethod" for d in decorators if isinstance(d, ast.Name)):
                        return_type = self._get_type_annotation(returns)
                        args = [(arg.arg, self._get_type_annotation(arg.annotation)) for arg in args]
                        staticmethods.append((method_name, args, return_type))
                    elif any(d.id == "classmethod" for d in decorators if isinstance(d, ast.Name)):
                        return_type = self._get_type_annotation(returns)
                        args = [(arg.arg, self._get_type_annotation(arg.annotation)) for arg in args[1:]]
                        classmethods.append((method_name, args, return_type))
                    else:
                        return_type = self._get_type_annotation(returns)
                        args = [(arg.arg, self._get_type_annotation(arg.annotation)) for arg in args[1:]]
                        defaults = [self._get_value_expr(d) for d in defaults]
                        methods.append((method_name, args, defaults, return_type))

        if has_builder_decorator:
            self.has_builder_decorator = True
            fields = {}
            for class_node in node.body:
                match class_node:
                    case ast.AnnAssign(target=ast.Name(id=attr_name), annotation=annotation):
                        fields[class_node.target.id] = self._get_type_annotation(class_node.annotation)

            for field_name, field_type in fields.items():
                if field_name.startswith("_param_"):
                    prop_name = field_name[7:]
                    if field_name.endswith("_u8"):
                        prop_name = prop_name[:-3]
                    properties.append((prop_name, field_type))
                    if field_type == "EmitIntensity":
                        field_type = "int | EmitIntensity"
                    elif field_type == "Phase":
                        field_type = "int | Phase"
                    methods.append(
                        (
                            f"with_{prop_name}",
                            [(prop_name, field_type)],
                            [],
                            class_name,
                        ),
                    )

                if field_name.startswith("_prop_"):
                    properties.append((field_name[6:], field_type))

        self.class_defs.append((class_name, base_classes, attributes, async_methods, methods, staticmethods, classmethods, properties))

    def _get_value_expr(self, expr):
        match expr:
            case ast.Constant(value=value):
                return value
            case ast.Name(id=id):
                return id
            case _:
                return "None"

    def _get_type_annotation(self, annotation):
        match annotation:
            case ast.Name(id=id):
                return id
            case ast.Constant(value=value):
                return str(value)
            case ast.Subscript(value=value, slice=sl):
                return f"{self._get_type_annotation(value)}[{self._get_type_annotation(sl)}]"
            case ast.Tuple(elts=elts):
                return f"{', '.join([self._get_type_annotation(elt) for elt in elts])}"
            case ast.List(elts=elts):
                return f"[{', '.join([self._get_type_annotation(elt) for elt in elts])}]"
            case ast.BinOp(left=left, op=ast.BitOr(), right=right):
                return f"{self._get_type_annotation(left)} | {self._get_type_annotation(right)}"
            case ast.Attribute(value=value, attr=attr):
                return f"{self._get_type_annotation(value)}.{attr}"
            case None:
                return "None"
            case _:
                return ""

    def generate_pyi(self):
        lines = []
        for class_name, base_classes, attributes, async_methods, methods, staticmethods, classmethods, properties in self.class_defs:
            lines.append(f"class {class_name}({', '.join(base_classes)}):")
            for attr_name, attr_type in attributes:
                lines.append(f"    {attr_name}: {attr_type}")
            for method_name, args, defaults, return_type in async_methods:
                defaults = ["None"] * (len(args) - len(defaults)) + defaults
                args_str = ", ".join(
                    [f"{name}: {ty}" + (f" = {default}" if default != "None" else "") for (name, ty), default in zip(args, defaults, strict=True)],
                )
                lines.append(f"    async def {method_name}(self, {args_str}) -> {return_type}: ...")
            for method_name, args, defaults, return_type in methods:
                defaults = ["None"] * (len(args) - len(defaults)) + defaults
                args_str = ", ".join(
                    [f"{name}: {ty}" + (f" = {default}" if default != "None" else "") for (name, ty), default in zip(args, defaults, strict=True)],
                )
                lines.append(f"    def {method_name}(self, {args_str}) -> {return_type}: ...")
            for method_name, args, return_type in staticmethods:
                args_str = ", ".join([f"{name}: {ty}" for name, ty in args])
                lines.append("    @staticmethod")
                lines.append(f"    def {method_name}({args_str}) -> {return_type}: ...")
            for method_name, args, return_type in classmethods:
                args_str = ", ".join([f"{name}: {ty}" for name, ty in args])
                lines.append("    @classmethod")
                lines.append(f"    def {method_name}(cls, {args_str}) -> {return_type}: ...")
            for prop_name, prop_type in properties:
                lines.append("    @property")
                lines.append(f"    def {prop_name}(self) -> {prop_type}: ...")
            lines.append("")
        return "\n".join(lines)


def gen_pyi():
    re_import = re.compile(r"(\s*)from (.*) import (.*)")
    re_import_as = re.compile(r"import (.*) as (.*)")
    re_typevar = re.compile(r"(.*) = TypeVar\((.*)\)")
    with working_dir(os.path.dirname(os.path.abspath(__file__))):
        files = set(glob.glob(str(pathlib.Path("pyautd3") / "**" / "*.py"), recursive=True)) - set(
            glob.glob(str(pathlib.Path("pyautd3") / "derive" / "*.py"), recursive=True),
        )
        for file in files:
            with open(file, "r", encoding="utf8") as f:
                content = f.read()
                tree = ast.parse(content, type_comments=True)
                generator = PyiGenerator()
                generator.visit(tree)

            if generator.has_builder_decorator:
                imports = []
                typevars = []

                for line in content.split("\n"):
                    match = re_import.match(line)
                    if match and line != "from pyautd3.derive.builder import builder":
                        imports.append(f"from {match.group(2)} import {match.group(3)}")
                    match = re_import_as.match(line)
                    if match:
                        imports.append(match.group(0))
                    match = re_typevar.match(line)
                    if match:
                        typevars.append(match.group(0))

                pyi_code = generator.generate_pyi()
                with open(file.replace(".py", ".pyi"), "w", encoding="utf8") as f:
                    f.write("\n".join(imports))
                    f.write("\n\n")
                    f.write("\n".join(typevars))
                    f.write("\n\n")
                    f.write(pyi_code)


class Config:
    _platform: str
    release: bool
    target: Optional[str]

    def __init__(self, args):
        self._platform = platform.system()

        if not self.is_windows() and not self.is_macos() and not self.is_linux():
            err(f'platform "{platform.system()}" is not supported.')
            sys.exit(-1)

        self.release = hasattr(args, "release") and args.release

        machine = platform.machine().lower()
        if hasattr(args, "arch") and args.arch is not None:
            machine = args.arch.lower()
        if machine in ["amd64", "x86_64"]:
            self.arch = "x64"
        elif machine in ["arm64", "aarch64"]:
            self.arch = "aarch64"
        elif machine in ["arm32", "armv7l"]:
            self.arch = "armv7l"
        else:
            err(f"Unsupported platform: {machine}")

    def is_windows(self):
        return self._platform == "Windows"

    def is_macos(self):
        return self._platform == "Darwin"

    def is_linux(self):
        return self._platform == "Linux"

    def is_pcap_available(self):
        if not self.is_windows():
            return True
        wpcap_exists = os.path.isfile("C:\\Windows\\System32\\wpcap.dll") and os.path.isfile("C:\\Windows\\System32\\Npcap\\wpcap.dll")
        packet_exists = os.path.isfile("C:\\Windows\\System32\\Packet.dll") and os.path.isfile("C:\\Windows\\System32\\Npcap\\Packet.dll")

        return wpcap_exists and packet_exists


def build_wheel(config: Config):
    with working_dir("."):
        if config.is_windows():
            with open("setup.cfg.template", "r") as setup:
                content = setup.read()
                content = content.replace(r"${classifiers_os}", "Operating System :: Microsoft :: Windows")
                match config.arch:
                    case "x64":
                        plat_name = "win-amd64"
                    case "aarch64":
                        plat_name = "win-arm64"
                    case _:
                        err(f"Unsupported architecture: {config.arch}")
                content = content.replace(r"${plat_name}", plat_name)
                with open("setup.cfg", "w") as f:
                    f.write(content)
            subprocess.run(["uv", "build"]).check_returncode()
        elif config.is_macos():
            with open("setup.cfg.template", "r") as setup:
                content = setup.read()
                content = content.replace(r"${classifiers_os}", "Operating System :: MacOS :: MacOS X")
                content = content.replace(r"${plat_name}", "macosx-11-0-arm64")
                with open("setup.cfg", "w") as f:
                    f.write(content)
            subprocess.run(["uv", "build"]).check_returncode()
        elif config.is_linux():
            with open("setup.cfg.template", "r") as setup:
                content = setup.read()
                content = content.replace(r"${classifiers_os}", "Operating System :: POSIX")
                match config.arch:
                    case "x64":
                        plat_name = "manylinux1_x86_64"
                    case "aarch64":
                        plat_name = "manylinux2014_aarch64"
                    case "armv7l":
                        plat_name = "linux_armv7l"
                content = content.replace(r"${plat_name}", plat_name)
                with open("setup.cfg", "w") as f:
                    f.write(content)
            subprocess.run(["uv", "build"]).check_returncode()


def should_update_dll(config: Config, version: str) -> bool:
    if config.is_windows():
        if not os.path.isfile("pyautd3/bin/autd3capi.dll"):
            return True
    elif config.is_macos():
        if not os.path.isfile("pyautd3/bin/libautd3capi.dylib"):
            return True
    elif config.is_linux():
        if not os.path.isfile("pyautd3/bin/libautd3capi.so"):
            return True

    if not os.path.isfile("VERSION"):
        return True

    with open("VERSION", "r") as f:
        old_version = f.read().strip()

    return old_version != version


def copy_dll(config: Config):
    with open("pyautd3/__init__.py", "r") as f:
        content = f.read()
        version = re.search(r'__version__ = "(.*)"', content).group(1).split(".")
        if "rc" in version[2] or "alpha" in version[2] or "beta" in version[2]:
            match = re.search(r"(\d+)(rc|alpha|beta)(\d+)", version[2])
            patch_version = match.group(1)
            pre = match.group(2)
            pre_version = match.group(3)
            version = f"{version[0]}.{version[1]}.{patch_version}-{pre}.{pre_version}"
        else:
            version = ".".join(version[:3])

    if not should_update_dll(config, version):
        return

    os.makedirs("pyautd3/bin", exist_ok=True)
    if config.is_windows():
        match config.arch:
            case "x64":
                url = f"https://github.com/shinolab/autd3-capi/releases/download/v{version}/autd3-v{version}-win-x64-shared.zip"
            case "aarch64":
                url = f"https://github.com/shinolab/autd3-capi/releases/download/v{version}/autd3-v{version}-win-aarch64-shared.zip"
            case _:
                err(f"Unsupported platform: {platform.machine()}")
        urllib.request.urlretrieve(url, "tmp.zip")
        shutil.unpack_archive("tmp.zip", ".")
        rm_f("tmp.zip")
        for dll in glob.glob("bin/*.dll"):
            shutil.copy(dll, "pyautd3/bin")
    elif config.is_macos():
        url = f"https://github.com/shinolab/autd3-capi/releases/download/v{version}/autd3-v{version}-macos-aarch64-shared.tar.gz"
        urllib.request.urlretrieve(url, "tmp.tar.gz")
        with tarfile.open("tmp.tar.gz", "r:gz") as tar:
            tar.extractall()
        rm_f("tmp.tar.gz")
        for dll in glob.glob("bin/*.dylib"):
            shutil.copy(dll, "pyautd3/bin")
    elif config.is_linux():
        match config.arch:
            case "x64":
                url = f"https://github.com/shinolab/autd3-capi/releases/download/v{version}/autd3-v{version}-linux-x64-shared.tar.gz"
            case "aarch64":
                url = f"https://github.com/shinolab/autd3-capi/releases/download/v{version}/autd3-v{version}-linux-armv7-shared.tar.gz"
            case "armv7l":
                url = f"https://github.com/shinolab/autd3-capi/releases/download/v{version}/autd3-v{version}-linux-aarch64-shared.tar.gz"
        urllib.request.urlretrieve(url, "tmp.tar.gz")
        with tarfile.open("tmp.tar.gz", "r:gz") as tar:
            tar.extractall()
        rm_f("tmp.tar.gz")
        for dll in glob.glob("bin/*.so"):
            shutil.copy(dll, "pyautd3/bin")

    shutil.copyfile("LICENSE", "pyautd3/LICENSE.txt")
    shutil.copyfile("ThirdPartyNotice.txt", "pyautd3/ThirdPartyNotice.txt")

    rmtree_f("bin")

    with open("VERSION", mode="w") as f:
        f.write(version)


def py_build(args):
    config = Config(args)

    gen_pyi()

    copy_dll(config)

    build_wheel(config)


def py_test(args):
    config = Config(args)

    with working_dir("."):
        gen_pyi()

        subprocess.run(["uv", "run", "mypy", "pyautd3", "--check-untyped-defs"]).check_returncode()
        subprocess.run(["uv", "run", "ruff", "check", "pyautd3"]).check_returncode()
        subprocess.run(["uv", "run", "mypy", "example", "--check-untyped-defs"]).check_returncode()
        subprocess.run(["uv", "run", "ruff", "check", "example"]).check_returncode()
        subprocess.run(["uv", "run", "mypy", "tests", "--check-untyped-defs"]).check_returncode()
        subprocess.run(["uv", "run", "ruff", "check", "tests"]).check_returncode()

        copy_dll(config)

        command = ["uv", "run", "pytest", "-n", "auto"]
        if config.is_pcap_available():
            command.append("--soem")
        subprocess.run(command).check_returncode()


def py_cov(args):
    config = Config(args)

    copy_dll(config)

    with working_dir("."):
        command = ["uv", "run", "pytest", "-n", "auto"]
        if config.is_pcap_available():
            command.append("--soem")
        command.append("--cov-config=.coveragerc")
        command.append("--cov=pyautd3")
        command.append("--cov-branch")
        command.append(f"--cov-report={args.cov_report}")
        subprocess.run(command).check_returncode()


def py_clear(_):
    with working_dir("."):
        rm_glob_f("*.png")
        rm_f("setup.cfg")
        rm_f(".coverage")
        rm_f("coverage.xml")
        rm_f("ThirdPartyNotice.txt")
        rm_f("VERSION")
        rmtree_f("dist")
        rmtree_f("build")
        rmtree_f("pyautd3.egg-info")
        rmtree_f("pyautd3/bin")
        rmtree_f(".mypy_cache")
        rmtree_f("htmlcov")
        rmtree_glob_f("./**/__pycache__/**/")
        rmtree_f("tools/wrapper-generator/target")


def util_update_ver(args):
    version: str = args.version

    tokens = version.split(".")
    if "-" in tokens[2]:
        match tokens[2].split("-")[1]:
            case "rc":
                patch_version = tokens[2].split("-")[0] + "rc" + tokens[3]
            case "alpha":
                patch_version = tokens[2].split("-")[0] + "a" + tokens[3]
            case "beta":
                patch_version = tokens[2].split("-")[0] + "b" + tokens[3]
        pkg_version = f"{tokens[0]}.{tokens[1]}.{patch_version}"
    else:
        pkg_version = version

    with working_dir("."):
        with open("pyautd3/__init__.py", "r") as f:
            content = f.read()
            content = re.sub(
                r'__version__ = "(.*)"',
                f'__version__ = "{version}"',
                content,
                flags=re.MULTILINE,
            )
        with open("pyautd3/__init__.py", "w") as f:
            f.write(content)

        with open("setup.cfg.template", "r") as f:
            content = f.read()
            content = re.sub(r"version = (.*)", f"version = {pkg_version}", content, flags=re.MULTILINE)
        with open("setup.cfg.template", "w") as f:
            f.write(content)

        with open("pyproject.toml", "r") as f:
            content = f.read()
            content = re.sub(r"^version = (.*)", f'version = "{pkg_version}"', content, flags=re.MULTILINE)
        with open("pyproject.toml", "w") as f:
            f.write(content)


def util_generate_wrapper(_):
    fetch_submodule()
    generate_wrapper()


def command_help(args):
    print(parser.parse_args([args.command, "--help"]))


if __name__ == "__main__":
    with working_dir(os.path.dirname(os.path.abspath(__file__))):
        parser = argparse.ArgumentParser(description="pyautd3 build script")
        subparsers = parser.add_subparsers()

        # build
        parser_py_build = subparsers.add_parser("build", help="see `build -h`")
        parser_py_build.add_argument("--arch", help="cross-compile for specific architecture (for Linux)")
        parser_py_build.set_defaults(handler=py_build)

        # test
        parser_py_test = subparsers.add_parser("test", help="see `test -h`")
        parser_py_test.set_defaults(handler=py_test)

        # cov
        parser_py_cov = subparsers.add_parser("cov", help="see `cov -h`")
        parser_py_cov.add_argument("--cov_report", help="coverage report type [term|xml|html]", default="term")
        parser_py_cov.set_defaults(handler=py_cov)

        # clear
        parser_py_clear = subparsers.add_parser("clear", help="see `clear -h`")
        parser_py_clear.set_defaults(handler=py_clear)

        # util
        parser_util = subparsers.add_parser("util", help="see `util -h`")
        subparsers_util = parser_util.add_subparsers()

        # util update version
        parser_util_upver = subparsers_util.add_parser("upver", help="see `util upver -h`")
        parser_util_upver.add_argument("version", help="version")
        parser_util_upver.set_defaults(handler=util_update_ver)

        # util generate wrapper
        parser_util_gen_wrapper = subparsers_util.add_parser("gen_wrap", help="see `util gen_wrap -h`")
        parser_util_gen_wrapper.set_defaults(handler=util_generate_wrapper)

        # help
        parser_help = subparsers.add_parser("help", help="see `help -h`")
        parser_help.add_argument("command", help="command name which help is shown")
        parser_help.set_defaults(handler=command_help)

        args = parser.parse_args()
        if hasattr(args, "handler"):
            args.handler(args)
        else:
            parser.print_help()
