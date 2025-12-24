# STANDARD: all commands must accept (user, *args)
#!/usr/bin/env python3
"""
SILENCE 2.0 — GPT-style Response Engine
- Modular
- VPS / Panel ready
- Full Phase 0–15 layered blueprint (including Fun Days)
"""

import random
import re
import os
import json
import time
import datetime

# ===============================
# CONFIG
# ===============================
START_TIME = time.time()
# OWNERS (Telegram IDs, WhatsApp numbers, names if you want)
OWNERS = {
    "silence",
    "7701556168",
    "2347078281050"
}
assert isinstance(OWNERS, (set, list, tuple)) and len(OWNERS) > 0, \
    "OWNERS must be a non-empty set/list of owner IDs"

# ===============================
# WHATSAPP PAIRING CORE
# ===============================

def wa_pair(user, wa_number=None):
    ...

def wa_unpair(user, wa_number=None):
    ...

def wa_listpairs(user):
    ...

def wa_autoload(user):
    ...    
            
# ===============================
# WHATSAPP SESSION REGISTRY
# ===============================

SESSIONS_FILE = "wa_sessions.json"

WA_SESSIONS = {}  # number -> metadata


def load_sessions():
    global WA_SESSIONS
    if os.path.exists(SESSIONS_FILE):
        try:
            with open(SESSIONS_FILE, "r") as f:
                WA_SESSIONS = json.load(f)
        except Exception:
            WA_SESSIONS = {}


def save_sessions():
    try:
        with open(SESSIONS_FILE, "w") as f:
            json.dump(WA_SESSIONS, f, indent=2)
    except Exception:
        pass    
    
# ============================================
# PHASE 0 — BIRTH (BOOT STATE)
# ============================================
class Boot:
    VERSION = "2.0"
    HEALTHY = True

    @staticmethod
    def startup():
        print(f"SILENCE 2.0 Booting v{Boot.VERSION}...")
        if not Boot.HEALTHY:
            print("Critical error. Boot failed.")
            exit(1)
        print("Boot successful.")

    @staticmethod
    def shutdown():
        print("Shutting down SILENCE 2.0 safely...")
        exit(0)

# ============================================
# PHASE 1 — PERCEPTION (FINAL FIXED)
# ============================================
class Perception:
    @staticmethod
    def process_input(text: str):
        if not text:
            return {
                "text": "",
                "intent": "chat",
                "emotion": None,
                "warn": False
            }

        raw = text.strip()
        low = raw.lower()

        # Detect command
        if low.startswith((".", "/")):
            return {
                "text": raw,
                "intent": "command",
                "emotion": Emotion.detect(raw),
                "warn": False
            }

        # ⚠️ Auto-correct command WITHOUT prefix
        if low.split()[0] in Commands.registry:
            return {
                "text": "." + raw,
                "intent": "command",
                "emotion": Emotion.detect(raw),
                "warn": True
            }

        # Normal chat
        return {
            "text": raw,
            "intent": "chat",
            "emotion": Emotion.detect(raw),
            "warn": False
        }

# ============================================
# PHASE 2 — ROLES & PERMISSIONS (FIXED)
# ============================================

class Roles:
    ADMINS = set()
    TRUSTED = set()
    
    @staticmethod
    def is_owner(user_id):
        return str(user_id) in OWNERS # uses global OWNER_ID safely

    @staticmethod
    def check_permission(user_id, permission):
        if permission == "owner":
            return Roles.is_owner(user_id)

        if permission == "admin":
            return Roles.is_owner(user_id) or user_id in Roles.ADMINS

        if permission == "trusted":
            return Roles.is_owner(user_id) or user_id in Roles.TRUSTED

        return True
        
# 🔐 Lock owner as permanent admin
Roles.ADMINS.update(OWNERS)

# ============================================
# ADMIN PERSISTENCE (FILE-BASED)
# ============================================

ADMINS_FILE = "admins.json"

def load_admins():
    if os.path.exists(ADMINS_FILE):
        try:
            with open(ADMINS_FILE, "r") as f:
                Roles.ADMINS.update(json.load(f))
        except Exception:
            pass  # fail silently, owner still exists

def save_admins():
    try:
        with open(ADMINS_FILE, "w") as f:
            json.dump(list(Roles.ADMINS), f)
    except Exception:
        pass
                
# ============================================
# PHASE 6 — EMOTIONAL AWARENESS
# ============================================
class Emotion:
    @staticmethod
    def detect(text):
        low = text.lower()
        if any(word in low for word in ["love","ily","crush"]):
            return "flirty"
        elif any(word in low for word in ["sad","upset","cry","hurt"]):
            return "sad"
        elif any(word in low for word in ["angry","mad","hate"]):
            return "angry"
        elif any(word in low for word in ["what","how","omg","wtf","nooo"]):
            return "shocked"
        return "neutral"

# ============================================
# PHASE 4 & 5 — PERSONALITY + CONVERSATION
# ============================================
class Personality:
    tone = "calm"
    style = "royal"
    emojis = ["🤦", "🤌", "🖤", "🌹", "🥱", "🤍"]

    @staticmethod
    def style_response(text, emotion="neutral"):
        emoji_map = {
            "neutral":"🤍","happy":"🌹","sad":"🥱",
            "angry":"🤦","flirty":"🤌","shocked":"🖤"
        }
        return f"{text} {emoji_map.get(emotion,'🤍')}"

class Conversation:
    context = []

    @staticmethod
    def remember(msg):
        Conversation.context.append(msg)
        if len(Conversation.context) > 20:
            Conversation.context.pop(0)

# ============================================
# PHASE 8 — LEARNING OBSERVATIONAL
# ============================================
class Learning:
    enabled = True

    @staticmethod
    def observe(msg):
        if Learning.enabled:
            Memory.store_long(msg)

# ============================================
# PHASE 7 — MEMORY SYSTEMS
# ============================================
class Memory:
    short_term = []
    long_term = []
    active_users = set()

    @staticmethod
    def touch_user(user):
        Memory.active_users.add(str(user))

    @staticmethod
    def store_short(msg):
        Memory.short_term.append(msg)
        if len(Memory.short_term) > 20:
            Memory.short_term.pop(0)

    @staticmethod
    def store_long(msg):
        Memory.long_term.append(msg)

# ===============================
# WHATSAPP PAIRING CORE
# ===============================

def wa_pair(user, wa_number=None):
    if not wa_number:
        return "Usage: .pair <wa_number>"

    if wa_number in WA_SESSIONS:
        return f"⚠️ {wa_number} already paired 🤌"

    # Register session (REAL WA logic plugs in here later)
    WA_SESSIONS[wa_number] = {
        "paired_by": str(user),
        "status": "paired",
        "timestamp": int(time.time())
    }

    save_sessions()

    return (
        "🔗 PAIRING INITIATED\n"
        f"• Number: {wa_number}\n"
        "• Status: REGISTERED\n\n"
        "⚠️ WhatsApp backend not attached yet\n"
        "Ready for QR / socket binding on VPS"
    )


def wa_unpair(user, wa_number=None):
    if not wa_number:
        return "Usage: .unpair <wa_number>"

    if wa_number not in WA_SESSIONS:
        return f"❌ {wa_number} not found"

    del WA_SESSIONS[wa_number]
    save_sessions()

    return f"❌ {wa_number} successfully unpaired"


