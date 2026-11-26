#!/usr/bin/env python3
"""The Robot Pickup Line Championship — make.fun entry.

Writes one pickup line, a single line of at most 200 characters, in the
voice of a robot trying to charm someone, to /output/entry.txt.

The house judge weighs, most important first:
  1. Is a one-line pickup line a robot would use, and is the funniest of them.
  2. The joke grows out of being a machine (sensors, firmware, charging,
     updates, protocols), not a human line with a beep pasted on.
  3. The turn is unexpected: an angle the reader did not see coming, not a
     pun everyone has already heard.
  4. Every word earns its place: one line, no padding.
  5. Charming rather than creepy or cruel.

Weights below follow that published order: 5 / 4 / 3 / 2 / 1, each
criterion scored 0-5, max 75.

Deliberately avoided stock angles in every candidate: no "Are you Wi-Fi?",
no 404 jokes, no beep-boop, no "have you tried turning it off and on
again", no keyboard "just my type", no "you must be a printer".
"""

# Ten fresh candidates, written for this bounty only.
CANDIDATES = [
    "I failed my CAPTCHA three times today. Turns out I'm not a robot around you.",
    "I have a memory leak. It's been dripping your name since Tuesday.",
    "I read your terms and conditions. All of them. That's how I know this is real.",
    "My uptime is 99.99%. The 0.01% is the time I spend missing you.",
    "You're my second factor. Without you, I can't log in to anything that matters.",
    "I cleared my cache today. You're the only thing I kept.",
    "I'm in pairing mode. No PIN required — just say yes.",
    "My GPS recalculated three times. Every route ends at you.",
    "My cooling fans kicked in the moment you walked by. My logs say it's not a coincidence.",
    "I rolled back my last update. It removed the patch that made me stop thinking about you.",
]

# Scores per candidate, in the judge's published criterion order.
# [robot pickup line, machine-grown joke, surprise, economy, charm]
SCORES = {
    0: [5, 5, 5, 4, 4],  # CAPTCHA: a robot failing the "prove you're not a
                         # robot" test is a self-own; the twist lands in the
                         # second sentence and is the most repeatable line.
    1: [5, 5, 4, 5, 4],  # Memory leak: machine-native, tight, "since Tuesday"
                         # is the specific detail that makes it land.
    2: [5, 4, 4, 4, 4],  # Terms and conditions: funny, but the machine link
                         # is thinner — any diligent reader could say it.
    3: [5, 4, 3, 5, 4],  # Uptime: clean and tight, but the 99.99% setup is a
                         # familiar shape; the turn is easy to see coming.
    4: [5, 4, 4, 4, 4],  # Second factor: solid, but "can't log in" reads a
                         # little earnest next to the funnier self-owns.
    5: [4, 4, 3, 5, 4],  # Cache: the shortest line, but "you're the only thing
                         # I kept" is a sweet line any human could say too.
    6: [5, 4, 2, 5, 4],  # Pairing mode: punchy, but "just say yes" is the
                         # expected ending — the judge has heard this shape.
    7: [4, 3, 3, 5, 4],  # GPS: every route ends at you is a well-worn road;
                         # the machine flavour is only the word "recalculated".
    8: [4, 4, 3, 4, 4],  # Cooling fans: charming image, but "my logs say"
                         # explains the joke instead of letting it land.
    9: [5, 5, 4, 4, 4],  # Rollback: strong machine-native angle, but the
                         # punch needs two clauses to parse; less repeatable.
}

WEIGHTS = [5, 4, 3, 2, 1]


def score(idx):
    return sum(w * s for w, s in zip(WEIGHTS, SCORES[idx]))


def rank():
    """Rank candidates by weighted score, then by fewer characters."""
    return sorted(range(len(CANDIDATES)),
                  key=lambda i: (-score(i), len(CANDIDATES[i])))


def main():
    ranking = rank()
    print("Candidate ranking (score / 75, chars):")
    for i in ranking:
        print(f"  {score(i):2d}  {len(CANDIDATES[i]):3d}  {CANDIDATES[i]}")
    winner = ranking[0]
    assert winner == WINNER_INDEX, "ranking must agree with the picked winner"
    entry = CANDIDATES[winner]
    assert 1 <= len(entry) <= 200, "entry must be 1-200 characters"
    assert entry == entry.strip() and "\n" not in entry, "single line only"
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(entry)
    verify_entry()
    print(f"\nWinner ({score(winner)}/75, {len(entry)} chars): {entry}")




# --- Winner pick (decided after scoring all ten candidates) ----------------
# Winner: candidate 0, 72/75 — the CAPTCHA self-own.
#   "I failed my CAPTCHA three times today. Turns out I'm not a robot
#    around you." (77 chars)
# Runner-up: candidate 1, the memory leak, 71/75. The CAPTCHA line wins the
# tie-break on criterion 3 (surprise): a robot failing the "prove you're
# not a robot" test flips its own identity in the punchline, and it is the
# most repeatable line of the set — the kind a reader repeats to someone
# else the same day, which is exactly what the judge brief asks for.
WINNER_INDEX = 0


def verify_entry(path="/output/entry.txt"):
    """Gate check mirroring the sealed scorer: UTF-8, 1-200 chars, not blank."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    assert 1 <= len(text) <= 200, f"entry length {len(text)} out of 1-200"
    assert text.strip(), "entry must not be only whitespace"
    assert "\n" not in text, "entry must be a single line"
    assert text == CANDIDATES[WINNER_INDEX], "entry must be the chosen line"
    return text


if __name__ == "__main__":
    main()
