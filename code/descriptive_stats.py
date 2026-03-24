"""
descriptive_stats.py
====================
Reproduces all descriptive statistics reported in the MQD-1209 dataset card.

Inputs (expected in ../data/ relative to this script):
    mqd-1209.csv      — main dataset (1,209 instances, tab-separated)
    mqd-13317.csv     — full annotation log (13,317 records, tab-separated)

Usage:
    python descriptive_stats.py

Requirements:
    pandas, numpy, scipy, scikit-learn
    pip install pandas numpy scipy scikit-learn
"""

import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, spearmanr
from sklearn.metrics import cohen_kappa_score

SEP = "-" * 60

# ── Load data ────────────────────────────────────────────────────────────────

df = pd.read_csv(
    "../data/mqd-1209.csv",
    sep="\t",
    quoting=3,
    on_bad_lines="skip",
)

df_full = pd.read_csv(
    "../data/mqd-13317.csv",
    sep="\t",
    quoting=3,
    on_bad_lines="skip",
)

# ── Section 1: Dataset shape ─────────────────────────────────────────────────

print(SEP)
print("SECTION 1 — DATASET SHAPE")
print(SEP)
print(f"MQD-1209  : {df.shape[0]} instances, {df.shape[1]} columns")
print(f"MQD-13317 : {df_full.shape[0]} annotation records")

# ── Section 2: Annotator counts (from full log) ───────────────────────────────

print(SEP)
print("SECTION 2 — ANNOTATORS (mqd-13317)")
print(SEP)

total_unique = df_full["ParticipantMD5"].nunique()
by_gender = df_full.groupby("GeneroCod")["ParticipantMD5"].nunique()
per_person = (
    df_full.groupby(["ParticipantMD5", "GeneroCod"])
    .size()
    .reset_index(name="n_annotations")
)
stats_per_person = per_person.groupby("GeneroCod")["n_annotations"].describe()

print(f"Total unique annotators : {total_unique}")
print(f"  Male   (m) : {by_gender.get('m', 0)}")
print(f"  Female (f) : {by_gender.get('f', 0)}")
print()
print("Annotations per person (by gender):")
print(stats_per_person.round(1))

# ── Section 3: Class distribution ────────────────────────────────────────────

print(SEP)
print("SECTION 3 — CLASS DISTRIBUTION")
print(SEP)

n = len(df)
for group, col in [
    ("Male",   "classificacao_majoritaria_masculino"),
    ("Female", "classificacao_majoritaria_feminino"),
]:
    vc = df[col].value_counts()
    print(f"{group} (n={n}):")
    for cls, cnt in vc.items():
        print(f"  {cls:<10}: {cnt:>4}  ({cnt / n * 100:.1f}%)")
    print()

# ── Section 4: Inter-group agreement ─────────────────────────────────────────

print(SEP)
print("SECTION 4 — INTER-GROUP AGREEMENT")
print(SEP)

concordant   = int(df["concordancia_grupos"].sum())
discordant   = n - concordant
print(f"Concordant  : {concordant} ({concordant / n * 100:.1f}%)")
print(f"Discordant  : {discordant} ({discordant / n * 100:.1f}%)")

label_map = {"negativa": 0, "neutra": 1, "positiva": 2}
y_masc = df["classificacao_majoritaria_masculino"].map(label_map)
y_fem  = df["classificacao_majoritaria_feminino"].map(label_map)

kappa = cohen_kappa_score(y_masc, y_fem)

# Bootstrap 95% CI for kappa
rng = np.random.default_rng(42)
boot_kappas = []
for _ in range(1000):
    idx = rng.integers(0, n, size=n)
    boot_kappas.append(cohen_kappa_score(y_masc.iloc[idx], y_fem.iloc[idx]))
ci_low, ci_high = np.percentile(boot_kappas, [2.5, 97.5])

ct = pd.crosstab(
    df["classificacao_majoritaria_masculino"],
    df["classificacao_majoritaria_feminino"],
)
chi2, p, dof, _ = chi2_contingency(ct)
cramers_v = np.sqrt(chi2 / (n * (min(ct.shape) - 1)))

print(f"\nCohen's kappa (κ)  : {kappa:.4f}")
print(f"95% CI (bootstrap) : [{ci_low:.4f} ; {ci_high:.4f}]")
print(f"Cramér's V         : {cramers_v:.4f}")
print(f"Chi² / p-value     : {chi2:.2f} / {p:.2e}")

# ── Section 5: Disagreement patterns ─────────────────────────────────────────

print(SEP)
print("SECTION 5 — DISAGREEMENT PATTERNS (n=188)")
print(SEP)

discord = df[df["concordancia_grupos"] == 0]
pairs = (
    discord.groupby([
        "classificacao_majoritaria_masculino",
        "classificacao_majoritaria_feminino",
    ])
    .size()
    .reset_index(name="n")
)
pairs["%"] = (pairs["n"] / len(discord) * 100).round(1)
print(pairs.sort_values("n", ascending=False).to_string(index=False))

# ── Section 6: Intra-group certainty ─────────────────────────────────────────

