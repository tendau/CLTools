import os
import json
from datetime import datetime
from platformdirs import user_data_dir

APP_NAME = "cl_llm"
USER_DATA_FILE = "user_data.json"

USER_DATA_PATH = os.path.join(user_data_dir(APP_NAME), USER_DATA_FILE)
SELF_PERSONALITY_FILE = "self_personality.json"
SELF_PERSONALITY_PATH = os.path.join(user_data_dir(APP_NAME), SELF_PERSONALITY_FILE)

def call_tool(tool_call):
    tool_name = tool_call["tool_name"]
    args = tool_call.get("arguments", {})

    if tool_name == "update_user":
        return update_user(args.get("entry_type"), args.get("entry"))
    elif tool_name == "get_user_profile":
        return get_user_profile()
    elif tool_name == "update_self_personality":
        return update_self_personality(args.get("trait"))
    else:
        return {"status": "error", "message": f"Unknown tool {tool_name}"}

def ensure_user_data_file():
    os.makedirs(os.path.dirname(USER_DATA_PATH), exist_ok=True)
    if not os.path.exists(USER_DATA_PATH):
        with open(USER_DATA_PATH, "w") as f:
            json.dump([], f)

def ensure_self_personality_file():
    os.makedirs(os.path.dirname(SELF_PERSONALITY_PATH), exist_ok=True)
    if not os.path.exists(SELF_PERSONALITY_PATH):
        with open(SELF_PERSONALITY_PATH, "w") as f:
            json.dump([], f)
             
def update_user(entry_type: str, entry: str):
    if entry_type not in ("fact", "mannerism") or not entry:
        return {"status": "error", "message": "Invalid entry type or missing entry"}

    ensure_user_data_file()

    try:
        with open(USER_DATA_PATH, "r") as f:
            user_data = json.load(f)
    except json.JSONDecodeError:
        user_data = []

    user_data.append({
        "entry_type": entry_type,
        "entry": entry,
        "timestamp": datetime.utcnow().isoformat()
    })

    with open(USER_DATA_PATH, "w") as f:
        json.dump(user_data, f, indent=2)

    return {"status": "success", "message": f"{entry_type.capitalize()} added."}

def update_self_personality(trait: str):
    if not trait or not isinstance(trait, str):
        return {"status": "error", "message": "Trait must be a non-empty string."}

    ensure_self_personality_file()

    try:
        with open(SELF_PERSONALITY_PATH, "r") as f:
            personality_data = json.load(f)
    except json.JSONDecodeError:
        personality_data = []

    # Avoid duplicates (exact match)
    if any(entry.get("trait") == trait for entry in personality_data):
        return {"status": "skipped", "message": "Trait already recorded."}

    personality_data.append({
        "trait": trait,
        "timestamp": datetime.utcnow().isoformat()
    })

    with open(SELF_PERSONALITY_PATH, "w") as f:
        json.dump(personality_data, f, indent=2)

    return {"status": "success", "message": "Personality trait added."}

def get_user_profile():
    ensure_user_data_file()

    try:
        with open(USER_DATA_PATH, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = []

    facts = [entry["entry"] for entry in data if entry["entry_type"] == "fact"]
    mannerisms = [entry["entry"] for entry in data if entry["entry_type"] == "mannerism"]

    return {
        "facts": facts,
        "mannerisms": mannerisms
    }

def get_self_personality():
    ensure_self_personality_file()

    try:
        with open(SELF_PERSONALITY_PATH, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = []

    return [entry["trait"] for entry in data]
