"""Load Release product DLLs and inspect exports/dependencies without test hooks."""
import ctypes
import os
from pathlib import Path
import subprocess
import sys

build = Path(sys.argv[1]).resolve()
cache = (build / "CMakeCache.txt").read_text()
assert "TREK_HOST_TESTS:BOOL=OFF" in cache
f11_reads = "TREK_HOST_F11_READS:BOOL=ON" in cache
definitions = (build / "host-bridge-definitions-Release.txt").read_text().splitlines()
assert ("F11_HOST_READ_ONLY=1" in definitions) == f11_reads
assert not any(item.startswith(("F11_ENABLE_PROMOTIONS", "F11_NATIVE_TEST_HOST", "F04_HISTORY_TESTING"))
               for item in definitions), definitions
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
for name in ("f11_personnel", "f11_promotion"):
    assert hasattr(f04, name) == f11_reads, name
for name in ("f11_commit_promotion", "f11_test_create", "f11_test_revoke", "f11_test_fault",
             "storage_test_hook", "gateway_test_after_dispatch"):
    assert not hasattr(f04, name), name
if windows:
    vswhere = Path(os.environ["ProgramFiles(x86)"]) / "Microsoft Visual Studio/Installer/vswhere.exe"
    paths = subprocess.check_output([str(vswhere), "-latest", "-products", "*", "-find", "VC/Tools/MSVC/*/bin/Hostx64/x64/dumpbin.exe"], text=True).splitlines()
    assert paths, "dumpbin unavailable"
    symbols = subprocess.check_output([paths[-1], "/exports", str(host)], text=True)
    dependencies = subprocess.check_output([paths[-1], "/dependents", str(host)], text=True)
    bridge_symbols = subprocess.check_output([paths[-1], "/exports", str(bridge)], text=True)
    bridge_dependencies = subprocess.check_output([paths[-1], "/dependents", str(bridge)], text=True)
else:
    symbols = subprocess.check_output(["nm", "-D", "-C", "--defined-only", str(host)], text=True)
    dependencies = subprocess.check_output(["ldd", str(host)], text=True)
    bridge_symbols = subprocess.check_output(["nm", "-a", "-C", "--defined-only", str(bridge)], text=True)
    bridge_dependencies = subprocess.check_output(["ldd", str(bridge)], text=True)
    assert "not found" not in dependencies + bridge_dependencies
for name in ("trek_host_institutional_version", "trek_host_institutional_submit", "trek_host_institutional_poll",
             "trek_host_institutional_current", "trek_host_academy_version", "trek_host_academy_submit", "trek_host_academy_poll",
             "query_view", "submit_order", "query_order", "cancel_order", "restore", "AcademyCandidateFactory",
             "AcademyPlayerBinding"):
    assert name in symbols, name
for name in ("GatewayTestAccess", "gateway_test", "storage_test_hook", "f11_commit_promotion", "test_visit",
             "BiographyValidator", "BiographyReceipt", "SemanticEvaluator", "BiographyAuthority",
             "RegisteredBiographyAuthority", "BiographyClaimEvidence",
             "HistoryPersistence", "WorldState", "AcademyCampaign", "academy_fail_at", "set_academy_fault",
             "academy_bind_test_hook", "AcademyInterface::", "InstitutionalQueries", "f11_host::"):
    assert name not in symbols, name
for name in ("TrekF11TrialHost", "f11_bootstrap_authorized_trial", "f11_test_", "f11_commit_promotion",
             "f11_trial_identity", "f11_trial_fact"):
    assert name not in symbols + bridge_symbols + dependencies + bridge_dependencies, name
assert "TrekF04Bridge" in dependencies
assert not any("TrialHost" in p.name or p.name.startswith((
    "host_native_tests", "host_fault_tests", "host_m0_tests", "host_persistence_tests",
    "host_h07_query_tests", "host_h07_admission_tests",
    "host_academy_feasibility_tests", "host_academy_candidate_", "host_academy_player_", "host_biography_tests",
    "host_ai_tests", "host_ai_smoke", "host_academy_fault_runtime", "libhost_academy_fault_runtime",
    "host_academy_persistence_", "host_academy_abi_",
)) for p in build.rglob("*") if p.is_file())
print(symbols)
print(dependencies)
print(bridge_dependencies)
print("TrekF04Bridge definitions:", *definitions)
print("PASS: Release product loaded, exports inspected, Core pin verified, tests OFF, no HOST test hooks/F11 trial")
