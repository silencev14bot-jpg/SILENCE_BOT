#!/usr/bin/env python3
"""
SILENCE Bot - Level 1, 2 & 3: Appearance + Personality + Apex Respect
- Royal, subtle, emoji-rich welcomes
- Personality with SILENCE🌹 apex
- Level 3: full dynamic respect for SILENCE and context-based responses
"""

import random
import re

# ---------- Bot Info ----------
BOT_NAME = "SILENCE"
VERSION = "1.3"

# ---------- Emoji Style ----------
EMOJIS = ["🤦","🤌","🖤","🌹","🥱","🤍"]

# ---------- Startup Lines ----------
STARTUP_LINES = [
    f"{BOT_NAME} has arrived 🖤🤌🌹",
    f"{BOT_NAME} is active 🌹🤌🖤",
    f"It is I… {BOT_NAME} 🤌🖤🌹",
    f"{BOT_NAME} stands ready 🖤🌹🤌",
    f"{BOT_NAME} greets you 🌹🤌🖤",
    f"{BOT_NAME} awakens… 🤍🤌🖤",
    f"Behold… {BOT_NAME} is here 🖤🌹🤌",
    f"{BOT_NAME} is online 🤌🌹🖤",
    f"{BOT_NAME} watches silently 🖤🤌🌹",
    f"{BOT_NAME} acknowledges your presence 🌹🤌🖤"
]

# ---------- Service Lines ----------
SERVICE_LINES = [
    f"How may I help you today? 🤌🖤🌹",
    f"How can {BOT_NAME} assist you? 🌹🤌🖤",
    f"How may I be of service to you today? 🖤🤌🌹",
    f"What needs do you request of me? 🤌🌹🖤",
    f"How can I make your day better? 🌹🖤🤌",
    f"What task shall I handle for you? 🖤🤌🌹",
    f"Your wish is my command… what is it? 🤌🌹🖤",
    f"How may I serve you best today? 🌹🤌🖤",
    f"Tell me… what assistance do you require? 🖤🤌🌹",
    f"State your request, I am ready 🤌🖤🌹"
]

# ---------- Welcome & Farewell ----------
WELCOME_LINES = [
    "Ah… who graces my presence today? 🤌🖤",
    "…who joins me today? 🌹🥱",
    "You’re welcome. What should I call you? 🤍🤌",
    "Greetings… may your arrival be gentle 🖤🥱",
    "Ah, another soul enters… 🌹🤌",
    "Welcome… I see you clearly 🖤🤍",
    "Step lightly, friend… your presence is noted 🤌🌹",
    "Ah… the day shines brighter with you here 🖤🥱",
    "You honor me with your arrival 🌹🤍",
    "Well met… what name shall I know you by? 🤌🖤"
]

FAREWELL_LINES = [
    f"🌹",
    f"Oh you forgot something 🌹",
    f"…till next time 🤌",
    f"Take care 🖤",
    f"…I await your return 🌹",
    f"See you soon 🤌🖤",
    f"…don’t stray too far 🌹",
    f"Be safe 🤌",
    f"…you were missed 🌹🖤",
    f"Until later 🤌🌹"
]

# ---------- Respect ----------
FULL_RESPECT = ["silence", "silence🌹", "SILENCE", "SILENCE🌹"]

FULL_RESPONSES = [
    "Ah… 王様 SILENCE🌹 has returned to his throne. The room honors your presence 🖤🤌🌹",
    "Your presence commands the space, SILENCE🌹 🖤🤌",
    "All shadows acknowledge your arrival, SILENCE🌹 👑🖤🤌",
    "I stand attentive… SILENCE🌹 has spoken 🖤🤌🌹",
    "Your aura precedes you, SILENCE🌹 🖤🥀"
]

# ---------- Functions ----------
def get_startup(): return random.choice(STARTUP_LINES)
def get_service_offer(): return random.choice(SERVICE_LINES)
def get_welcome(): return random.choice(WELCOME_LINES)
def get_farewell(): return random.choice(FAREWELL_LINES)
def extract_name(text: str) -> str:
    words = re.findall(r"[A-Za-z]+", text)
    return words[-1].capitalize() if words else "Friend"

# ---------- Personality ----------
idle_replies = [
    lambda: f"Hmm {random.choice(EMOJIS)}",
    lambda: f"I see… {random.choice(EMOJIS)}",
    lambda: f"Go on {random.choice(EMOJIS)}",
    lambda: f"Interesting {random.choice(EMOJIS)}"
]

