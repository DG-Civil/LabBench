"""
LabBench - Clinical Lab Quick Reference (Streamlit edition)

Run locally:   streamlit run streamlit_app.py
Deploy:        Streamlit Community Cloud -> main file path: streamlit_app.py
"""
import pandas as pd
import streamlit as st

import calcs
from lab_data import (CRITICAL_CALL, EXPOSURE, ORDER_OF_DRAW, RANGES, REJECTION, SOURCES,
                      TESTS, TRANSFUSION_REACTION, TROUBLESHOOTING, TUBES, UNITS)

st.set_page_config(page_title="LabBench - Clinical Lab Reference", page_icon="🧪",
                   layout="centered", initial_sidebar_state="collapsed")

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown("""
<style>
/* Streamlit draws a fixed 3.75rem toolbar at the top; push content below it */
.block-container {padding-top: 4.75rem !important; padding-bottom: 3rem; max-width: 760px;}
@media (max-width: 640px) {
  .block-container {padding-top: 4.25rem !important; padding-left: 0.9rem; padding-right: 0.9rem;}
}
.lb-head {background:#0f4c5c;color:#fff;border-radius:14px;padding:14px 16px;margin-bottom:10px}
.lb-head b {font-size:1.25rem}
.lb-head span {opacity:.85;font-size:.85rem;display:block}
.lb-card {border:1px solid rgba(128,128,128,.25);border-radius:12px;padding:12px 14px;margin:6px 0}
.lb-dot {display:inline-block;width:14px;height:14px;border-radius:50%;
         border:1px solid rgba(0,0,0,.25);vertical-align:middle;margin-right:6px}
.lb-cap {display:inline-block;width:22px;height:30px;border-radius:6px 6px 3px 3px;
         border:1px solid rgba(0,0,0,.25);vertical-align:middle;margin-right:10px}
.lb-num {display:inline-block;width:26px;height:26px;border-radius:50%;background:#0f4c5c;color:#fff;
         text-align:center;line-height:26px;font-weight:700;margin-right:8px;font-size:.85rem}
.lb-small {font-size:.85rem;opacity:.8}
.lb-crit {color:#b42318;font-weight:600}
</style>
""", unsafe_allow_html=True)

PAGES = {
    "home": "🏠 Home",
    "tubes": "🧪 Order of Draw & Tubes",
    "tests": "🔎 Test Lookup",
    "ranges": "📈 Ranges & Critical Values",
    "calc": "🧮 Calculators",
    "qc": "📊 QC / Westgard",
    "bb": "🩸 Blood Bank",
    "trouble": "⚠️ Troubleshooting",
    "reject": "🚫 Specimen Rejection",
    "critical": "🔔 Critical Value Call",
    "safety": "🛡️ Safety",
    "about": "📚 Sources & About",
}
KEYS = list(PAGES)


# ---------------------------------------------------------------------------
# Navigation (synced with ?page= in the URL so pages can be bookmarked)
# ---------------------------------------------------------------------------
def _init_nav():
    qp = st.query_params.get("page", "home")
    if "nav" not in st.session_state:
        st.session_state.nav = qp if qp in PAGES else "home"


def _sync_nav():
    st.query_params["page"] = st.session_state.nav
    st.session_state.q = ""


def goto(key):
    st.session_state.nav = key
    st.query_params["page"] = key
    st.session_state.q = ""


_init_nav()
if "q" not in st.session_state:
    st.session_state.q = ""

st.markdown('<div class="lb-head"><b>🧪 LabBench</b><span>Clinical Lab Quick Reference · adult values, US units</span></div>',
            unsafe_allow_html=True)
st.selectbox("Section", KEYS, format_func=lambda k: PAGES[k], key="nav", on_change=_sync_nav,
             label_visibility="collapsed")
st.text_input("Search", key="q", placeholder="Search tests, tubes, ranges, calculators…",
              label_visibility="collapsed")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def dot(tid):
    t = TUBES[tid]
    return f'<span class="lb-dot" style="background:{t["color"]}"></span>'


def cap(tid):
    t = TUBES[tid]
    return f'<span class="lb-cap" style="background:{t["color"]}"></span>'


def tube_names(tids):
    return " or ".join(TUBES[t]["name"] for t in tids)


