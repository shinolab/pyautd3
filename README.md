# pyautd3

![build](https://github.com/shinolab/pyautd3/workflows/build/badge.svg)
[![codecov](https://codecov.io/gh/shinolab/pyautd3/graph/badge.svg?precision=2)](https://codecov.io/gh/shinolab/pyautd3)
[![PyPI version](https://img.shields.io/pypi/v/pyautd3)](https://pypi.org/project/pyautd3/)

[autd3](https://github.com/shinolab/autd3-rs) library for python3.11+

## Install

```
pip install pyautd3
```

## Example

see [example](./example)

## For macOS and Linux users

`pyautd3.link.SOEM` uses `libpcap` which requires root permission.
If you want to use `pyautd3.link.SOEM`, please add permission as follows.

### macOS

```
sudo chmod +r /dev/bpf*
```

### linux

```
sudo setcap cap_net_raw,cap_net_admin=eip <your python path>
```

## LICENSE

See [LICENSE](./LICENSE) and [ThirdPartyNotice](./ThirdPartyNotice.txt).

# Author

Shun Suzuki, 2022-2024