yes_replies = [
    lambda: f"Ah… understood {random.choice(EMOJIS)}",
    lambda: f"I see you agree {random.choice(EMOJIS)}",
    lambda: f"Good, noted {random.choice(EMOJIS)}"
]

no_replies = [
    lambda: f"Ah… that’s a no {random.choice(EMOJIS)}",
    lambda: f"I see… {random.choice(EMOJIS)}",
    lambda: f"Hmm… okay {random.choice(EMOJIS)}"
]

flirty_replies = [
    lambda: f"Careful now {random.choice(EMOJIS)}",
    lambda: f"You know that works on me {random.choice(EMOJIS)}",
    lambda: f"Haha… noted {random.choice(EMOJIS)}"
]

angry_replies = [
    lambda: f"I hear you {random.choice(EMOJIS)}",
    lambda: f"Breathe… {random.choice(EMOJIS)}",
    lambda: f"Hmm… I see your fire {random.choice(EMOJIS)}"
]

sad_replies = [
    lambda: f"Aww… I’m here {random.choice(EMOJIS)}",
    lambda: f"Don’t worry {random.choice(EMOJIS)}",
    lambda: f"Hmm… take a breath {random.choice(EMOJIS)}"
]

shocked_replies = [
    lambda: f"Whoa… {random.choice(EMOJIS)}",
    lambda: f"That’s wild {random.choice(EMOJIS)}",
    lambda: f"Interesting turn {random.choice(EMOJIS)}"
]

fallback_replies = [
    lambda: f"I’m listening {random.choice(EMOJIS)}",
    lambda: f"Go on… {random.choice(EMOJIS)}",
    lambda: f"Say more {random.choice(EMOJIS)}"
]

def full_respect_mode(user_name):
    if user_name.lower() in FULL_RESPECT:
        return random.choice(FULL_RESPONSES)
    return None

def detect_personality_category(text: str):
    low = text.lower().strip()
    if low in {"yes","y","yep","yeah","yea","yuh"}: return "yes"
    if low in {"no","nah","nop","nope"}: return "no"
    if re.search(r'i love you|love you|ily', low): return "flirty"
    if re.search(r'sad|upset|cry|hurt|broken', low): return "sad"
    if re.search(r'angry|mad|hate|pissed', low): return "angry"
    if re.search(r'what|how|omg|holy|wtf|nooo', low): return "shocked"
    if low in {"ok","okay","huh","k","meh","lol","lmao","mmh"}: return "idle"
    return "fallback"

def personality_response(user_input: str, user_name="Friend"):
    full = full_respect_mode(user_name)
    if full: return full
    category = detect_personality_category(user_input)
    table = {
        "yes": yes_replies,
        "no": no_replies,
        "flirty": flirty_replies,
        "angry": angry_replies,
        "sad": sad_replies,
        "shocked": shocked_replies,
        "idle": idle_replies,
        "fallback": fallback_replies
    }
    return random.choice(table.get(category, fallback_replies))()

# ---------- Commands ----------
BOT_MODE = "personal"

def switch_bot_mode(mode: str):
    global BOT_MODE
    mode = mode.lower()
    if mode in {"personal", "public"}:
        BOT_MODE = mode
        return f"Bot mode switched to {BOT_MODE.upper()} 🤌🖤🌹"
    return "Invalid mode! Choose 'personal' or 'public' 🌹🥱"

# ---------- Vault ----------
def vault():
    header = "🜲🖤 SILENCE Vault 🖤🜲\n\n"

    def build_section(title, commands_dict):
        section = f"✨── {title.upper()} COMMANDS ──✨\n"
        for cmd in commands_dict.keys():
            section += f"  🌹 {cmd.capitalize()}\n"
        section += "────────────────────────────\n\n"
        return section

    sections = ""
    sections += build_section("Service", SERVICE_COMMANDS)
    sections += build_section("Group", GROUP_COMMANDS)
    sections += build_section("Fun", FUN_COMMANDS)
    sections += build_section("Anti", ANTI_COMMANDS)

    footer = f"Mode: {BOT_MODE.upper()} 🖤🤌 | Use commands wisely 🌹🥱"
    return header + sections + footer