def show_test(t, expanded=False):
    name, _kw, dept, tids, note = t
    with st.expander(f"{name}  ·  {tube_names(tids)}", expanded=expanded):
        st.caption(dept)
        for i, tid in enumerate(tids):
            tb = TUBES[tid]
            st.markdown(f'{cap(tid)}<b>{"or " if i else ""}{tb["name"]}</b> — {tb["additive"]} · '
                        f'invert {tb["inversions"]}', unsafe_allow_html=True)
        if note:
            st.info(note)


def parse_float(s):
    try:
        return float(str(s).strip())
    except (TypeError, ValueError):
        return None


def src_name(key):
    return SOURCES[key][0] if key else "—"


def ranges_df(rows):
    return pd.DataFrame([{
        "Test": r["name"],
        "Reference": calcs.ref_text(r),
        "Critical": calcs.crit_text(r),
        "Units": r["unit"],
        "Department": r["dept"],
    } for r in rows])


def show_flag(r, v):
    res = calcs.classify(r, v)
    if not res:
        return
    label, level = res
    msg = f"**{label}** — {r['name']} {v:g} {r['unit']} (reference {calcs.ref_text(r)}; critical {calcs.crit_text(r)})"
    if level == "crit":
        st.error(msg + "  \nFollow the critical value call procedure.")
    elif level == "abn":
        st.warning(msg)
    else:
        st.success(msg)


