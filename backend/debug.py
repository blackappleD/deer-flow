#!/usr/bin/env python
"""Debug entrypoint for the local yuanfa workflow."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from workflow.lead_agent import lead_agent


def main() -> None:
    print("=" * 50)
    print("Yuanfa Workflow Debug Mode")
    print("Input plain text for a normal case")
    print("Use '/critical' prefix to simulate emergency major case")
    print("Type 'quit' or 'exit' to stop")
    print("=" * 50)

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in {"quit", "exit"}:
                print("Goodbye!")
                break

            payload = {
                "query": user_input,
                "summary": user_input,
                "title": "Interactive yuanfa case",
                "case_id": "case-debug-001",
                "requested_by": "AION",
                "severity": "medium",
                "emergency": False,
                "major": False,
            }
            if user_input.startswith("/critical"):
                payload.update(
                    {
                        "query": user_input.removeprefix("/critical").strip() or "critical incident",
                        "summary": user_input.removeprefix("/critical").strip() or "critical incident",
                        "severity": "critical",
                        "emergency": True,
                        "major": True,
                    }
                )

            result = lead_agent["invoke"](payload)
            print("\nAgent:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except KeyboardInterrupt:
            print("\nInterrupted. Goodbye!")
            break


if __name__ == "__main__":
    main()