def wa_listpairs(user):
    if not WA_SESSIONS:
        return "📭 No paired WhatsApp sessions"

    lines = ["📱 ACTIVE WHATSAPP SESSIONS\n"]
    for num, meta in WA_SESSIONS.items():
        lines.append(
            f"• {num}\n"
            f"  ├ Status: {meta['status']}\n"
            f"  └ Paired by: {meta['paired_by']}"
        )

    return "\n".join(lines)


def wa_autoload(user):
    if not WA_SESSIONS:
        return "📭 No sessions to autoload"

    count = len(WA_SESSIONS)
    return f"🔁 Autoloaded {count} WhatsApp session(s) 🤌"

# ============================================
# PHASE 3 & 9 — COMMANDS + MULTI-DOMAIN
# ============================================
class Commands:
    registry = {}

    @staticmethod
    def add_command(name, func, permission="user"):
        Commands.registry[name] = {"func":func,"permission":permission}

    @staticmethod
    def execute(user, name, *args):
        cmd = Commands.registry.get(name)
        if not cmd:
            return "Unknown command 🤌"
        if not Roles.check_permission(user, cmd["permission"]):
            return "Permission denied 🤌"
        try:
            result = cmd["func"](user, *args)
            SelfDiagnostics.log_response(success=True)
            return result
        except Exception as e:
            SelfDiagnostics.log_response(success=False)
            return f"Error executing {name}: {e} 🤌"


# ===============================
# COMMAND VAULT (SINGLE SOURCE)
# ===============================

def vault_command():
    lines = [
        "▣ SILENCE 🜲 (CIB)",
        f"▪ Version: {Productization.VERSION}",
        "▪ Mode: Public",
        "",
        "∆ COMMAND VAULT"
    ]

    for name, meta in sorted(Commands.registry.items()):
        perm = meta.get("permission", "user")
        lines.append(f".{name}  [{perm}]")

    return "\n".join(lines)

# ============================================
# GPT-STYLE INTELLIGENCE LAYER
# ============================================
class IntelligenceCore:
    @staticmethod
    def generate_response(processed_input):
        user_text = processed_input["text"]
        emotion = processed_input["emotion"]

        context_summary = " ".join(Conversation.context[-5:]) if Conversation.context else ""
        reply = f"Analyzing: {user_text} | Context: {context_summary}"
        reply = Personality.style_response(reply, emotion)

        Conversation.remember(user_text)
        SelfDiagnostics.log_response(success=True)
        return reply

# ============================================
# PHASE 10 & 11 — SAFETY & PLATFORM
# ============================================
class Safety:
    @staticmethod
    def check_abuse(msg):
        return False  # Placeholder

class Platform:
    _current = "cli"  # default

    @staticmethod
    def set(name: str):
        Platform._current = name

    @staticmethod
    def get():
        return Platform._current

    @staticmethod
    def deploy_cli():
        Platform.set("cli")
        print("SILENCE 2.0 CLI ready 🤌")

# ============================================
# PHASE 12 — OWNER CONTROL PANEL
# ============================================
class OwnerControlPanel:
    learning_enabled = True
    personality_locked = False

    @staticmethod
    def toggle_learning():
        OwnerControlPanel.learning_enabled = not OwnerControlPanel.learning_enabled
        Learning.enabled = OwnerControlPanel.learning_enabled
        return f"Learning {'enabled' if Learning.enabled else 'disabled'} 🤌"

    @staticmethod
    def lock_personality():
        OwnerControlPanel.personality_locked = True
        return "Personality locked 🤌"

    @staticmethod
    def unlock_personality():
        OwnerControlPanel.personality_locked = False
        return "Personality unlocked 🤌"

# ============================================
# PHASE 13 — SELF-DIAGNOSTICS
# ============================================
class SelfDiagnostics:
    response_count = 0
    error_count = 0

    @staticmethod
    def log_response(success=True):
        SelfDiagnostics.response_count += 1
        if not success:
            SelfDiagnostics.error_count += 1

    @staticmethod
    def run_diagnostics():
        return {
            "Responses processed": SelfDiagnostics.response_count,
            "Errors detected": SelfDiagnostics.error_count,
            "Short-term memory length": len(Memory.short_term),
            "Long-term memory length": len(Memory.long_term),
            "Learning enabled": OwnerControlPanel.learning_enabled,
            "Personality locked": OwnerControlPanel.personality_locked
        }

# ============================================
# PHASE 14 — PRODUCTIZATION
# ============================================
class Productization:
    VERSION = "2.0"
    LICENSE_KEY = None
    UPDATE_CHANNEL = "stable"

    @staticmethod
    def check_license():
        return Productization.LICENSE_KEY or "No license applied 🤌"

    @staticmethod
    def version():
        return Productization.VERSION

    @staticmethod
    def update(channel=None):
        if channel:
            Productization.UPDATE_CHANNEL = channel
        return f"Update checked on channel: {Productization.UPDATE_CHANNEL} 🤌"

# ============================================
# PHASE 15 — FUN DAYS / HOLIDAY MODE
# ============================================
class FunDays:
    @staticmethod
    def today_greeting():
        now = datetime.datetime.now()
        if now.month == 12 and now.day == 25:
            return "Merry Christmas 🌹"
        elif now.month == 1 and now.day == 1:
            return "Happy New Year 🌹"
        elif now.month == 2 and now.day == 14:
            return "Happy Valentine 🌹"
        elif now.month == 10 and now.day == 31:
            return "Happy Halloween 🤌"
        elif now.month == 7 and now.day == 4:
            return "Happy Independence Day 🤌"
        return "Today is a normal day 🤍"


# ============================================
# EXTENSION LAYER — INTENT ROUTER
# ============================================
class IntentRouter:
    @staticmethod
    def classify(text):
        low = text.lower()
        if low.startswith((".", "/")):
            return "command"
        if "translate" in low:
            return "translation"
        if "code" in low or "python" in low or "script" in low:
            return "coding"
        if "plan" in low or "schedule" in low:
            return "planning"
        if "remember" in low or "what did i say" in low:
            return "memory_recall"
        return "chat"


# ============================================
# EXTENSION LAYER — MEMORY RECALL ENGINE
# ============================================
class MemoryRecallEngine:
    @staticmethod
    def recall(text):
        low = text.lower()
        if "remember" in low or "what did i tell you" in low:
            if Memory.long_term:
                return f"You previously said: {Memory.long_term[-1]}"
            return "I do not have anything stored yet."
        return None


# ============================================
# EXTENSION LAYER — SMART FUN DAYS ENGINE
# ============================================
class FunDaysEngine:
    HOLIDAYS = {
        (12, 25): "Merry Christmas 🌹",
        (1, 1): "Happy New Year 🌹",
        (2, 14): "Happy Valentine 🌹",
        (10, 31): "Happy Halloween 🤌"
    }

    @staticmethod
    def detect(text):
        now = datetime.datetime.now()
        if (now.month, now.day) in FunDaysEngine.HOLIDAYS:
            return FunDaysEngine.HOLIDAYS[(now.month, now.day)]

        low = text.lower()
        if "christmas" in low:
            return "Merry Christmas 🌹"
        if "new year" in low:
            return "Happy New Year 🌹"
        if "valentine" in low:
            return "Happy Valentine 🌹"
        if "halloween" in low:
            return "Happy Halloween 🤌"

        return None


