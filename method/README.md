# How every number on the page was produced

Nothing here is quoted from a website; all of it is computed.

| script | what it produces |
|---|---|
| `chart.py` | Sidereal positions of all nine grahas + the lagna (Swiss Ephemeris, Lahiri ayanamsa). This is where **Moon → Purva Ashadha pada 4** comes from. |
| `sensitivity.py` | Re-runs the Moon against **7 different ayanamsas**. Every one used in Indian practice returns the same pada — that is the robustness claim on the page. |
| `panchang.py` | Tithi, nitya yoga, Vimshottari dasha balance, and the exact clock window during which pada 4 was running (06:32–13:11 IST). |
| `namkaran.py` | Screens three weeks of dates for Namkaran against tithi, nakshatra and weekday rules. This is what flagged the traditional 11th and 12th days as compromised. |
| `score.py` | Chaldean letter values + Cheiro's compound table 10–52, and the gate: fortunate compound **and** a root friendly to both Moolank 1 and Bhagyank 9. Run it directly to print the seven permitted totals. |

```
python3 chart.py && python3 sensitivity.py && python3 score.py
```

Requires `pyswisseph`.