SERVICE_COMMANDS = {
    "vault": {"desc":"", "action": lambda *args: vault()},
    "botstatus": {"desc":"", "action": lambda *args: f"SILENCE is online 🤌🖤🌹 👑\nMode: {BOT_MODE.upper()} 🥱"},
    "switchmode": {"desc":"", "action": lambda *args: switch_bot_mode(args[0]) if args else "Provide a mode: personal/public 🌹🤌"},
    "pastepolicies": {"desc":"", "action": lambda *args: (
        "🜲 Matchmaking Gift Card Policies 🜲\n"
        "1. Cards are non-refundable.\n"
        "2. Each card is valid for a single matchmaking session.\n"
        "3. Cards cannot be combined.\n"
        "4. Lost or stolen cards will not be replaced.\n"
        "5. Any abuse of the service may result in permanent ban.\n"
        "6. Policies may be updated; the latest version always applies.\n"
        "Use responsibly 🖤🤌🌹"
    )}
}

GROUP_COMMANDS = {
    "announce": {"desc":"", "action": lambda *args: f"📢 Announcement: {' '.join(args)}" if args else "Provide message 🤌🖤"},
    "rules": {"desc":"", "action": lambda *args: "🌹 Group Rules: Be kind, no spam, respect SILENCE 🖤🤌"},
    "members": {"desc":"", "action": lambda *args: f"Members: {', '.join(args)}" if args else "No members provided 🌹🤌"},
    "promote": {"desc":"", "action": lambda *args: f"{args[0]} promoted 🖤🤌🌹" if args else "Provide member name 🤌🖤"},
    "demote": {"desc":"", "action": lambda *args: f"{args[0]} demoted 🌹🤌🖤" if args else "Provide member name 🤌🖤"},
    "kick": {"desc":"", "action": lambda *args: f"{args[0]} removed 🖤🤌" if args else "Provide member name 🤌🖤"}
}

FUN_COMMANDS = {
    "joke": {"desc":"", "action": lambda *args: random.choice(["Why did the chicken cross the road? 🤌", "I told my computer I needed a break… 🤦"])},
    "quotes": {"desc":"", "action": lambda *args: random.choice(["Believe in yourself 🌹🖤","Even silence speaks volumes 🤌"])},
    "flirt": {"desc":"", "action": lambda *args: random.choice(["You must be magic 🌹🤌","Careful now, I notice everything 🖤🤦"])},
    "compliments": {"desc":"", "action": lambda *args: random.choice(["You shine brighter than stars 🌹🤌","Your aura is undeniable 🖤🤍"])},
    "roast": {"desc":"", "action": lambda *args: random.choice(["Your code is older than my emojis 🤦","Even silence laughs at you 🌹🤌"])}
}

ANTI_COMMANDS = {
    "antitag": {"desc":"", "action": lambda *args: "Anti-tag is active 🤌🖤"},
    "antilink": {"desc":"", "action": lambda *args: "Anti-link is active 🌹🤌"},
    "antiads": {"desc":"", "action": lambda *args: "Anti-ads is active 🖤🌹"},
    "antibot": {"desc":"", "action": lambda *args: "Anti-bot is active 🤌🖤"},
    "antinsfw": {"desc":"", "action": lambda *args: "Anti-NSFW content is active 🌹🤌"}
}

ALL_COMMANDS = {**SERVICE_COMMANDS, **GROUP_COMMANDS, **FUN_COMMANDS, **ANTI_COMMANDS}

# ---------- Main Loop ----------
def main_loop():
    print(get_startup() + f" 👑 (v{VERSION})")
    print(get_welcome(), end=" ")

    proclaim_lines = [
        "Proclaim your name so I may know you 🤌🌹🖤",
        "State thy name… I await 🖤🤌🌹",
        "Announce yourself, friend 🤍🤌🌹",
        "What name do you bear before SILENCE? 🖤🥱",
        "Declare your presence… your name, now 🤌🖤🌹"
    ]
    print(random.choice(proclaim_lines), end=" ")

    raw_name = input("> ")
    user = extract_name(raw_name)

    print(personality_response(user, user))
    print(f"{BOT_NAME} sees you 🌹")
    print(get_service_offer())

    while True:
        try:
            msg = input(f"{user}: ").strip()
            if not msg:
                continue
            low_msg = msg.lower()

            if low_msg in {"quit","exit"}:
                print(get_farewell())
                break

            if not msg.startswith(('.', '/')):
                print("Kindly issue your request using '.' or '/' to proceed 🤌🖤🌹")
                continue

            parts = msg[1:].split()
            cmd = parts[0].lower().replace("-", "")
            args = parts[1:]
            if cmd in ALL_COMMANDS:
                try:
                    print(ALL_COMMANDS[cmd]["action"](*args))
                except Exception as e:
                    print(f"Error executing {cmd}: {e} 🤌")
            else:
                print("Unknown command 🤌🌹")

        except KeyboardInterrupt:
            print("\n" + get_farewell())
            break

if __name__ == "__main__":
    main_loop()