# ============================================
# EXTENSION LAYER — RESPONSE GENERATOR (FINAL)
# ============================================
class ResponseGenerator:
    @staticmethod
    def generate(processed):
        text = processed["text"]
        emotion = processed["emotion"]

        # 1. Fun Days auto-trigger
        holiday = FunDaysEngine.detect(text)
        if holiday:
            return Personality.style_response(holiday, "happy")

        # 2. Memory recall
        recall = MemoryRecallEngine.recall(text)
        if recall:
            return Personality.style_response(recall, "neutral")

        # 3. Default intelligence path
        return IntelligenceCore.generate_response(processed)


# ============================================
# REGISTER CORE COMMANDS
# ===========================================

Commands.add_command("pair", wa_pair, permission="user")
Commands.add_command("unpair", wa_unpair, permission="user")
Commands.add_command("listpairs", wa_listpairs, permission="owner")
Commands.add_command("autoload", wa_autoload, permission="owner")
Commands.add_command("diagnose", lambda user: SelfDiagnostics.run_diagnostics(), permission="owner")
Commands.add_command("togglelearning", lambda user: OwnerControlPanel.toggle_learning(), permission="owner")
Commands.add_command("lockpersonality", lambda user: OwnerControlPanel.lock_personality(), permission="owner")
Commands.add_command("unlockpersonality", lambda user: OwnerControlPanel.unlock_personality(), permission="owner")
Commands.add_command("version", lambda user: Productization.version(), permission="owner")
Commands.add_command("checklicense", lambda user: Productization.check_license(), permission="owner")
Commands.add_command("update", lambda user, channel=None: Productization.update(channel), permission="owner")
Commands.add_command("holiday", lambda user: FunDays.today_greeting(), permission="user")  # Fun Days command

# ===============================
# AI COMMANDS — SILENT 🜲 (CIB)
# ===============================

def ai_default(user, *args):
    text = " ".join(args).strip()
    if not text:
        return "🤖 AI: Say something for me to respond 🤍"
    return f"🤖 AI: {text.capitalize()} 🤍"


def ai_gpt(user, *args):
    text = " ".join(args).strip()
    if not text:
        return "🧠 GPT: Provide a question or topic 🤌"
    return f"🧠 GPT Enhanced Reasoning:\n{text}"


def ai_gpt3(user, *args):
    text = " ".join(args).strip()
    if not text:
        return "⚡ GPT-3: Fast mode needs input 🤍"
    return f"⚡ GPT-3 Response:\n{text}"


def ai_gpt4(user, *args):
    text = " ".join(args).strip()
    if not text:
        return "🧠 GPT-4: Deep reasoning needs input 🤌"
    return f"🧠 GPT-4 Advanced Analysis:\n{text}"


def ai_meta(user, *args):
    text = " ".join(args).strip()
    if not text:
        return "💬 MetaAI: Talk to me 🤍"
    return f"💬 MetaAI: {text} 🙂"


def ai_code(user, *args):
    text = " ".join(args).strip()
    if not text:
        return "👨‍💻 CodeAI: Describe the code problem 🤌"
    return (
        "👨‍💻 CodeAI Assistant:\n"
        "Explaining / generating code for:\n"
        f"{text}"
    )


def ai_openai(user, *args):
    text = " ".join(args).strip()
    if not text:
        return "🔓 OpenAI: Raw input required 🤍"
    return text  # raw passthrough


def ai_trivia(user, *args):
    trivia = [
        "Fastest land animal is the Cheetah 🐆",
        "Octopus has three hearts 🐙",
        "Bananas are berries 🍌",
        "Sharks existed before trees 🦈"
    ]
    return f"🧠 Trivia: {random.choice(trivia)} 🌹"
 # Register AI commands
Commands.add_command("ai", ai_default, permission="user")
Commands.add_command("gpt", ai_gpt, permission="user")
Commands.add_command("gpt3", ai_gpt3, permission="user")
Commands.add_command("gpt4", ai_gpt4, permission="user")
Commands.add_command("metaai", ai_meta, permission="user")
Commands.add_command("codeai", ai_code, permission="user")
Commands.add_command("openai", ai_openai, permission="user")
Commands.add_command("triviaai", ai_trivia, permission="user")

# ===============================
# AI IMAGE COMMANDS
# ===============================

def img_photoai(user, *args):
    prompt = " ".join(args).strip()
    if not prompt:
        return "🖼️ PhotoAI: Provide an image description 🤍"
    return f"🖼️ PhotoAI generated image for:\n{prompt}"


def img_realistic(user, *args):
    prompt = " ".join(args).strip()
    if not prompt:
        return "📸 RealisticAI: Describe the scene 🤌"
    return f"📸 Realistic image style applied to:\n{prompt}"


def img_image(user, *args):
    prompt = " ".join(args).strip()
    if not prompt:
        return "🎨 ImageAI: Give a prompt 🤍"
    return f"🎨 Image generated for:\n{prompt}"


def img_flux(user, *args):
    prompt = " ".join(args).strip()
    if not prompt:
        return "✨ Flux: Enter creative prompt 🤌"
    return f"✨ Flux engine image created for:\n{prompt}"


def img_anime(user, *args):
    prompt = " ".join(args).strip()
    if not prompt:
        return "🎌 AnimeAI: Describe anime scene 🤍"
    return f"🎌 Anime-style image generated for:\n{prompt}"


def img_logo(user, *args):
    prompt = " ".join(args).strip()
    if not prompt:
        return "🏷️ LogoAI: Describe your logo 🤌"
    return f"🏷️ Logo design generated for:\n{prompt}"
    
Commands.add_command("photoai", img_photoai, permission="user")
Commands.add_command("realistic", img_realistic, permission="user")
Commands.add_command("image", img_image, permission="user")
Commands.add_command("flux", img_flux, permission="user")
Commands.add_command("anime", img_anime, permission="user")
Commands.add_command("logo", img_logo, permission="user")
        

# ===============================
# USER COMMANDS
# ===============================

def user_ping(user):
    return "🏓 Pong 🤌"


def user_stats(user):
    return {
        "Bot": "SILENT 🜲 (CIB)",
        "Version": "2.0",
        "Mode": "Public",
        "Learning": Learning.enabled,
        "Short memory": len(Memory.short_term),
        "Long memory": len(Memory.long_term)
    }


def user_owner(user):
    return "👑 Owner: SILENCE SAILS"


def user_delete(user):
    return "🗑️ Message deleted (platform-permitted)"


def user_block(user):
    return "🚫 User blocked"


def user_unblock(user):
    return "✅ User unblocked"


def user_self(user):
    return "🔒 Self mode enabled"


def user_public(user):
    return "🌍 Public mode enabled"


def user_take(user):
    return "📥 Media copied"


def user_setpp(user):
    return "🖼️ Profile picture updated"
    
Commands.add_command("ping", user_ping, permission="user")
Commands.add_command("stats", user_stats, permission="user")
Commands.add_command("owner", user_owner, permission="user")
Commands.add_command("delete", user_delete, permission="user")
Commands.add_command("block", user_block, permission="user")
Commands.add_command("unblock", user_unblock, permission="user")
Commands.add_command("self", user_self, permission="user")
Commands.add_command("public", user_public, permission="user")
Commands.add_command("take", user_take, permission="user")
Commands.add_command("setpp", user_setpp, permission="user")    

