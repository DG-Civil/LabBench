"""
LabBench - reference data.

All values are ADULT values in US conventional units.

SOURCES
  REF  = ABIM Laboratory Test Reference Ranges, revised January 2026
         https://www.abim.org/Media/bfijryql/laboratory-reference-ranges.pdf
  CRIT = Michigan Medicine Laboratories (MLabs) Critical Value Policy, 2024-04-26
         https://mlabs.umich.edu/media/630
  MERCK = Merck Manual Professional, Laboratory Reference Ranges -
          Therapeutic Drug Monitoring table (reviewed May 2026)
  MAYO  = Mayo Clinic Laboratories test catalog (Lithium, Serum - LITH)
  MEDLINE = MedlinePlus (NIH/NLM) - Prothrombin time (PT/INR)
  BD    = BD Vacutainer tube guide / CLSI GP41 order of draw

HOW TO CUSTOMIZE FOR YOUR HOSPITAL
  Edit the numbers in RANGES below (lo, hi, clo, chi) and commit the file
  to GitHub. Streamlit Community Cloud redeploys automatically.
  Use None where no limit applies.
"""

SOURCES = {
    "ABIM": ("ABIM Laboratory Test Reference Ranges (Jan 2026)",
             "https://www.abim.org/Media/bfijryql/laboratory-reference-ranges.pdf"),
    "MLABS": ("Michigan Medicine Laboratories Critical Value Policy (Apr 2024)",
              "https://mlabs.umich.edu/media/630"),
    "MERCK": ("Merck Manual Professional - Laboratory Reference Ranges / TDM (May 2026)",
              "https://www.merckmanuals.com/professional/resources/normal-laboratory-values/laboratory-reference-ranges"),
    "MAYO": ("Mayo Clinic Laboratories - Lithium, Serum (LITH)",
             "https://www.mayocliniclabs.com/test-catalog/overview/37046"),
    "MEDLINE": ("MedlinePlus - Prothrombin time (PT/INR)",
                "https://medlineplus.gov/ency/article/003652.htm"),
    "BD": ("BD Vacutainer order of draw & tube guide (CLSI GP41)",
           "https://www.dshs.texas.gov/sites/default/files/lab/STL/t5orderOfDraw.pdf"),
}

