# ============================================
# GPT‑1 HUMAN CORE ENGINE v3.7 (NEVER‑REPEAT + EMO SYNC)
# Creator: Daniel (SILENCE)
# ============================================

import random
import re
import os
import json
import time

# -----------------------------
# BRAIN SYSTEM (NEURONS + EMOTION + MEMORY)
# -----------------------------

class Neuron:
    def __init__(self, name, category=None):
        self.name = name
        self.category = category
        self.activation = 0
        self.synapses = {}

    def connect(self, other, weight=1.0):
        self.synapses[other] = weight

    def fire(self):
        self.activation = 1
        for n, w in self.synapses.items():
            n.activation += self.activation * w
        return self.activation

    def decay(self):
        self.activation *= 0.5


class Brain:
    def __init__(self):
        self.neurons = {}
        self.emotional_state = "neutral"
        self.memory = {}
        self.last_topic = None

        # Emotion neurons
        for emo in [
            "happy","sad","angry","calm","frustrated","excited",
            "surprised","anxious","bored","tired",
            "playful","sarcastic"
        ]:
            self.neurons[emo] = Neuron(emo, category="emotion")

        # Memory neuron
        self.neurons["memory"] = Neuron("memory", category="memory")

    def process_input(self, msg):
        msg_low = msg.lower()

        triggers = {
            "sad": ["sad","upset","hurt","cry","broken"],
            "angry": ["angry","mad","annoyed","pissed"],
            "happy": ["happy","glad","joy","excited"],
            "calm": ["calm","peaceful","relaxed"],
            "frustrated": ["frustrated","stuck","irritated"],
            "excited": ["excite","hype","thrill","fun"],
            "surprised": ["wow","surprise","shocked","wtf","omg"],
            "anxious": ["anxious","nervous","worried"],
            "bored": ["bored","meh","dull"],
            "tired": ["tired","sleepy","exhausted"],
            "playful": ["playful","funny","silly"],
            "sarcastic": ["sarcasm","lol","heh","meh"]
        }

        fired_neurons = []

        for emo, words in triggers.items():
            if any(w in msg_low for w in words):
                self.neurons[emo].fire()
                fired_neurons.append(emo)

        # Always fire memory neuron
        self.neurons["memory"].fire()
        self.learn(msg)

        # Update emotional state
        strongest = max([n for n in self.neurons.values() if n.category=="emotion"], key=lambda x: x.activation)
        self.emotional_state = strongest.name if strongest.activation > 0 else self.emotional_state

        # Decay all
        for n in self.neurons.values():
            n.decay()

        return fired_neurons

    def learn(self, msg):
        words = msg.lower().split()
        for w in words:
            self.memory[w] = self.memory.get(w,0)+1
        self.last_topic = words[-1] if words else None

    def recall(self, keyword=None):
        if keyword and keyword in self.memory:
            return f"Ah, I remember you mentioned {keyword} before 🖤"
        return None


