# pyautd3

[autd3](https://github.com/shinolab/autd3-rs) library for python3.10+

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

MIT

# Author

Shun Suzuki, 2022-2023