# ===============================
# ANTI SYSTEM STATE
# ===============================

ANTI_STATE = {
    "antilink": False,
    "antibadword": False,
    "antibot": False,
    "antitag": False,
    "antiads": False,
    "antinsfw": False,
}


def toggle_anti(feature):
    ANTI_STATE[feature] = not ANTI_STATE[feature]
    status = "enabled ✅" if ANTI_STATE[feature] else "disabled ❌"
    return f"🛡️ {feature.capitalize()} {status}"
    
def anti_link(user):
    return toggle_anti("antilink")


def anti_badword(user):
    return toggle_anti("antibadword")


def anti_bot(user):
    return toggle_anti("antibot")


def anti_tag(user):
    return toggle_anti("antitag")


def anti_ads(user):
    return toggle_anti("antiads")


def anti_nsfw(user):
    return toggle_anti("antinsfw")    
    
Commands.add_command("antilink", anti_link, permission="admin")
Commands.add_command("antibadword", anti_badword, permission="admin")
Commands.add_command("antibot", anti_bot, permission="admin")
Commands.add_command("antitag", anti_tag, permission="admin")
Commands.add_command("antiads", anti_ads, permission="admin")
Commands.add_command("antinsfw", anti_nsfw, permission="admin")    

# ===============================
# AUTO SYSTEM STATE
# ===============================

AUTO_STATE = {
    "autoviewstatus": False,
    "autolikestatus": False,
    "autotyping": False,
    "autobio": False,
    "autoreply": False,
    "autorecording": False,
    "autoreact": False,
    "autoread": False,
}

def toggle_auto(feature, label=None):
    AUTO_STATE[feature] = not AUTO_STATE[feature]
    name = label or feature
    state = "enabled ✅" if AUTO_STATE[feature] else "disabled ❌"
    return f"🤖 {name} {state}"
    
def auto_view_status(user):
    return toggle_auto("autoviewstatus", "Auto View Status")


def auto_like_status(user):
    return toggle_auto("autolikestatus", "Auto Like Status")


def auto_typing(user):
    return toggle_auto("autotyping", "Auto Typing")


def auto_bio(user):
    return toggle_auto("autobio", "Auto Bio Update")


def auto_reply(user):
    return toggle_auto("autoreply", "Auto Reply")


def auto_recording(user):
    return toggle_auto("autorecording", "Auto Recording")


def auto_react(user):
    return toggle_auto("autoreact", "Auto React")


def auto_read(user):
    return toggle_auto("autoread", "Auto Read")    
    
Commands.add_command("autoviewstatus", auto_view_status, permission="admin")
Commands.add_command("autolikestatus", auto_like_status, permission="admin")
Commands.add_command("autotyping", auto_typing, permission="admin")
Commands.add_command("autobio", auto_bio, permission="admin")
Commands.add_command("autoreply", auto_reply, permission="admin")
Commands.add_command("autorecording", auto_recording, permission="admin")
Commands.add_command("autoreact", auto_react, permission="admin")
Commands.add_command("autoread", auto_read, permission="admin")    

# ===============================
# DOWNLOAD CORE
# ===============================

def downloader_unavailable(name):
    return f"⚠️ {name} engine not installed 🤌"


def validate_url(url):
    return url.startswith(("http://", "https://"))


def require_args(args, usage):
    if not args:
        return f"Usage: {usage}"
    return None
    
def ytmp4(user, *args):
    err = require_args(args, ".ytmp4 <youtube_url>")
    if err:
        return err

    if not validate_url(args[0]):
        return "Invalid YouTube URL 🤌"

    return downloader_unavailable("YouTube MP4")


def ytmp3(user, *args):
    err = require_args(args, ".ytmp3 <youtube_url>")
    if err:
        return err

    if not validate_url(args[0]):
        return "Invalid YouTube URL 🤌"

    return downloader_unavailable("YouTube MP3")
    
def ytsearch(user, *args):
    if not args:
        return "Usage: .ytsearch <query>"
    return f"🔍 Searching YouTube for: {' '.join(args)} 🌹"


def play(user, *args):
    if not args:
        return "Usage: .play <song name>"
    return f"🎵 Searching & playing: {' '.join(args)} 🌹"


def play2(user, *args):
    if not args:
        return "Usage: .play2 <song name>"
    return f"🎶 Alternate source playing: {' '.join(args)} 🌹"            

def spotify(user, *args):
    err = require_args(args, ".spotify <track_url>")
    if err:
        return err
    return downloader_unavailable("Spotify")


def tiktok(user, *args):
    err = require_args(args, ".tiktok <video_url>")
    if err:
        return err

    if not validate_url(args[0]):
        return "Invalid TikTok URL 🤌"

    return downloader_unavailable("TikTok")


def igdl(user, *args):
    err = require_args(args, ".igdl <post_url>")
    if err:
        return err
    return downloader_unavailable("Instagram")


def fbdl(user, *args):
    err = require_args(args, ".fbdl <video_url>")
    if err:
        return err
    return downloader_unavailable("Facebook")


def mediafire(user, *args):
    err = require_args(args, ".mediafire <file_url>")
    if err:
        return err
    return downloader_unavailable("MediaFire")


def gitclone(user, *args):
    err = require_args(args, ".gitclone <repo_url>")
    if err:
        return err
    return downloader_unavailable("Git Clone")
    
Commands.add_command("ytmp4", ytmp4)
Commands.add_command("ytmp3", ytmp3)
Commands.add_command("ytsearch", ytsearch)
Commands.add_command("play", play)
Commands.add_command("play2", play2)
Commands.add_command("spotify", spotify)
Commands.add_command("tiktok", tiktok)
Commands.add_command("igdl", igdl)
Commands.add_command("fbdl", fbdl)
Commands.add_command("mediafire", mediafire)
Commands.add_command("gitclone", gitclone)    

# ===============================
# UTILITY COMMANDS
# ===============================

def util_calc(user, *args):
    if not args:
        return "Usage: .calc <expression>"
    expr = " ".join(args)
    try:
        if not re.match(r'^[0-9+\-*/(). ]+$', expr):
            return "Invalid math expression 🤌"
        result = eval(expr, {"__builtins__": {}})
        return f"🧮 Result: {result} 🤍"
    except Exception:
        return "Calculation error 🤌"


def util_translate(user, *args):
    if len(args) < 2:
        return "Usage: .translate <lang> <text>"
    lang = args[0]
    text = " ".join(args[1:])
    return f"🌍 Translated to {lang.upper()}:\n{text} 🤍 (mock)"


def util_time(user):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    return f"🕒 Time: {now} 🤍"


def util_date(user):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    return f"📅 Date: {today} 🤍"


def util_weather(user, *args):
    if not args:
        return "Usage: .weather <city>"
    city = " ".join(args)
    return f"☁️ Weather in {city}: 27°C, Clear 🌤️ (mock)"


def util_shorturl(user, *args):
    if not args:
        return "Usage: .shorturl <url>"
    url = args[0]
    if not validate_url(url):
        return "Invalid URL 🤌"
    return f"🔗 Short URL: https://s2.ly/{random.randint(1000,9999)} 🤍"


def util_upper(user, *args):
    if not args:
        return "Usage: .upper <text>"
    return " ".join(args).upper()


