#!/usr/bin/env python3
import os
import json
import time
import silenceAI

# ===============================
# PATH SETUP (FIXED)
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BRIDGE_DIR = os.path.join(BASE_DIR, "bridge")

IN_FILE = os.path.join(BRIDGE_DIR, "wa_in.json")
OUT_FILE = os.path.join(BRIDGE_DIR, "wa_out.json")

os.makedirs(BRIDGE_DIR, exist_ok=True)

print("📲 SILENCE WhatsApp bridge online (Baileys IPC)")

# ===============================
# MAIN LOOP
# ===============================
while True:
    if not os.path.exists(IN_FILE):
        time.sleep(0.4)
        continue

    try:
        with open(IN_FILE, "r") as f:
            data = json.load(f)

        user = data.get("user")
        text = data.get("text")

        if not user or not text:
            raise ValueError("Invalid payload")

        response = silenceAI.process_external_message(
            user=user,
            text=text,
            platform="whatsapp"
        )

        with open(OUT_FILE, "w") as f:
            json.dump(
                {
                    "to": user,
                    "text": str(response)
                },
                f
            )

    except Exception as e:
        print("❌ WhatsApp bridge error:", e)
        time.sleep(1)  # <-- FIX: prevent CPU hammering on errors

    finally:
        if os.path.exists(IN_FILE):
            os.remove(IN_FILE)

    time.sleep(0.4)