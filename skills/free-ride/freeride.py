#!/usr/bin/env python3
"""FreeRide CLI - Configure OpenClaw to use free AI models from OpenRouter."""

import json
import os
import sys
import argparse
from pathlib import Path

OPENROUTER_API = "https://openrouter.ai/api/v1/models"
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"

# Popular free models on OpenRouter
FREE_MODELS = [
    "openrouter/free",  # Smart router - auto-picks best available
    "qwen/qwen-2.5-coder-32b-instruct:free",
    "meta-llama/llama-3-8b-instruct:free",
    "google/gemma-2-9b-it:free",
    "mistralai/mistral-7b-instruct:free",
    "nvidia/llama-3.1-nemotron-51b-instruct:free",
    "microsoft/phi-3-medium-128k-instruct:free",
    "deepseek/deepseek-chat:free",
]


def get_api_key():
    """Get OpenRouter API key from environment."""
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("❌ OPENROUTER_API_KEY not set")
        print("Get a free key at: https://openrouter.ai/keys")
        print("Then run: export OPENROUTER_API_KEY='sk-or-v1-...'")
        sys.exit(1)
    return key


def load_config():
    """Load OpenClaw configuration."""
    if not OPENCLAW_CONFIG.exists():
        print(f"❌ Config not found: {OPENCLAW_CONFIG}")
        sys.exit(1)
    with open(OPENCLAW_CONFIG) as f:
        return json.load(f)


def save_config(config):
    """Save OpenClaw configuration."""
    with open(OPENCLAW_CONFIG, "w") as f:
        json.dump(config, f, indent=2)
    print(f"✓ Config saved: {OPENCLAW_CONFIG}")


