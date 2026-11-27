"""Load the Release product by its C ABI only, without native test binaries."""

import ctypes as c
import os
from pathlib import Path
import sys
import time


class Status(c.Structure):
    _fields_ = [("size", c.c_uint32), ("state", c.c_uint32), ("generation", c.c_uint64),
                ("principal", c.c_uint32), ("institutional", c.c_uint32)]


class InstitutionalRequest(c.Structure):
    _fields_ = [(name, c.c_uint32) for name in ("size", "version", "operation", "reserved")] + [
        (name, c.c_uint64) for name in ("generation", "correlation", "event_id")]

class InstitutionalCompletion(c.Structure):
    _fields_ = [(name, c.c_uint32) for name in ("size", "code", "operation", "reserved")] + [
        (name, c.c_uint64) for name in ("ticket", "correlation", "generation", "epoch", "world_revision",
                                      "event_id", "effective_tick", "original_revision")] + [
        (name, c.c_uint32) for name in ("rank", "service_status", "from_rank", "to_rank")]


def inspect(host, bridge):
    for name in ("f04_history_test_delta", "f04_history_test_validate_full"):
        assert not hasattr(bridge, name), name

    handle = c.c_void_p
    code = c.c_uint32
    host.trek_host_abi_version.argtypes = []
    host.trek_host_abi_version.restype = code
    host.trek_host_create.argtypes = [code, c.c_char_p, code, c.POINTER(handle)]
    host.trek_host_create.restype = code
    host.trek_host_status.argtypes = [handle, c.POINTER(Status)]
    host.trek_host_status.restype = code
    host.trek_host_destroy.argtypes = [handle]
    host.trek_host_destroy.restype = None
    for name in ("submit", "poll", "discard"):
        getattr(host, f"trek_host_{name}")
    for name in ("bind_player", "receive_order", "execute_order", "core_session"):
        assert not hasattr(host, f"trek_host_{name}"), name

    assert host.trek_host_abi_version() == 1
    client = handle()
    assert host.trek_host_create(2, None, 0, c.byref(client)) == 100 and not client
    assert host.trek_host_create(1, None, 0, c.byref(client)) == 0 and client
    try:
        status = Status(c.sizeof(Status))
        for _ in range(200):
            result = host.trek_host_status(client, c.byref(status))
            if result != 101:
                break
            time.sleep(0.005)
        assert result == 0
        assert (status.state, status.generation, status.principal, status.institutional) == (0, 0, 2, 21)
        assert c.sizeof(InstitutionalRequest) == 40 and c.sizeof(InstitutionalCompletion) == 96
        host.trek_host_institutional_version.restype = code
        assert host.trek_host_institutional_version() == 1
        host.trek_host_institutional_submit.argtypes = [handle, c.POINTER(InstitutionalRequest), c.POINTER(c.c_uint64)]
        host.trek_host_institutional_poll.argtypes = [handle, c.c_uint64, c.POINTER(InstitutionalCompletion)]
        request = InstitutionalRequest(c.sizeof(InstitutionalRequest), 1, 1, 0, 0, 123, 0)
        ticket = c.c_uint64()
        for _ in range(200):
            result = host.trek_host_institutional_submit(client, c.byref(request), c.byref(ticket))
            if result != 101: break
            time.sleep(0.005)
        assert result == 0 and ticket.value
        completion = InstitutionalCompletion(c.sizeof(InstitutionalCompletion))
        for _ in range(200):
            result = host.trek_host_institutional_poll(client, ticket, c.byref(completion))
            if result not in (101, 102): break
            time.sleep(0.005)
        assert result == 0 and completion.code == 2 and completion.correlation == 123
        assert bytes(completion)[32:] == bytes(c.sizeof(completion) - 32)

    finally:
        host.trek_host_destroy(client)
    print("PASS: loaded C ABI 1 from tests-OFF binary, negotiated version and queried closed client")


if __name__ == "__main__":
    build = Path(sys.argv[1]).resolve()
    assert "TREK_HOST_TESTS:BOOL=OFF" in (build / "CMakeCache.txt").read_text()
    windows = os.name == "nt"
    path = next(build.rglob("TrekHost.dll" if windows else "libTrekHost.so"))
    bridge = next(build.rglob("TrekF04Bridge.dll" if windows else "libTrekF04Bridge.so"))
    assert not any(build.rglob("host_abi_tests*"))
    if windows:
        with os.add_dll_directory(str(path.parent)):
            inspect(c.CDLL(str(path)), c.CDLL(str(bridge)))
    else:
        inspect(c.CDLL(str(path)), c.CDLL(str(bridge)))
