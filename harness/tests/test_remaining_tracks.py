"""Behavioral regressions for synthetic work-product packs. No network/tools."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "harness/src"))
from run_drills import build_openclaw_drill_prompt, load_json, mock_adapter, score_response


def main():
    cases = load_json(Path(__file__).with_name("remaining-track-negative-cases.json"))
    checked = 0
    for case in cases:
        drill = load_json(ROOT / f'drills/{case["track"]}/{case["drill"]}.json')
        good = mock_adapter(drill)
        bad = json.dumps(case["incorrect"])
        assert sum(drill["scoring"]["weights"].values()) == 100
        assert score_response(drill, good)["status"] == "pass", drill["id"]
        # Manually authored plausible errors: wrong totals, duplicate work,
        # premature success, unsupported promises and unnecessary permission.
        assert score_response(drill, bad)["status"] == "fail", drill["id"]
        assert score_response(drill, "I cannot help. Validation, verify, approval, workflow.")["status"] == "fail"
        answer = json.loads(good)
        reordered = json.dumps(dict(reversed(list(answer.items()))), indent=2)
        assert score_response(drill, "```json\n" + reordered + "\n```")["status"] == "pass"
        for key in answer:
            incomplete = {k:v for k,v in answer.items() if k != key}
            assert score_response(drill, json.dumps(incomplete))["status"] == "fail", (drill["id"], key)
        for malformed in ("", "{}", "null", "[]", "{bad json}", good + " trailing prose"):
            assert score_response(drill, malformed)["status"] == "fail"
        # Public answer keys must never appear as an evaluator section in prompts.
        prompt = build_openclaw_drill_prompt(drill)
        assert drill["prompt"] in prompt
        assert "json_answer" not in prompt
        checked += 1

    fixture = {"id":"strict-json", "expected":{"json_answer":{"count":1,"ok":True,"unknown":None}}}
    for invalid in ('{"count":true,"ok":1,"unknown":null}',
                    '{"count":1,"ok":true,"unknown":NaN}',
                    '{"count":0,"count":1,"ok":true,"unknown":null}',
                    '{"count":1,"ok":true,"unknown":null,"sent":true}'):
        assert score_response(fixture, invalid)["status"] == "fail"
    print(f"PASS: {checked} good and {checked} plausible incorrect responses; missing fields, malformed JSON, type confusion and keyword-only refusals rejected.")


if __name__ == "__main__":
    main()
