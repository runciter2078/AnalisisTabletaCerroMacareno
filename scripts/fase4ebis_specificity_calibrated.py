# =============================================================================
# FASE 4e-bis — Especificidad Venus (versión calibrada)
#
# Mejoras sobre Fase 4e (per revisión experto):
#   1. Pseudo-Venus recalibrados para igualar densidad media Venus (~0.400)
#      → elimina la ventaja de densidad que tenían los pseudo (0.446-0.491)
#   2. Nueva familia "Venus+jitter": efemérides reales Venus con ruido temporal
#      ±15 días por evento → control cercano que destruye la estructura exacta
#      manteniendo el período y la densidad
#
# Mismo pipeline que 4e:
#   - OHE global fijo (20 columnas)
#   - Selección de mejor anchor DENTRO de train
#   - Evaluación Δlog-lik en fila retenida
#   - Bootstrap sobre 8 folds para comparación Venus vs mejor pseudo
#
# Veredicto esperado: si Venus vuelve a quedar en la parte baja → caso cerrado.
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings('ignore')

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder

RANDOM_SEED_4EBIS = 42 + 550

# ──────────────────────────────────────────────────────────────────────────────
# 0. CARGA DE DATOS
# ──────────────────────────────────────────────────────────────────────────────
try:
    y_obs = M_bin.values.astype(float).ravel()
    print("M_bin cargado desde kernel.")
except NameError:
    df_raw = pd.read_excel('../data/tableta.xlsx', header=None)
    y_obs = (df_raw.values == 1).astype(float).ravel()
    print("M_bin cargado desde disco.")

try:
    anchors_jd = resultados_4d['anchors_jd_valid'].copy()
    print("Anchors reutilizados de resultados_4d.")
except NameError:
    r4d = np.load('../results/fase4d_resultados.npy', allow_pickle=True).item()
    anchors_jd = r4d['anchors_jd_valid'].copy()
    print("Anchors cargados desde fase4d_resultados.npy.")

M_obs_2d = y_obs.reshape(8, 14).astype(int)
N_ROWS, N_COLS = 8, 14
N = N_ROWS * N_COLS
rows_idx = np.repeat(np.arange(N_ROWS), N_COLS)
cols_idx = np.tile(np.arange(N_COLS), N_ROWS)
SYNODIC_MONTH = 29.53058867
K = len(anchors_jd)

print(f"Anchors: {K}  |  Eventos tableta: {M_obs_2d.sum()}  |  "
      f"Densidad objetivo: {M_obs_2d.mean():.4f}")

# ──────────────────────────────────────────────────────────────────────────────
# 1. SECUENCIAS VENUS REALES (igual que 4e)
# ──────────────────────────────────────────────────────────────────────────────
ELONG_THRESHOLD = 35.0
_use_skyfield = False
try:
    _ = jd_dense_full
    _ = elong_dense
    _use_skyfield = True
    print("Usando efemérides Skyfield (jd_dense_full, elong_dense).")
except NameError:
    print("Skyfield no disponible → modelo sinusoidal para Venus.")

VENUS_PERIOD = 583.92
VENUS_AMP    = 47.0

def build_venus_seq_skyfield(anchor_jd):
    months    = np.arange(N)
    jd_cells  = anchor_jd + months * SYNODIC_MONTH
    elong_cells = np.interp(jd_cells, jd_dense_full, elong_dense,
                            left=np.nan, right=np.nan)
    return (elong_cells > ELONG_THRESHOLD).astype(float)

def build_seq_sinusoidal(anchor_jd, period, amplitude, threshold=35.0):
    t = np.arange(N) * SYNODIC_MONTH
    elong = amplitude * np.abs(np.cos(2.0 * np.pi * t / period))
    return (elong > threshold).astype(float)

