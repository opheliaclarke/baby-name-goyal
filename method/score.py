#!/usr/bin/env python3
"""Chaldean numerology scorer for the Goyal baby-name shortlist.
Chaldean map + Cheiro compound table reused from the verified numerology-brand/method/score.py."""

CHALDEAN = {}
for n, letters in {1:"AIJQY",2:"BKR",3:"CGLS",4:"DMT",5:"EHNX",6:"UVW",7:"OZ",8:"FP"}.items():
    for ch in letters: CHALDEAN[ch] = n

PYTH = {ch: (i % 9) + 1 for i, ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}

# Cheiro compound verdicts 10-52 (F=fortunate, M=mixed, U=unfortunate)
COMPOUND = {
 10:("F","Wheel of Fortune — honour and faith; fortunate in the narrow sense that one's plans get carried out. Rise AND fall are intrinsic"),
 11:("U","Hidden dangers, treachery from others"),
 12:("U","The Sacrifice / the Victim"),
 13:("M","Upheaval and change — Cheiro says it is NOT unfortunate: power and dominion to those who understand it"),
 14:("M","Fortunate for money, speculation and change in business, but always a strong element of risk"),
 15:("M","Unnamed by Cheiro. Lucky with a fortunate number, but ruthless if tied to a 4 or an 8"),
 16:("U","Tower struck by lightning — fatality"),
 17:("F","Star of Peace and Love — rises above trials, lasting name"),
 18:("U","Materialism destroying spirit — treachery, quarrels"),
 19:("F","The Sun / Prince of Heaven — success, honour, happiness. Cheiro's most fortunate"),
 20:("M","The Awakening — spiritual call, materially weak"),
 21:("F","The Crown of the Magi — advancement, honour, victory after struggle"),
 22:("U","Good man blinded — illusion, delusion"),
 23:("F","ROYAL STAR OF THE LION — help from superiors assured, greatest promise"),
 24:("F","Gain through love and rank; assistance from those above"),
 25:("M","Strength gained through experience and trial"),
 26:("U","Gravest warnings — ruin through association and bad advice"),
 27:("F","The Sceptre — authority, command, reward of the intellect"),
 28:("M","Great promise undone by poor planning; loss through misplaced trust"),
 29:("U","Uncertainties, treachery, deception by others"),
 30:("M","Thoughtful deduction, mental superiority; materially indifferent"),
 31:("U","Isolation, lonely, not fortunate materially"),
 32:("F","Magical power, like 23; success while plans are held to"),
 33:("F","Same as 24 — assistance from rank and affection"),
 34:("M","Same as 25"),
 35:("U","Same as 26"),
 36:("F","Same as 27"),
 37:("F","Good friendships, partnerships, love; fortunate"),
 38:("U","Same as 29"),
 39:("M","Same as 30"),
 40:("U","Same as 31"),
 41:("F","Same as 32 — magical combinations"),
 42:("F","Same as 24"),
 43:("U","Revolution, upheaval, strife, failure"),
 44:("U","Same as 26"),
 45:("F","Same as 27"),
 46:("F","Same as 37"),
 47:("U","Same as 29"),
 48:("M","Same as 30"),
 49:("U","Same as 31"),
 50:("F","Same as 32"),
 51:("M","The Warrior — high power and sudden advancement, but it ends by threatening enemies and danger"),
 52:("U","Same as 43"),
}

# Numerology planetary rulers
PLANET = {1:"Sun",2:"Moon",3:"Jupiter",4:"Rahu",5:"Mercury",6:"Venus",7:"Ketu",8:"Saturn",9:"Mars"}

# --- THE CHILD'S NUMBERS -------------------------------------------------
# DOB 28-07-2026
MOOLANK  = 1   # day 28 -> 2+8 = 10 -> 1  (Sun)
BHAGYANK = 9   # 2+8+0+7+2+0+2+6 = 27 -> 9  (Mars)

# Friendship of the name-root to Moolank 1 (Sun) and Bhagyank 9 (Mars).
# Sun's friends: Moon(2), Jupiter(3), Mars(9). Neutral: Mercury(5). Enemy: Venus(6), Saturn(8), Rahu(4), Ketu(7).
# Mars's friends: Sun(1), Moon(2), Jupiter(3). Enemy: Mercury(5), Ketu(7). Neutral: Venus(6), Saturn(8), Rahu(4).
FRIEND_1 = {1:"own",2:"friend",3:"friend",9:"friend",5:"neutral",4:"enemy",6:"enemy",7:"enemy",8:"enemy"}
FRIEND_9 = {9:"own",1:"friend",2:"friend",3:"friend",6:"neutral",8:"neutral",4:"neutral",5:"enemy",7:"enemy"}

def reduce_num(n):
    while n > 9: n = sum(int(d) for d in str(n))
    return n

def chaldean(name):
    s = "".join(c for c in name.upper() if c.isalpha())
    return sum(CHALDEAN.get(c, 0) for c in s)

def pyth(name):
    s = "".join(c for c in name.upper() if c.isalpha())
    return sum(PYTH.get(c, 0) for c in s)

def score(name):
    ch = chaldean(name); root = reduce_num(ch)
    verdict, meaning = COMPOUND.get(ch, ("F" if ch in (1,3,5,6,9) else "M", "single-digit total"))
    f1, f9 = FRIEND_1.get(root,"?"), FRIEND_9.get(root,"?")
    # GATE: compound must be Fortunate AND root must be friendly/own to BOTH 1 and 9
    ok_compound = verdict == "F"
    ok_root = f1 in ("own","friend") and f9 in ("own","friend")
    py = pyth(name); pyroot = reduce_num(py)
    return dict(name=name, ch=ch, root=root, planet=PLANET[root], verdict=verdict, meaning=meaning,
                f1=f1, f9=f9, ok=ok_compound and ok_root, ok_compound=ok_compound, ok_root=ok_root,
                py=py, pyroot=pyroot, dual=(root==pyroot),
                full=chaldean(name+"Goyal"), full_root=reduce_num(chaldean(name+"Goyal")),
                full_verdict=COMPOUND.get(chaldean(name+"Goyal"),("?","?"))[0])

if __name__ == "__main__":
    import sys
    print("Moolank  (day 28)        =", reduce_num(28), PLANET[reduce_num(28)])
    print("Bhagyank (28+07+2026)    =", reduce_num(2+8+0+7+2+0+2+6), PLANET[reduce_num(27)])
    print("Surname GOYAL Chaldean   =", chaldean("Goyal"))
    print()
    # Which totals PASS the gate? Enumerate every compound 1..60
    print("PASSING TOTALS (fortunate compound + root friendly to BOTH 1 and 9):")
    good=[]
    for t in range(1,61):
        r=reduce_num(t)
        v=COMPOUND.get(t,("F" if t in (1,3,5,6,9) else "M",""))[0]
        if v=="F" and FRIEND_1.get(r) in ("own","friend") and FRIEND_9.get(r) in ("own","friend"):
            good.append(t); print(f"   {t:>2}  -> root {r} ({PLANET[r]})   {COMPOUND.get(t,('','single digit'))[1][:60]}")
    print("\n  => target totals:", good)
    for n in sys.argv[1:]:
        r=score(n); print(r)
