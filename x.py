#!/usr/bin/env python3


import argparse
import contextlib
import glob
import os
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import urllib.request
from typing import Optional


def fetch_submodule():
    if shutil.which("git") is not None:
        with working_dir(os.path.dirname(os.path.abspath(__file__))):
            subprocess.run(["git", "submodule", "update", "--init", "--recursive"]).check_returncode()
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


def err(msg: str):
    print("\033[91mERR \033[0m: " + msg)


def warn(msg: str):
    print("\033[93mWARN\033[0m: " + msg)


def info(msg: str):
    print("\033[92mINFO\033[0m: " + msg)


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


@contextlib.contextmanager
def set_env(key, value):
    env = os.environ.copy()
    os.environ[key] = value
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(env)


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

    def is_cuda_available(self):
        return shutil.which("nvcc") is not None

    def is_pcap_available(self):
        if not self.is_windows():
            return True
        wpcap_exists = os.path.isfile("C:\\Windows\\System32\\wpcap.dll") and os.path.isfile("C:\\Windows\\System32\\Npcap\\wpcap.dll")
        packet_exists = os.path.isfile("C:\\Windows\\System32\\Packet.dll") and os.path.isfile("C:\\Windows\\System32\\Npcap\\Packet.dll")

        return wpcap_exists and packet_exists

    def python_module(self, cmd):
        r = ["python" if self.is_windows() else "python3", "-m"]
        r.extend(cmd)
        return r


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
            subprocess.run(config.python_module(["build", "-w"])).check_returncode()
        elif config.is_macos():
            with open("setup.cfg.template", "r") as setup:
                content = setup.read()
                content = content.replace(r"${classifiers_os}", "Operating System :: MacOS :: MacOS X")
                content = content.replace(r"${plat_name}", "macosx-11-0-arm64")
                with open("setup.cfg", "w") as f:
                    f.write(content)
            subprocess.run(config.python_module(["build", "-w"])).check_returncode()
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
            subprocess.run(config.python_module(["build", "-w"])).check_returncode()


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
        version = (
            ".".join(version) if version[2].endswith("rc") or version[2].endswith("alpha") or version[2].endswith("beta") else ".".join(version[:3])
        )

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

    copy_dll(config)

    build_wheel(config)

    if not args.no_install:
        with working_dir("."):
            version = ""
            with open("setup.cfg.template", "r") as setup:
                content = setup.read()
                m = re.search("version = (.*)", content)
                version = m.group(1)
            command = config.python_module(["pip", "install"])
            if config.is_windows():
                match config.arch:
                    case "x64":
                        plat_name = "win_amd64"
                    case "aarch64":
                        plat_name = "win_arm64"
                    case _:
                        err(f"Unsupported architecture: {config.arch}")
            elif config.is_macos():
                if platform.machine() in ["ADM64", "x86_64"]:
                    err(f'platform "{platform.system()}/{platform.machine()}" is not supported.')
                else:
                    plat_name = "macosx_11_0_arm64"
            elif config.is_linux():
                match config.arch:
                    case "x64":
                        plat_name = "manylinux1_x86_64"
                    case "aarch64":
                        plat_name = "manylinux2014_aarch64"
                    case "armv7l":
                        plat_name = "linux_armv7l"
            else:
                err(f'platform "{platform.system()}/{platform.machine()}" is not supported.')
                sys.exit(-1)
            command.append(f"dist/pyautd3-{version}-py3-none-{plat_name}.whl")
            command.append("--force")
            subprocess.run(command).check_returncode()


def py_test(args):
    config = Config(args)

    copy_dll(config)

    with working_dir("."):
        subprocess.run(config.python_module(["mypy", "pyautd3", "--check-untyped-defs"])).check_returncode()
        subprocess.run(config.python_module(["ruff", "check", "pyautd3"])).check_returncode()
        subprocess.run(config.python_module(["mypy", "example", "--check-untyped-defs"])).check_returncode()
        subprocess.run(config.python_module(["ruff", "check", "example"])).check_returncode()
        subprocess.run(config.python_module(["mypy", "tests", "--check-untyped-defs"])).check_returncode()
        subprocess.run(config.python_module(["ruff", "check", "tests"])).check_returncode()

        command = config.python_module(["pytest", "-n", "auto"])
        if config.is_pcap_available():
            command.append("--soem")
        if config.is_cuda_available():
            command.append("--cuda")
        subprocess.run(command).check_returncode()


def py_cov(args):
    config = Config(args)

    copy_dll(config)

    with working_dir("."):
        command = config.python_module(["pytest", "-n", "auto"])
        if config.is_pcap_available():
            command.append("--soem")
        if config.is_cuda_available():
            command.append("--cuda")
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
        parser_py_build.add_argument("--no-install", action="store_true", help="skip install python package")
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
