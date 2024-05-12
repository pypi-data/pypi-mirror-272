# simple_bgpfuzz_rpc

A bgp rpc monitor for boofuzz.

### Introduction

Use this monitor to detect the state of the object under test for fuzz testing.

### Usage

```[python]
# myrpc.py
import simple_bgpfuzz_rpc

if name == '__main__':
    simple_bgpfuzz_rpc.main()
```

then run this following command:

```
python myrpc.py --ip [TARGET'S IP] --port [RPC port] --monitor [frr | bird | openbgpd]

```

### Install

```
$ pip install simple-bgpfuzz-rpc
```

### License

This module use MIT license.
