#!/usr/bin/env python3
"""FULL-NAME gate: score '<First> Goyal' as one string.
Same two tests as before, but applied to the full total: fortunate Cheiro compound
AND root friendly to BOTH Moolank 1 (Sun) and Bhagyank 9 (Mars)."""
import sys; sys.path.insert(0,'/root/workspace/baby-name-goyal')
from score import score, chaldean, reduce_num, COMPOUND, PLANET, FRIEND_1, FRIEND_9

GOYAL = chaldean("Goyal")
print(f"GOYAL = {GOYAL}  (root {reduce_num(GOYAL)} = {PLANET[reduce_num(GOYAL)]})")
print(f"So every full-name total = first-name total + {GOYAL}\n")

def passes(total):
    if total not in COMPOUND: return False, "outside Cheiro's 10-52 series — ungraded"
    v,_ = COMPOUND[total]
    r = reduce_num(total)
    if v != "F": return False, f"compound {total} is {v}"
    if FRIEND_1.get(r) not in ("own","friend"): return False, f"root {r} {PLANET[r]} is {FRIEND_1.get(r)} to Sun"
    if FRIEND_9.get(r) not in ("own","friend"): return False, f"root {r} {PLANET[r]} is {FRIEND_9.get(r)} to Mars"
    return True, COMPOUND[total][1]

print("FULL-NAME totals that pass, and the first-name total each demands:")
print("-"*88)
need = []
for t in range(GOYAL+1, 61):
    ok, why = passes(t)
    if ok:
        first = t - GOYAL
        need.append(first)
        print(f"  full {t:>2} (root {reduce_num(t)} {PLANET[reduce_num(t)]:<8}) <- first name must total {first:>2}   {why[:46]}")
print(f"\n  => first-name totals to hunt for: {sorted(need)}")

print("\nMinimum possible totals (so we know what is unreachable):")
for pre in ("Dh","Bh","Ph"):
    print(f"  any {pre}- name starts at {chaldean(pre)}")

print("\n" + "="*88)
print("THE KEY QUESTION — which totals pass BOTH gates (first-name-only AND full-name)?")
print("="*88)
FIRST_GATE = {1,3,9,19,21,27,36,37,45,46}
both=[]
for f in sorted(FIRST_GATE):
    ok, why = passes(f+GOYAL)
    mark = "PASSES BOTH" if ok else f"fails full ({why})"
    print(f"  first {f:>2} -> full {f+GOYAL:>2}   {mark}")
    if ok: both.append(f)
print(f"\n  => ONLY first-name total(s) {both} satisfy both readings.")