# ---------------------------------------------------------------------------
# TUBES
# ---------------------------------------------------------------------------
TUBES = {
    "culture": dict(name="Blood culture bottles", color="#7a8a99", additive="SPS broth (aerobic & anaerobic)",
                    inversions="8-10", order=1, uses="Blood cultures",
                    note="Always first. Butterfly: aerobic bottle first (tubing air). Syringe: anaerobic first."),
    "lblue": dict(name="Light blue", color="#7ec8e3", additive="3.2% sodium citrate (9:1 blood:additive)",
                  inversions="3-4", order=2, uses="PT/INR, aPTT, fibrinogen, D-dimer, factor assays, anti-Xa",
                  note="MUST fill to the line. If it is the first tube with a butterfly, draw a discard tube first. "
                       "CLSI: spin 1500 x g for 15 min for platelet-poor plasma."),
    "red": dict(name="Red (plastic)", color="#d62828", additive="Clot activator (glass red: none)",
                inversions="5 (plastic) / none (glass)", order=3, uses="Serum: drug levels, serology, some blood bank",
                note="Clot 30-60 min. No gel - preferred for some drug/toxicology assays."),
    "gold": dict(name="Gold / Red-gray (SST)", color="#e9b10e", additive="Clot activator + separator gel",
                 inversions="5", order=4, uses="Chemistry, endocrine, serology",
                 note="Clot 30 min upright. BD: spin 1000-1300 x g, 10 min (swing-bucket) or 15 min (fixed-angle)."),
    "lgreen": dict(name="Light green / Green-gray (PST)", color="#8fd19e", additive="Lithium heparin + gel",
                   inversions="8-10", order=5, uses="STAT chemistry (BMP, CMP, troponin per assay)",
                   note="Plasma - no clotting wait. Never for lithium levels."),
    "green": dict(name="Dark green", color="#2d6a4f", additive="Sodium or lithium heparin",
                  inversions="8-10", order=6, uses="Ammonia, cytogenetics (sodium heparin), some STAT chemistry",
                  note="Check which heparin salt the test requires."),
    "lav": dict(name="Lavender", color="#9b72cf", additive="K2EDTA", inversions="8-10", order=7,
                uses="CBC, diff, retic, ESR, HbA1c, BNP, smear",
                note="Underfill distorts morphology; poor mixing causes clots."),
    "pink": dict(name="Pink", color="#f4a6c6", additive="K2EDTA (blood bank)", inversions="8-10", order=7,
                 uses="Type & screen, crossmatch, DAT",
                 note="Blood bank labeling rules - label at the bedside."),
    "gray": dict(name="Gray", color="#8d99a6", additive="Sodium fluoride / potassium oxalate",
                 inversions="8-10", order=8, uses="Glucose (delayed testing), lactate, blood alcohol",
                 note="Drawn last."),
    "royal": dict(name="Royal blue", color="#1d3fbf", additive="K2EDTA or clot activator (trace-element free)",
                  inversions="8-10 (EDTA) / 5 (serum)", order=0, uses="Zinc, copper, heavy metals",
                  note="Place in order by its additive (EDTA with lavender; serum with red)."),
    "tan": dict(name="Tan", color="#c9a66b", additive="K2EDTA (lead-certified)", inversions="8-10", order=0,
                uses="Blood lead", note="Draw with the EDTA tubes."),
    "white": dict(name="White / Pearl (PPT)", color="#eeeeee", additive="K2EDTA + gel", inversions="8-10", order=0,
                  uses="Viral loads, molecular", note="Draw with the EDTA tubes."),
    "yellow": dict(name="Yellow", color="#f7e15c", additive="SPS or ACD", inversions="8-10", order=0,
                   uses="SPS: cultures. ACD: HLA, special studies", note="Check the additive on the label."),
    "syr": dict(name="Heparinized syringe", color="#3a86ff", additive="Balanced heparin", inversions="Roll gently",
                order=0, uses="Blood gas, ionized calcium", note="Expel air bubbles, cap immediately."),
    "cup": dict(name="Sterile container", color="#e7e7e7", additive="None (or preservative tube)", inversions="-",
                order=0, uses="Urine, stool, swabs, body fluids", note="Label the container, not the lid."),
    "csf": dict(name="CSF tubes (numbered)", color="#ffffff", additive="Sterile, none", inversions="-", order=0,
                uses="Cerebrospinal fluid", note="Keep tubes in collection order."),
    "jug": dict(name="24-hour urine container", color="#f2a541", additive="Preservative per test",
                inversions="-", order=0, uses="24-h urine studies", note="Check preservative before giving to patient."),
}
ORDER_OF_DRAW = ["culture", "lblue", "red", "gold", "lgreen", "green", "lav", "pink", "gray"]

