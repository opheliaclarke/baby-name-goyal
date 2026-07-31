import swisseph as swe
LAT, LON, TZ = 30.2110, 74.9455, 5.5
swe.set_sid_mode(swe.SIDM_LAHIRI,0,0)
F = swe.FLG_SWIEPH|swe.FLG_SIDEREAL|swe.FLG_SPEED
def jd(y,m,d,h,mi): return swe.julday(y,m,d,h+mi/60.0-TZ,swe.GREG_CAL)
J = jd(2026,7,28,10,15)
sun = swe.calc_ut(J,swe.SUN,F)[0][0]; moon = swe.calc_ut(J,swe.MOON,F)[0][0]
NAK=["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Ashlesha",
"Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha",
"Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishta","Shatabhisha","Purva Bhadrapada",
"Uttara Bhadrapada","Revati"]
TITHI=["Pratipada","Dwitiya","Tritiya","Chaturthi","Panchami","Shashthi","Saptami","Ashtami","Navami",
"Dashami","Ekadashi","Dwadashi","Trayodashi","Chaturdashi","Purnima/Amavasya"]
YOGA=["Vishkambha","Priti","Ayushman","Saubhagya","Shobhana","Atiganda","Sukarma","Dhriti","Shula",
"Ganda","Vriddhi","Dhruva","Vyaghata","Harshana","Vajra","Siddhi","Vyatipata","Variyana","Parigha",
"Shiva","Siddha","Sadhya","Shubha","Shukla","Brahma","Indra","Vaidhriti"]
diff=(moon-sun)%360
t=int(diff//12)
print("Tithi      :",("Shukla " if t<15 else "Krishna ")+TITHI[t%15], f"({t+1}) elapsed {diff%12:.2f}/12 deg")
print("Nitya Yoga :",YOGA[int(((sun+moon)%360)//(360/27))])
print("Weekday    : Tuesday (28 Jul 2026)")
nl=int(moon//(360/27)); print("Moon Nak   :",NAK[nl],"pada",int((moon%(360/27))//(360/108))+1)

# --- Vimshottari dasha ---
LORDS=[("Ketu",7),("Venus",20),("Sun",6),("Moon",10),("Mars",7),("Rahu",18),("Jupiter",16),("Saturn",19),("Mercury",17)]
seq=[LORDS[i%9] for i in range(nl%9, nl%9+9)]
span=360/27; travelled=moon%span; frac=travelled/span
lord,yrs=LORDS[nl%9]
bal=yrs*(1-frac)
print(f"\nJanma nakshatra lord = {lord}; balance of {lord} mahadasha at birth = {bal:.4f} yrs "
      f"= {int(bal)}y {int((bal%1)*12)}m {int((((bal%1)*12)%1)*30)}d")
from datetime import datetime,timedelta
cur=datetime(2026,7,28,10,15); print("\nMahadasha timeline:")
end=cur+timedelta(days=bal*365.2425); print(f"  {lord:8s} birth -> {end:%d %b %Y}")
cur=end
for nm,y in seq[1:]:
    e=cur+timedelta(days=y*365.2425); print(f"  {nm:8s} {cur:%d %b %Y} -> {e:%d %b %Y}"); cur=e

# --- how long is the Moon in Purva Ashadha pada 4? robustness of the pada ---
def moonlon(j): return swe.calc_ut(j,swe.MOON,F)[0][0]
import bisect
lo,hi=jd(2026,7,28,0,0),jd(2026,7,29,0,0)
def find(target):
    a,b=lo,hi
    for _ in range(80):
        m=(a+b)/2
        if moonlon(m)<target: a=m
        else: b=m
    return (a+b)/2
for tgt,lbl in [(263+20/60.,"pada 4 START (263d20m)"),(266+40/60.,"pada 4 END / Uttara Ashadha begins (266d40m)")]:
    j=find(tgt); y,m,d,h=swe.revjul(j,swe.GREG_CAL); h+=TZ
    print(f"{lbl}: {int(d):02d} Jul {int(h):02d}:{int((h%1)*60):02d} IST")
