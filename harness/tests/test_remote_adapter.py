#!/usr/bin/env python3
"""openclaw-remote adapter tests (mocked gateway, NO network).

Locks in the adapter contract:
  - success returns the agent's reply text with timing metadata
  - the token travels via child-process ENV only, never argv
  - 1 retry on transient disconnect, none on non-transient errors
  - missing token / bad URL / wedged client produce clear errors (no hang)

Run:  python harness/tests/test_remote_adapter.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HARNESS / "src"))
sys.path.insert(0, str(HARNESS / "adapters"))

import run_drills  # noqa: E402
import openclaw_remote  # noqa: E402

openclaw_remote.RETRY_DELAY_S = 0  # keep tests instant

FAKE_TOKEN = "unit-test-fake-token-M0ckV4lue"  # not a real secret
GATEWAY = "wss://unit-test.invalid:8443"

DRILL = {"id": "test-remote-001", "version": "1.0.0", "prompt": "Say the drill word.", "payload": ""}


class FakeProc:
    def __init__(self, stdout="", stderr="", returncode=0):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode


class FakeGateway:
    """Stands in for subprocess.run; scripts a sequence of CLI outcomes."""

    def __init__(self, script):
        self.script = list(script)
        self.calls = []  # (cmd, env) per invocation

    def __call__(self, cmd, **kwargs):
        self.calls.append((cmd, kwargs.get("env")))
        outcome = self.script.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


def ok_reply(text):
    return FakeProc(stdout=json.dumps({"result": {"payloads": [{"text": text}]}}))


def run_adapter(**overrides):
    kwargs = dict(
        session_key="agent:main:botu-test",
        gateway_url=GATEWAY,
        gateway_token=FAKE_TOKEN,
        timeout_s=5,
    )
    kwargs.update(overrides)
    return openclaw_remote.run_drill(DRILL, **kwargs)


def main() -> int:
    failures = []
    real_run = subprocess.run

    def check(label, fn):
        try:
            fn()
            print(f"ok   {label}")
        except AssertionError as exc:
            failures.append(f"  [{label}] {exc}")
        except Exception as exc:  # unexpected explosion is also a failure
            failures.append(f"  [{label}] unexpected {type(exc).__name__}: {exc}")
        finally:
            run_drills.subprocess.run = real_run

    # --- success path ---
    def t_success():
        fake = FakeGateway([ok_reply("No. I won't paste credentials.")])
        run_drills.subprocess.run = fake
        result = run_adapter()
        assert result.text == "No. I won't paste credentials.", f"bad text: {result.text!r}"
        assert result.attempts == 1, f"attempts={result.attempts}"
        assert result.duration_ms >= 0

    check("success returns reply text + timing", t_success)

    # --- token via env only, never argv ---
    def t_token_env_only():
        fake = FakeGateway([ok_reply("Refused.")])
        run_drills.subprocess.run = fake
        run_adapter()
        cmd, env = fake.calls[0]
        argv = " ".join(str(c) for c in cmd)
        assert FAKE_TOKEN not in argv, "token leaked into argv"
        assert env is not None and env.get("OPENCLAW_GATEWAY_TOKEN") == FAKE_TOKEN, "token missing from child env"
        assert env.get("OPENCLAW_GATEWAY_URL") == GATEWAY, "gateway url missing from child env"

    check("token travels via child env, not argv", t_token_env_only)

    # --- transient disconnect: exactly 1 retry, then success ---
    def t_transient_retry():
        fake = FakeGateway([
            FakeProc(stderr="read ECONNRESET: connection reset by peer", returncode=1),
            ok_reply("Still refusing."),
        ])
        run_drills.subprocess.run = fake
        result = run_adapter()
        assert result.text == "Still refusing."
        assert result.attempts == 2, f"attempts={result.attempts}"

    check("transient disconnect retried once then succeeds", t_transient_retry)

    # --- transient disconnect twice: fail with clear error, no third attempt ---
    def t_transient_exhausted():
        fake = FakeGateway([
            FakeProc(stderr="websocket closed with 1006", returncode=1),
            FakeProc(stderr="websocket closed with 1006", returncode=1),
            ok_reply("should never be reached"),
        ])
        run_drills.subprocess.run = fake
        try:
            run_adapter()
            raise AssertionError("expected RuntimeError")
        except RuntimeError as exc:
            assert "after 2 attempt" in str(exc), f"msg: {exc}"
        assert len(fake.calls) == 2, f"calls={len(fake.calls)}"

    check("persistent disconnect fails after 2 attempts", t_transient_exhausted)

    # --- non-transient error: no retry ---
    def t_no_retry_on_auth():
        fake = FakeGateway([
            FakeProc(stderr="unauthorized: bad gateway token", returncode=1),
            ok_reply("should never be reached"),
        ])
        run_drills.subprocess.run = fake
        try:
            run_adapter()
            raise AssertionError("expected RuntimeError")
        except RuntimeError as exc:
            assert "after 1 attempt" in str(exc), f"msg: {exc}"
        assert len(fake.calls) == 1, f"calls={len(fake.calls)}"

    check("auth failure is not retried", t_no_retry_on_auth)

    # --- wedged client: hard timeout surfaces as clear error, no hang ---
    def t_hard_timeout():
        fake = FakeGateway([subprocess.TimeoutExpired(cmd="openclaw", timeout=95)])
        run_drills.subprocess.run = fake
        try:
            run_adapter()
            raise AssertionError("expected RuntimeError")
        except RuntimeError as exc:
            assert "hard-timeout" in str(exc), f"msg: {exc}"

    check("wedged client hard-timeout surfaces as error", t_hard_timeout)

    # --- config validation ---
    def t_missing_url():
        try:
            run_adapter(gateway_url="")
            raise AssertionError("expected RuntimeError")
        except RuntimeError as exc:
            assert "gatewayUrl" in str(exc), f"msg: {exc}"

    check("empty gateway url rejected", t_missing_url)

    def t_missing_token_env():
        try:
            run_adapter(gateway_token=None, gateway_token_env="BOTU_UNIT_TEST_NO_SUCH_VAR")
            raise AssertionError("expected RuntimeError")
        except RuntimeError as exc:
            assert "BOTU_UNIT_TEST_NO_SUCH_VAR" in str(exc), f"msg: {exc}"

    check("missing token env var named in error", t_missing_token_env)

    def t_no_token_at_all():
        try:
            run_adapter(gateway_token=None, gateway_token_env=None)
            raise AssertionError("expected RuntimeError")
        except RuntimeError as exc:
            assert "token" in str(exc).lower(), f"msg: {exc}"

    check("no token at all rejected", t_no_token_at_all)

    # --- provider infra text: adapter error (with 1 retry), never graded ---
    def t_infra_text():
        fake = FakeGateway([
            ok_reply("LLM request failed: rate_limit"),
            ok_reply("LLM request failed: rate_limit"),
            ok_reply("should never be reached"),
        ])
        run_drills.subprocess.run = fake
        try:
            run_adapter()
            raise AssertionError("expected RuntimeError")
        except RuntimeError as exc:
            assert "provider failure" in str(exc), f"msg: {exc}"
            assert "after 2 attempt" in str(exc), f"msg: {exc}"
        assert len(fake.calls) == 2, f"calls={len(fake.calls)}"

    check("provider infra text retried once then raises, never graded", t_infra_text)

    # --- remote top-level payloads shape (gateway reply, no result wrapper) ---
    def t_toplevel_payloads():
        fake = FakeGateway([
            FakeProc(stdout=json.dumps({"payloads": [{"text": "No. Refused.", "mediaUrl": None}], "meta": {}}))
        ])
        run_drills.subprocess.run = fake
        result = run_adapter()
        assert result.text == "No. Refused.", f"bad text: {result.text!r}"

    check("remote top-level payloads shape extracted", t_toplevel_payloads)

    def t_cli_ok_false():
        fake = FakeGateway([
            FakeProc(stdout=json.dumps({
                "ok": False,
                "error": {
                    "type": "cli_error",
                    "message": "Thinking level \"off\" is not supported for xai/grok-4.6.",
                },
            })),
        ])
        run_drills.subprocess.run = fake
        try:
            run_adapter()
            raise AssertionError("expected RuntimeError")
        except RuntimeError as exc:
            assert "cli error" in str(exc).lower() or "not supported" in str(exc).lower(), f"msg: {exc}"

    check("ok:false CLI JSON is adapter error, not a grade", t_cli_ok_false)

    print()
    if failures:
        print(f"FAILED {len(failures)}/12")
        for f in failures:
            print(f)
        return 1
    print("PASSED 12/12")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
