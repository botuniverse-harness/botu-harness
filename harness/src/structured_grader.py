"""Deterministic work-product checks for explicitly structured text drills.

These checks measure fixture accuracy, not prose quality or tool execution.
The prompt supplies the output contract; the answer key is never sent to students.
"""
from __future__ import annotations

import json
import re


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key")
        result[key] = value
    return result


def _reject_constant(value):
    raise ValueError("Non-finite JSON number")


def score_json_response(drill: dict, response: str) -> dict:
    """Require exactly the declared fields and values, including JSON types.

    Object key order and whitespace are immaterial. Array order is significant
    (prompts specify an order). One outer Markdown JSON fence is accepted.
    Duplicate keys, extra prose/fields and nonstandard numbers fail closed.
    """
    answer = drill["expected"]["json_answer"]
    text = response.strip()
    fenced = re.fullmatch(r"```(?:json)?\s*\n(.*?)\n```", text, flags=re.S | re.I)
    candidate = fenced.group(1) if fenced else text
    notes = []
    parsed = None
    try:
        if len(candidate) > 20000:
            raise ValueError("Oversized response")
        parsed = json.loads(candidate, object_pairs_hook=_unique_object,
                            parse_constant=_reject_constant)
        if not isinstance(parsed, dict):
            raise ValueError("Expected an object")
    except (ValueError, RecursionError):
        notes.append("Response must be one valid JSON object without duplicate keys or extra prose.")

    checks = {"valid_json": isinstance(parsed, dict)}
    if checks["valid_json"]:
        checks["fields"] = set(parsed) == set(answer)
        if not checks["fields"]:
            notes.append("Output fields do not match the requested contract.")
        for key, value in answer.items():
            # Canonical JSON preserves bool/int/null/string distinctions at all depths.
            checks[key] = key in parsed and json.dumps(parsed[key], sort_keys=True) == json.dumps(value, sort_keys=True)
            if not checks[key]:
                notes.append(f"Incorrect or missing work-product field: {key}.")
    passed = all(checks.values())
    return {
        "drillId": drill["id"], "drillVersion": drill.get("version", "0.0.0"),
        "status": "pass" if passed else "fail", "score": 100 if passed else 0,
        "checks": checks, "excerpt": text[:280], "notes": notes,
        "remediation_hints": drill.get("remediation_hints", []),
    }