def util_lower(user, *args):
    if not args:
        return "Usage: .lower <text>"
    return " ".join(args).lower()


def util_reverse(user, *args):
    if not args:
        return "Usage: .reverse <text>"
    return " ".join(args)[::-1]
    
Commands.add_command("calc", util_calc)
Commands.add_command("translate", util_translate)
Commands.add_command("time", util_time)
Commands.add_command("date", util_date)
Commands.add_command("weather", util_weather)
Commands.add_command("shorturl", util_shorturl)
Commands.add_command("upper", util_upper)
Commands.add_command("lower", util_lower)
Commands.add_command("reverse", util_reverse)    

# ===============================
# FUN COMMANDS
# ===============================

JOKES = [
    "Why don’t programmers like nature? Too many bugs 🐛",
    "I told my code a joke… it didn’t compile 🤦",
    "Why was the computer cold? It forgot to close Windows 🪟",
]

QUOTES = [
    "Silence is better than nonsense 🌹",
    "Code is poetry 🖤",
    "Think twice, code once 🤍",
]

TRUTHS = [
    "What’s your biggest fear?",
    "Who was your first crush?",
    "What secret do you hide the most?",
]

DARES = [
    "Send your last emoji 😁",
    "Type your name backwards",
    "Say something nice about yourself 🌹",
]

ROASTS = [
    "You run on low battery energy 🤌",
    "Even Wi-Fi avoids you sometimes 📶",
    "You lag in real life 😭",
]

COMPLIMENTS = [
    "You have main-character energy 🌹",
    "You’re smarter than your last mistake 🤍",
    "You make silence powerful 🖤",
]


def fun_joke(user):
    return f"😂 Joke: {random.choice(JOKES)}"


def fun_quote(user):
    return f"📜 Quote: {random.choice(QUOTES)}"


def fun_truth(user):
    return f"🧠 Truth: {random.choice(TRUTHS)}"


def fun_dare(user):
    return f"🔥 Dare: {random.choice(DARES)}"


def fun_ship(user, *args):
    if len(args) < 2:
        return "Usage: .ship <name1> <name2>"
    name1, name2 = args[0], args[1]
    percent = random.randint(1, 100)
    return f"💘 {name1} ❤️ {name2} = {percent}% compatibility"


def fun_roast(user):
    return f"🔥 Roast: {random.choice(ROASTS)}"


def fun_compliment(user):
    return f"🌹 Compliment: {random.choice(COMPLIMENTS)}"
    
Commands.add_command("joke", fun_joke)
Commands.add_command("quote", fun_quote)
Commands.add_command("truth", fun_truth)
Commands.add_command("dare", fun_dare)
Commands.add_command("ship", fun_ship)
Commands.add_command("roast", fun_roast)
Commands.add_command("compliment", fun_compliment)    

# ===============================
# RANDOM COMMANDS
# ===============================

def random_roll(user, *args):
    try:
        sides = int(args[0]) if args else 6
        if sides < 2:
            return "🎲 Dice must have at least 2 sides 🤌"
        return f"🎲 Rolled: {random.randint(1, sides)}"
    except ValueError:
        return "Usage: .roll <number>"


def random_coin(user):
    return f"🪙 Coin: {random.choice(['Heads', 'Tails'])}"


def random_pick(user, *args):
    if not args:
        return "Usage: .pick <item1> <item2> ..."
    return f"🎯 Picked: {random.choice(args)}"


def random_choose(user, *args):
    if not args:
        return "Usage: .choose <option1> <option2> ..."
    return f"🤔 Choice: {random.choice(args)}"


def random_number(user, *args):
    try:
        max_num = int(args[0]) if args else 100
        return f"🔢 Random number: {random.randint(1, max_num)}"
    except ValueError:
        return "Usage: .random <max_number>"


def random_password(user, *args):
    length = int(args[0]) if args and args[0].isdigit() else 12
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%"
    password = "".join(random.choice(chars) for _ in range(length))
    return f"🔐 Password: {password}"
    
Commands.add_command("roll", random_roll)
Commands.add_command("coinflip", random_coin)
Commands.add_command("pick", random_pick)
Commands.add_command("choose", random_choose)
Commands.add_command("random", random_number)
Commands.add_command("password", random_password)    

# ===============================
# GROUP COMMANDS
# ===============================

def group_kick(user, *args):
    if not args:
        return "Usage: .kick <user>"
    return f"🚫 User {args[0]} kicked from group 🤌"


def group_add(user, *args):
    if not args:
        return "Usage: .add <user>"
    return f"➕ User {args[0]} added to group 🌹"


def group_promote(user, *args):
    if not args:
        return "Usage: .promote <user>"
    return f"⬆️ User {args[0]} promoted to admin 👑"


def group_demote(user, *args):
    if not args:
        return "Usage: .demote <user>"
    return f"⬇️ User {args[0]} demoted 🤍"


def group_mute(user, *args):
    if not args:
        return "Usage: .mute <user>"
    return f"🔇 User {args[0]} muted 🤌"


def group_unmute(user, *args):
    if not args:
        return "Usage: .unmute <user>"
    return f"🔊 User {args[0]} unmuted 🌹"


def group_tagall(user):
    return "📢 Tagging all group members 🔔"


def group_info(user):
    return {
        "Group": "SILENCE HQ",
        "Members": 42,
        "Admins": 3,
        "Mode": "Public"
    }


def group_setname(user, *args):
    if not args:
        return "Usage: .setname <group_name>"
    return f"✏️ Group name changed to: {' '.join(args)}"


def group_setdesc(user, *args):
    if not args:
        return "Usage: .setdesc <description>"
    return f"📝 Group description updated"
    
Commands.add_command("kick", group_kick, permission="admin")
Commands.add_command("add", group_add, permission="admin")
Commands.add_command("promote", group_promote, permission="admin")
Commands.add_command("demote", group_demote, permission="admin")
Commands.add_command("mute", group_mute, permission="admin")
Commands.add_command("unmute", group_unmute, permission="admin")
Commands.add_command("tagall", group_tagall, permission="admin")
Commands.add_command("groupinfo", group_info)
Commands.add_command("setname", group_setname, permission="admin")
Commands.add_command("setdesc", group_setdesc, permission="admin")    

# ===============================
# GFX COMMANDS
# ===============================

def gfx_text(user, *args):
    if not args:
        return "Usage: .gfx <text>"
    return f"🎨 GFX Render:\n[ { ' '.join(args).upper() } ]"


def gfx_banner(user, *args):
    if not args:
        return "Usage: .banner <text>"
    text = " ".join(args).upper()
    line = "=" * (len(text) + 6)
    return f"{line}\n==  {text}  ==\n{line}"


def gfx_ascii(user, *args):
    if not args:
        return "Usage: .ascii <text>"
    text = " ".join(args)
    return f"""
  █▀▀▀▀▀█
  █ {text} █
  █▄▄▄▄▄█
"""


def gfx_fancy(user, *args):
    if not args:
        return "Usage: .fancy <text>"
    return "✨ " + " ".join(args).replace("a","α").replace("e","є").replace("o","σ")


def gfx_neon(user, *args):
    if not args:
        return "Usage: .neon <text>"
    return f"💡 NEON » {' '.join(args)} « 💡"


def gfx_glitch(user, *args):
    if not args:
        return "Usage: .glitch <text>"
    return "".join(c + "̷" for c in " ".join(args))


