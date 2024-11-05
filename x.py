#!/usr/bin/env python3

import argparse
import ast
import pathlib
import re
import shutil

from tools.autd3_build_utils.autd3_build_utils import (
    BaseConfig,
    err,
    fetch_submodule,
    remove,
    rremove,
    run_command,
    substitute_in_file,
    working_dir,
)
from tools.autd3_build_utils.pyi_generator import PyiGenerator


def gen_pyi() -> None:
    re_typevar = re.compile(r"(.*) = TypeVar\((.*)\)")
    files = set(pathlib.Path("pyautd3").rglob("*.py")) - set(pathlib.Path("pyautd3/derive").rglob("*.py"))
    for file in files:
        with file.open(encoding="utf8") as f:
            content = f.read()
            tree = ast.parse(content, type_comments=True)
            generator = PyiGenerator()
            generator.visit(tree)

        if generator.should_generate:
            imports = generator.imports
            typevars = []

            for line in content.split("\n"):
                match = re_typevar.match(line)
                if match:
                    typevars.append(match.group(0))

            pyi_code = generator.generate_pyi()
            with file.with_suffix(".pyi").open("w", encoding="utf8") as f:
                f.write("\n".join(imports))
                f.write("\n\n")
                f.write("\n".join(typevars))
                f.write("\n\n")
                f.write(pyi_code)


class Config(BaseConfig):
    release: bool

    def __init__(self, args) -> None:  # noqa: ANN001
        super().__init__(args)


def build_wheel(config: Config) -> None:
    plat_name: str
    if config.is_windows():
        match config.arch:
            case "x64":
                plat_name = "win-amd64"
            case "aarch64":
                plat_name = "win-arm64"
    elif config.is_macos():
        plat_name = "macosx-11-0-arm64"
    elif config.is_linux():
        match config.arch:
            case "x64":
                plat_name = "manylinux1_x86_64"
            case "aarch64":
                plat_name = "manylinux2014_aarch64"
            case "armv7l":
                plat_name = "linux_armv7l"
    substitute_in_file("setup.cfg.template", [("plat_name = PLATNAME", f"plat_name = {plat_name}")], target_file="setup.cfg")
    run_command(["uv", "build"])


def should_update_dll(config: Config, version: str) -> bool:
    if config.is_windows():
        if not pathlib.Path("pyautd3/bin/autd3capi.dll").exists():
            return True
    elif config.is_macos():
        if not pathlib.Path("pyautd3/bin/libautd3capi.dylib").exists():
            return True
    elif config.is_linux() and not pathlib.Path("pyautd3/bin/libautd3capi.so").exists():
        return True

    version_file = pathlib.Path("VERSION")
    if not version_file.exists():
        return True

    old_version = version_file.read_text().strip()
    return old_version != version


def copy_dll(config: Config) -> None:
    with pathlib.Path("pyautd3/__init__.py").open() as f:
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

    config.download_and_extract("autd3-capi", "autd3", version, ["pyautd3/bin"])
    shutil.copyfile("LICENSE", "pyautd3/LICENSE.txt")
    shutil.copyfile("ThirdPartyNotice.txt", "pyautd3/ThirdPartyNotice.txt")
    remove("bin")
    pathlib.Path("VERSION").write_text(version)


def py_build(args) -> None:  # noqa: ANN001
    config = Config(args)
    gen_pyi()
    copy_dll(config)
    build_wheel(config)


def py_test(args) -> None:  # noqa: ANN001
    config = Config(args)
    gen_pyi()
    run_command(["uv", "run", "mypy", "pyautd3", "--check-untyped-defs"])
    run_command(["uv", "run", "ruff", "check", "pyautd3"])
    run_command(["uv", "run", "mypy", "example", "--check-untyped-defs"])
    run_command(["uv", "run", "ruff", "check", "example"])
    run_command(["uv", "run", "mypy", "tests", "--check-untyped-defs"])
    run_command(["uv", "run", "ruff", "check", "tests"])
    copy_dll(config)
    run_command(["uv", "run", "pytest", "-n", "auto"])


def py_cov(args) -> None:  # noqa: ANN001
    config = Config(args)
    copy_dll(config)
    gen_pyi()
    run_command(
        command=[
            "uv",
            "run",
            "pytest",
            "-n",
            "auto",
            "--cov-config=.coveragerc",
            "--cov=pyautd3",
            "--cov-branch",
            f"--cov-report={args.cov_report}",
        ],
    )


def py_clear(_) -> None:  # noqa: ANN001
    remove("setup.cfg")
    remove(".coverage")
    remove("LICENSE")
    remove("ThirdPartyNotice.txt")
    remove("VERSION")
    remove("dist")
    remove("pyautd3.egg-info")
    remove("pyautd3/bin")
    remove("pyautd3/LICENSE.txt")
    remove("pyautd3/ThirdPartyNotice.txt")
    remove("htmlcov")
    remove(".ruff_cache")
    remove(".mypy_cache")
    remove(".pytest_cache")
    rremove("./**/__pycache__/**/")
    rremove("uv.lock")


def util_update_ver(args) -> None:  # noqa: ANN001
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

    substitute_in_file("pyautd3/__init__.py", [(r'__version__ = "(.*)"', f'__version__ = "{version}"')])
    substitute_in_file("setup.cfg.template", [(r"version = (.*)", f"version = {pkg_version}")])
    substitute_in_file("pyproject.toml", [(r'^version = "(.*)"', f'version = "{pkg_version}"')], flags=re.MULTILINE)


def util_generate_wrapper(_) -> None:  # noqa: ANN001
    if shutil.which("cargo") is not None:
        with working_dir("tools/wrapper-generator"):
            run_command(["cargo", "run"])
    else:
        err("cargo is not installed. Skip generating wrapper.")


def command_help(args) -> None:  # noqa: ANN001
    print(parser.parse_args([args.command, "--help"]))  # noqa: T201


if __name__ == "__main__":
    with working_dir(pathlib.Path(__file__).parent):
        fetch_submodule()

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