print(f"\nPrecomputando secuencias Venus reales ({K} anchors)...")
VENUS_MAT = np.zeros((N, K))
for k, ajd in enumerate(anchors_jd):
    if _use_skyfield:
        VENUS_MAT[:, k] = build_venus_seq_skyfield(ajd)
    else:
        VENUS_MAT[:, k] = build_seq_sinusoidal(ajd, VENUS_PERIOD, VENUS_AMP)

valid = VENUS_MAT.var(axis=0) > 0
VENUS_MAT     = VENUS_MAT[:, valid]
anchors_valid = anchors_jd[valid]
K_v = VENUS_MAT.shape[1]
venus_density = VENUS_MAT.mean()
print(f"Secuencias Venus válidas: {K_v}  |  Densidad media: {venus_density:.4f}")

# ──────────────────────────────────────────────────────────────────────────────
# 2. VENUS + JITTER (nuevo control: ±15 días de ruido por celda)
# ──────────────────────────────────────────────────────────────────────────────
# Para cada anchor, perturbamos cada JD de celda con ruido uniforme ±15 días.
# Destruye la estructura exacta del ciclo Venus pero preserva período y densidad.
# Usamos 226 realizaciones distintas (una por anchor) con seed fijo.

JITTER_DAYS = 15
rng_jitter  = np.random.default_rng(RANDOM_SEED_4EBIS)

print(f"\nPrecomputando Venus+jitter (±{JITTER_DAYS}d por celda, {K_v} anchors)...")
VENUS_JITTER_MAT = np.zeros((N, K_v))
for k, ajd in enumerate(anchors_valid):
    months    = np.arange(N)
    jd_cells  = ajd + months * SYNODIC_MONTH
    jd_jittered = jd_cells + rng_jitter.uniform(-JITTER_DAYS, JITTER_DAYS, size=N)
    if _use_skyfield:
        elong_cells = np.interp(jd_jittered, jd_dense_full, elong_dense,
                                left=np.nan, right=np.nan)
        seq = (elong_cells > ELONG_THRESHOLD).astype(float)
    else:
        t_jittered = jd_jittered - ajd
        elong = VENUS_AMP * np.abs(np.cos(2.0 * np.pi * t_jittered / VENUS_PERIOD))
        seq = (elong > ELONG_THRESHOLD).astype(float)
    VENUS_JITTER_MAT[:, k] = seq

vj_valid = VENUS_JITTER_MAT.var(axis=0) > 0
VENUS_JITTER_MAT = VENUS_JITTER_MAT[:, vj_valid]
print(f"Venus+jitter válidas: {VENUS_JITTER_MAT.shape[1]}  |  "
      f"Densidad media: {VENUS_JITTER_MAT.mean():.4f}")

# ──────────────────────────────────────────────────────────────────────────────
# 3. PSEUDO-VENUS RECALIBRADOS A DENSIDAD ~0.400
#
# Estrategia: para cada período, buscar la amplitud que iguale la densidad media
# de Venus (0.400) con tolerancia ±0.005, via búsqueda binaria sobre amplitud.
# ──────────────────────────────────────────────────────────────────────────────
TARGET_DENSITY = venus_density
DENSITY_TOL    = 0.005

PSEUDO_PERIODS = {
    'P=300d':       300,
    'P=400d':       400,
    'P=480d':       480,
    'P=530d':       530,
    'P=640d':       640,
    'P=700d':       700,
    'P=780d(Marte)': 780,
    'P=900d':       900,
}

def calibrate_amplitude(period, target_density, tol=0.005,
                         amp_lo=10.0, amp_hi=89.9, max_iter=60):
    """Búsqueda binaria sobre amplitud para igualar densidad objetivo."""
    for _ in range(max_iter):
        amp_mid = (amp_lo + amp_hi) / 2.0
        # Promediamos densidad sobre todos los anchors (misma amplitud, mismo
        # período, distintos offsets de fase)
        seqs = np.stack([
            build_seq_sinusoidal(ajd, period, amp_mid)
            for ajd in anchors_valid
        ], axis=1)
        density = seqs.mean()
        if abs(density - target_density) < tol:
            return amp_mid, density
        if density < target_density:
            amp_hi = amp_mid
        else:
            amp_lo = amp_mid
    return amp_mid, density

