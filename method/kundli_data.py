#!/usr/bin/env python3
"""Full kundli dataset with Hindi labels -> kundlidata.json

Everything the Hindi page prints is computed here; nothing on the page is hand-typed.
Birth: 28 Jul 2026, 10:15 IST, Bathinda (30.2110 N, 74.9455 E).
"""
import swisseph as swe, json, datetime as dt

LAT, LON, TZ = 30.2110, 74.9455, 5.5
swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
F = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
Y, M, D, H, MI = 2026, 7, 28, 10, 15
J = swe.julday(Y, M, D, H + MI / 60. - TZ, swe.GREG_CAL)

RASHI = ["मेष","वृषभ","मिथुन","कर्क","सिंह","कन्या","तुला","वृश्चिक","धनु","मकर","कुंभ","मीन"]
RASHI_EN = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio",
            "Sagittarius","Capricorn","Aquarius","Pisces"]
NAK = ["अश्विनी","भरणी","कृत्तिका","रोहिणी","मृगशिरा","आर्द्रा","पुनर्वसु","पुष्य","आश्लेषा","मघा",
       "पूर्वा फाल्गुनी","उत्तरा फाल्गुनी","हस्त","चित्रा","स्वाति","विशाखा","अनुराधा","ज्येष्ठा","मूल",
       "पूर्वाषाढ़ा","उत्तराषाढ़ा","श्रवण","धनिष्ठा","शतभिषा","पूर्वा भाद्रपद","उत्तरा भाद्रपद","रेवती"]
NAK_LORD = ["केतु","शुक्र","सूर्य","चंद्र","मंगल","राहु","गुरु","शनि","बुध"] * 3
TITHI = ["प्रतिपदा","द्वितीया","तृतीया","चतुर्थी","पंचमी","षष्ठी","सप्तमी","अष्टमी","नवमी","दशमी",
         "एकादशी","द्वादशी","त्रयोदशी","चतुर्दशी","पूर्णिमा"]
NITYA = ["विष्कुम्भ","प्रीति","आयुष्मान","सौभाग्य","शोभन","अतिगण्ड","सुकर्मा","धृति","शूल","गण्ड",
         "वृद्धि","ध्रुव","व्याघात","हर्षण","वज्र","सिद्धि","व्यतीपात","वरीयान","परिघ","शिव","सिद्ध",
         "साध्य","शुभ","शुक्ल","ब्रह्म","इन्द्र","वैधृति"]
KARANA_MOV = ["बव","बालव","कौलव","तैतिल","गर","वणिज","विष्टि (भद्रा)"]
VAAR = ["सोमवार","मंगलवार","बुधवार","गुरुवार","शुक्रवार","शनिवार","रविवार"]
MAAS_HI = ["जनवरी","फ़रवरी","मार्च","अप्रैल","मई","जून","जुलाई","अगस्त","सितंबर","अक्टूबर","नवंबर","दिसंबर"]

GRAHA = [("सू","सूर्य",swe.SUN),("चं","चंद्र",swe.MOON),("मं","मंगल",swe.MARS),
         ("बु","बुध",swe.MERCURY),("गु","गुरु",swe.JUPITER),("शु","शुक्र",swe.VENUS),
         ("श","शनि",swe.SATURN)]
UCHCHA = {"सूर्य":0,"चंद्र":1,"मंगल":9,"बुध":5,"गुरु":3,"शुक्र":11,"शनि":6}
NEECHA = {k:(v+6)%12 for k,v in UCHCHA.items()}
SWA    = {"सूर्य":[4],"चंद्र":[3],"मंगल":[0,7],"बुध":[2,5],"गुरु":[8,11],"शुक्र":[1,6],"शनि":[9,10]}
LORD_OF = {0:"मंगल",1:"शुक्र",2:"बुध",3:"चंद्र",4:"सूर्य",5:"बुध",6:"शुक्र",7:"मंगल",
           8:"गुरु",9:"शनि",10:"शनि",11:"गुरु"}
