"""Load Release product DLLs and inspect exports/dependencies without test hooks."""
import ctypes
import os
from pathlib import Path
import subprocess
import sys

build = Path(sys.argv[1]).resolve()
assert "TREK_HOST_TESTS:BOOL=OFF" in (build / "CMakeCache.txt").read_text()
windows = os.name == "nt"
host = next(build.rglob("TrekHost.dll" if windows else "libTrekHost.so"))
bridge = next(build.rglob("TrekF04Bridge.dll" if windows else "libTrekF04Bridge.so"))
if windows:
    dll_dir = os.add_dll_directory(str(host.parent))
ctypes.CDLL(str(host))
f04 = ctypes.CDLL(str(bridge))
f04.f04_core_sha.restype = ctypes.c_char_p
assert f04.f04_core_sha() == b"76a7b7b485616d8c4994f384a90f123bf333591d"
for name in ("f05_submit", "f05_receive", "f05_execute_order", "f05_order", "f05_result", "f05_player_binding", "f04_history_snapshot"):
    getattr(f04, name)
for name in ("f11_commit_promotion", "storage_test_hook", "gateway_test_after_dispatch"):
    assert not hasattr(f04, name), name
if windows:
    vswhere = Path(os.environ["ProgramFiles(x86)"]) / "Microsoft Visual Studio/Installer/vswhere.exe"
    paths = subprocess.check_output([str(vswhere), "-latest", "-products", "*", "-find", "VC/Tools/MSVC/*/bin/Hostx64/x64/dumpbin.exe"], text=True).splitlines()
    assert paths, "dumpbin unavailable"
    symbols = subprocess.check_output([paths[-1], "/exports", str(host)], text=True)
    dependencies = subprocess.check_output([paths[-1], "/dependents", str(host)], text=True)
else:
    symbols = subprocess.check_output(["nm", "-D", "-C", "--defined-only", str(host)], text=True)
    dependencies = subprocess.check_output(["ldd", str(host)], text=True)
    assert "not found" not in dependencies
for name in ("query_view", "submit_order", "query_order", "cancel_order", "restore"):
    assert name in symbols, name
for name in ("GatewayTestAccess", "gateway_test", "storage_test_hook", "f11_commit_promotion", "test_visit"):
    assert name not in symbols, name
assert "TrekF04Bridge" in dependencies
assert not any("TrialHost" in p.name or p.name.startswith((
    "host_native_tests", "host_fault_tests", "host_m0_tests", "host_persistence_tests",
    "host_academy_feasibility_tests",
)) for p in build.rglob("*") if p.is_file())
print(symbols)
print(dependencies)
print("PASS: Release product loaded, exports inspected, Core pin verified, tests OFF, no HOST test hooks/F11 trial")
