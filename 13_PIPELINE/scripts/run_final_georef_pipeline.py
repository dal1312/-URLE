#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[2]
scripts = root / "13_PIPELINE/scripts"

steps = [
    scripts / "check_gcp_status.py",
    scripts / "promote_verified_gcps.py",
    scripts / "build_gdal_commands.py",
]

for step in steps:
    print("RUN", step.name)
    result = subprocess.run([sys.executable, str(step)], cwd=root)
    if result.returncode != 0:
        print("STOP", step.name, "code", result.returncode)
        raise SystemExit(result.returncode)

print("PIPELINE READY")
print("Next: execute 13_PIPELINE/scripts/gdal_georef_final_commands.sh in an environment with GDAL")