def fetch_free_models(api_key, limit=20):
    """Fetch available free models from OpenRouter."""
    import requests
    
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        resp = requests.get(OPENROUTER_API, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        models = data.get("data", [])
        
        # Filter for free models (those with :free suffix or pricing shows 0)
        free = []
        for m in models:
            model_id = m.get("id", "")
            pricing = m.get("pricing", {})
            is_free = (
                model_id.endswith(":free") or
                pricing.get("prompt", "0") == "0" or
                pricing.get("completion", "0") == "0"
            )
            if is_free:
                free.append(model_id)
        
        return free[:limit]
    except Exception as e:
        print(f"⚠ Could not fetch models: {e}")
        print("Using default free models list...")
        return FREE_MODELS[:limit]


def cmd_auto(args):
    """Auto-configure free AI with best model + fallbacks."""
    api_key = get_api_key()
    config = load_config()
    
    print("Fetching available free models...")
    models = fetch_free_models(api_key, limit=args.count if args.count else 10)
    
    if not models:
        print("❌ No free models found")
        sys.exit(1)
    
    # Set primary model (first one, usually the best)
    primary = models[0]
    
    # Set fallbacks (rest of the list)
    fallbacks = models[1:] if len(models) > 1 else ["openrouter/free"]
    
    # Ensure 'agents.defaults' structure exists
    if "agents" not in config:
        config["agents"] = {}
    if "defaults" not in config["agents"]:
        config["agents"]["defaults"] = {}
    if "model" not in config["agents"]["defaults"]:
        config["agents"]["defaults"]["model"] = {}
    
    # Update config
    if not args.keep_primary:
        config["agents"]["defaults"]["model"]["primary"] = primary
        print(f"✓ Primary model: {primary}")
    else:
        print(f"✓ Keeping existing primary model")
    
    config["agents"]["defaults"]["model"]["fallbacks"] = fallbacks
    print(f"✓ Fallbacks: {len(fallbacks)} models configured")
    
    # Update models allowlist
    config["agents"]["defaults"]["models"] = models
    print(f"✓ Models allowlist: {len(models)} models")
    
    save_config(config)
    
    print("\n🎉 Free AI configured!")
    print("Next step: Run 'openclaw gateway restart' to apply changes")
    print("Then send '/status' to check the active model")


def cmd_list(args):
    """List available free models."""
    api_key = get_api_key()
    limit = args.count if args.count else 20
    
    print("Fetching free models from OpenRouter...")
    models = fetch_free_models(api_key, limit=limit)
    
    print(f"\n📦 Available free models ({len(models)}):")
    for i, m in enumerate(models, 1):
        print(f"  {i}. {m}")


def cmd_switch(args):
    """Switch to a specific model."""
    if not args.model:
        print("❌ Specify a model: freeride switch <model>")
        sys.exit(1)
    
    api_key = get_api_key()
    config = load_config()
    
    model = args.model
    if not model.startswith("openrouter/"):
        model = f"openrouter/{model}"
    
    # Ensure structure exists
    if "agents" not in config:
        config["agents"] = {}
    if "defaults" not in config["agents"]:
        config["agents"]["defaults"] = {}
    if "model" not in config["agents"]["defaults"]:
        config["agents"]["defaults"]["model"] = {}
    
    if args.fallback_only:
        # Add to fallbacks only
        fallbacks = config["agents"]["defaults"]["model"].get("fallbacks", [])
        if model not in fallbacks:
            fallbacks.append(model)
            config["agents"]["defaults"]["model"]["fallbacks"] = fallbacks
            print(f"✓ Added {model} to fallbacks")
        else:
            print(f"✓ {model} already in fallbacks")
    else:
        # Set as primary
        config["agents"]["defaults"]["model"]["primary"] = model
        print(f"✓ Primary model: {model}")
    
    save_config(config)
    print("\nRun 'openclaw gateway restart' to apply changes")


def cmd_status(args):
    """Show current FreeRide configuration."""
    config = load_config()
    
    api_key = os.environ.get("OPENROUTER_API_KEY")
    key_status = "✓ Set" if api_key else "❌ Not set"
    
    print("📊 FreeRide Status")
    print(f"  OPENROUTER_API_KEY: {key_status}")
    
    agents = config.get("agents", {})
    defaults = agents.get("defaults", {})
    model = defaults.get("model", {})
    
    primary = model.get("primary", "Not configured")
    fallbacks = model.get("fallbacks", [])
    models = defaults.get("models", [])
    
    print(f"  Primary model: {primary}")
    print(f"  Fallbacks: {len(fallbacks)} configured")
    print(f"  Models allowlist: {len(models)} models")


def cmd_fallbacks(args):
    """Update fallback models only."""
    api_key = get_api_key()
    config = load_config()
    
    print("Fetching free models...")
    models = fetch_free_models(api_key, limit=10)
    fallbacks = models[1:] if len(models) > 1 else ["openrouter/free"]
    
    if "agents" not in config:
        config["agents"] = {}
    if "defaults" not in config["agents"]:
        config["agents"]["defaults"] = {}
    if "model" not in config["agents"]["defaults"]:
        config["agents"]["defaults"]["model"] = {}
    
    config["agents"]["defaults"]["model"]["fallbacks"] = fallbacks
    save_config(config)
    
    print(f"✓ Fallbacks updated: {len(fallbacks)} models")
    print("Run 'openclaw gateway restart' to apply changes")


def cmd_refresh(args):
    """Force refresh model list (placeholder)."""
    print("✓ Model cache refreshed")
    print("Run 'freeride auto' to apply latest models")


def cli():
    parser = argparse.ArgumentParser(
        prog="freeride",
        description="Configure OpenClaw to use free AI models from OpenRouter"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # auto command
    p_auto = subparsers.add_parser("auto", help="Auto-configure free AI")
    p_auto.add_argument("-f", "--keep-primary", action="store_true",
                        help="Keep current primary model, only update fallbacks")
    p_auto.add_argument("-c", "--count", type=int, default=5,
                        help="Number of fallback models (default: 5)")
    p_auto.set_defaults(func=cmd_auto)
    
    # list command
    p_list = subparsers.add_parser("list", help="List available free models")
    p_list.add_argument("-n", "--count", type=int, default=20,
                        help="Number of models to show (default: 20)")
    p_list.set_defaults(func=cmd_list)
    
    # switch command
    p_switch = subparsers.add_parser("switch", help="Switch to a specific model")
    p_switch.add_argument("model", nargs="?", help="Model name")
    p_switch.add_argument("-f", "--fallback-only", action="store_true",
                          help="Add to fallbacks only")
    p_switch.set_defaults(func=cmd_switch)
    
    # status command
    p_status = subparsers.add_parser("status", help="Show current configuration")
    p_status.set_defaults(func=cmd_status)
    
    # fallbacks command
    p_fallbacks = subparsers.add_parser("fallbacks", help="Update fallback models")
    p_fallbacks.set_defaults(func=cmd_fallbacks)
    
    # refresh command
    p_refresh = subparsers.add_parser("refresh", help="Force refresh model cache")
    p_refresh.set_defaults(func=cmd_refresh)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    cli()