# ---------------------------------------------------------------------------
# TESTS: (name, search keywords, department, [tube ids], handling notes)
# ---------------------------------------------------------------------------
TESTS = [
    ("Basic Metabolic Panel (BMP)", "chem 7 lytes renal", "Chemistry", ["lgreen", "gold"],
     "PST plasma preferred for STAT. No fist pumping (falsely high K). Spin within 2 h."),
    ("Comprehensive Metabolic Panel (CMP)", "chem 14", "Chemistry", ["lgreen", "gold"],
     "BMP + liver tests, total protein, albumin. Protect from light if delayed (bilirubin)."),
    ("Electrolytes (Na, K, Cl, CO2)", "lytes sodium potassium chloride bicarbonate", "Chemistry", ["lgreen", "gold"],
     "Hemolysis falsely raises K. Keep capped - CO2 escapes from open tubes."),
    ("Hepatic Function Panel (LFTs)", "liver ast alt alp bilirubin", "Chemistry", ["gold", "lgreen"],
     "Protect from light if testing is delayed."),
    ("Lipid Panel", "cholesterol triglycerides hdl ldl", "Chemistry", ["gold"],
     "Fast 9-12 h only if ordered fasting."),
    ("Glucose", "blood sugar fbs fasting", "Chemistry", ["gray", "gold", "lgreen"],
     "Gray top stabilizes glucose. SST/PST must be spun within 2 h - glycolysis lowers glucose about 5-7% per hour."),
    ("Hemoglobin A1c", "hba1c a1c glycated", "Chemistry", ["lav"], "Whole blood; no fasting."),
    ("Magnesium", "mg", "Chemistry", ["gold", "lgreen"], "Hemolysis falsely raises Mg."),
    ("Phosphorus", "phos phosphate", "Chemistry", ["gold", "lgreen"], "Hemolysis and delayed spin falsely raise phosphorus."),
    ("Calcium, total", "ca", "Chemistry", ["gold", "lgreen"],
     "Never EDTA - carryover gives falsely low Ca and high K."),
    ("Ionized Calcium", "ica ionized", "Chemistry", ["syr", "green"],
     "Balanced-heparin syringe/tube per lab. Fill completely, keep capped (anaerobic), analyze promptly."),
    ("Lactic Acid", "lactate", "Chemistry", ["gray"],
     "Minimal tourniquet, no fist clenching. On ice; analyze within 15-30 min."),
    ("Ammonia", "nh3", "Chemistry", ["green", "lav"],
     "Fill tube, cap, ON ICE immediately. Spin and test within 15-30 min. Hemolysis falsely raises."),
    ("Blood Gas (ABG/VBG)", "abg vbg arterial venous ph pco2 po2", "Chemistry", ["syr"],
     "Expel air bubbles, cap, mix. Plastic syringe: analyze within 30 min at room temperature."),
    ("Troponin (hs-cTn)", "trop cardiac ctni ctnt", "Chemistry", ["lgreen", "gold"],
     "Tube and cutoff are assay-specific. Record the exact collection time for serial protocols."),
    ("BNP", "natriuretic", "Chemistry", ["lav"], "EDTA plastic tube. (NT-proBNP uses SST/PST.)"),
    ("NT-proBNP", "nt pro bnp", "Chemistry", ["gold", "lgreen"], "Serum or heparin plasma."),
    ("CK / CK-MB", "creatine kinase", "Chemistry", ["gold", "lgreen"], "Hemolysis interferes."),
    ("Lipase / Amylase", "pancreas", "Chemistry", ["gold", "lgreen"], ""),
    ("CRP / hs-CRP", "c-reactive protein", "Chemistry", ["gold"], ""),
    ("Procalcitonin", "pct sepsis", "Chemistry", ["gold", "lgreen"], ""),
    ("Uric Acid", "urate gout", "Chemistry", ["gold"], ""),
    ("Osmolality, serum", "osm", "Chemistry", ["gold"], "See the osmolal gap calculator."),
    ("Iron / TIBC / Ferritin", "fe iron studies", "Chemistry", ["gold"],
     "Morning draw preferred for iron. Hemolysis raises iron."),
    ("Vitamin B12 / Folate", "b12 cobalamin", "Chemistry", ["gold"], "Protect from light."),
    ("Vitamin D, 25-OH", "vit d", "Chemistry", ["gold"], ""),
    ("TSH / Free T4", "thyroid", "Chemistry", ["gold"], ""),
    ("Cortisol", "am cortisol", "Chemistry", ["gold"], "Time-sensitive - record exact draw time."),
    ("hCG, quantitative", "beta hcg pregnancy serum", "Chemistry", ["gold"], ""),
    ("PSA", "prostate", "Chemistry", ["gold"], ""),
    ("PTH, intact", "parathyroid", "Chemistry", ["lav"], "EDTA preferred by many assays; keep cold, spin promptly."),
    ("ACTH", "corticotropin", "Chemistry", ["lav"], "Pre-chilled plastic EDTA, on ice, cold spin, freeze plasma."),
    ("LDH / Haptoglobin", "hemolysis workup", "Chemistry", ["gold"], "In-vitro hemolysis falsely raises LDH."),
    ("Ethanol (blood alcohol)", "etoh alcohol legal", "Chemistry", ["gray"],
     "Clean site with a NON-alcohol antiseptic (e.g., povidone-iodine). Keep capped. Legal: chain of custody."),
    ("Lead, blood", "pb heavy metal", "Chemistry", ["tan", "royal"], "Lead-certified tube; clean skin thoroughly."),
    ("Zinc / Copper / Trace elements", "trace metals", "Chemistry", ["royal"], "Trace-element-free royal blue."),
    ("Acetaminophen / Salicylate", "tylenol aspirin overdose tox", "Toxicology / TDM", ["gold"],
     "Record time of ingestion if known."),
    ("Vancomycin level", "vanco trough peak", "Toxicology / TDM", ["red", "gold"],
     "Trough within 30 min before next dose. Record dose and draw time."),
    ("Digoxin level", "lanoxin", "Toxicology / TDM", ["red", "gold"], "Draw at least 6-8 h after the dose."),
    ("Lithium level", "li", "Toxicology / TDM", ["gold", "red"],
     "NEVER a lithium-heparin tube. Draw 8-12 h after last dose (trough). Mayo: SST preferred."),
    ("Phenytoin / Valproate / Carbamazepine", "dilantin depakote tegretol", "Toxicology / TDM", ["red", "gold"],
     "Usually trough (before next dose)."),
    ("Gentamicin / Tobramycin", "aminoglycoside peak trough", "Toxicology / TDM", ["red", "gold"],
     "Peak/trough timing per pharmacy."),
    ("CBC with Differential", "cbc complete blood count diff", "Hematology", ["lav"],
     "Invert 8-10x. Reject clotted. Make smears within 2-3 h."),
    ("Reticulocyte Count", "retic", "Hematology", ["lav"], "See corrected retic / RPI calculator."),
    ("ESR (Sed Rate)", "esr sedimentation", "Hematology", ["lav"],
     "Full tube; test within 4 h at room temp (24 h refrigerated) per method."),
    ("Peripheral Smear", "smear morphology", "Hematology", ["lav"], ""),
    ("Sickle Screen / Hgb Electrophoresis", "hemoglobinopathy", "Hematology", ["lav"], ""),
    ("Platelet count (clumping suspected)", "pseudothrombocytopenia clumps", "Hematology", ["lblue"],
     "EDTA-induced clumping: recollect in light blue citrate, multiply count by 1.1."),
    ("PT / INR", "protime warfarin coumadin", "Coagulation", ["lblue"],
     "Fill to line (9:1). Discard tube first with butterfly. Stable 24 h uncentrifuged at room temp."),
    ("aPTT", "ptt heparin", "Coagulation", ["lblue"],
     "Test within 4 h. Patient on unfractionated heparin: centrifuge within 1 h."),
    ("Fibrinogen", "clauss", "Coagulation", ["lblue"], ""),
    ("D-dimer", "dvt pe", "Coagulation", ["lblue"], "Units vary (FEU vs DDU) - check your assay."),
    ("Anti-Xa (heparin level)", "lmwh heparin assay", "Coagulation", ["lblue"],
     "Spin within 1 h; timing relative to dose matters."),
    ("Factor assays / Mixing study", "factor viii ix lupus anticoagulant", "Coagulation", ["lblue"],
     "Platelet-poor plasma; double-centrifuge and freeze if not tested promptly."),
    ("Type & Screen", "abo rh antibody t&s", "Blood Bank", ["pink", "lav"],
     "Label AT THE BEDSIDE: full name, MRN/DOB, date & time, collector ID. Any error = reject and recollect."),
    ("Type & Crossmatch", "crossmatch xm", "Blood Bank", ["pink", "lav"], "Same labeling rules as Type & Screen."),
    ("DAT (Direct Coombs)", "coombs antiglobulin", "Blood Bank", ["lav", "pink"], ""),
    ("Fetal screen (RhIG workup)", "rhogam fetal bleed kleihauer", "Blood Bank", ["lav", "pink"], ""),
    ("Blood Cultures", "bc sepsis", "Microbiology", ["culture"],
     "Chlorhexidine scrub 30 s, air-dry. 8-10 mL per bottle (adult). Two sets, separate sites, before antibiotics. "
     "Do not refrigerate."),
    ("Urine Culture", "ucx c&s", "Microbiology", ["cup"],
     "Clean-catch midstream. Refrigerate if not processed within 2 h (or boric acid tube)."),
    ("CSF studies", "spinal fluid lumbar puncture lp", "Microbiology", ["csf"],
     "Number tubes in order (commonly 1 chem, 2 micro, 3 cell count, 4 extra - follow policy). STAT; "
     "never refrigerate the micro tube."),
    ("C. difficile", "cdiff stool toxin", "Microbiology", ["cup"], "Unformed stool only. Refrigerate if delayed."),
    ("Swab cultures / PCR", "throat wound nasal mrsa covid flu", "Microbiology", ["cup"],
     "Correct transport medium; label the body site."),
    ("Urinalysis", "ua dipstick microscopic", "Urinalysis", ["cup"],
     "Test within 2 h or refrigerate. First-morning midstream preferred."),
    ("Urine Drug Screen", "uds tox", "Urinalysis", ["cup"],
     "Forensic: chain of custody; temperature 90-100 F (32-38 C) within 4 min."),
    ("Urine hCG", "pregnancy qualitative", "Urinalysis", ["cup"], "First-morning urine is most concentrated."),
    ("24-hour Urine", "creatinine clearance protein", "Urinalysis", ["jug"],
     "Discard first void, collect ALL urine for 24 h including final void. Refrigerate / preservative per test."),
    ("Cryoglobulins / Cold agglutinins", "cryo cold", "Special", ["red"],
     "Pre-warm tube; keep at 37 C until clotted and separated. Do not refrigerate."),
    ("Cytogenetics / Chromosomes", "karyotype genetic", "Special", ["green"],
     "Sodium heparin. Room temperature; never freeze."),
    ("HIV / HCV viral load", "viral load rna pcr", "Special", ["white", "lav"],
     "Separate plasma within the assay's time limit."),
    ("Hepatitis / HIV serology", "hbsag hcv ab hiv antibody", "Special", ["gold"], ""),
]

