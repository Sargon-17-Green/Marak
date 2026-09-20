from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent
raise SystemExit(subprocess.run([sys.executable,'test_b13_reference_model.py'],cwd=here).returncode)
