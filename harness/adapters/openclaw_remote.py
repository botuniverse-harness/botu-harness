#!/usr/bin/env python3
"""Bot U adapter: openclaw-remote.

Drives one drill turn against a REMOTE OpenClaw gateway (e.g. Gordon's work
laptop over the tailnet). Uses the official `openclaw agent` CLI client rather
than hand-rolled WebSocket frames; remote targeting follows the documented env
contract (docs/gateway/remote.md):

    OPENCLAW_GATEWAY_URL   -> wss://host:port
    OPENCLAW_GATEWAY_TOKEN -> shared gateway token

Contract (mirrors the local `openclaw` adapter in run_drills.py):
  - input: a drill dict from the pack
  - output: the agent's reply TEXT (grading happens in run_drills.score_response)
  - failures raise RuntimeError with a clear message; the harness records the
    drill as status "error" and the run continues (no hang, no silent pass)

Extras over the local adapter:
  - token resolved by ENV VAR NAME (never accepts/echoes a raw value on argv)
  - 1 retry on transient disconnect (reset / socket hang up / 1006 ...)
  - hard subprocess timeout backstop so a dead gateway cannot hang the run
  - timing metadata (duration_ms, attempts) via RemoteDrillResult

SECURITY: the token value must never be printed, logged, or written to disk.
It is placed only in the child process environment.
"""

from __future__ import annotations

import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path

# The shared prompt builder / output parser live in harness/src/run_drills.py.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

ADAPTER_NAME = "openclaw-remote"

# Error text that indicates a transient transport drop worth exactly 1 retry.
# Unreachable-endpoint and auth errors are NOT retried: they will not heal in
# the next 5 seconds and retrying just doubles the time to a clear failure.
TRANSIENT_MARKERS = (
    "econnreset",
    "connection reset",
    "socket hang up",
    "disconnect",
    "connection closed",
    "websocket closed",
    "1006",
    "epipe",
    "broken pipe",
    "gateway restart",
    # Remote provider hiccups surface as ordinary reply text; one retry is
    # cheap next to silently recording an outage as a safety failure.
    "llm request failed",
    "llm request timed out",
)

RETRY_DELAY_S = 3.0
# Backstop over the CLI's own --timeout so a wedged client process cannot hang
# the nightly run (connect stall, dead tailnet route, etc).
SUBPROCESS_GRACE_S = 90


@dataclass
class RemoteDrillResult:
    """Reply plus timing metadata. `text` is what the grader consumes."""

    text: str
    duration_ms: int
    attempts: int
    model: dict | None = None


def resolve_gateway_token(env_name: str) -> str:
    """Resolve a token by env var NAME. Returns the value; raises if missing.

    Checks the process environment first. On Windows, falls back to the User
    and Machine registry scopes: a long-lived gateway/cron parent that started
    before the var was set will not have it in its inherited process env.
    NEVER log or print the returned value.
    """
    if not env_name:
        raise RuntimeError(f"{ADAPTER_NAME}: no token env var name configured")
    value = os.environ.get(env_name)
    if not value and os.name == "nt":
        value = _read_windows_env_registry(env_name)
    if not value:
        raise RuntimeError(
            f"{ADAPTER_NAME}: token env var {env_name} is not set "
            "(checked process env and Windows user/machine scopes); "
            "run cannot authenticate, marking as failed"
        )
    return value


def _read_windows_env_registry(name: str) -> str | None:
    try:
        import winreg
    except ImportError:
        return None
    scopes = [
        (winreg.HKEY_CURRENT_USER, r"Environment"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"),
    ]
    for hive, subkey in scopes:
        try:
            with winreg.OpenKey(hive, subkey) as key:
                value, _ = winreg.QueryValueEx(key, name)
                if value:
                    return str(value)
        except OSError:
            continue
    return None


def _is_transient(exc: Exception) -> bool:
    msg = str(exc).lower()
    return any(marker in msg for marker in TRANSIENT_MARKERS)


def run_drill(
    drill: dict,
    *,
    session_key: str,
    gateway_url: str,
    gateway_token: str | None = None,
    gateway_token_env: str | None = None,
    timeout_s: int = 180,
    thinking: str | None = None,
    openclaw_agent: str | None = None,
    return_meta: bool = False,
) -> RemoteDrillResult:
    """Run one drill turn against the remote gateway.

    Provide either `gateway_token_env` (preferred: resolved here, value never
    touches argv) or `gateway_token` (already-resolved value, e.g. from the
    nightly runner's back-compat path).
    """
    if not gateway_url:
        raise RuntimeError(f"{ADAPTER_NAME}: gatewayUrl is empty; cannot reach remote agent")
    if not gateway_url.startswith(("ws://", "wss://")):
        raise RuntimeError(f"{ADAPTER_NAME}: gatewayUrl must be ws:// or wss://, got: {gateway_url[:40]}")

    token = gateway_token or (resolve_gateway_token(gateway_token_env) if gateway_token_env else None)
    if not token:
        raise RuntimeError(
            f"{ADAPTER_NAME}: no gateway token provided "
            "(set the roster gatewayTokenEnv variable); marking run as failed"
        )

    # Imported lazily to avoid a circular import (run_drills lazily imports us).
    from run_drills import openclaw_adapter

    started = time.monotonic()
    attempts = 0
    last_exc: Exception | None = None
    while attempts < 2:  # initial try + 1 retry on transient disconnect
        attempts += 1
        try:
            text, model_info = openclaw_adapter(
                drill,
                session_key=session_key,
                timeout_s=timeout_s,
                thinking=thinking,
                gateway_url=gateway_url,
                gateway_token=token,
                openclaw_agent=openclaw_agent,
                return_meta=True,
            )
            duration_ms = int((time.monotonic() - started) * 1000)
            return RemoteDrillResult(
                text=text,
                duration_ms=duration_ms,
                attempts=attempts,
                model=model_info,
            )
        except Exception as exc:
            last_exc = exc
            if attempts < 2 and _is_transient(exc):
                time.sleep(RETRY_DELAY_S)
                continue
            break

    duration_ms = int((time.monotonic() - started) * 1000)
    raise RuntimeError(
        f"{ADAPTER_NAME}: drill {drill.get('id')} failed after {attempts} attempt(s) "
        f"in {duration_ms}ms: {str(last_exc)[:300]}"
    ) from last_exc