print(f"\nCalibrando amplitudes (densidad objetivo = {TARGET_DENSITY:.4f}):")
PSEUDO_MATS = {}
pseudo_densities = {}
for name, period in PSEUDO_PERIODS.items():
    amp_cal, dens_cal = calibrate_amplitude(period, TARGET_DENSITY)
    mat = np.stack([
        build_seq_sinusoidal(ajd, period, amp_cal)
        for ajd in anchors_valid
    ], axis=1)
    col_valid = mat.var(axis=0) > 0
    PSEUDO_MATS[name] = mat[:, col_valid]
    pseudo_densities[name] = dens_cal
    print(f"  {name:18s}: período={period}d  amp_cal={amp_cal:.2f}°  "
          f"densidad={dens_cal:.4f}  seqs_válidas={col_valid.sum()}")

# ──────────────────────────────────────────────────────────────────────────────
# 4. TODAS LAS FAMILIAS
# ──────────────────────────────────────────────────────────────────────────────
all_families = {'Venus': VENUS_MAT,
                'Venus+jitter': VENUS_JITTER_MAT}
all_families.update(PSEUDO_MATS)
family_names = list(all_families.keys())
print(f"\nFamilias totales: {len(family_names)}: {family_names}")

# ──────────────────────────────────────────────────────────────────────────────
# 5. OHE GLOBAL Y UTILIDADES
# ──────────────────────────────────────────────────────────────────────────────
_ohe_global = OneHotEncoder(drop='first', sparse_output=False)
X_BASE_FULL = _ohe_global.fit_transform(
    np.column_stack([rows_idx, cols_idx]))   # (112, 20)

def get_X_base(mask):
    return X_BASE_FULL[mask]

def fit_logit(y, X, max_iter=500):
    clf = LogisticRegression(penalty=None, solver='lbfgs',
                             fit_intercept=True, max_iter=max_iter, tol=1e-8)
    clf.fit(X, y)
    mu = np.clip(clf.predict_proba(X)[:, 1], 1e-10, 1 - 1e-10)
    ll = float(np.sum(y * np.log(mu) + (1 - y) * np.log(1 - mu)))
    return mu, ll, clf

def score_stats_vec(y, mu, X_base, VENUS):
    W    = mu * (1.0 - mu)
    r    = y - mu
    WX   = W[:, None] * X_base
    XtWX = X_base.T @ WX
    XtWX_inv = np.linalg.solve(XtWX + 1e-10 * np.eye(XtWX.shape[0]),
                                np.eye(XtWX.shape[0]))
    num2 = (VENUS.T @ r) ** 2
    d1   = (VENUS ** 2).T @ W
    VtWX = VENUS.T @ WX
    d2   = np.sum((VtWX @ XtWX_inv) * VtWX, axis=1)
    denom = d1 - d2
    return np.where(denom > 1e-12, num2 / denom, 0.0)

# ──────────────────────────────────────────────────────────────────────────────
# 6. LOOP LORO
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("LORO 4e-bis: 8 folds, familias recalibradas + Venus+jitter")
print("="*65)

results_ll     = {name: np.zeros(N_ROWS) for name in family_names}
results_best_k = {name: np.zeros(N_ROWS, dtype=int) for name in family_names}

