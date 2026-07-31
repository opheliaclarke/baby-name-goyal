import swisseph as swe
LAT,LON,TZ=30.2110,74.9455,5.5
jd=swe.julday(2026,7,28,10+15/60.-TZ,swe.GREG_CAL)
NAK=["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Ashlesha",
"Magha","P.Phalguni","U.Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha",
"Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishta","Shatabhisha","P.Bhadrapada",
"U.Bhadrapada","Revati"]
SYL={19:["Bu","Dha","Pha","Dha"],20:["Be","Bo","Ja","Ji"]}
modes=[("Lahiri (Indian govt standard)",swe.SIDM_LAHIRI),("Krishnamurti / KP",swe.SIDM_KRISHNAMURTI),
       ("Raman",swe.SIDM_RAMAN),("Fagan-Bradley (Western sidereal)",swe.SIDM_FAGAN_BRADLEY),
       ("Yukteshwar",swe.SIDM_YUKTESHWAR),("True Chitrapaksha",swe.SIDM_TRUE_CITRA),
       ("True Revati",swe.SIDM_TRUE_REVATI)]
print(f"{'ayanamsa':<34}{'value':>9}  {'Moon sid.':>10}  nakshatra / pada / syllable")
print("-"*94)
for name,m in modes:
    swe.set_sid_mode(m,0,0)
    ay=swe.get_ayanamsa_ut(jd)
    lon=swe.calc_ut(jd,swe.MOON,swe.FLG_SWIEPH|swe.FLG_SIDEREAL)[0][0]
    n=int(lon//(360/27)); pada=int((lon%(360/27))//(360/108))+1
    syl=SYL.get(n,["?"]*4)[pada-1]
    print(f"{name:<34}{ay:9.4f}  {lon:10.4f}  {NAK[n]:<16} pada {pada}  -> {syl}")