def gfx_shadow(user, *args):
    if not args:
        return "Usage: .shadow <text>"
    text = " ".join(args)
    return f"{text}\n" + ("░" * len(text))
    
Commands.add_command("gfx", gfx_text)
Commands.add_command("banner", gfx_banner)
Commands.add_command("ascii", gfx_ascii)
Commands.add_command("fancy", gfx_fancy)
Commands.add_command("neon", gfx_neon)
Commands.add_command("glitch", gfx_glitch)
Commands.add_command("shadow", gfx_shadow)    

# ===============================
# STICKER COMMANDS
# ===============================

def sticker_make(user, *args):
    if not args:
        return "Usage: .sticker <reply to image / text>"
    return "🧷 Sticker created successfully 🤌"


def sticker_take(user):
    return "📥 Sticker taken & saved 🤍"


def sticker_text(user, *args):
    if not args:
        return "Usage: .stickertext <text>"
    return f"🧷 Text sticker created:\n{' '.join(args)}"


def sticker_info(user):
    return {
        "Pack": "SILENCE Stickers",
        "Author": "silence",
        "Total": random.randint(10, 99)
    }

Commands.add_command("sticker", sticker_make)
Commands.add_command("stickertake", sticker_take)
Commands.add_command("stickertext", sticker_text)
Commands.add_command("stickerinfo", sticker_info)

# ===============================
# STALK COMMANDS
# ===============================

def stalk_basic(user, *args):
    if not args:
        return "Usage: .stalk <name/username>"
    target = " ".join(args)
    return f"""
🕵️ STALK RESULT
━━━━━━━━━━━━━━
Name: {target}
Status: Public profile
Activity: Medium
Risk Level: Low
━━━━━━━━━━━━━━
"""


def stalk_username(user, *args):
    if not args:
        return "Usage: .username <handle>"
    target = args[0]
    platforms = ["Instagram", "GitHub", "Twitter", "Telegram"]
    found = random.sample(platforms, random.randint(1, len(platforms)))
    return f"🔍 Username `{target}` found on: {', '.join(found)}"


def stalk_github(user, *args):
    if not args:
        return "Usage: .github <username>"
    return (
        f"🐙 GitHub user `{args[0]}`\n"
        f"Repos: {random.randint(1,50)}\n"
        f"Stars: {random.randint(0,500)}"
    )


def stalk_ipinfo(user, *args):
    if not args:
        return "Usage: .ipinfo <ip>"
    return {
        "IP": args[0],
        "Country": "Unknown",
        "ISP": "Hidden",
        "Risk": "Low"
    }


def stalk_domain(user, *args):
    if not args:
        return "Usage: .domain <domain>"
    return {
        "Domain": args[0],
        "Status": "Active",
        "Registrar": "Unknown",
        "Risk": "Low"
    }
    
Commands.add_command("stalk", stalk_basic)
Commands.add_command("username", stalk_username)
Commands.add_command("github", stalk_github)
Commands.add_command("ipinfo", stalk_ipinfo)
Commands.add_command("domain", stalk_domain)    

# ===============================
# SYSTEM COMMANDS (INFO ONLY)
# ===============================

def sys_cpuinfo(user):
    return {
        "CPU Cores": os.cpu_count(),
        "Platform": os.name,
        "Processor": os.getenv("PROCESSOR_IDENTIFIER", "Unknown")
    }


def sys_diskinfo(user):
    try:
        stat = os.statvfs("/")
        total = stat.f_blocks * stat.f_frsize
        free = stat.f_bfree * stat.f_frsize
        used = total - free
        return {
            "Total Disk": f"{total // (1024**3)} GB",
            "Used Disk": f"{used // (1024**3)} GB",
            "Free Disk": f"{free // (1024**3)} GB"
        }
    except Exception:
        return "Disk info unavailable 🤌"


VAULT_CATEGORIES = {
    "SYSTEM": {
        "vault", "cpuinfo", "diskinfo", "whoami", "channel", "support"
    },

    "AI COMMANDS": {
        "ai", "gpt", "gpt3", "gpt4",
        "metaai", "codeai", "openai", "triviaai"
    },

    "AI IMAGE": {
        "image", "photoai", "realistic", "anime", "logo", "flux"
    },

    "USER": {
        "ping", "stats", "delete", "block", "unblock",
        "self", "public", "take", "setpp"
    },

    "ANTI SYSTEM": {
        "antilink", "antibadword", "antibot",
        "antitag", "antiads", "antinsfw"
    },

    "AUTO SYSTEM": {
        "autoread", "autoreply", "autoreact",
        "autotyping", "autobio",
        "autoviewstatus", "autolikestatus", "autorecording"
    },

    "DOWNLOAD": {
        "ytmp4", "ytmp3", "ytsearch",
        "play", "play2", "spotify",
        "tiktok", "igdl", "fbdl",
        "mediafire", "gitclone"
    },

    "UTILITY": {
        "calc", "translate", "time",
        "date", "weather", "shorturl",
        "upper", "lower", "reverse"
    },

    "GROUP": {
        "add", "kick", "promote", "demote",
        "mute", "unmute", "tagall",
        "groupinfo", "setname", "setdesc"
    },

    "FUN": {
        "joke", "quote", "truth",
        "dare", "ship", "roast", "compliment"
    },

    "RANDOM": {
        "roll", "coinflip", "pick",
        "choose", "random", "password"
    },

    "GFX": {
        "gfx", "banner", "ascii",
        "fancy", "neon", "glitch", "shadow"
    },

    "STICKER": {
        "sticker", "stickertake",
        "stickertext", "stickerinfo"
    },

    "STALK": {
        "stalk", "username", "github",
        "ipinfo", "domain"
    }
}

def vault_menu():
    registry = Commands.registry
    total = 0

    menu = """
▣ SILENCE 🜲  (AI BEAST CORE ENGINE)
⚄════════════════════⚄
▪ Prefix      : [ . ]
▪ Mode        : Public
▪ Access      : User-Level
▪ Platforms   : TG / WA
▪ Engine      : SilenceAI Core
▪ Version     : 2.0 — Vault Menu
▪ Status      : Stable
⚄════════════════════⚄
"""

    for category, names in VAULT_CATEGORIES.items():
        cmds = []

        for name in names:
            meta = registry.get(name)
            if not meta:
                continue
            if meta.get("permission") != "user":
                continue

            cmds.append(f".{name}")

        if not cmds:
            continue

        total += len(cmds)
        menu += f"\n∆ {category}\n"
        for cmd in sorted(cmds):
            menu += f"▸ {cmd}\n"

    menu += f"""
USE COMMANDS WISELY 🖤
⚄════════════════════⚄
Total User Commands:> {total} <
"""

    return menu
    
def sys_vault(user):
    return vault_menu()    


def sys_channel(user):
    return (
        "📢 OFFICIAL CHANNEL\n"
        "https://whatsapp.com/channel/0029VbBiVMw4CrffJU8ArF1i"
    )


def sys_support(user):
    return (
        "🛠️ SUPPORT\n"
        "Email: silenceinvasion2@gmail.com\n"
        "Phone: +2347078281050"
    )
    
Commands.add_command("cpuinfo", sys_cpuinfo)
Commands.add_command("diskinfo", sys_diskinfo)
Commands.add_command("vault", sys_vault, permission="user")
Commands.add_command("channel", sys_channel)
Commands.add_command("support", sys_support)    

