import swisseph as swe

# Birth data
# 28 July 2026, 10:15 AM IST, Bathinda, Punjab
LAT, LON = 30.2110, 74.9455   # Bathinda
TZ = 5.5
Y,M,D = 2026,7,28
H,MI = 10,15

ut_hour = H + MI/60.0 - TZ
jd_ut = swe.julday(Y, M, D, ut_hour, swe.GREG_CAL)
print("JD(UT) =", jd_ut)

swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
ayan = swe.get_ayanamsa_ut(jd_ut)
print("Lahiri ayanamsa = %.6f" % ayan)

FLAGS = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

bodies = [("Sun",swe.SUN),("Moon",swe.MOON),("Mars",swe.MARS),("Mercury",swe.MERCURY),
          ("Jupiter",swe.JUPITER),("Venus",swe.VENUS),("Saturn",swe.SATURN),
          ("Rahu(mean)",swe.MEAN_NODE),("Rahu(true)",swe.TRUE_NODE)]

SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio",
         "Sagittarius","Capricorn","Aquarius","Pisces"]
NAK = ["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya",
       "Ashlesha","Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati",
       "Vishakha","Anuradha","Jyeshtha","Mula","Purva Ashadha","Uttara Ashadha","Shravana",
       "Dhanishta","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati"]

def fmt(lon):
    s = int(lon//30); deg = lon-30*s
    d=int(deg); m=int((deg-d)*60); sec=((deg-d)*60-m)*60
    n = int(lon//(360/27)); pada = int((lon % (360/27)) // (360/108)) + 1
    return f"{SIGNS[s]:12s} {d:2d}°{m:02d}'{sec:04.1f}\"  | {NAK[n]:18s} pada {pada}"

print()
for name, pl in bodies:
    pos, _ = swe.calc_ut(jd_ut, pl, FLAGS)
    retro = " (R)" if pos[3] < 0 else ""
    print(f"{name:11s} {pos[0]:10.6f}  {fmt(pos[0])}{retro}")

# Ascendant / houses (Placidus + Whole sign info)
cusps, ascmc = swe.houses_ex(jd_ut, LAT, LON, b'P', swe.FLG_SIDEREAL)
print()
print(f"{'Ascendant':11s} {ascmc[0]:10.6f}  {fmt(ascmc[0])}")
print(f"{'MC':11s} {ascmc[1]:10.6f}  {fmt(ascmc[1])}")