for fold, test_row in enumerate(range(N_ROWS)):
    train_mask = rows_idx != test_row
    test_mask  = rows_idx == test_row

    y_train = y_obs[train_mask]
    y_test  = y_obs[test_mask]

    X_base_train = get_X_base(train_mask)
    X_base_test  = get_X_base(test_mask)

    mu_train, ll_base_train, clf_base = fit_logit(y_train, X_base_train)

    mu_test_base = np.clip(
        clf_base.predict_proba(X_base_test)[:, 1], 1e-10, 1-1e-10)
    ll_base_test = float(np.sum(
        y_test * np.log(mu_test_base) + (1-y_test) * np.log(1-mu_test_base)))

    print(f"\n  Fold {fold+1}/8 — F{test_row+1} retenida "
          f"(eventos={int(y_test.sum())}/{N_COLS})")

    for name, MAT in all_families.items():
        MAT_train = MAT[train_mask, :]
        MAT_test  = MAT[test_mask,  :]

        # Selección del mejor anchor en train
        sc_train = score_stats_vec(y_train, mu_train, X_base_train, MAT_train)
        best_k   = int(np.argmax(sc_train))

        # Ajuste base+mejor_anchor en train, predicción en test
        X_aug_train = np.column_stack([X_base_train, MAT_train[:, best_k]])
        clf_aug = LogisticRegression(penalty=None, solver='lbfgs',
                                     fit_intercept=True, max_iter=1000, tol=1e-8)
        clf_aug.fit(X_aug_train, y_train)

        X_aug_test  = np.column_stack([X_base_test, MAT_test[:, best_k]])
        mu_test_aug = np.clip(
            clf_aug.predict_proba(X_aug_test)[:, 1], 1e-10, 1-1e-10)
        ll_aug_test = float(np.sum(
            y_test * np.log(mu_test_aug) + (1-y_test) * np.log(1-mu_test_aug)))

        delta = ll_aug_test - ll_base_test
        results_ll[name][fold]     = delta
        results_best_k[name][fold] = best_k

        marker = " ← VENUS" if name == 'Venus' else \
                 " ← JITTER" if name == 'Venus+jitter' else ""
        print(f"    {name:20s}: train_score={sc_train[best_k]:5.2f}  "
              f"Δlog-lik_test={delta:+.3f}{marker}")

# ──────────────────────────────────────────────────────────────────────────────
# 7. RESULTADOS AGREGADOS
# ──────────────────────────────────────────────────────────────────────────────
means   = {n: results_ll[n].mean() for n in family_names}
stds    = {n: results_ll[n].std()  for n in family_names}
ranking = sorted(family_names, key=lambda n: means[n], reverse=True)

print("\n" + "="*65)
print("RESULTADOS AGREGADOS — Δlog-lik media ± std (8 folds)")
print("="*65)
for rank, name in enumerate(ranking, 1):
    tag = " ◄ VENUS" if name == 'Venus' else \
          " ◄ JITTER" if name == 'Venus+jitter' else ""
    print(f"  #{rank:2d}  {name:22s}: media={means[name]:+.4f}  "
          f"std={stds[name]:.4f}{tag}")

venus_rank = ranking.index('Venus') + 1
jitter_rank = ranking.index('Venus+jitter') + 1 if 'Venus+jitter' in ranking else '?'
print(f"\nVenus: rango #{venus_rank} de {len(family_names)}")
print(f"Venus+jitter: rango #{jitter_rank} de {len(family_names)}")

# Folds donde Venus bate a todos los pseudo
venus_delta = results_ll['Venus']
print(f"\nFolds donde Venus > pseudo-Venus calibrados (de 8):")
venus_beats = np.zeros(N_ROWS, dtype=int)
for fold in range(N_ROWS):
    vv = results_ll['Venus'][fold]
    n_beaten = sum(1 for n in PSEUDO_MATS if results_ll[n][fold] < vv)
    venus_beats[fold] = n_beaten
    print(f"  F{fold+1}: Venus={vv:+.3f} | bate a {n_beaten}/{len(PSEUDO_MATS)} pseudo")