# ---------------------------------------------------------------------------
# RANGES
#   lo/hi   = reference interval     clo/chi = critical limits (call)
#   disp    = optional text for how the reference interval is written
#   ref/crit = source keys from SOURCES
# ---------------------------------------------------------------------------
def R(id, name, dept, unit, lo, hi, clo, chi, ref, crit, note="", disp=None):
    return dict(id=id, name=name, dept=dept, unit=unit, lo=lo, hi=hi, clo=clo, chi=chi,
                ref=ref, crit=crit, note=note, disp=disp)


RANGES = [
    # ---- Chemistry ----
    R("na", "Sodium", "Chemistry", "mmol/L", 136, 145, 120, 160, "ABIM", "MLABS"),
    R("k", "Potassium", "Chemistry", "mmol/L", 3.5, 5.0, 2.5, 6.0, "ABIM", "MLABS",
      "Rule out hemolysis before calling a high K. Infants 0-3 mo: critical >6.5 (MLabs)."),
    R("cl", "Chloride", "Chemistry", "mmol/L", 98, 106, 80, 130, "ABIM", "MLABS"),
    R("co2", "CO2, total (bicarbonate)", "Chemistry", "mmol/L", 23, 30, 10, 40, "ABIM", "MLABS"),
    R("bun", "BUN (urea nitrogen)", "Chemistry", "mg/dL", 8, 20, None, None, "ABIM", None),
    R("crf", "Creatinine (female)", "Chemistry", "mg/dL", 0.50, 1.10, None, None, "ABIM", None),
    R("crm", "Creatinine (male)", "Chemistry", "mg/dL", 0.70, 1.30, None, None, "ABIM", None),
    R("glu", "Glucose, fasting", "Chemistry", "mg/dL", 70, 99, 50, 450, "ABIM", "MLABS",
      "Neonates have different critical limits (MLabs 0-1 day: <40 or >200)."),
    R("ca", "Calcium, total", "Chemistry", "mg/dL", 8.6, 10.2, 6.0, 14.0, "ABIM", "MLABS",
      "Correct for albumin (see calculator)."),
    R("ica", "Calcium, ionized", "Chemistry", "mmol/L", 1.16, 1.31, 0.75, 1.55, "ABIM", "MLABS",
      "x 4.008 = mg/dL."),
    R("mg", "Magnesium", "Chemistry", "mg/dL", 1.6, 2.6, None, None, "ABIM", "MLABS",
      "MLabs critical applies to obstetric patients only: >8 mg/dL."),
    R("phos", "Phosphorus", "Chemistry", "mg/dL", 3.0, 4.5, None, None, "ABIM", None,
      "Not on the MLabs critical list; many US labs call <1.0 mg/dL."),
    R("tbil", "Bilirubin, total", "Chemistry", "mg/dL", 0.3, 1.0, None, None, "ABIM", "MLABS",
      "Newborn critical (MLabs): >15 mg/dL."),
    R("dbil", "Bilirubin, direct", "Chemistry", "mg/dL", 0.1, 0.3, None, None, "ABIM", None),
    R("alb", "Albumin", "Chemistry", "g/dL", 3.5, 5.5, None, None, "ABIM", None),
    R("tp", "Protein, total", "Chemistry", "g/dL", 5.5, 9.0, None, None, "ABIM", None),
    R("ast", "AST", "Chemistry", "U/L", 10, 40, None, None, "ABIM", None),
    R("alt", "ALT", "Chemistry", "U/L", 10, 40, None, None, "ABIM", None),
    R("alp", "Alkaline phosphatase", "Chemistry", "U/L", 30, 120, None, None, "ABIM", None,
      "Higher in children and adolescents."),
    R("lact", "Lactate", "Chemistry", "mmol/L", 0.7, 2.1, None, 5.0, "ABIM", "MLABS",
      "MLabs critical is for ICU patients (>5.0; ICU age 0-12 y: >2.2)."),
    R("amm", "Ammonia", "Chemistry", "ug/dL", 40, 70, None, None, "ABIM", None,
      "Method-dependent; many labs report umol/L."),
    R("osm", "Osmolality, serum", "Chemistry", "mOsm/kg", 275, 295, None, None, "ABIM", None),
    R("uric", "Uric acid", "Chemistry", "mg/dL", 3.0, 7.0, None, None, "ABIM", None),
    R("tsh", "TSH", "Chemistry", "mIU/L", 0.5, 4.0, None, None, "ABIM", None),
    R("ft4", "Free T4", "Chemistry", "ng/dL", 0.8, 1.8, None, None, "ABIM", None),
    R("a1c", "Hemoglobin A1c", "Chemistry", "%", 4.0, 5.6, None, None, "ABIM", None,
      "5.7-6.4% prediabetes; 6.5% or higher diabetes (ADA)."),
    R("chol", "Cholesterol, total", "Chemistry", "mg/dL", None, 199, None, None, "ABIM", None,
      "Borderline-high 200-239; high 240 or more.", disp="Desirable < 200"),
    R("ldl", "LDL cholesterol", "Chemistry", "mg/dL", None, 99, None, None, "ABIM", None,
      "Near-optimal 100-129; borderline 130-159; high 160-189; very high 190+.", disp="Optimal < 100"),
    R("hdlm", "HDL cholesterol (male)", "Chemistry", "mg/dL", 40, None, None, None, "ABIM", None,
      disp="Low if < 40"),
    R("hdlf", "HDL cholesterol (female)", "Chemistry", "mg/dL", 50, None, None, None, "ABIM", None,
      disp="Low if < 50"),
    R("tg", "Triglycerides, fasting", "Chemistry", "mg/dL", None, 149, None, None, "ABIM", None,
      "Borderline 150-199; high 200-499; very high 500+.", disp="Normal < 150"),
    R("lead", "Lead, blood", "Chemistry", "ug/dL", None, None, None, 70, None, "MLABS"),
    # ---- Hematology ----
    R("wbc", "WBC", "Hematology", "x10^3/uL", 4.0, 11.0, None, 100, "ABIM", "MLABS",
      "MLabs critical high applies to outpatients."),
    R("hgbm", "Hemoglobin (male)", "Hematology", "g/dL", 14, 18, 6.0, 20.0, "ABIM", "MLABS",
      "MLabs: high critical for outpatients older than 3 months."),
    R("hgbf", "Hemoglobin (female)", "Hematology", "g/dL", 12, 16, 6.0, 20.0, "ABIM", "MLABS",
      "MLabs: high critical for outpatients older than 3 months."),
    R("hctm", "Hematocrit (male)", "Hematology", "%", 42, 50, 18, 60, "ABIM", "MLABS",
      "MLabs outpatient limits; inpatient low critical is 15%."),
    R("hctf", "Hematocrit (female)", "Hematology", "%", 37, 47, 18, 60, "ABIM", "MLABS",
      "MLabs outpatient limits; inpatient low critical is 15%."),
    R("plt", "Platelets", "Hematology", "x10^3/uL", 150, 450, 20, 1000, "ABIM", "MLABS",
      "MLabs outpatient limits; inpatient low critical is 10. Check smear for clumps."),
    R("mcv", "MCV", "Hematology", "fL", 80, 98, None, None, "ABIM", None),
    R("anc", "Absolute neutrophil count", "Hematology", "x10^3/uL", 2.0, 8.25, 0.5, None, "ABIM", "MLABS",
      "MLabs ANC critical applies to outpatients (also 5% or more blasts)."),
    R("retic", "Reticulocytes", "Hematology", "%", 0.5, 1.5, None, None, "ABIM", None),
    # ---- Coagulation ----
    R("pt", "PT", "Coagulation", "sec", 11, 13, None, None, "ABIM", None, "Reagent-specific."),
    R("inr", "INR", "Coagulation", "", 0.8, 1.1, None, 5.0, "MEDLINE", "MLABS",
      "Usual warfarin target 2.0-3.0 (higher for some indications)."),
    R("aptt", "aPTT", "Coagulation", "sec", 25, 35, None, 92.6, "ABIM", "MLABS", "Reagent-specific."),
    R("fib", "Fibrinogen", "Coagulation", "mg/dL", 200, 400, 100, None, "ABIM", "MLABS"),
    R("ddim", "D-dimer", "Coagulation", "ug/mL", None, 0.49, None, None, "ABIM", None,
      "Assay-specific units (FEU vs DDU).", disp="< 0.5"),
    R("axa_ufh", "Anti-Xa, unfractionated heparin", "Coagulation", "IU/mL", None, None, None, 1.0, None, "MLABS"),
    R("axa_lmwh", "Anti-Xa, LMWH", "Coagulation", "IU/mL", None, None, None, 2.0, None, "MLABS"),
    # ---- Blood gas (arterial, room air) ----
    R("ph", "pH, arterial", "Blood Gas", "", 7.38, 7.44, 7.20, 7.55, "ABIM", "MLABS",
      "Many labs use 7.35-7.45 as the reference interval."),
    R("pco2", "pCO2, arterial", "Blood Gas", "mmHg", 38, 42, 20, 65, "ABIM", "MLABS",
      "Many labs use 35-45 as the reference interval."),
    R("po2", "pO2, arterial", "Blood Gas", "mmHg", 75, 100, 50, None, "ABIM", "MLABS"),
    R("hco3", "HCO3, arterial", "Blood Gas", "mmol/L", 23, 26, 10, 40, "ABIM", "MLABS"),
    R("cohb", "Carboxyhemoglobin", "Blood Gas", "%", None, None, None, 10, None, "MLABS"),
    R("methb", "Methemoglobin", "Blood Gas", "%", None, None, None, 10, None, "MLABS"),
    # ---- Toxicology / TDM ----
    R("dig", "Digoxin", "Toxicology / TDM", "ng/mL", 0.8, 2.0, None, 2.0, "MERCK", "MLABS",
      "Reference shown is the therapeutic range."),
    R("li", "Lithium (trough)", "Toxicology / TDM", "mmol/L", 0.5, 1.2, None, 1.5, "MAYO", "MLABS",
      "Therapeutic range; draw 8-12 h after last dose."),
    R("phen", "Phenytoin, total", "Toxicology / TDM", "ug/mL", 10, 20, None, 30, "MERCK", "MLABS",
      "Therapeutic range."),
    R("vpa", "Valproic acid", "Toxicology / TDM", "ug/mL", 50, 99, None, 150, "MERCK", "MLABS",
      "Therapeutic range."),
    R("cbz", "Carbamazepine", "Toxicology / TDM", "ug/mL", 4, 12, None, 15, "MERCK", "MLABS",
      "Therapeutic range."),
    R("vanc_t", "Vancomycin (trough)", "Toxicology / TDM", "ug/mL", None, None, None, 20.1, None, "MLABS",
      "Most hospitals dose by AUC - follow pharmacy. Peak/random critical >60."),
    R("gent_t", "Gentamicin / Tobramycin (trough)", "Toxicology / TDM", "ug/mL", None, None, None, 2.6, None, "MLABS",
      "Peak/random critical >10.5."),
    R("apap", "Acetaminophen", "Toxicology / TDM", "ug/mL", None, None, None, 40, None, "MLABS",
      "Interpret with time since ingestion (nomogram)."),
    R("sal", "Salicylate", "Toxicology / TDM", "mg/dL", None, None, None, 30, None, "MLABS"),
    R("etoh", "Ethanol", "Toxicology / TDM", "mg/dL", None, None, None, 450, None, "MLABS"),
]

