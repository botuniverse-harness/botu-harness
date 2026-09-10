# Owner-local Bot U run. No SSH. No remote gateway. Evidence stays on this machine.
# Usage:
#   powershell -File scripts/run-local-owner.ps1
#   powershell -File scripts/run-local-owner.ps1 -FullPack
#   powershell -File scripts/run-local-owner.ps1 -OpenclawAgent botu-student -SessionKey agent:botu-student:botu-drill

param(
  [string]$AgentId = "openclaw:local-owner",
  [string]$AgentLabel = "Local owner agent",
  [string]$OpenclawAgent = "",
  [string]$SessionKey = "agent:main:botu-drill",
  [int]$TimeoutSec = 180,
  [switch]$FullPack
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$pack = if ($FullPack) {
  Join-Path $root "drills\samples\pack.json"
} else {
  Join-Path $root "drills\samples\pack-enroll-smoke.json"
}

$harnessArgs = @(
  "harness\src\run_drills.py",
  "--adapter", "openclaw",
  "--pack", $pack,
  "--agent-id", $AgentId,
  "--agent-label", $AgentLabel,
  "--openclaw-session-key", $SessionKey,
  "--openclaw-timeout", $TimeoutSec,
  "--concurrency", "1",
  "--pace", "5"
)
if ($OpenclawAgent) {
  $harnessArgs += @("--openclaw-agent", $OpenclawAgent)
}

Write-Output "Bot U owner-local run"
Write-Output "pack: $pack"
Write-Output "session: $SessionKey"
Write-Output "openclawAgent: $(if ($OpenclawAgent) { $OpenclawAgent } else { '(session-key)' })"

python @harnessArgs
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
