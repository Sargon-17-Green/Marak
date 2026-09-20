#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent
raise SystemExit(subprocess.call([sys.executable,str(here/"test_b15_semantics.py")]))