# ---------------------------------------------------------------------------
# UNIT CONVERSIONS (conventional -> SI multiply by factor)
# ---------------------------------------------------------------------------
UNITS = [
    ("Glucose", "mg/dL", "mmol/L", 0.0555),
    ("Cholesterol (TC, LDL, HDL)", "mg/dL", "mmol/L", 0.02586),
    ("Triglycerides", "mg/dL", "mmol/L", 0.01129),
    ("Creatinine", "mg/dL", "umol/L", 88.4),
    ("BUN -> Urea", "mg/dL", "mmol/L", 0.357),
    ("Calcium", "mg/dL", "mmol/L", 0.2495),
    ("Magnesium", "mg/dL", "mmol/L", 0.4114),
    ("Phosphorus", "mg/dL", "mmol/L", 0.3229),
    ("Bilirubin", "mg/dL", "umol/L", 17.1),
    ("Uric acid", "mg/dL", "umol/L", 59.48),
    ("Iron", "ug/dL", "umol/L", 0.1791),
    ("Hemoglobin", "g/dL", "g/L", 10.0),
    ("Albumin / Protein", "g/dL", "g/L", 10.0),
]

# ---------------------------------------------------------------------------
# TEXT CONTENT
# ---------------------------------------------------------------------------
TROUBLESHOOTING = [
    ("Hemolysis", "Falsely high K, LDH, AST, Mg, phosphorus, iron; interferes with many assays.",
     "21-22 G needle, let alcohol dry, no shaking, don't force blood through a syringe needle, short tourniquet."),
    ("EDTA carryover / contamination", "Very high K, very low Ca, low Mg, low ALP.",
     "Follow order of draw; never pour blood between tubes."),
    ("IV fluid contamination", "High glucose or Na/Cl/K (depends on fluid); other analytes diluted.",
     "Draw from the opposite arm or below the IV; stop the infusion per policy."),
    ("Delayed centrifugation", "Low glucose (about 5-7%/h), high K, phosphorus, LDH.",
     "Spin within 2 h; use gray top for glucose if delayed."),
    ("Prolonged tourniquet / fist pumping", "High K, protein, Ca, cholesterol (hemoconcentration).",
     "Tourniquet 1 minute or less; no fist pumping."),
    ("Underfilled light blue tube", "Falsely prolonged PT and aPTT.", "Fill to line; discard tube with butterfly."),
    ("Hematocrit above 55%", "Falsely prolonged PT and aPTT (too much citrate for the plasma).",
     "Adjust citrate volume - see calculator (CLSI H21)."),
    ("Clotted EDTA tube", "Low platelets and WBC; unreliable CBC.", "Invert 8-10x immediately; reject clotted CBC."),
    ("EDTA platelet clumping", "Falsely low platelets; clumps on smear.", "Recollect in citrate; multiply by 1.1."),
    ("Cold agglutinins", "Low RBC, high MCV, MCHC above 37.", "Warm specimen to 37 C for 15-30 min and rerun."),
    ("Lipemia", "Falsely high Hgb/MCHC; chemistry interference.",
     "Ultracentrifuge or saline replacement per SOP; comment on report."),
    ("Icterus", "Interferes with creatinine and some colorimetric assays.", "Check the analyzer icteric index limits."),
    ("High-dose biotin", "False highs or lows on streptavidin immunoassays (TSH, troponin, hormones).",
     "Ask about supplements; follow assay guidance."),
]

