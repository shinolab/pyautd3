import platform  # noqa: INP001
import re
import shutil
import tarfile
import urllib.request
from pathlib import Path


def download_and_extract(repo: str, name: str, version: str) -> None:
    url: str
    base_url = f"https://github.com/shinolab/{repo}/releases/download/v{version}/{name}-v{version}"
    if platform.system() == "Windows":
        url = f"{base_url}-win-x64-shared.zip"
    elif platform.system() == "Darwin":
        url = f"{base_url}-macos-aarch64-shared.tar.gz"
    else:
        url = f"{base_url}-linux-x64-shared.tar.gz"

    tmp_file = Path("tmp.zip" if url.endswith(".zip") else "tmp.tar.gz")
    urllib.request.urlretrieve(url, tmp_file)  # noqa: S310
    if tmp_file.suffix == ".zip":
        shutil.unpack_archive(tmp_file, ".")
    else:
        with tarfile.open(tmp_file, "r:gz") as tar:
            tar.extractall(filter="fully_trusted")  # noqa: S202
    tmp_file.unlink()

    dst_dir = Path("pyautd3/bin")
    dst_dir.mkdir(parents=True, exist_ok=True)

    for dll in Path("bin").glob("*.dll"):
        shutil.copy(dll, dst_dir)
    for dylib in Path("bin").glob("*.dylib"):
        shutil.copy(dylib, dst_dir)
    for so in Path("bin").glob("*.so"):
        shutil.copy(so, dst_dir)
    shutil.rmtree("bin")


def should_update_dll(version: str) -> bool:
    if platform.system() == "Windows":
        if not Path("pyautd3/bin/autd3capi.dll").exists():
            return True
    elif platform.system() == "Darwin":
        if not Path("pyautd3/bin/libautd3capi.dylib").exists():
            return True
    elif not Path("pyautd3/bin/libautd3capi.so").exists():
        return True

    version_file = Path("VERSION")
    if not version_file.exists():
        return True

    old_version = version_file.read_text().strip()
    return old_version != version


def copy_dll() -> None:
    with Path("pyautd3/__init__.py").open() as f:
        content = f.read()
        version = re.search(r'__version__ = "(.*)"', content).group(1).split(".")  # type: ignore[union-attr]
        if "rc" in version[2] or "alpha" in version[2] or "beta" in version[2]:
            match = re.search(r"(\d+)(rc|alpha|beta)(\d+)", version[2])
            patch_version = match.group(1)  # type: ignore[union-attr]
            pre = match.group(2)  # type: ignore[union-attr]
            pre_version = match.group(3)  # type: ignore[union-attr]
            version = f"{version[0]}.{version[1]}.{patch_version}-{pre}.{pre_version}"
        else:
            version = ".".join(version[:3])

    if not should_update_dll(version):
        return

    download_and_extract("autd3-capi", "autd3", version)
    shutil.copyfile("LICENSE", "pyautd3/LICENSE.txt")
    shutil.copyfile("ThirdPartyNotice.txt", "ThirdPartyNotice-orig.txt")

    download_and_extract("autd3-capi-emulator", "autd3", version)
    notice = Path("ThirdPartyNotice-orig.txt").read_text() + "\n" + Path("ThirdPartyNotice.txt").read_text()
    Path("ThirdPartyNotice.txt").write_text(notice)
    shutil.copyfile("ThirdPartyNotice.txt", "pyautd3/ThirdPartyNotice.txt")

    Path("VERSION").write_text(version)


if __name__ == "__main__":
    copy_dll()
