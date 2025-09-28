# 🔒 Password Strength Checker 🔒

A simple Python tool to evaluate password strength and provide practical tips to improve security.  
Includes optional visual feedback using a bar chart if `matplotlib` is installed.

## Features
- Estimates password strength based on character variety (entropy) and length
- Warns if the password is common or contains easy-to-guess parts
- Shows estimated crack times in different attack scenarios
- Provides actionable improvement suggestions
- Optional visual bar chart for a quick overview

## Requirements
- Python 3.7+
- Optional: `matplotlib` for visual bar chart

Install `matplotlib` (optional):

```bash
pip install matplotlib
```

## Example output:

```🔒 Simple Password Check 🔒```

```Enter your password. The input is hidden and not stored.```
```Password:``` Password

```✅ Status: Good```

```🔢 Length: 8 characters```

```(Internal score: 45.6 — not necessary to understand.)```

```‼️  WARNING: This is a common password. Very easy to break. ‼️```

```--- Scenarios (how fast it can be cracked) ---```

```- Online, very limited (login forms) (10/s): 847.6 centuries — Practically impossible to break.```

```- Online, lightly limited (older sites) (100/s): 84.8 centuries — Practically impossible to break.```

```- Local attack (single GPU) (1,000,000,000/s): 7.4 h — Broken within a day.```

```- Big attacker (GPU cluster) (100,000,000,000/s): 4.5 min — Broken in under an hour.```

```--- Quick advice ---```

```Good. You can still improve.```

```Tips:```

```➕ Make it longer (12+ characters).```

```🔢 Add numbers.```

```🔣 Add symbols (e.g. !?@#).```

```⚠️  Don't use common or very short passwords.```

```🔐 Final tip: Use MFA (Multi-Factor Authentication) when possible. 👍```

Also the visual bar chart will appear if `MATPLOTLIB` installed.

## Notes:

- Your password is never stored. The tool only evaluates it locally.
- Estimated cracking times are approximations; actual times depend on attacker resources.
- For stronger protection, combine a strong password with MFA.