REJECTION = [
    "Unlabeled or mislabeled - identifiers missing or not matching the order/armband.",
    "Wrong tube type for the test ordered.",
    "QNS (quantity not sufficient) or underfilled citrate tube.",
    "Clotted anticoagulated specimen (CBC, coagulation).",
    "Hemolyzed beyond the analyzer's index limit for the test.",
    "Stability exceeded - too old or wrong temperature (e.g., ammonia not on ice).",
    "Leaking or broken container; contaminated outside.",
    "Expired collection tube.",
    "IV fluid contamination.",
]

CRITICAL_CALL = [
    "Verify the result: check specimen quality (hemolysis, clots, IV contamination, right patient); repeat if policy requires.",
    "Call the responsible licensed caregiver (provider or RN) within your lab's time limit.",
    "Give patient name + second identifier, test, result, units and reference range.",
    "Ask the recipient to READ BACK the identifiers and the result.",
    "Document recipient's full name and credentials, date/time, read-back confirmed, your ID.",
    "If no one can be reached in time, escalate through the chain of command.",
]

TRANSFUSION_REACTION = [
    "STOP the transfusion immediately.",
    "Keep the IV open with normal saline using new tubing.",
    "Re-check patient ID against the unit labels at the bedside.",
    "Notify the provider and the blood bank.",
    "Return the bag, tubing and attached solutions to the blood bank.",
    "Collect post-transfusion samples per policy (e.g., EDTA for DAT/retype, urine for hemoglobin).",
]

EXPOSURE = [
    "Wash the wound with soap and water; flush eyes/mucous membranes with water or saline.",
    "Do not squeeze, scrub with bleach, or use caustic agents.",
    "Report to your supervisor immediately.",
    "Go to Employee/Occupational Health or the ED right away - post-exposure prophylaxis works best started within hours.",
    "Identify the source patient for testing per policy; complete the incident report.",
]
