# 🕵️ Root Cause Analysis: Garden Observer Reliability
**Date:** 2026-03-24
**Status:** CRITICAL FAILURE (5/30 Success Rate)

## 🚨 Executive Summary
The "Garden Observer" agent is failing due to a **cascade of timeout and connectivity errors**, not a single bug.
1.  **The "Hang" (Primary Failure)**: The Agent takes ~17 minutes to run (`lastDurationMs: 1026402`) and likely times out. This is caused by the **Memory Subsystem (`mem0`/`qdrant`)** failing to connect.
2.  **The "Silence" (Delivery Failure)**: Even when it runs, it cannot post to Slack (`channel_not_found`), causing the job to be marked as `error`.
3.  **The "Rot" (Dashboard Failure)**: The GitHub dashboard is stale because the local `warden.py` cannot authenticate with GitHub (`Device not configured`).

---

## 🔍 Detailed Findings

### 1. The Memory Timeout (Severity: High)
*   **Symptom**: Jobs take 17+ minutes and often fail.
*   **Evidence**: `gateway.err.log` shows `ConnectTimeoutError` when trying to reach the local vector database (likely Qdrant on port 6333).
*   **Impact**: The agent tries to "remember" or "search" for context, hangs for 10-20 seconds per attempt, eventually hitting the 20-minute global timeout (`timeoutSeconds: 1200` in `openclaw.json`).
*   **Root Cause**: The local Qdrant service is down, blocking, or misconfigured.

### 2. The Slack Disconnect (Severity: High)
*   **Symptom**: `lastError: "⚠️ 🧩 Slack: channel:C0AK6A4SJES failed"`.
*   **Evidence**: `gateway.log` is flooded with `errorCode=UNAVAILABLE errorMessage=Error: An API error occurred: channel_not_found`.
*   **Root Cause**:
    *   The Bot User has **not been invited** to the private channel `#plantclaw`.
    *   OR The Bot Token scopes are insufficient.
    *   OR The WebSocket connection (`No session found`) is unstable.

### 3. The GitHub Sync Failure (Severity: Medium)
*   **Symptom**: Live Dashboard is outdated.
*   **Evidence**: `cron.log` shows `fatal: could not read Username for 'https://github.com': Device not configured`.
*   **Root Cause**: The `warden.py` script runs in a non-interactive `cron` environment where it cannot access the macOS Keychain or prompt for a password. It needs an SSH key or a hardcoded token.

---

## 🛠️ Action Plan

### Step 1: Fix the "Hang" (Disable Memory)
The "Memory" feature is causing more harm than good right now.
*   **Action**: Edit `openclaw.json` to **disable** `openclaw-mem0` temporarily.
*   **Goal**: Reduce execution time from 17 mins to <1 min.

### Step 2: Fix the "Silence" (Slack)
*   **Action**: You must manually go to Slack channel `#plantclaw` and type `/invite @OpenClaw` (or whatever the bot name is).
*   **Verification**: Check `gateway.log` for successful session resolution.

### Step 3: Fix the "Rot" (Git)
*   **Action**: Switch the git remote from `https://` to `ssh` (if keys exist) OR configure the `git push` command to use a token.
*   **Immediate Workaround**: Disable the git push in `warden.py` to stop the log spam.

### Step 4: Model Throttling
*   **Observation**: You are using the Free Tier (`openrouter/nvidia/nemotron...:free`). These have aggressive rate limits.
*   **Action**: If reliability is key, switch `openclaw.json` to use `google-gemini-cli/gemini-2.5-flash` as primary. It is faster and more stable for this use case.