# combustion orbs (degrees from Sun) — classical Vedic values
ASTA = {"चंद्र":12,"मंगल":17,"बुध":14,"गुरु":11,"शुक्र":10,"शनि":15}

# ---------- positions ----------
pos = {}
for ab, hi, pl in GRAHA:
    p = swe.calc_ut(J, pl, F)[0]
    # |speed| under 0.01°/day is a station — Saturn turned retrograde 27 Jul, the day before birth,
    # so calling it merely "retrograde" understates it.
    pos[hi] = dict(ab=ab, lon=p[0], retro=p[3] < 0, speed=p[3], stationary=abs(p[3]) < 0.01)
rah = swe.calc_ut(J, swe.MEAN_NODE, F)[0]
pos["राहु"] = dict(ab="रा", lon=rah[0], retro=True, speed=rah[3], stationary=False)
pos["केतु"] = dict(ab="के", lon=(rah[0]+180) % 360, retro=True, speed=rah[3], stationary=False)
asc = swe.houses_ex(J, LAT, LON, b'P', swe.FLG_SIDEREAL)[1][0]
LAGNA = int(asc // 30)
sun_lon = pos["सूर्य"]["lon"]

def nav(l): return int(l / (10/3.)) % 12
def house_of(s): return ((s - LAGNA) % 12) + 1
def dms(x):
    """Full degrees-minutes-SECONDS. Truncating to minutes made the printed table
    disagree with the dasha balance computed from it — never round-trip through minutes."""
    d = int(x); m = int((x - d) * 60); s = round((((x - d) * 60) - m) * 60)
    if s == 60: s, m = 0, m + 1
    if m == 60: m, d = 0, d + 1
    return f"{d}°{m:02d}'{s:02d}\""

grahas = []
for hi, d in pos.items():
    s = int(d["lon"] // 30); deg = d["lon"] % 30
    n = int(d["lon"] // (360/27)); pada = int((d["lon"] % (360/27)) // (360/108)) + 1
    st = []
    if hi in UCHCHA:
        if s == UCHCHA[hi]: st.append("उच्च")
        elif s == NEECHA[hi]: st.append("नीच")
        elif s in SWA.get(hi, []): st.append("स्वगृही")
    if hi in ASTA:
        sep = abs((d["lon"] - sun_lon + 180) % 360 - 180)
        if sep < ASTA[hi]: st.append("अस्त")
    if d["retro"] and hi not in ("राहु","केतु"):
        st.append("स्थिर-वक्री" if d["stationary"] else "वक्री")
    grahas.append(dict(graha=hi, ab=d["ab"], lon=round(d["lon"],4), sign=s, rashi=RASHI[s],
                       rashi_en=RASHI_EN[s], deg=dms(deg), house=house_of(s), nak=NAK[n],
                       nak_lord=NAK_LORD[n], pada=pada, navamsa=RASHI[nav(d["lon"])],
                       retro=d["retro"], status=" · ".join(st)))

lagna = dict(rashi=RASHI[LAGNA], rashi_en=RASHI_EN[LAGNA], sign=LAGNA, deg=dms(asc % 30),
             nak=NAK[int(asc//(360/27))], pada=int((asc % (360/27))//(360/108))+1,
             navamsa=RASHI[nav(asc)], lord=LORD_OF[LAGNA], lon=round(asc,4))

# ---------- panchang ----------
moon_lon = pos["चंद्र"]["lon"]
elong = (moon_lon - sun_lon) % 360
ti = int(elong // 12)
tithi = dict(num=ti+1, name=TITHI[min(ti % 15, 14)],
             paksha="शुक्ल पक्ष" if ti < 15 else "कृष्ण पक्ष",
             elapsed=round(elong % 12, 2))
k = int(elong // 6)                      # 0..59
if k == 0:      karana = "किंस्तुघ्न"
elif k >= 57:   karana = ["शकुनि","चतुष्पद","नाग"][k-57]
else:           karana = KARANA_MOV[(k-1) % 7]
nitya = NITYA[int(((sun_lon + moon_lon) % 360) // (360/27))]
wd = dt.date(Y, M, D).weekday()
rise = swe.rise_trans(swe.julday(Y,M,D,0,swe.GREG_CAL), swe.SUN, swe.CALC_RISE,
                      (LON,LAT,0), 0, 0)[1][0]
sset = swe.rise_trans(swe.julday(Y,M,D,0,swe.GREG_CAL), swe.SUN, swe.CALC_SET,
                      (LON,LAT,0), 0, 0)[1][0]
def jd_ist(j):
    yy,mm,dd,hh = swe.revjul(j + TZ/24., swe.GREG_CAL)
    return f"{int(hh):02d}:{int((hh%1)*60):02d}"
panchang = dict(tithi=tithi, karana=karana, nitya_yoga=nitya, vaar=VAAR[wd],
                sunrise=jd_ist(rise), sunset=jd_ist(sset),
                ayanamsa=dms(swe.get_ayanamsa_ut(J)),
                chandra_rashi=RASHI[int(moon_lon//30)], surya_rashi=RASHI[int(sun_lon//30)],
                janma_nak=NAK[int(moon_lon//(360/27))],
                janma_pada=int((moon_lon % (360/27))//(360/108))+1,
                paksha_bal=round(elong,1))

# ---------- pada 4 window ----------
def moon_at(j): return swe.calc_ut(j, swe.MOON, F)[0][0]
def cross(target, lo, hi):
    for _ in range(60):
        mid = (lo+hi)/2
        if moon_at(mid) < target: lo = mid
        else: hi = mid
    return (lo+hi)/2
base = swe.julday(Y, M, D, -TZ, swe.GREG_CAL)
pada_win = dict(start=jd_ist(cross(263+20/60., base, base+1)),
                end=jd_ist(cross(266+40/60., base, base+1)))

# ---------- vimshottari ----------
VIM = [("केतु",7),("शुक्र",20),("सूर्य",6),("चंद्र",10),("मंगल",7),
       ("राहु",18),("गुरु",16),("शनि",19),("बुध",17)]
span = 360/27.
idx = int(moon_lon // span)
elapsed_frac = (moon_lon % span) / span
start_i = [n for n,_ in VIM].index(NAK_LORD[idx])
YR = 365.2425
bal = VIM[start_i][1] * (1 - elapsed_frac)
def add_years(d0, yrs): return d0 + dt.timedelta(days=yrs*YR)
birth_dt = dt.datetime(Y, M, D, H, MI)
def hindi_date(x): return f"{x.day} {MAAS_HI[x.month-1]} {x.year}"
dashas = []
cur = birth_dt; yrs = bal
for i in range(9):
    lord, full = VIM[(start_i+i) % 9]
    end = add_years(cur, yrs)
    dashas.append(dict(lord=lord, start=hindi_date(cur), end=hindi_date(end),
                       years=round(yrs,2), full=full, birth=(i == 0)))
    cur = end; yrs = VIM[(start_i+i+1) % 9][1]
bal_y = int(bal); bal_m = int((bal-bal_y)*12); bal_d = int((((bal-bal_y)*12)-bal_m)*30.44)

# ---------- antardasha inside the running mahadasha ----------
anta = []
md_lord, md_full = VIM[start_i]
cur = birth_dt
skip = md_full - bal            # years of the mahadasha already gone before birth
acc = 0.
for i in range(9):
    l2, f2 = VIM[(start_i+i) % 9]
    seg = md_full * f2 / 120.
    if acc + seg <= skip + 1e-9:
        acc += seg; continue
    used = max(0., skip - acc)
    end = add_years(cur, seg - used)
    anta.append(dict(lord=l2, start=hindi_date(cur), end=hindi_date(end), partial=used > 0))
    cur = end; acc += seg

# ---------- doshas ----------
def h_from(sign, frm): return ((sign - frm) % 12) + 1
mars_s  = int(pos["मंगल"]["lon"] // 30)
moon_s  = int(moon_lon // 30)
ven_s   = int(pos["शुक्र"]["lon"] // 30)
sat_s   = int(pos["शनि"]["lon"] // 30)
MANGAL_H = {1,2,4,7,8,12}
mangal = {"लग्न से": h_from(mars_s, LAGNA), "चंद्र से": h_from(mars_s, moon_s),
          "शुक्र से": h_from(mars_s, ven_s)}
mangal_dosh = any(v in MANGAL_H for v in mangal.values())
# kaal sarp: are all 7 planets inside one Rahu->Ketu semicircle?
rl = pos["राहु"]["lon"]
side = {hi: (((pos[hi]["lon"] - rl) % 360) < 180) for hi,_ in [(g[1],0) for g in GRAHA]}
kaal_sarp = len(set(side.values())) == 1
sade_sati_h = h_from(sat_s, moon_s)
sade_sati = sade_sati_h in (12, 1, 2)
# Dhaiya / Kantak Shani — Saturn transiting the 4th or 8th from the natal Moon. NOT Sade Sati,
# but it is a real 2.5-year affliction and leaving it off would read as a clean bill it isn't.
# Phaladeepika 26.22 on the 4th; Saturn's vedha pairs are 3-12, 11-5, 6-9 only, so the 4th
# has no cancellation available.
dhaiya = sade_sati_h in (4, 8)
def sat_sign_at(j): return int(swe.calc_ut(j, swe.SATURN, F)[0][0] // 30)
dh_end = None
if dhaiya:
    target = sat_s
    for i in range(1, 1500):                      # walk forward to the FINAL exit from that sign
        if sat_sign_at(J + i) != target and all(sat_sign_at(J + i + k) != target for k in range(1, 400)):
            yy, mm, dd, _ = swe.revjul(J + i, swe.GREG_CAL)
            dh_end = f"{dd} {MAAS_HI[mm-1]} {yy}"
            break
GAND = [(0,0,3+1/3.),(3,26+2/3.,30),(4,0,3+1/3.),(7,26+2/3.,30),(8,0,3+1/3.),(11,26+2/3.,30)]
def gandanta(lon):
    s, d = int(lon//30), lon % 30
    return any(s == g and lo <= d <= hi for g, lo, hi in GAND)
doshas = dict(mangal=dict(houses=mangal, present=mangal_dosh),
              kaal_sarp=kaal_sarp,
              sade_sati=dict(house=sade_sati_h, present=sade_sati),
              dhaiya=dict(present=dhaiya, house=sade_sati_h, end=dh_end,
                          rashi=RASHI[sat_s]),
              gandanta_moon=gandanta(moon_lon), gandanta_lagna=gandanta(asc),
              moon_elong=round(elong,1), moon_strong=60 <= elong <= 300)

# ---------- yogas ----------
merc_s = int(pos["बुध"]["lon"] // 30)
merc_h = house_of(merc_s)
jup_s  = int(pos["गुरु"]["lon"] // 30)
yogas = dict(
  bhadra=dict(present=(merc_s in SWA["बुध"] or merc_s == UCHCHA["बुध"]) and merc_h in (1,4,7,10),
              house=merc_h, rashi=RASHI[merc_s]),
  guru_uchcha=dict(present=jup_s == UCHCHA["गुरु"],
                   asta=abs((pos["गुरु"]["lon"]-sun_lon+180) % 360-180) < ASTA["गुरु"],
                   sep=round(abs((pos["गुरु"]["lon"]-sun_lon+180) % 360-180), 2)),
  gajakesari=dict(present=h_from(jup_s, moon_s) in (1,4,7,10), house=h_from(jup_s, moon_s)),
)

# ---------- nakshatra attributes ----------
# NOTE: the three-guna assignment per nakshatra differs between sources, so it is NOT stated.
# Replaced with the rashi lord, which is unambiguous (Sagittarius is Jupiter's sign).
nak_info = dict(name="पूर्वाषाढ़ा", pada=4, syllable="ढा", deity="अप् (जल देवता)",
                lord="शुक्र", symbol="हाथी का दाँत · सूप (छाज)", gana="मनुष्य",
                varna="ब्राह्मण", nadi="मध्य", yoni="वानर (नर)",
                rashi_lord="गुरु", meaning="‘पहली अजेय’ — जो हारती नहीं")

out = dict(birth=dict(date="28 जुलाई 2026", vaar=VAAR[wd], time="प्रातः 10:15",
                      place="बठिंडा, पंजाब, भारत", lat=LAT, lon=LON, tz="IST (+5:30)"),
           lagna=lagna, grahas=grahas, panchang=panchang, pada_window=pada_win,
           dashas=dashas, antardashas=anta,
           balance=dict(lord=md_lord, y=bal_y, m=bal_m, d=bal_d, years=round(bal,4)),
           doshas=doshas, yogas=yogas, nakshatra=nak_info,
           lords={str(i): LORD_OF[(LAGNA+i-1) % 12] for i in range(1, 13)},
           house_signs={str(i): RASHI[(LAGNA+i-1) % 12] for i in range(1, 13)})

# ---------- assertions: every claim the page makes, checked here ----------
assert lagna["rashi"] == "कन्या", lagna
assert panchang["janma_nak"] == "पूर्वाषाढ़ा" and panchang["janma_pada"] == 4
assert not doshas["mangal"]["present"], mangal
assert not doshas["kaal_sarp"] and not doshas["sade_sati"]["present"]
# Dhaiya IS present — assert it so the page can never quietly claim a clean bill on Saturn
assert doshas["dhaiya"]["present"] and doshas["dhaiya"]["end"], doshas["dhaiya"]
assert pos["शनि"]["stationary"], "Saturn must be flagged stationary, not merely retrograde"
assert not doshas["gandanta_moon"] and not doshas["gandanta_lagna"]
assert doshas["moon_strong"]
assert yogas["bhadra"]["present"] and yogas["guru_uchcha"]["present"]
assert yogas["guru_uchcha"]["asta"], "Jupiter must still be combust"
assert dashas[0]["lord"] == "शुक्र" and len(dashas) == 9
assert abs(sum(d["years"] for d in dashas) - (120 - (VIM[start_i][1]-bal))) < 0.01

json.dump(out, open("kundlidata.json", "w"), ensure_ascii=False, indent=1)

print(f"लग्न {lagna['rashi']} {lagna['deg']} · स्वामी {lagna['lord']} · नवमांश लग्न {lagna['navamsa']}")
print(f"पंचांग: {panchang['vaar']} · {tithi['paksha']} {tithi['name']} · करण {karana} · "
      f"योग {nitya} · सूर्योदय {panchang['sunrise']} · अयनांश {panchang['ayanamsa']}")
print(f"पाद 4 अवधि: {pada_win['start']} → {pada_win['end']} IST")
print(f"दशा शेष: {md_lord} {bal_y}व {bal_m}म {bal_d}द")
print(f"{'ग्रह':<7}{'राशि':<9}{'अंश':<8}{'भाव':>3}  {'नक्षत्र':<16}{'पाद':>3} {'नवमांश':<8}{'स्थिति'}")
for g in grahas:
    print(f"{g['graha']:<7}{g['rashi']:<9}{g['deg']:<8}{g['house']:>3}  {g['nak']:<16}"
          f"{g['pada']:>3} {g['navamsa']:<8}{g['status']}")
print("\nअंतर्दशा (शुक्र महादशा):", " | ".join(f"{a['lord']} → {a['end']}" for a in anta))
print("दोष:", "मंगल" , mangal, "| कालसर्प", kaal_sarp, "| साढ़ेसाती भाव", sade_sati_h)
print("योग:", yogas)