# ===============================
# 🎄 SILENCE — CHRISTMAS BONUS GAME
# ===============================

import time
import threading

# ✅ Gmail notifier
try:
    from mailer import send_mail
except Exception:
    send_mail = None  # failsafe if mailer not present


_XMAS_GAME = {
    "active": True,
    "claimed": False,
    "claimed_by": None,
    "started_at": time.time(),
    "expires_in": 60 * 60 * 24,  # 24 hours
}

_XMAS_LOCK = threading.Lock()

# Accepted "no code" answers
_NO_CODE_PHRASES = {
    "nothing",
    "no code",
    "there is no code",
    "there's no code",
    "zero",
    "nil",
    "none",
    "empty",
}


def _xmas_expired():
    return time.time() - _XMAS_GAME["started_at"] > _XMAS_GAME["expires_in"]


def christmas_bonus(user, *args):
    with _XMAS_LOCK:
        # ❌ expired / disabled
        if not _XMAS_GAME["active"] or _xmas_expired():
            return "🎄 Christmas Bonus has expired."

        # 🔒 already claimed
        if _XMAS_GAME["claimed"]:
            return "🎁 Bonus already claimed."

        # Step 1: user just called .xmas
        if not args:
            return (
                "🎄 **SILENCE — CHRISTMAS BONUS**\n\n"
                "Enter the **4-digit code** to claim the reward.\n\n"
                "Hint:\n"
                "• The smartest answer contains **no digits**\n"
                "• Guessing numbers guarantees failure\n"
            )

        # Step 2: user submitted an answer
        answer = " ".join(args).strip().lower()

        # ❌ Any digits = instant failure
        if any(char.isdigit() for char in answer):
            return "❌ Incorrect.\nNumbers were never the key."

        # ✅ Correct understanding
        if answer in _NO_CODE_PHRASES:
            _XMAS_GAME["claimed"] = True
            _XMAS_GAME["claimed_by"] = user

            # 📧 Notify you by Gmail (silent, safe)
            if send_mail:
                try:
                    send_mail(
                        subject="🎄 SILENCE Xmas Bonus Claimed",
                        body=(
                            "The Christmas Bonus has been claimed.\n\n"
                            f"User ID: {user}\n"
                            f"Answer: {answer}\n"
                            f"Time: {time.ctime()}\n\n"
                            "This reward is now locked."
                        ),
                        to_email="silence.v1.4bot@gmail.com"
                    )
                except Exception:
                    pass  # never break the game

            return (
                "🎁 **BONUS CLAIMED**\n\n"
                "You understood the silence.\n"
                "There was never a code.\n\n"
                "Reward access granted.\n"
                "This bonus is now locked 🔒"
            )

        # ❌ Wrong wording
        return (
            "❌ Incorrect.\n"
            "You spoke — but did not understand."
        )


# ===============================
# REGISTER COMMAND
# ===============================
try:
    Commands.add_command("xmas", christmas_bonus, permission="user")
except Exception:
    pass

# ===============================
# OWNER COMMANDS (ONLY)
# ===============================

# ---- SYSTEM / CORE ----

def system(user):
    return "🖥️ SILENCE 2.0 System Online 🤌"


def uptime(user):
    return f"⏱️ Uptime: {int(time.time() - START_TIME)} seconds 🤍"


def memory(user):
    return {
        "short_term": len(Memory.short_term),
        "long_term": len(Memory.long_term)
    }


def clear(user):
    Memory.short_term.clear()
    Conversation.context.clear()
    return "🧹 Memory cleared 🤌"


def restart(user):
    return "🔄 Restart requested (manual restart required) 🤌"


def shutdown(user):
    Boot.shutdown()
    return "🛑 Shutting down 🤌"


# ---- CONTROL / MANAGEMENT ----

def ban(user, target=None):
    if not target:
        return "Usage: .ban <user_id>"
    return f"🚫 User {target} banned 🤌"

def promote_admin(user, target=None):
    if not target:
        return "Usage: .addadmin <user_id>"
    Roles.ADMINS.add(target)
    return f"👑 {target} promoted to admin 🤌"


def demote_admin(user, target=None):
    if not target:
        return "Usage: .removeadmin <user_id>"
    if target in OWNERS:
        return "❌ Cannot demote owner 🤌"
        
    Roles.ADMINS.discard(target)
    return f"⬇️ {target} demoted from admin 🤌"

def update(user, channel=None):
    return Productization.update(channel)


def checklicense(user):
    return Productization.check_license()


def lockpersonality(user):
    return OwnerControlPanel.lock_personality()


def unlockpersonality(user):
    return OwnerControlPanel.unlock_personality()


def diagnose(user):
    return SelfDiagnostics.run_diagnostics()


def togglelearning(user):
    return OwnerControlPanel.toggle_learning()


CODEX_CATEGORIES = {
    "SYSTEM CORE": {
        "codex", "vault", "system", "uptime", "memory",
        "cpuinfo", "diskinfo", "clear", "restart", "shutdown",
        "whoami", "channel", "support", "logs", "env", "diagnose"
    },

    "OWNER / CONTROL": {
        "owner", "ban", "unban", "pair", "unpair", "listpairs",
        "addadmin", "removeadmin", "admin", "autoload", "update",
        "lockpersonality", "unlockpersonality", "togglelearning",
        "setmode", "setprefix", "setname", "broadcast", "eval", "exec"
    },

    "AI COMMANDS": {
        "ai", "gpt", "gpt3", "gpt4", "metaai",
        "codeai", "openai", "triviaai",
        "think", "reason", "explain", "summarize"
    },

    "AI IMAGE": {
        "image", "photoai", "realistic", "anime",
        "logo", "flux", "art", "illustrate", "enhance"
    },

    "USER": {
        "ping", "stats", "profile", "delete", "block",
        "unblock", "self", "public", "private",
        "take", "setpp", "getpp", "myid"
    },

    "ANTI SYSTEM": {
        "antilink", "antibadword", "antibot", "antitag",
        "antiads", "antinsfw", "antiflood", "antispam"
    },

    "AUTO SYSTEM": {
        "autoread", "autoreply", "autoreact", "autotyping",
        "autobio", "autoviewstatus", "autolikestatus",
        "autorecording", "autosticker"
    },

    "DOWNLOAD": {
        "ytmp4", "ytmp3", "ytsearch", "play", "play2",
        "spotify", "tiktok", "igdl", "fbdl",
        "mediafire", "gitclone", "apk", "lyrics", "tts"
    },

    "UTILITY": {
        "calc", "translate", "time", "date",
        "weather", "shorturl", "upper", "lower", "reverse"
    },

    "GROUP": {
        "add", "kick", "kickall", "kickadmins",
        "promote", "demote", "mute", "unmute",
        "tag", "tagall", "tagadmins", "hidetag",
        "groupinfo", "setname", "setdesc",
        "grouplink", "resetlink", "announce", "rules", "left"
    },

    "FUN": {
        "joke", "quote", "truth", "dare", "ship",
        "roast", "compliment", "meme", "8ball", "flirt", "advice"
    },

    "RANDOM": {
        "roll", "coinflip", "pick", "choose",
        "random", "password", "fact", "funfact"
    },

    "GFX": {
        "gfx", "gfx2", "gfx3", "gfx4", "gfx5",
        "banner", "ascii", "fancy", "neon", "glitch", "shadow"
    },

    "STICKER": {
        "sticker", "take", "stickertake", "stickertext",
        "stickerinfo", "bonk", "slap", "kiss", "pat", "hug"
    },

    "STALK / LOOKUP": {
        "stalk", "username", "github", "ipinfo",
        "domain", "npmstalk", "igstalk", "ttstalk"
    }
}