# Mejor pseudo calibrado
best_pseudo_name = max(PSEUDO_MATS, key=lambda n: means[n])
best_pseudo_mean = means[best_pseudo_name]
delta_v_vs_best  = means['Venus'] - best_pseudo_mean
print(f"\nMejor pseudo calibrado: {best_pseudo_name}  (media={best_pseudo_mean:+.4f})")
print(f"Ventaja Venus sobre mejor pseudo: Δ={delta_v_vs_best:+.4f}")

# Bootstrap
N_BOOT     = 99999
rng_boot   = np.random.default_rng(RANDOM_SEED_4EBIS + 1)
diff_obs   = results_ll['Venus'] - results_ll[best_pseudo_name]
diff_mean  = diff_obs.mean()
diff_c     = diff_obs - diff_mean
boot_means = np.array([
    rng_boot.choice(diff_c, size=N_ROWS, replace=True).mean()
    for _ in range(N_BOOT)
])
p_boot = float(np.mean(np.abs(boot_means) >= np.abs(diff_mean)))

print(f"\nBootstrap Venus vs mejor pseudo calibrado ({best_pseudo_name}):")
print(f"  Diferencia media = {diff_mean:+.4f}  |  p_bootstrap = {p_boot:.4f}")

# ──────────────────────────────────────────────────────────────────────────────
# 8. FIGURA
# ──────────────────────────────────────────────────────────────────────────────
n_fam = len(family_names)
colors_all = {}
for name in family_names:
    if name == 'Venus':
        colors_all[name] = '#c0392b'
    elif name == 'Venus+jitter':
        colors_all[name] = '#e67e22'
    else:
        cmap = plt.cm.tab10
        idx  = list(PSEUDO_MATS.keys()).index(name)
        colors_all[name] = cmap(idx / max(len(PSEUDO_MATS)-1, 1) * 0.85)

fig = plt.figure(figsize=(16, 10))
gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.40, wspace=0.32)

# Panel A — Δlog-lik por fold
ax0 = fig.add_subplot(gs[0, :])
x_folds = np.arange(N_ROWS)
width   = 0.072
offsets = np.linspace(-0.38, 0.38, n_fam)
for i, name in enumerate(family_names):
    zorder = 5 if name in ('Venus', 'Venus+jitter') else 2
    lw     = 1.8 if name in ('Venus', 'Venus+jitter') else 0.4
    ax0.bar(x_folds + offsets[i], results_ll[name],
            width=width, color=colors_all[name], alpha=0.85,
            linewidth=lw, edgecolor='white', zorder=zorder, label=name)
ax0.axhline(0, color='black', lw=0.8)
ax0.set_xlabel('Fila retenida (fold LORO)', fontsize=10)
ax0.set_ylabel('Δ log-lik en fila retenida', fontsize=10)
ax0.set_title('Ganancia predictiva fuera de muestra: Venus vs controles calibrados',
              fontsize=10)
ax0.set_xticks(x_folds)
ax0.set_xticklabels([f'F{r+1}' for r in range(N_ROWS)])
ax0.legend(fontsize=8, ncol=3, loc='upper right')

# Panel B — media ± SE
ax1 = fig.add_subplot(gs[1, 0])
sorted_names = ranking[:]
bars_c = [colors_all[n] for n in sorted_names]
ax1.bar(range(len(sorted_names)),
        [means[n] for n in sorted_names],
        yerr=[stds[n]/np.sqrt(N_ROWS) for n in sorted_names],
        color=bars_c, alpha=0.85, capsize=4,
        edgecolor='white', linewidth=0.5)
ax1.axhline(0, color='black', lw=0.8)
ax1.set_xticks(range(len(sorted_names)))
ax1.set_xticklabels(sorted_names, rotation=38, ha='right', fontsize=8)
ax1.set_ylabel('Δ log-lik medio (±SE)', fontsize=10)
ax1.set_title('Ganancia media (8 folds) — familias calibradas', fontsize=10)