DISCLAIMER = ("Typical adult reference values (ABIM, Jan 2026) and critical limits (Michigan Medicine "
              "Laboratories). Always follow **your hospital laboratory's** validated ranges and policies.")


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------
def page_search(q):
    s = q.lower().strip()
    tests = [t for t in TESTS if s in (t[0] + " " + t[1] + " " + t[2]).lower()]
    rngs = [r for r in RANGES if s in r["name"].lower() or s == r["id"]]
    tubes = [k for k, t in TUBES.items() if s in (t["name"] + " " + t["additive"] + " " + t["uses"]).lower()]
    if not (tests or rngs or tubes):
        st.write(f"No matches for “{q}”.")
        return
    if tests:
        st.subheader("Tests")
        for t in tests:
            show_test(t, expanded=len(tests) == 1)
    if rngs:
        st.subheader("Ranges")
        st.dataframe(ranges_df(rngs), hide_index=True)
    if tubes:
        st.subheader("Tubes")
        for k in tubes:
            t = TUBES[k]
            st.markdown(f'{cap(k)}<b>{t["name"]}</b> — {t["additive"]} · invert {t["inversions"]}<br>'
                        f'<span class="lb-small">{t["uses"]}. {t["note"]}</span>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def page_home():
    tiles = [("tubes", "Order of draw, additives, inversions"),
             ("tests", f"Tube & handling for {len(TESTS)} tests"),
             ("ranges", "Reference & critical values, flag a result"),
             ("calc", "eGFR, anion gap, dilutions, RCF, more"),
             ("qc", "Westgard rules + Levey-Jennings chart"),
             ("bb", "ABO/Rh compatibility, reactions"),
             ("trouble", "Pre-analytical errors"),
             ("critical", "Read-back checklist"),
             ("safety", "Needlestick, spills")]
    for i in range(0, len(tiles), 2):
        cols = st.columns(2)
        for col, (k, d) in zip(cols, tiles[i:i + 2]):
            with col:
                st.button(PAGES[k], key=f"tile_{k}", on_click=goto, args=(k,))
                st.caption(d)

    st.divider()
    st.subheader("Quick value check")
    names = {r["id"]: f'{r["name"]} ({r["unit"]})' if r["unit"] else r["name"] for r in RANGES}
    c1, c2 = st.columns([3, 2])
    rid = c1.selectbox("Analyte", list(names), format_func=names.get, key="home_rid")
    v = parse_float(c2.text_input("Result", key="home_val", placeholder="value"))
    if v is not None:
        show_flag(next(r for r in RANGES if r["id"] == rid), v)
    st.caption(DISCLAIMER)


def page_tubes():
    st.header("Order of Draw")
    st.caption("CLSI GP41 sequence - same for tube holder, butterfly and syringe transfer.")
    for i, k in enumerate(ORDER_OF_DRAW, 1):
        t = TUBES[k]
        st.markdown(f'<div class="lb-card"><span class="lb-num">{i}</span>{cap(k)}<b>{t["name"]}</b><br>'
                    f'<span class="lb-small">{t["additive"]} · <b>invert {t["inversions"]}</b><br>'
                    f'{t["uses"]}<br>{t["note"]}</span></div>', unsafe_allow_html=True)
    st.success("Memory aid: **S**top **L**ight **R**ed, **S**tay **P**ut, **G**reen **L**ight **G**o — "
               "Sterile cultures, Light blue, Red, SST, PST, Green, Lavender, Gray.")
    st.subheader("Other tubes & containers")
    for k, t in TUBES.items():
        if k in ORDER_OF_DRAW:
            continue
        st.markdown(f'<div class="lb-card">{cap(k)}<b>{t["name"]}</b><br><span class="lb-small">'
                    f'{t["additive"]} · invert {t["inversions"]}<br>{t["uses"]}. {t["note"]}</span></div>',
                    unsafe_allow_html=True)
    st.subheader("Key timings")
    st.markdown("""
- SST / gold: clot **30 min** upright before spinning; plain red: **30–60 min**.
- Spin serum/plasma within **2 h** of collection.
- Tourniquet on **1 minute** or less.
- Invert gently — never shake (hemolysis).
""")


def page_tests():
    st.header("Test Lookup")
    depts = ["All"] + sorted({t[2] for t in TESTS})
    dept = st.selectbox("Department", depts, key="test_dept")
    pool = [t for t in TESTS if dept == "All" or t[2] == dept]
    names = [t[0] for t in pool]
    pick = st.selectbox("Test (type to filter)", names, key="test_pick")
    show_test(next(t for t in pool if t[0] == pick), expanded=True)
    st.subheader("All tests" if dept == "All" else f"All {dept} tests")
    st.markdown("".join(
        f'<div class="lb-card">{"".join(dot(x) for x in t[3])}<b>{t[0]}</b><br>'
        f'<span class="lb-small">{tube_names(t[3])}{" — " + t[4] if t[4] else ""}</span></div>'
        for t in pool), unsafe_allow_html=True)
    st.caption("Confirm specimen requirements in your hospital laboratory's test directory.")


def page_ranges():
    st.header("Ranges & Critical Values")
    st.warning(DISCLAIMER)
    depts = ["All"] + list(dict.fromkeys(r["dept"] for r in RANGES))
    dept = st.radio("Department", depts, horizontal=True, key="rng_dept")
    rows = [r for r in RANGES if dept == "All" or r["dept"] == dept]

    st.subheader("Check a result")
    names = {r["id"]: f'{r["name"]} ({r["unit"]})' if r["unit"] else r["name"] for r in rows}
    c1, c2 = st.columns([3, 2])
    rid = c1.selectbox("Analyte", list(names), format_func=names.get, key="rng_rid")
    v = parse_float(c2.text_input("Result", key="rng_val", placeholder="value"))
    r = next(x for x in rows if x["id"] == rid)
    if v is not None:
        show_flag(r, v)
    with st.container(border=True):
        a, b = st.columns(2)
        a.metric("Reference", calcs.ref_text(r), help=r["unit"] or None)
        b.metric("Critical", calcs.crit_text(r))
        if r["note"]:
            st.caption(r["note"])
        st.caption(f"Reference source: {src_name(r['ref'])} · Critical source: {src_name(r['crit'])}")

    st.subheader("Full table")
    df = ranges_df(rows)
    st.dataframe(df, hide_index=True)
    full = pd.DataFrame([{**{k: r[k] for k in ("id", "name", "dept", "unit", "lo", "hi", "clo", "chi")},
                          "reference_source": src_name(r["ref"]), "critical_source": src_name(r["crit"]),
                          "note": r["note"]} for r in RANGES])
    st.download_button("⬇️ Download all ranges (CSV) for supervisor review",
                       full.to_csv(index=False).encode("utf-8"), "labbench_ranges.csv", "text/csv")


def num(label, value, key, step=None, fmt=None):
    kw = {}
    if step is not None:
        kw["step"] = float(step)
    if fmt:
        kw["format"] = fmt
    return st.number_input(label, value=float(value), key=key, **kw)


def page_calc():
    st.header("Calculators")
    options = ["Unit converter", "eGFR (CKD-EPI 2021)", "Corrected calcium", "Anion gap",
               "Calculated osmolality & gap", "LDL (Friedewald & NIH/Sampson)", "A1c → eAG / IFCC",
               "Centrifuge RPM ↔ RCF", "Dilution (C1V1 = C2V2)", "Dilution factor result",
               "Absolute count / ANC", "WBC corrected for nRBC", "Corrected retic & RPI", "RBC indices",
               "Manual cell count (hemacytometer)", "INR from PT", "Citrate adjustment (Hct > 55%)"]
    c = st.selectbox("Calculator", options, key="calc_pick")
    box = st.container(border=True)
    with box:
        if c == "Unit converter":
            idx = st.selectbox("Analyte", range(len(UNITS)), format_func=lambda i: UNITS[i][0], key="u_a")
            name, cu, su, f = UNITS[idx]
            direction = st.radio("Direction", [f"{cu} → {su}", f"{su} → {cu}"], horizontal=True, key="u_dir")
            v = num("Value", 100, "u_v")
            if direction.startswith(cu):
                st.metric("Result", f"{v * f:.3g} {su}")
            else:
                st.metric("Result", f"{v / f:.3g} {cu}")
            st.caption(f"{cu} × {f} = {su}")

        elif c.startswith("eGFR"):
            a, b = st.columns(2)
            cr = a.number_input("Creatinine (mg/dL)", value=1.0, min_value=0.1, step=0.1, key="e_cr")
            age = b.number_input("Age (years)", value=50.0, min_value=18.0, step=1.0, key="e_age")
            sex = st.radio("Sex", ["Female", "Male"], horizontal=True, key="e_sex")
            e = calcs.egfr_ckd_epi_2021(cr, age, sex == "Female")
            st.metric("eGFR", f"{e:.0f} mL/min/1.73 m²")
            st.write(f"CKD stage **{calcs.ckd_stage(e)}**")
            st.caption("CKD-EPI 2021 (race-free), adults 18+ with stable creatinine.")

        elif c == "Corrected calcium":
            a, b = st.columns(2)
            ca = a.number_input("Total calcium (mg/dL)", value=8.0, step=0.1, key="c_ca")
            al = b.number_input("Albumin (g/dL)", value=2.5, step=0.1, key="c_al")
            st.metric("Corrected calcium", f"{calcs.corrected_calcium(ca, al):.1f} mg/dL")
            st.caption("Ca + 0.8 × (4.0 − albumin). Ionized calcium is more accurate when available.")

        elif c == "Anion gap":
            a, b, d = st.columns(3)
            na = a.number_input("Na", value=140.0, key="a_na")
            cl = b.number_input("Cl", value=104.0, key="a_cl")
            hc = d.number_input("HCO3", value=24.0, key="a_hc")
            ag = calcs.anion_gap(na, cl, hc)
            st.metric("Anion gap", f"{ag:.1f} mmol/L")
            al = parse_float(st.text_input("Albumin g/dL (optional, for albumin correction)", key="a_al"))
            if al is not None:
                st.write(f"Albumin-corrected AG: **{calcs.albumin_corrected_ag(ag, al):.1f}**")
            st.caption("Reference interval depends on your analyzer.")

        elif c.startswith("Calculated osmolality"):
            a, b, d = st.columns(3)
            na = a.number_input("Na (mmol/L)", value=140.0, key="o_na")
            gl = b.number_input("Glucose (mg/dL)", value=100.0, key="o_gl")
            bun = d.number_input("BUN (mg/dL)", value=14.0, key="o_bun")
            et = parse_float(st.text_input("Ethanol mg/dL (optional)", key="o_et"))
            ms = parse_float(st.text_input("Measured osmolality (optional)", key="o_ms"))
            osm = calcs.calc_osmolality(na, gl, bun, et)
            st.metric("Calculated osmolality", f"{osm:.0f} mOsm/kg")
            if ms is not None:
                gap = ms - osm
                (st.warning if gap > 10 else st.success)(f"Osmolal gap: **{gap:.0f}**" +
                                                         (" — elevated (>10)" if gap > 10 else ""))
            st.caption("2 × Na + glucose/18 + BUN/2.8 (+ ethanol/3.7)")

        elif c.startswith("LDL"):
            a, b, d = st.columns(3)
            tc = a.number_input("Total chol", value=200.0, key="l_tc")
            hdl = b.number_input("HDL", value=50.0, key="l_hdl")
            tg = d.number_input("TG", value=150.0, key="l_tg")
            s = calcs.ldl_sampson(tc, hdl, tg)
            fr = calcs.ldl_friedewald(tc, hdl, tg)
            x, y = st.columns(2)
            x.metric("NIH / Sampson", f"{s:.0f} mg/dL", help="Valid for TG up to 800 mg/dL")
            y.metric("Friedewald", "N/A (TG > 400)" if fr is None else f"{fr:.0f} mg/dL")
            st.write(f"Non-HDL cholesterol: **{tc - hdl:.0f} mg/dL**")

        elif c.startswith("A1c"):
            a1c = st.number_input("HbA1c (%)", value=7.0, step=0.1, key="h_a")
            eag = calcs.a1c_to_eag(a1c)
            x, y = st.columns(2)
            x.metric("eAG", f"{eag:.0f} mg/dL")
            y.metric("IFCC", f"{calcs.a1c_to_ifcc(a1c):.0f} mmol/mol")
            st.write("Normal" if a1c < 5.7 else "Prediabetes range" if a1c < 6.5 else "Diabetes range")

        elif c.startswith("Centrifuge"):
            rad = st.number_input("Rotor radius (cm, center to tube bottom)", value=15.0, min_value=1.0, key="r_rad")
            mode = st.radio("Convert", ["RPM → RCF", "RCF → RPM"], horizontal=True, key="r_mode")
            if mode == "RPM → RCF":
                rpm = st.number_input("RPM", value=3000.0, step=100.0, key="r_rpm")
                st.metric("RCF", f"{calcs.rpm_to_rcf(rpm, rad):,.0f} × g")
            else:
                g = st.number_input("RCF (× g)", value=1300.0, step=50.0, key="r_g")
                st.metric("RPM", f"{calcs.rcf_to_rpm(g, rad):,.0f}")
            st.caption("RCF = 1.118 × 10⁻⁵ × r × RPM². BD gel tubes: 1000–1300 × g for 10 min (swing-bucket).")

        elif c.startswith("Dilution (C1V1"):
            solve = st.radio("Solve for", ["C1", "V1", "C2", "V2"], horizontal=True, index=3, key="d_s")
            vals = {}
            cols = st.columns(3)
            i = 0
            for k, default in (("C1", 10.0), ("V1", 1.0), ("C2", 2.0), ("V2", 5.0)):
                if k == solve:
                    continue
                vals[k] = cols[i].number_input(k, value=default, key=f"d_{k}")
                i += 1
            try:
                name, res = calcs.solve_c1v1(vals.get("C1"), vals.get("V1"), vals.get("C2"), vals.get("V2"))
                st.metric(name, f"{res:.4g}")
            except ZeroDivisionError:
                st.error("Values cannot be zero.")

        elif c == "Dilution factor result":
            a, b = st.columns(2)
            s = a.number_input("Sample volume", value=1.0, min_value=0.001, key="f_s")
            d = b.number_input("Diluent volume", value=9.0, min_value=0.0, key="f_d")
            df_ = calcs.dilution_factor(s, d)
            st.metric("Dilution factor", f"1:{df_:g}")
            r = parse_float(st.text_input("Result measured on diluted sample (optional)", key="f_r"))
            if r is not None:
                st.metric("Reportable result", f"{r * df_:.4g}")

        elif c.startswith("Absolute count"):
            a, b = st.columns(2)
            w = a.number_input("WBC (×10³/µL)", value=8.0, key="b_w")
            p = b.number_input("Cell % (e.g., segs + bands)", value=60.0, key="b_p")
            v = calcs.absolute_count(w, p)
            st.metric("Absolute count", f"{v:.2f} ×10³/µL")
            if v < 0.5:
                st.error("If neutrophils: ANC < 0.5 — critical (MLabs outpatient).")

        elif c.startswith("WBC corrected"):
            a, b = st.columns(2)
            w = a.number_input("Uncorrected WBC (×10³/µL)", value=12.0, key="n_w")
            n = b.number_input("nRBC per 100 WBC", value=20.0, key="n_n")
            st.metric("Corrected WBC", f"{calcs.wbc_corrected_nrbc(w, n):.2f} ×10³/µL")

        elif c.startswith("Corrected retic"):
            a, b = st.columns(2)
            r = a.number_input("Retic (%)", value=3.0, key="t_r")
            h = b.number_input("Hematocrit (%)", value=25.0, key="t_h")
            cr, mf, rpi = calcs.retic_index(r, h)
            x, y = st.columns(2)
            x.metric("Corrected retic", f"{cr:.2f} %")
            y.metric("RPI", f"{rpi:.2f}", help=f"Maturation factor {mf}")
            st.write("Adequate marrow response" if rpi >= 2 else "Inadequate response (hypoproliferative)")

        elif c == "RBC indices":
            a, b, d = st.columns(3)
            hgb = a.number_input("Hgb (g/dL)", value=14.0, key="i_h")
            hct = b.number_input("Hct (%)", value=42.0, min_value=1.0, key="i_t")
            rbc = d.number_input("RBC (×10⁶/µL)", value=4.7, min_value=0.1, key="i_r")
            mcv, mch, mchc = calcs.rbc_indices(hgb, hct, rbc)
            x, y, z = st.columns(3)
            x.metric("MCV", f"{mcv:.1f} fL")
            y.metric("MCH", f"{mch:.1f} pg")
            z.metric("MCHC", f"{mchc:.1f} g/dL")
            st.caption(f"Rule of three: Hgb × 3 ≈ Hct ({hgb * 3:.0f} vs {hct:.0f})")

        elif c.startswith("Manual cell count"):
            a, b, d = st.columns(3)
            n = a.number_input("Cells counted", value=150.0, key="m_c")
            sq = b.number_input("Large squares", value=4.0, min_value=1.0, key="m_sq")
            dil = d.number_input("Dilution factor", value=20.0, min_value=1.0, key="m_d")
            v = calcs.manual_cell_count(n, sq, dil)
            st.metric("Count", f"{v:,.0f} cells/µL")
            st.caption("Neubauer: each large square = 0.1 µL.")

        elif c == "INR from PT":
            a, b, d = st.columns(3)
            pt = a.number_input("Patient PT (s)", value=25.0, key="p_pt")
            mn = b.number_input("Mean normal PT (s)", value=12.0, min_value=0.1, key="p_mn")
            isi = d.number_input("ISI", value=1.0, step=0.01, key="p_isi")
            st.metric("INR", f"{calcs.inr(pt, mn, isi):.2f}")

        elif c.startswith("Citrate"):
            a, b = st.columns(2)
            h = a.number_input("Hematocrit (%)", value=60.0, key="z_h")
            vb = b.number_input("Blood volume (mL)", value=2.7, step=0.1, key="z_v")
            st.metric("Citrate volume", f"{calcs.citrate_volume(h, vb):.2f} mL")
            st.caption("CLSI H21: C = 0.00185 × (100 − Hct) × V. Needed only when Hct > 55%.")


def page_qc():
    st.header("QC / Westgard checker")
    a, b = st.columns(2)
    mean = a.number_input("Target mean", value=100.0, key="q_m")
    sd = b.number_input("Target SD", value=2.0, min_value=0.0001, key="q_s")
    raw = st.text_area("Control results, oldest → newest (comma or space separated)",
                       "99, 101, 100.5, 102, 98, 103, 104.5, 105", key="q_v")
    vals = [parse_float(x) for x in raw.replace(",", " ").split()]
    vals = [v for v in vals if v is not None]
    if not vals:
        st.info("Enter at least one control value.")
        return
    res = calcs.westgard(vals, mean, sd)
    if res["status"] == "reject":
        st.error("**REJECT RUN**  \n" + "  \n".join(f"**{r}**: {d}" for r, d in res["rules"]))
    elif res["status"] == "warning":
        st.warning("**1-2s WARNING** — inspect with the other rules before accepting.")
    else:
        st.success("**ACCEPT** — no Westgard rule violated.")
    n = len(vals)
    chart = pd.DataFrame({"Result (z)": res["z"], "+3 SD": [3] * n, "+2 SD": [2] * n, "Mean": [0] * n,
                          "-2 SD": [-2] * n, "-3 SD": [-3] * n}, index=range(1, n + 1))
    st.line_chart(chart, color=["#127a8a", "#b42318", "#d4a017", "#7f8c8d", "#d4a017", "#b42318"], height=280)
    x, y, z, w = st.columns(4)
    x.metric("Latest z", f"{res['z'][-1]:.2f}")
    y.metric("Obs. mean", f"{res['mean']:.2f}")
    z.metric("Obs. SD", f"{res['sd']:.2f}")
    w.metric("CV", f"{res['cv']:.1f}%" if res["cv"] is not None else "—")
    st.caption("Single-level evaluation across runs. Apply your lab's QC policy and multi-level rules "
               "before reporting patient results.")


def page_bb():
    st.header("Blood Bank")
    groups = ["O", "A", "B", "AB"]
    rbc = {"O": ["O"], "A": ["A", "O"], "B": ["B", "O"], "AB": ["AB", "A", "B", "O"]}
    pla = {"O": ["O", "A", "B", "AB"], "A": ["A", "AB"], "B": ["B", "AB"], "AB": ["AB"]}

    def table(m):
        return pd.DataFrame({f"Donor {d}": ["✅" if d in m[p] else "—" for p in groups] for d in groups},
                            index=[f"Patient {p}" for p in groups])

    st.subheader("Red cells")
    st.table(table(rbc))
    st.subheader("Plasma")
    st.table(table(pla))
    st.markdown("""
- **Universal red cell donor:** O negative. **Universal plasma donor:** AB.
- Rh-negative patients receive Rh-negative red cells (especially females of childbearing potential).
- Platelets: ABO-compatible preferred — follow blood bank policy.
""")
    st.subheader("Suspected transfusion reaction")
    for i, s in enumerate(TRANSFUSION_REACTION, 1):
        st.markdown(f"**{i}.** {s}")
    st.subheader("Labeling — zero tolerance")
    st.markdown("""
- Label at the bedside, in the patient's presence.
- Full name + MRN or DOB exactly matching the armband.
- Date, time and collector's ID.
- Any mismatch or missing item → reject and recollect.
""")


def page_trouble():
    st.header("Troubleshooting")
    for name, effect, fix in TROUBLESHOOTING:
        with st.expander(name):
            st.markdown(f"**Effect:** {effect}  \n**Prevent / fix:** {fix}")


def page_reject():
    st.header("Specimen Rejection")
    st.markdown("\n".join(f"- {r}" for r in REJECTION))
    st.subheader("When rejecting")
    st.markdown("""
- Notify the unit/provider promptly and request recollection.
- Document the reason, who was notified and when.
- Never relabel a specimen collected by someone else.
- Irreplaceable specimens (CSF, tissue, body fluids): follow the exception policy with supervisor approval.
""")


def page_critical():
    st.header("Critical Value Call")
    for i, s in enumerate(CRITICAL_CALL, 1):
        st.markdown(f"**{i}.** {s}")
    st.info("Critical limits in this app come from the Michigan Medicine Laboratories policy. "
            "Use your hospital's own critical value list.")
    st.button("Open Ranges & Critical Values", on_click=goto, args=("ranges",))


def page_safety():
    st.header("Safety")
    st.subheader("Needlestick or blood exposure")
    for i, s in enumerate(EXPOSURE, 1):
        st.markdown(f"**{i}.** {s}")
    st.subheader("Blood or body-fluid spill")
    st.markdown("""
- Gloves (plus gown/eye protection if splashing).
- Absorb with paper towels; pick up glass with forceps or a scoop — never hands.
- Disinfect with an EPA-registered disinfectant or freshly made 1:10 bleach; observe the label contact time.
- Discard as biohazard waste; wash hands.
""")
    st.subheader("Everyday")
    st.markdown("""
- Activate the needle safety device immediately; never recap by hand.
- Sharps container no more than ¾ full.
- Balance the centrifuge; keep the lid closed until it stops completely.
- Hand hygiene before and after every patient and glove change.
""")


def page_about():
    st.header("Sources & About")
    st.markdown("All ranges are **adult values in US conventional units**. Sources:")
    for key, (name, url) in SOURCES.items():
        st.markdown(f"- [{name}]({url})")
    st.markdown("""
**Important**
- Every US hospital laboratory must establish or verify its own reference ranges (CAP/CLIA).
  The values here are typical published values, not your hospital's.
- To use your hospital's values, edit `lab_data.py` in the GitHub repository; the app redeploys automatically.
- This app stores no patient information. It is a quick reference, not a substitute for laboratory procedures.
""")


ROUTES = {"home": page_home, "tubes": page_tubes, "tests": page_tests, "ranges": page_ranges, "calc": page_calc,
          "qc": page_qc, "bb": page_bb, "trouble": page_trouble, "reject": page_reject,
          "critical": page_critical, "safety": page_safety, "about": page_about}

if st.session_state.q.strip():
    page_search(st.session_state.q)
else:
    ROUTES[st.session_state.nav]()

st.divider()
st.caption("LabBench · quick reference for laboratory professionals · verify against your laboratory's policies.")