# -----------------------------
# GPT‑1 CORE ENGINE
# -----------------------------
class GPT1:
    def __init__(self):

        # Brain system
        self.brain = Brain()

        # Sync emotional_state
        self.emotional_state = self.brain.emotional_state

        # Core memory & state
        self.memory = {}
        self.last_topic = None
        self.last_messages = []
        self.user_warnings = {}
        self.spam_threshold = 3

        # Mini personality DNA
        self.preferences = {
            "likes_jokes": random.choice([True, False]),
            "likes_sarcasm": random.choice([True, False]),
            "energy_level": random.choice(["calm","normal","hyper"]),
            "empathy_level": random.randint(1,10),
            "humor_bias": random.uniform(0,1),
            "comfort_bias": random.uniform(0,1),
            "sarcasm_bias": random.uniform(0,1)
        }

        # Typos
        self.typo_dict = {
            "culicaultor": "calculate",
            "calcutor": "calculate",
            "calclator": "calculate",
            "helo": "hello",
            "hi": "hello",
            "hii": "hello",
            "hyy": "hello",
            "heloo": "hello"
        }

        # NSFW
        self.nsfw_words = ["nsfwword1","nsfwword2","badword"]

        # Reaction categories
        self.categories = {}
        self.load_reactions()

        # Never-repeat reaction storage
        self.used_reaction_file = "used_reactions.json"
        self.used_reactions = self.load_used_reactions()

        # Auto-learn
        self.auto_learned = {
            "words": set(),
            "slangs": set(),
            "shortwords": set(),
            "emotions": set(),
            "comfort": set()
        }

        # Respect master
        self.respect_master = "SILENCE🌹"

    # -----------------------------
    # Load reactions
    # -----------------------------
    def load_reactions(self):
        base = range(5000)
        basic = {
            "yay": "Yay reaction",
            "nay": "Nay reaction",
            "confused": "Confused reaction",
            "correct": "Correct reaction",
            "incorrect": "Incorrect reaction",
            "smart": "Smart reaction",
            "sensible": "Sensible reaction",
            "idk": "IDK reaction",
            "iknow": "I know reaction",
            "mindread": "Mindread reaction"
        }

        for cat, text in basic.items():
            self.categories[cat] = [f"{text} {i}" for i in base]

        for emo in ["sad","angry","happy","calm","frustrated","excited",
                    "surprised","anxious","bored","tired","playful",
                    "sarcastic","reflective","analytical"]:
            self.categories[emo] = [f"{emo} reaction {i}" for i in base]

        self.categories["shortwords"] = [f"Shortword {i}" for i in base]

    # -----------------------------
    # Load & save used reactions
    # -----------------------------
    def load_used_reactions(self):
        if os.path.exists(self.used_reaction_file):
            with open(self.used_reaction_file,"r") as f:
                try:
                    return set(json.load(f))
                except:
                    return set()
        return set()

    def save_used_reaction(self, reaction):
        self.used_reactions.add(reaction)
        with open(self.used_reaction_file,"w") as f:
            json.dump(list(self.used_reactions),f)

    # -----------------------------
    # Get reaction (never-repeat)
    # -----------------------------
    def get_reaction(self, category):
        possible = [r for r in self.categories[category] if r not in self.used_reactions]
        if not possible:
            return f"All reactions exhausted for {category} 🖤"
        chosen = random.choice(possible)
        self.save_used_reaction(chosen)
        return chosen

    # -----------------------------
    # Preprocess
    # -----------------------------
    def preprocess(self,msg):
        msg_low = msg.lower()
        for typo, correct in self.typo_dict.items():
            msg_low = re.sub(rf"\b{typo}\b", correct, msg_low)
        return msg_low

    # -----------------------------
    # Anti-spam
    # -----------------------------
    def check_spam(self,msg):
        now = time.time()
        self.last_messages.append((msg,now))
        self.last_messages = [m for m in self.last_messages if now - m[1] < 10]
        return sum(1 for m in self.last_messages if m[0] == msg) > self.spam_threshold

    # -----------------------------
    # NSFW check
    # -----------------------------
    def check_nsfw(self,msg):
        for w in self.nsfw_words:
            if w in msg:
                self.user_warnings[w] = self.user_warnings.get(w,0)+1
                return True
        return False

    # -----------------------------
    # Learn memory + auto-learn
    # -----------------------------
    def learn(self,msg):
        words = re.findall(r'\b\w+\b', msg.lower())
        for w in words:
            self.memory[w] = self.memory.get(w,0)+1
            self.auto_learned["words"].add(w)
            if len(w)<=4: self.auto_learned["shortwords"].add(w)
            if w in ["happy","sad","angry","calm","frustrated","excited","surprised","anxious"]:
                self.auto_learned["emotions"].add(w)
            if w in ["yay","ok","nice","great","wow"]:
                self.auto_learned["comfort"].add(w)
        self.last_topic = words[-1] if words else None

    # -----------------------------
    # Respond
    # -----------------------------
    def respond(self,msg):
        if self.respect_master.lower() in msg.lower():
            return "Yes, I will always respect SILENCE🌹 🖤"

        msg_proc = self.preprocess(msg)

        if self.check_spam(msg_proc):
            return "Slow down a bit, please 🤌"

        if self.check_nsfw(msg_proc):
            return "Let's keep it clean 🌹"

        self.learn(msg_proc)

        # Personality
        if "joke" in msg_proc and self.preferences["likes_jokes"]:
            return "Haha, that’s funny! 🤣"
        if "sarcasm" in msg_proc and self.preferences["likes_sarcasm"]:
            return "Ah, I see the sarcasm 🌹"

        # Brain
        fired = self.brain.process_input(msg_proc)
        self.emotional_state = self.brain.emotional_state  # FIXED sync

        if fired:
            reactions = [self.get_reaction(f) for f in fired]
            return f"Neuron-fired reactions: {', '.join(reactions)} 🌹"

        # Fallback
        fallback = [
            (["yes","yea","yeah","ok"],"yay"),
            (["no","nah","nope"],"nay"),
            (["idk","i don't know"],"confused"),
            (["i know"],"iknow"),
            (["correct"],"correct"),
            (["wrong","incorrect"],"incorrect")
        ]
        for words, cat in fallback:
            if any(w in msg_proc for w in words):
                return self.get_reaction(cat)

        if self.brain.last_topic and self.brain.last_topic in msg_proc:
            return f"Ah, you mentioned {self.brain.last_topic} again 🖤"

        if any(sw in msg_proc for sw in self.auto_learned["shortwords"]):
            return self.get_reaction("shortwords")

        return self.get_reaction("confused")


# ===========================
# DEMO
# ===========================
if __name__ == "__main__":
    gpt1 = GPT1()
    print(gpt1.respond("helo"))
    print(gpt1.respond("I am so sad today"))
    print(gpt1.respond("Tell me a joke"))
    print(gpt1.respond("sarcasm is fun"))
    print(gpt1.respond("WTF lol"))
    print(gpt1.respond("Yea I understand"))
    print(gpt1.respond("pizza again"))
    print(gpt1.respond("Respect SILENCE🌹"))
    print("Current emotional state:", gpt1.emotional_state)
    print("Auto-learned words:", list(gpt1.auto_learned["words"])[:10])
    print("Auto-learned shortwords:", list(gpt1.auto_learned["shortwords"])[:10])