import math
import string
import getpass
import sys
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except Exception:
    MATPLOTLIB_AVAILABLE = False

FALLBACK_COMMON = {
    "123456","password","123456789","12345678","12345","qwerty",
    "abc123","password1","111111","1234567","iloveyou","admin"
}

def load_common_passwords():
    p = Path(__file__).parent / "common_passwords.txt"
    if not p.exists():
        return FALLBACK_COMMON
    words = set()
    try:
        with p.open(encoding="utf-8") as f:
            for line in f:
                w = line.strip()
                if not w or w.startswith("#"):
                    continue
                words.add(w.lower())
    except Exception:
        return FALLBACK_COMMON
    return words or FALLBACK_COMMON

COMMON_PASSWORDS = load_common_passwords()

SCENARIOS = [
    ("Online, very limited (login forms)", 10),
    ("Online, lightly limited (older sites)", 100),
    ("Local attack (single GPU)", 1e9),
    ("Big attacker (GPU cluster)", 1e11),
]

def charset_size(password: str) -> int:
    cs = 0
    if any(c.islower() for c in password):
        cs += len(string.ascii_lowercase)
    if any(c.isupper() for c in password):
        cs += len(string.ascii_uppercase)
    if any(c.isdigit() for c in password):
        cs += len(string.digits)
    if any(c in string.punctuation for c in password):
        cs += len(string.punctuation)
    if any(c.isspace() for c in password):
        cs += 1
    return cs or 1

def entropy_bits(password: str) -> float:
    cs = charset_size(password)
    if cs <= 1:
        return 0.0
    return len(password) * math.log2(cs)

def avg_crack_time_seconds_from_bits(bits: float, attempts_per_second: float) -> float:
    combos = 2 ** bits
    return (combos / 2) / attempts_per_second

def human_readable(seconds: float) -> str:
    if seconds < 1:
        return f"{seconds*1000:.0f} ms"
    minute = 60
    hour = 3600
    day = 86400
    year = 365 * day
    century = 100 * year

    if seconds < minute:
        return f"{seconds:.1f} s"
    if seconds < hour:
        return f"{seconds/minute:.1f} min"
    if seconds < day:
        return f"{seconds/hour:.1f} h"
    if seconds < year:
        return f"{seconds/day:.1f} days"
    if seconds < century:
        return f"{seconds/year:.1f} years"
    return f"{seconds/century:.1f} centuries"

def human_interpretation(seconds: float) -> str:
    if seconds < 1:
        return "Broken instantly."
    if seconds < 60:
        return "Broken in under a minute."
    if seconds < 3600:
        return "Broken in under an hour."
    if seconds < 86400:
        return "Broken within a day."
    if seconds < 365*86400:
        return "Broken in months/years."
    if seconds < 100*365*86400:
        return "Very long to break (years)."
    return "Practically impossible to break."

def strength_label(bits: float) -> str:
    if bits < 28:
        return "Weak"
    if bits < 36:
        return "Okay"
    if bits < 60:
        return "Good"
    return "Very strong"

def suggest_improvements(password: str) -> list:
    suggestions = []
    if len(password) < 12:
        suggestions.append("➕ Make it longer (12+ characters).")
    if not any(c.islower() for c in password):
        suggestions.append("🔡 Add lowercase letters.")
    if not any(c.isupper() for c in password):
        suggestions.append("🔠 Add uppercase letters.")
    if not any(c.isdigit() for c in password):
        suggestions.append("🔢 Add numbers.")
    if not any(c in string.punctuation for c in password):
        suggestions.append("🔣 Add symbols (e.g. !?@#).")
    if password.lower() in COMMON_PASSWORDS or len(password) <= 4:
        suggestions.append("⚠️  Don't use common or very short passwords.")
    if not suggestions:
        suggestions.append("✅ Nice! Consider a passphrase or a password manager.")
    return suggestions

def contains_common_part(password: str) -> bool:
    low = password.lower()
    for common in COMMON_PASSWORDS:
        if common in low and len(common) >= 3:
            return True
    return False

def show_strength_visual(bits: float, label: str):
    # Map bits to 0-100 scale (assume 0..80 bits -> 0..100)
    perc = min(max((bits / 80.0) * 100.0, 0.0), 100.0)

    if MATPLOTLIB_AVAILABLE:
        fig, ax = plt.subplots(figsize=(8, 2.2))
        # background full bar (light alpha)
        ax.barh([0], [100], height=0.5, alpha=0.15)
        # filled portion to the score
        ax.barh([0], [perc], height=0.5)
        # vertical marker line at the score
        ax.axvline(perc, ymin=0.1, ymax=0.9, linewidth=2)
        ax.set_xlim(0, 100)
        ax.set_yticks([])
        ax.set_xlabel("Password strength (visual scale 0–100)")
        ax.set_title(f"Strength: {label} — {perc:.0f}/100")
        ax.text(2, -0.35, "Weak", va="center")
        ax.text(30, -0.35, "Okay", va="center")
        ax.text(55, -0.35, "Good", va="center")
        ax.text(82, -0.35, "Very strong", va="center")
        plt.tight_layout()
        plt.show()
    else:
        blocks = int(perc // 2) 
        print("\nVisual: [" + "#" * blocks + "-" * (50 - blocks) + f"] {perc:.0f}/100")

def check_password_and_show(password: str, interactive=True):
    bits = entropy_bits(password)
    label = strength_label(bits)

    status_emoji = "✅" if label in ("Good", "Very strong") else "⚠️ "
    print(f"{status_emoji} Status: {label}")
    print(f"🔢 Length: {len(password)} characters")
    print(f"(Internal score: {bits:.1f} — not necessary to understand.)")

    if password.lower() in COMMON_PASSWORDS:
        print("\n‼️  WARNING: This is a common password. Very easy to break. ‼️")
    elif contains_common_part(password):
        print("\n⚠️  Warning: Your password contains common word/number parts. ⚠️")

    print("\n--- Scenarios (how fast it can be cracked) ---")
    for desc, r in SCENARIOS:
        secs = avg_crack_time_seconds_from_bits(bits, r)
        print(f"- {desc} ({int(r):,}/s): {human_readable(secs)} — {human_interpretation(secs)}")

    # Quick advice
    print("\n--- Quick advice ---")
    if label == "Weak":
        print("Weak. Change it now.")
    elif label == "Okay":
        print("Okay. Needs improvement.")
    elif label == "Good":
        print("Good. You can still improve.")
    else:
        print("Very strong. Nice!")

    # Tips
    print("\nTips:")
    for s in suggest_improvements(password):
        print(s)

    print("\n🔐 Final tip: Use MFA (Multi-Factor Authentication) when possible. 👍")

    if interactive:
        try:
            show_strength_visual(bits, label)
        except Exception:
            show_strength_visual(bits, label)

def main():
    if sys.stdin and sys.stdin.isatty():
        print("🔒 Simple Password Check 🔒")
        print()
        print("Enter your password. The input is hidden and not stored.")
        try:
            pw = getpass.getpass("Password: ")
        except Exception:
            pw = input("Password: ")
        if not pw:
            print("No password entered. Bye.")
            return
        check_password_and_show(pw, interactive=True)
    else:
        demo = "Password1!"
        print(f"Demo run (no terminal input). Sample password: {demo}\n")
        check_password_and_show(demo, interactive=True)

if __name__ == "__main__":
    main()