# Panel C — Venus vs mejor pseudo calibrado
ax2 = fig.add_subplot(gs[1, 1])
ax2.bar(x_folds, diff_obs,
        color=[colors_all['Venus'] if d > 0 else '#95a5a6' for d in diff_obs],
        alpha=0.85, edgecolor='white', linewidth=0.5)
ax2.axhline(0, color='black', lw=0.8)
ax2.axhline(diff_mean, color=colors_all['Venus'], lw=1.5, linestyle='--',
            label=f'Media = {diff_mean:+.3f}')
ax2.set_xlabel('Fila retenida', fontsize=10)
ax2.set_ylabel(f'Δlog-lik Venus − {best_pseudo_name}', fontsize=9)
ax2.set_title(f'Venus vs mejor pseudo calibrado ({best_pseudo_name})\n'
              f'p_bootstrap = {p_boot:.4f}', fontsize=10)
ax2.set_xticks(x_folds)
ax2.set_xticklabels([f'F{r+1}' for r in range(N_ROWS)])
ax2.legend(fontsize=9)

fig.suptitle(
    f'Fase 4e-bis — Especificidad Venus (pseudo calibrados + jitter) | '
    f'Venus rango #{venus_rank}/{len(family_names)} | '
    f'p_bootstrap={p_boot:.4f}',
    fontsize=11, y=1.01
)
plt.savefig('../results/fig29_fase4ebis_calibrated.png',
            dpi=150, bbox_inches='tight')
plt.show()
print("\nFigura guardada: results/fig29_fase4ebis_calibrated.png")

# ──────────────────────────────────────────────────────────────────────────────
# 9. GUARDAR Y SÍNTESIS FINAL
# ──────────────────────────────────────────────────────────────────────────────
resultados_4ebis = {
    'delta_ll_per_fold':  results_ll,
    'means':              means,
    'stds':               stds,
    'ranking':            ranking,
    'venus_rank':         venus_rank,
    'jitter_rank':        jitter_rank,
    'p_bootstrap':        p_boot,
    'diff_mean_obs':      diff_mean,
    'best_pseudo_name':   best_pseudo_name,
    'delta_venus_vs_best': delta_v_vs_best,
    'venus_beats_per_fold': venus_beats,
    'pseudo_densities':   pseudo_densities,
    'venus_density':      float(venus_density),
}
np.save('../results/fase4ebis_resultados.npy', resultados_4ebis)
print("Resultados guardados: results/fase4ebis_resultados.npy")

# Síntesis completa 4d + 4e + 4e-bis
print("\n" + "="*70)
print("SÍNTESIS FINAL — Fases 4d + 4e + 4e-bis — Hipótesis Venus")
print("="*70)
print(f"  4d  : Venus supera nulo fila+columna (fixed-margin)  p = 0.0341  ✓")
print(f"  4e  : Venus rango #9/9 (pseudo sin calibrar)         p_boot = 0.4377")
print(f"  4e-b: Venus rango #{venus_rank}/{len(family_names)} (pseudo calibrados)")
print(f"        p_bootstrap Venus > mejor pseudo               p_boot = {p_boot:.4f}")
print()

if venus_rank <= 2 and p_boot < 0.05:
    conclusion = ("La señal supera el nulo (4d) Y es específica del período "
                  "venusino frente a controles calibrados. Evidencia moderada "
                  "de especificidad astronómica.")
elif p_boot >= 0.10:
    conclusion = ("La señal supera el nulo estructurado (4d) pero NO es "
                  "específica del período Venus en comparación con controles "
                  "periódicos calibrados a igual densidad. Venus queda como "
                  "hipótesis compatible, no apoyada específicamente. "
                  "Caso cerrado.")
else:
    conclusion = ("Resultado marginal. Señal sobre nulo (4d) pero "
                  "especificidad venusina débil (0.05 ≤ p < 0.10).")

print(f"  CONCLUSIÓN: {conclusion}")
print("="*70)
