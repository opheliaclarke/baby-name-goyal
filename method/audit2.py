#!/usr/bin/env python3
"""The two numerology layers I computed but never SHOWED: Pythagorean cross-check, and Lo Shu gaps."""
import sys; sys.path.insert(0,'/root/workspace/baby-name-goyal')
from score import chaldean, pyth, reduce_num, COMPOUND, PLANET, FRIEND_1, FRIEND_9
G=15
FIN=["Dhyann","Dheer","Dhanvin","Dharmik","Phalit","Bhargava","Dhruv"]

print("="*80); print("5. PYTHAGOREAN CROSS-CHECK — I used Chaldean throughout and never showed the other table")
print("="*80)
print("   (Chaldean and Pythagorean agree on only 10 of 26 letters, so this is a real 'what if')")
print(f"\n{'NAME':<11}{'CHALDEAN':>20}{'PYTHAGOREAN':>22}   agree on root?")
print("-"*80)
for n in FIN:
    c=chaldean(n); p=pyth(n)
    cr,pr=reduce_num(c),reduce_num(p)
    print(f"{n:<11}{c:>4} -> {cr} {PLANET[cr]:<9}{p:>6} -> {pr} {PLANET[pr]:<9}   {'YES' if cr==pr else 'no'}")
print(f"\n{'':<11}{'CHALDEAN +Goyal':>20}{'PYTHAGOREAN +Goyal':>22}")
print(f"   GOYAL: Chaldean {chaldean('Goyal')} (root {reduce_num(chaldean('Goyal'))}) · Pythagorean {pyth('Goyal')} (root {reduce_num(pyth('Goyal'))})")
for n in FIN:
    c=chaldean(n)+chaldean("Goyal"); p=pyth(n)+pyth("Goyal")
    cr,pr=reduce_num(c),reduce_num(p)
    ok = COMPOUND.get(c,("?",""))[0]=="F" and FRIEND_1.get(cr) in("own","friend") and FRIEND_9.get(cr) in("own","friend")
    print(f"{n:<11}{c:>4} -> {cr} {PLANET[cr]:<9}{p:>6} -> {pr} {PLANET[pr]:<9}   {'chaldean gate: PASS' if ok else 'chaldean gate: fail'}")

print("\n"+"="*80); print("6. LO SHU GAPS — does the name supply the digits his birth date is missing?")
print("="*80)
missing={1,3,4,5,9}
print(f"   birth date 28-07-2026 is missing: {sorted(missing)}   (note: BOTH his Moolank 1 and Bhagyank 9)")
print(f"\n{'NAME':<11}{'alone':>7}{'root':>6}   {'+Goyal':>7}{'root':>6}   digits this name introduces")
print("-"*80)
for n in FIN:
    c=chaldean(n); f=c+G; cr,fr=reduce_num(c),reduce_num(f)
    supplied = sorted({int(d) for d in str(c)} | {cr} | {int(d) for d in str(f)} | {fr})
    fills = sorted(set(supplied) & missing)
    print(f"{n:<11}{c:>7}{cr:>6}   {f:>7}{fr:>6}   fills {fills if fills else '—'}")
