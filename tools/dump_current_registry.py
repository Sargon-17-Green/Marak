from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from compiler.parse.current_registry import CURRENT_REGISTRY


def main() -> None:
    target = ROOT / "spec" / "CURRENT_CONSTRUCTION_REGISTRY.json"
    target.write_text(
        json.dumps(CURRENT_REGISTRY.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(target)


if __name__ == "__main__":
    main()