print(SEP)
print("SECTION 6 — INTRA-GROUP CERTAINTY (votes_majority / 4)")
print(SEP)

df["certainty_male"]   = df["votos_maioria_masculino"] / 4
df["certainty_female"] = df["votos_maioria_feminino"]  / 4

for group, col in [("Male", "certainty_male"), ("Female", "certainty_female")]:
    s = df[col]
    unani = (s == 1.0).sum()
    print(
        f"{group}: mean={s.mean():.4f}  median={s.median():.4f}  "
        f"std={s.std():.4f}  unanimity={unani} ({unani / n * 100:.1f}%)"
    )

# ── Section 7: Response time by agreement ────────────────────────────────────

print(SEP)
print("SECTION 7 — RESPONSE TIME BY AGREEMENT CONDITION")
print(SEP)

for conc_val, label in [(1, "Concordant"), (0, "Discordant")]:
    sub = df[df["concordancia_grupos"] == conc_val]
    print(f"{label} (n={len(sub)}):")
    for group, col in [
        ("Male",   "duracao_media_masculino"),
        ("Female", "duracao_media_feminino"),
    ]:
        s = sub[col]
        print(
            f"  {group}: median={s.median():.2f}s  "
            f"mean={s.mean():.2f}s  std={s.std():.2f}s"
        )
    print()

# ── Section 8: Phrase length ──────────────────────────────────────────────────

print(SEP)
print("SECTION 8 — PHRASE LENGTH")
print(SEP)

df["n_tokens"] = df["frase"].str.split().str.len()
df["n_chars"]  = df["frase"].str.len()

for metric, col in [("Tokens (words)", "n_tokens"), ("Characters", "n_chars")]:
    s = df[col]
    print(
        f"{metric}: mean={s.mean():.2f}  median={s.median():.2f}  "
        f"std={s.std():.2f}  min={s.min()}  max={s.max()}  "
        f"p25={s.quantile(0.25):.0f}  p75={s.quantile(0.75):.0f}"
    )

bins   = [0, 5, 10, 20, 40, 999]
labels = ["1-5", "6-10", "11-20", "21-40", "41+"]
df["token_range"] = pd.cut(df["n_tokens"], bins=bins, labels=labels)
print()
print("Distribution by token range:")
vc = df["token_range"].value_counts().sort_index()
for rng, cnt in vc.items():
    print(f"  {rng:<8}: {cnt:>4}  ({cnt / n * 100:.1f}%)")

# ── Section 9: Correlations ───────────────────────────────────────────────────

print(SEP)
print("SECTION 9 — SPEARMAN CORRELATIONS")
print(SEP)

p99_m = df["duracao_media_masculino"].quantile(0.99)
p99_f = df["duracao_media_feminino"].quantile(0.99)
sub_m = df[df["duracao_media_masculino"] <= p99_m]
sub_f = df[df["duracao_media_feminino"]  <= p99_f]

r1, p1 = spearmanr(sub_m["duracao_media_masculino"], sub_m["certainty_male"])
r2, p2 = spearmanr(sub_f["duracao_media_feminino"],  sub_f["certainty_female"])
r3, p3 = spearmanr(df["certainty_male"],   df["certainty_female"])
r4, p4 = spearmanr(df["concordancia_grupos"], df["duracao_media_masculino"])
r5, p5 = spearmanr(df["concordancia_grupos"], df["duracao_media_feminino"])

rows = [
    ("Duration × certainty [Male]",    r1, p1, f"excl. outliers >p99, n={len(sub_m)}"),
    ("Duration × certainty [Female]",  r2, p2, f"excl. outliers >p99, n={len(sub_f)}"),
    ("Certainty male × certainty fem", r3, p3, ""),
    ("Agreement × duration [Male]",    r4, p4, ""),
    ("Agreement × duration [Female]",  r5, p5, ""),
]

for desc, r, p, note in rows:
    sig = "***" if p < 0.001 else ("**" if p < 0.01 else ("*" if p < 0.05 else "n.s."))
    note_str = f"  ({note})" if note else ""
    print(f"{desc:<38}: rho={r:+.4f}  p={p:.4e}  {sig}{note_str}")

# ── Section 10: Descriptive stats for all numeric columns ─────────────────────

print(SEP)
print("SECTION 10 — DESCRIPTIVE STATS (all numeric attributes)")
print(SEP)

num_cols = [
    "duracao_media_masculino", "votos_maioria_masculino",
    "total_positiva_masculino", "total_negativa_masculino", "total_neutra_masculino",
    "duracao_media_feminino", "votos_maioria_feminino",
    "total_positiva_feminino", "total_negativa_feminino", "total_neutra_feminino",
    "concordancia_grupos",
]

for col in num_cols:
    s = df[col]
    print(
        f"{col:<38}: mean={s.mean():.4f}  median={s.median():.4f}  "
        f"std={s.std():.4f}  min={s.min():.4f}  max={s.max():.4f}"
    )

print(SEP)
print("All statistics successfully reproduced.")
print(SEP)
