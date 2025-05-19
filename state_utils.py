# state_utils.py

import json
import os
from datetime import datetime

def log_state_change(key, value):
    preview = str(value)
    if isinstance(value, str) and len(preview) > 120:
        preview = preview[:100] + "... [truncated]"
    elif isinstance(value, list):
        preview = f"List of {len(value)} items"
    elif isinstance(value, dict):
        preview = f"Dict with {len(value.keys())} keys"
    print(f"[STATE UPDATE] '{key}' → {preview}")

def update_state(state, key, value):
    """Add or update a value in the shared state with logging."""
    log_state_change(key, value)
    state[key] = value

def save_state_to_json(state, path="state_snapshot.json"):
    """Save the full state to a JSON file."""
    with open(path, "w") as f:
        json.dump(state, f, indent=2)
    print(f"💾 State saved to {path}")

def load_state_from_json(path="state_snapshot.json"):
    """Load a saved state from a JSON file."""
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    else:
        raise FileNotFoundError(f"No state file found at {path}")

def validate_state_keys(state, required_keys):
    """Ensure all required keys exist in the state before passing to agents."""
    missing = [k for k in required_keys if k not in state]
    if missing:
        raise KeyError(f"Missing required keys in state: {missing}")
    return True

def print_final_state(state):
    """Nicely print the final state with readable previews."""
    print("\n📦 Final State Snapshot:")
    for k, v in state.items():
        if isinstance(v, str) and len(v) > 150:
            preview = v[:150] + "... [truncated]"
        elif isinstance(v, list):
            preview = f"List with {len(v)} items"
        elif isinstance(v, dict):
            preview = f"Dict with {len(v.keys())} keys"
        else:
            preview = str(v)
        print(f"  {k}: {preview}")

def timestamped_filename(prefix="state", ext="json"):
    """Generate a timestamped filename for saving versions."""
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{prefix}_{ts}.{ext}"