"""
LabBench - calculator and rule functions (pure Python, no Streamlit).
"""
import math


def classify(r, v):
    """Return (label, level) for value v against range dict r.
    level: 'crit', 'abn', 'ok'."""
    if v is None:
        return None
    if r["clo"] is not None and v < r["clo"]:
        return ("CRITICAL LOW", "crit")
    if r["chi"] is not None and v > r["chi"]:
        return ("CRITICAL HIGH", "crit")
    if r["lo"] is not None and v < r["lo"]:
        return ("LOW", "abn")
    if r["hi"] is not None and v > r["hi"]:
        return ("HIGH", "abn")
    return ("WITHIN REFERENCE", "ok")


def ref_text(r):
    if r.get("disp"):
        return r["disp"]
    lo, hi = r["lo"], r["hi"]
    if lo is not None and hi is not None:
        return f"{lo:g} - {hi:g}"
    if lo is not None:
        return f">= {lo:g}"
    if hi is not None:
        return f"<= {hi:g}"
    return "-"


def crit_text(r):
    parts = []
    if r["clo"] is not None:
        parts.append(f"< {r['clo']:g}")
    if r["chi"] is not None:
        parts.append(f"> {r['chi']:g}")
    return "  or  ".join(parts) if parts else "None listed"


# ---------------- Chemistry ----------------
def egfr_ckd_epi_2021(scr, age, female):
    """CKD-EPI 2021 race-free creatinine equation. mL/min/1.73 m2."""
    k = 0.7 if female else 0.9
    a = -0.241 if female else -0.302
    e = 142 * min(scr / k, 1) ** a * max(scr / k, 1) ** -1.200 * 0.9938 ** age
    return e * (1.012 if female else 1.0)


def ckd_stage(e):
    if e >= 90:
        return "G1 - normal or high"
    if e >= 60:
        return "G2 - mildly decreased"
    if e >= 45:
        return "G3a - mildly to moderately decreased"
    if e >= 30:
        return "G3b - moderately to severely decreased"
    if e >= 15:
        return "G4 - severely decreased"
    return "G5 - kidney failure"


def corrected_calcium(ca, albumin):
    return ca + 0.8 * (4.0 - albumin)


def anion_gap(na, cl, hco3, k=None):
    ag = na - (cl + hco3)
    return ag if k is None else ag + k


def albumin_corrected_ag(ag, albumin):
    return ag + 2.5 * (4.0 - albumin)


def calc_osmolality(na, glucose, bun, ethanol=None):
    osm = 2 * na + glucose / 18 + bun / 2.8
    if ethanol:
        osm += ethanol / 3.7
    return osm


def ldl_friedewald(tc, hdl, tg):
    if tg > 400:
        return None
    return tc - hdl - tg / 5


def ldl_sampson(tc, hdl, tg):
    """NIH (Sampson) equation, valid TG up to 800 mg/dL."""
    non_hdl = tc - hdl
    return tc / 0.948 - hdl / 0.971 - (tg / 8.56 + tg * non_hdl / 2140 - tg * tg / 16100) - 9.44


def a1c_to_eag(a1c):
    return 28.7 * a1c - 46.7


def a1c_to_ifcc(a1c):
    return (a1c - 2.15) * 10.929


# ---------------- Hematology ----------------
def absolute_count(wbc, percent):
    return wbc * percent / 100


def wbc_corrected_nrbc(wbc, nrbc):
    return wbc * 100 / (100 + nrbc)


def retic_index(retic, hct):
    corrected = retic * hct / 45
    if hct >= 40:
        mf = 1.0
    elif hct >= 30:
        mf = 1.5
    elif hct >= 20:
        mf = 2.0
    else:
        mf = 2.5
    return corrected, mf, corrected / mf


def rbc_indices(hgb, hct, rbc):
    return hct * 10 / rbc, hgb * 10 / rbc, hgb * 100 / hct  # MCV, MCH, MCHC


def manual_cell_count(cells, squares, dilution):
    """Neubauer: each large square = 0.1 uL."""
    return cells * dilution / (squares * 0.1)


# ---------------- Coagulation ----------------
def inr(pt, mnpt, isi):
    return (pt / mnpt) ** isi


def citrate_volume(hct, blood_ml):
    """CLSI H21: C (mL) = 0.00185 x (100 - Hct) x V(blood mL)."""
    return 0.00185 * (100 - hct) * blood_ml


# ---------------- General lab ----------------
def rpm_to_rcf(rpm, radius_cm):
    return 1.118e-5 * radius_cm * rpm ** 2


def rcf_to_rpm(rcf, radius_cm):
    return math.sqrt(rcf / (1.118e-5 * radius_cm))


def dilution_factor(sample, diluent):
    return (sample + diluent) / sample


def solve_c1v1(c1=None, v1=None, c2=None, v2=None):
    """Exactly one argument must be None; returns (name, value)."""
    if c1 is None:
        return "C1", c2 * v2 / v1
    if v1 is None:
        return "V1", c2 * v2 / c1
    if c2 is None:
        return "C2", c1 * v1 / v2
    return "V2", c1 * v1 / c2


# ---------------- QC / Westgard ----------------
def westgard(values, mean, sd):
    """Single-level Westgard evaluation on the most recent result.
    Returns dict with z-scores, violated rules, status, observed stats."""
    z = [(v - mean) / sd for v in values]
    n = len(z)
    rules = []
    last = z[-1]
    if abs(last) > 3:
        rules.append(("1-3s", "Latest result beyond +/-3 SD (random error)"))
    if n >= 2 and (all(x > 2 for x in z[-2:]) or all(x < -2 for x in z[-2:])):
        rules.append(("2-2s", "Two consecutive results beyond the same 2 SD limit (systematic error)"))
    if n >= 2:
        a, b = z[-2], z[-1]
        if (a > 2 and b < -2) or (a < -2 and b > 2):
            rules.append(("R-4s", "Consecutive results span more than 4 SD (random error; classically within a run)"))
    if n >= 4 and (all(x > 1 for x in z[-4:]) or all(x < -1 for x in z[-4:])):
        rules.append(("4-1s", "Four consecutive results beyond the same 1 SD limit (systematic error)"))
    if n >= 10 and (all(x > 0 for x in z[-10:]) or all(x < 0 for x in z[-10:])):
        rules.append(("10x", "Ten consecutive results on the same side of the mean (shift)"))
    if rules:
        status = "reject"
    elif abs(last) > 2:
        status = "warning"
    else:
        status = "accept"
    obs_mean = sum(values) / n
    obs_sd = math.sqrt(sum((v - obs_mean) ** 2 for v in values) / (n - 1)) if n > 1 else 0.0
    cv = obs_sd / obs_mean * 100 if obs_mean else None
    return dict(z=z, rules=rules, status=status, mean=obs_mean, sd=obs_sd, cv=cv)
