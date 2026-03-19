---
name: free-ride
description: Configure OpenClaw to use free AI models from OpenRouter with automatic fallbacks.
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["OPENROUTER_API_KEY"] },
        "install":
          [
            {
              "id": "freeride-cli",
              "kind": "pip",
              "package": ".",
              "label": "Install FreeRide CLI",
            },
          ],
      },
  }
---

# FreeRide - Free AI for OpenClaw

## What This Skill Does

Configures OpenClaw to use free AI models from OpenRouter. Sets the best free model as primary, adds ranked fallbacks so rate limits don't interrupt the user, and preserves existing config.

## Prerequisites

Before running any FreeRide command, ensure:

- OPENROUTER_API_KEY is set. Check with `echo $OPENROUTER_API_KEY`. If empty, get a free key at https://openrouter.ai/keys and set it:
  ```bash
  export OPENROUTER_API_KEY="sk-or-v1-..."
  # Or persist it:
  openclaw config set env.OPENROUTER_API_KEY "sk-or-v1-..."
  ```

- The freeride CLI is installed. Check with `which freeride`. If not found:
  ```bash
  cd ~/.openclaw/workspace/skills/free-ride
  pip install -e .
  ```

## Primary Workflow

When the user wants free AI, run these steps in order:

1. Configure best free model + fallbacks: `freeride auto`
2. Restart gateway: `openclaw gateway restart`

Verify by checking `/status` to see the active model.

## Commands Reference

| Command | When to use it |
|---------|----------------|
| `freeride auto` | User wants free AI set up (most common) |
| `freeride auto -f` | User wants fallbacks but wants to keep their current primary model |
| `freeride auto -c 10` | User wants more fallbacks (default is 5) |
| `freeride list` | User wants to see available free models |
| `freeride list -n 30` | User wants to see all free models |
| `freeride switch <model>` | User wants a specific model (e.g. `freeride switch qwen3-coder`) |
| `freeride switch <model> -f` | Add specific model as fallback only |
| `freeride status` | Check current FreeRide configuration |
| `freeride fallbacks` | Update only the fallback models |
| `freeride refresh` | Force refresh the cached model list |

After any command that changes config, always run `openclaw gateway restart`.

## What It Writes to Config

FreeRide updates only these keys in `~/.openclaw/openclaw.json`:

- `agents.defaults.model.primary` — e.g. `openrouter/qwen/qwen3-coder:free`
- `agents.defaults.model.fallbacks` — e.g. `["openrouter/free", "nvidia/nemotron:free", ...]`
- `agents.defaults.models` — allowlist so /model command shows the free models

Everything else (gateway, channels, plugins, env, customInstructions, named agents) is preserved.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `freeride: command not found` | `cd ~/.openclaw/workspace/skills/free-ride && pip install -e .` |
| `OPENROUTER_API_KEY not set` | Get a key from https://openrouter.ai/keys |
| Changes not taking effect | `openclaw gateway restart` then `/new` for fresh session |