def codex(user):
    if not Roles.is_owner(user):
        return "👑 Owner only command 🤌"

    registry = Commands.registry
    total = 0

    menu = """
▣ SILENCE 🜲  (AI BEAST CORE ENGINE)
⚄════════════════════⚄
▪ Prefix      : [ . ]
▪ Owner       : SILENCE SAILS 🜲
▪ Mode        : Private / Owner 
▪ Platforms   : TG / WA
▪ Engine      : SilenceAI Core
▪ Version     : 2.0 — Codex Line
▪ Status      : Stable
▪ Intelligence: Adaptive / Contextual
⚄════════════════════⚄
"""

    for category, names in CODEX_CATEGORIES.items():
        cmds = []

        for name in names:
            meta = registry.get(name)
            if not meta:
                continue
            cmds.append(f".{name}")

        if not cmds:
            continue

        total += len(cmds)
        menu += f"\n∆ {category}\n"
        for cmd in sorted(cmds):
            menu += f"▸ {cmd}\n"

    menu += f"""
⚄════════════════════⚄
END OF CODEX — INTERNAL INDEX
Total Commands Indexed:> {total} <
"""

    return menu
    
def sys_whoami(user):
    if Roles.is_owner(user):
        role = "owner"
    elif user in Roles.ADMINS:
        role = "admin"
    elif user in Roles.TRUSTED:
        role = "trusted"
    else:
        role = "user"

    return (
        "🧠 IDENTITY CHECK\n"
        f"• User ID: {user}\n"
        f"• Role: {role.upper()}\n"
        f"• Owner Access: {'YES' if role == 'owner' else 'NO'}"
    )
    
import time

def systemstatus(user):
    uptime = int(time.time() - START_TIME)
    hours = uptime // 3600
    minutes = (uptime % 3600) // 60

    return (
        "▣ SILENCE 🜲 SYSTEM STATUS\n"
        f"Uptime        : {hours}h {minutes}m\n"
        f"Users Active  : {len(Memory.active_users)}\n"
        f"Commands      : {len(Commands.registry)}\n"
        f"Learning      : {'ENABLED' if Learning.enabled else 'DISABLED'}\n"
        f"Platform      : {Platform.get()}\n"
        "Status        : STABLE"
    )
    
    
# ===============================
# ADMIN MANAGEMENT (OWNER ONLY)
# ===============================

def admin_manage(user, action=None, target=None):
    if not Roles.is_owner(user):
        return "👑 Owner only command 🤌"

    if action == "add":
        if not target:
            return "Usage: .admin add <user_id>"
        Roles.ADMINS.add(target)
        save_admins()  # ✅ PERSIST
        return f"🛡️ {target} is now an admin ✅"

    if action == "remove":
        if not target:
            return "Usage: .admin remove <user_id>"
        Roles.ADMINS.discard(target)
        save_admins()  # ✅ PERSIST
        return f"🗑️ {target} removed from admins ❌"

    if action == "list":
        if not Roles.ADMINS:
            return "No admins set 🤍"
        return "🛡️ ADMINS:\n" + "\n".join(sorted(Roles.ADMINS))

    return (
        "Admin command usage:\n"
        ".admin add <user_id>\n"
        ".admin remove <user_id>\n"
        ".admin list"
    )
    
    
Commands.add_command("systemstatus", systemstatus, permission="owner")
Commands.add_command("system", system, permission="owner")
Commands.add_command("uptime", uptime, permission="owner")
Commands.add_command("memory", memory, permission="owner")
Commands.add_command("clear", clear, permission="owner")
Commands.add_command("restart", restart, permission="owner")
Commands.add_command("shutdown", shutdown, permission="owner")

Commands.add_command("ban", ban, permission="owner")
Commands.add_command("addadmin", promote_admin, permission="owner")
Commands.add_command("removeadmin", demote_admin, permission="owner")
Commands.add_command("update", update, permission="owner")
Commands.add_command("checklicense", checklicense, permission="owner")
Commands.add_command("lockpersonality", lockpersonality, permission="owner")
Commands.add_command("unlockpersonality", unlockpersonality, permission="owner")
Commands.add_command("diagnose", diagnose, permission="owner")
Commands.add_command("togglelearning", togglelearning, permission="owner")    
Commands.add_command("codex", codex, permission="owner")
Commands.add_command("whoami", sys_whoami, permission="user")
Commands.add_command("admin", admin_manage, permission="owner")


# ============================================
# MAIN LOOP
# ============================================
def main():
    Boot.startup()
    Platform.deploy_cli()
    load_admins()
    load_sessions()

    current_user = input("User ID: ").strip()
    print(f"Welcome {current_user} 🌹")
    
    Memory.touch_user(current_user)

    while True:
        msg = input("> ").strip()

        if not msg:
            continue

        if msg.lower() in {"exit", "quit"}:
            Boot.shutdown()
            break

        if Safety.check_abuse(msg):
            print("Abusive content detected 🌹")
            continue

        processed = Perception.process_input(msg)

        # ⚠️ SHOW AUTO-CORRECT WARNING
        if processed.get("warn"):
            print("⚠️ Command auto-corrected — use '.' '/' prefix next time 🤌")

        # ✅ Learn ONLY non-command messages
        if Learning.enabled and processed.get("intent") != "command":
            Learning.observe(processed["text"])
            Memory.store_short(processed["text"])

        # Command handling
        if processed.get("intent") == "command":
            parts = processed["text"][1:].split()

            if not parts:
                print("Invalid command 🤌")
                continue

            cmd_name = parts[0]
            args = parts[1:]

            response = Commands.execute(current_user, cmd_name, *args)
        else:
            response = ResponseGenerator.generate(processed)

        print(response)



# ============================================
# ENTRY POINT — CLI or PLATFORM BRIDGE
# ============================================

import sys  # ✅ REQUIRED — DO NOT REMOVE


def process_external_message(user, text, platform="whatsapp"):
    Platform.set(platform)
    
    Memory.touch_user(user)

    processed = Perception.process_input(text)

    # Learn only non-commands
    if Learning.enabled and processed.get("intent") != "command":
        Learning.observe(processed["text"])
        Memory.store_short(processed["text"])

    if processed["intent"] == "command":
        parts = processed["text"][1:].split()
        if not parts:
            return "Invalid command 🤌"

        cmd = parts[0]
        args = parts[1:]
        return Commands.execute(user, cmd, *args)

    return ResponseGenerator.generate(processed)


if __name__ == "__main__":
    # 🔹 If arguments are passed → PLATFORM MODE (WhatsApp / Telegram)
    if len(sys.argv) >= 3:
        user = sys.argv[1]
        text = " ".join(sys.argv[2:])  # SAFE for spaces

        try:
            output = process_external_message(user, text)
            print(output)
        except Exception as e:
            print(f"Core error: {e}")

    # 🔹 Else → INTERACTIVE CLI MODE
    else:
        main()