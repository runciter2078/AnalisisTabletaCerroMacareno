# =============================================================================
# FASE 4e — Especificidad Venus vs pseudo-Venus con validación LORO
#
# Pregunta: ¿es la señal Venus (p=0.034, Fase 4d) ESPECÍFICAMENTE venusina,
# o la reproduce igual cualquier patrón periódico comparable?
#
# Diseño:
#   - 8 familias de pseudo-Venus con períodos sinódicos distintos al de Venus
#     (300, 400, 480, 530, 640, 700, 780, 900 días)
#   - Mismos 226 anchors JD que Venus → comparación estrictamente apples-to-apples
#   - Métrica: Δlog-lik(modelo+Venus) − Δlog-lik(modelo_base) en fila retenida
#   - 8 folds LORO (Leave-One-Row-Out) → ~14 celdas de test por fold
#   - Veredicto: ¿Venus supera de forma consistente a todos los pseudo-Venus?
#
# Dependencias del kernel (Fase 4d):
#   M_bin, resultados_4d (o fase4d_resultados.npy)
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings('ignore')

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder

RANDOM_SEED_4E = 42 + 500

# ──────────────────────────────────────────────────────────────────────────────
# 0. CARGA DE DATOS Y RESULTADOS FASE 4d
# ──────────────────────────────────────────────────────────────────────────────
try:
    y_obs = M_bin.values.astype(float).ravel()
    print("M_bin cargado desde kernel.")
except NameError:
    import openpyxl
    df_raw = pd.read_excel('../data/tableta.xlsx', header=None)
    y_obs = (df_raw.values == 1).astype(float).ravel()
    print("M_bin cargado desde disco.")

try:
    anchors_jd = resultados_4d['anchors_jd_valid'].copy()
    VENUS_MATRIX_full = None   # se reconstruirá abajo si es necesario
    print("resultados_4d disponible en kernel.")
    _r4d_in_kernel = True
except NameError:
    r4d = np.load('../results/fase4d_resultados.npy', allow_pickle=True).item()
    anchors_jd = r4d['anchors_jd_valid'].copy()
    _r4d_in_kernel = False
    print("resultados_4d cargado desde disco.")

M_obs_2d = y_obs.reshape(8, 14).astype(int)
N_ROWS, N_COLS = 8, 14
N = N_ROWS * N_COLS
rows_idx = np.repeat(np.arange(N_ROWS), N_COLS)
cols_idx = np.tile(np.arange(N_COLS), N_ROWS)

SYNODIC_MONTH = 29.53058867
K = len(anchors_jd)
print(f"Anchors disponibles: {K}  |  Eventos en tableta: {M_obs_2d.sum()}")

# ──────────────────────────────────────────────────────────────────────────────
# 1. RECONSTRUIR VENUS_MATRIX (112 × K) si no está en memoria
# ──────────────────────────────────────────────────────────────────────────────
# Para Venus usamos el mismo grid de elongaciones que en Fase 4d.
# Si Skyfield y el grid están en el kernel, los reutilizamos.
# Si no, usamos el modelo sinusoidal de Venus como aproximación rápida
# (período 583.92 días, amplitud 47°, umbral 35°) — produce secuencias
# estadísticamente equivalentes para este test.

ELONG_THRESHOLD = 35.0
VENUS_PERIOD    = 583.92    # días (período sinódico medio)
VENUS_AMP       = 47.0      # grados (elongación máxima media)


def build_seq_sinusoidal(anchor_jd, period, amplitude=47.0, threshold=35.0):
    """
    Secuencia binaria de 112 celdas usando modelo sinusoidal de elongación.
    La célula m corresponde a JD = anchor_jd + m * SYNODIC_MONTH.
    elong(t) = amplitude * |cos(2π * (t - anchor_jd) / period)|
    Marca 1 si elong > threshold.
    """
    months = np.arange(N)
    t_days = months * SYNODIC_MONTH
    elong  = amplitude * np.abs(np.cos(2.0 * np.pi * t_days / period))
    return (elong > threshold).astype(float)


def build_venus_seq_skyfield(anchor_jd, jd_grid, elong_grid):
    """Secuencia Venus desde efemérides reales (si disponibles)."""
    months    = np.arange(N)
    jd_cells  = anchor_jd + months * SYNODIC_MONTH
    elong_cells = np.interp(jd_cells, jd_grid, elong_grid,
                            left=np.nan, right=np.nan)
    return (elong_cells > ELONG_THRESHOLD).astype(float)


# Intentar usar efemérides reales para Venus; si no, sinusoidal
_use_skyfield = False
try:
    _ = jd_dense_full   # variable del kernel (Fase 4b/4c)
    _ = elong_dense
    _use_skyfield = True
    print("Usando efemérides Skyfield para Venus.")
except NameError:
    print("Skyfield no disponible → modelo sinusoidal para Venus (aprox. equivalente).")

print(f"\nPrecomputando secuencias Venus ({K} anchors)...")
VENUS_MAT = np.zeros((N, K))
for k, ajd in enumerate(anchors_jd):
    if _use_skyfield:
        VENUS_MAT[:, k] = build_venus_seq_skyfield(ajd, jd_dense_full, elong_dense)
    else:
        VENUS_MAT[:, k] = build_seq_sinusoidal(ajd, VENUS_PERIOD, VENUS_AMP)

# Filtrar columnas constantes
valid = VENUS_MAT.var(axis=0) > 0
VENUS_MAT = VENUS_MAT[:, valid]
anchors_valid = anchors_jd[valid]
K_v = VENUS_MAT.shape[1]
print(f"Secuencias Venus válidas: {K_v}")

# ──────────────────────────────────────────────────────────────────────────────
# 2. FAMILIAS PSEUDO-VENUS
# ──────────────────────────────────────────────────────────────────────────────
# Períodos escogidos para cubrir: por debajo de Venus, por encima, y Mars.
# Amplitudes ajustadas para densidad comparable (~40% de celdas activas).
# Venus real: 584d, amplitud 47° → densidad ≈ 37-42%
# Para cada pseudo, mismos anchors JD → comparación apples-to-apples.

PSEUDO_VENUS = {
    'P=300d':  dict(period=300,  amplitude=46.0),
    'P=400d':  dict(period=400,  amplitude=46.0),
    'P=480d':  dict(period=480,  amplitude=46.5),
    'P=530d':  dict(period=530,  amplitude=46.5),
    'P=640d':  dict(period=640,  amplitude=47.0),
    'P=700d':  dict(period=700,  amplitude=47.0),
    'P=780d (Marte)': dict(period=780, amplitude=47.0),
    'P=900d':  dict(period=900,  amplitude=47.5),
}

print(f"\nPrecomputando {len(PSEUDO_VENUS)} familias pseudo-Venus ({K_v} anchors c/u)...")
PSEUDO_MATS = {}
for name, params in PSEUDO_VENUS.items():
    mat = np.zeros((N, K_v))
    for k, ajd in enumerate(anchors_valid):
        mat[:, k] = build_seq_sinusoidal(ajd, params['period'], params['amplitude'])
    col_valid = mat.var(axis=0) > 0
    PSEUDO_MATS[name] = mat[:, col_valid]
    print(f"  {name}: {col_valid.sum()} secuencias válidas  "
          f"(densidad media = {mat.mean():.3f})")

print(f"\nVenus real (Skyfield): densidad media = {VENUS_MAT.mean():.3f}")

# ──────────────────────────────────────────────────────────────────────────────
# 3. UTILIDADES COMPARTIDAS
# ──────────────────────────────────────────────────────────────────────────────
def make_X_base(r_idx, c_idx):
    """One-hot fila+columna (drop first) para índices dados."""
    ohe = OneHotEncoder(drop='first', sparse_output=False)
    return ohe.fit_transform(np.column_stack([r_idx, c_idx]))


def fit_logit(y, X, max_iter=500):
    """Logit sin penalización. Devuelve (mu, log-lik)."""
    clf = LogisticRegression(penalty=None, solver='lbfgs',
                             fit_intercept=True, max_iter=max_iter, tol=1e-8)
    clf.fit(X, y)
    mu = np.clip(clf.predict_proba(X)[:, 1], 1e-10, 1 - 1e-10)
    ll = float(np.sum(y * np.log(mu) + (1 - y) * np.log(1 - mu)))
    return mu, ll, clf


def score_stats_vec(y, mu, X_base, VENUS):
    """Score (Rao LM) stats vectorizados — mismo que Fase 4d."""
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


def predict_logit_plus_covariate(clf_base, X_base_train, best_vec_train,
                                  X_base_test,  best_vec_test, y_train):
    """
    Ajusta logit(y_train ~ X_base + best_vec) y evalúa log-lik en test.
    Devuelve delta_ll_test = ll_test(base+venus) - ll_test(base).
    """
    # Modelo base + covariable Venus sobre entrenamiento
    X_aug = np.column_stack([X_base_train, best_vec_train])
    clf_aug = LogisticRegression(penalty=None, solver='lbfgs',
                                  fit_intercept=True, max_iter=1000, tol=1e-8)
    clf_aug.fit(X_aug, y_train)

    # Predicción en test
    X_test_aug  = np.column_stack([X_base_test, best_vec_test])
    mu_test_aug = np.clip(clf_aug.predict_proba(X_test_aug)[:, 1], 1e-10, 1-1e-10)
    mu_test_base = np.clip(clf_base.predict_proba(X_base_test)[:, 1],  1e-10, 1-1e-10)

    # Log-lik en test (solo las celdas de la fila retenida)
    # y_test necesita inferirse: no lo pasamos, se calcula fuera
    return mu_test_aug, mu_test_base


# ──────────────────────────────────────────────────────────────────────────────
# 4. LOOP LORO: 8 folds, 1 fila retenida por fold
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("LORO: 8 folds (cada fold retiene 1 fila)")
print("="*60)

all_families = {'Venus': VENUS_MAT}
all_families.update(PSEUDO_MATS)
family_names = list(all_families.keys())

# Resultados: delta_ll_test por fold y familia
# delta_ll_test = ll_test(base+familia) - ll_test(base_solo)
results_ll  = {name: np.zeros(N_ROWS) for name in family_names}
results_best_k = {name: np.zeros(N_ROWS, dtype=int) for name in family_names}

for fold, test_row in enumerate(range(N_ROWS)):
    # Máscaras de entrenamiento y test
    train_mask = rows_idx != test_row
    test_mask  = rows_idx == test_row

    y_train = y_obs[train_mask]
    y_test  = y_obs[test_mask]
    r_train = rows_idx[train_mask]
    c_train = cols_idx[train_mask]
    r_test  = rows_idx[test_mask]
    c_test  = cols_idx[test_mask]

    X_base_train = make_X_base(r_train, c_train)
    X_base_test  = make_X_base(r_test,  c_test)

    # Modelo base sobre entrenamiento
    mu_train, ll_base_train, clf_base_train = fit_logit(y_train, X_base_train)

    # Log-lik base en test
    mu_test_base_only = np.clip(
        clf_base_train.predict_proba(X_base_test)[:, 1], 1e-10, 1-1e-10)
    ll_base_test = float(np.sum(
        y_test * np.log(mu_test_base_only) +
        (1 - y_test) * np.log(1 - mu_test_base_only)))

    fold_msg = f"Fold {fold+1}/8 (fila retenida = F{test_row+1}, " \
               f"eventos={int(y_test.sum())}/{N_COLS})"
    print(f"\n  {fold_msg}")

    for name, MAT in all_families.items():
        # Score stats en datos de entrenamiento para elegir mejor anchor
        scores_train = score_stats_vec(y_train, mu_train,
                                        X_base_train, MAT[train_mask, :])
        best_k  = int(np.argmax(scores_train))
        best_sc = scores_train[best_k]

        # Ajustar modelo base + mejor anchor, predecir en test
        mu_test_aug, mu_test_base = predict_logit_plus_covariate(
            clf_base_train,
            X_base_train, MAT[train_mask, best_k],
            X_base_test,  MAT[test_mask,  best_k],
            y_train
        )

        # Delta log-lik en test
        ll_aug_test = float(np.sum(
            y_test * np.log(mu_test_aug) + (1 - y_test) * np.log(1 - mu_test_aug)))
        delta = ll_aug_test - ll_base_test

        results_ll[name][fold]     = delta
        results_best_k[name][fold] = best_k

        marker = " ← VENUS" if name == 'Venus' else ""
        print(f"    {name:22s}: train_score={best_sc:.2f}  "
              f"Δlog-lik_test={delta:+.3f}{marker}")

# ──────────────────────────────────────────────────────────────────────────────
# 5. RESULTADOS AGREGADOS
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("RESULTADOS AGREGADOS — Δlog-lik en fila retenida (media ± std)")
print("="*60)

means = {n: results_ll[n].mean() for n in family_names}
stds  = {n: results_ll[n].std()  for n in family_names}

# Ranking
ranking = sorted(family_names, key=lambda n: means[n], reverse=True)

for rank, name in enumerate(ranking, 1):
    marker = " ◄ VENUS" if name == 'Venus' else ""
    print(f"  #{rank:1d}  {name:24s}: media={means[name]:+.4f}  "
          f"std={stds[name]:.4f}{marker}")

# Venus vs cada pseudo-Venus: folds donde Venus gana
venus_delta = results_ll['Venus']
print(f"\nFolds donde Venus > pseudo-Venus (de 8):")
venus_rank_per_fold = np.zeros(N_ROWS, dtype=int)
for fold in range(N_ROWS):
    venus_val = results_ll['Venus'][fold]
    n_beaten  = sum(1 for n in PSEUDO_MATS if results_ll[n][fold] < venus_val)
    venus_rank_per_fold[fold] = n_beaten
    print(f"  F{fold+1}: Venus={venus_val:+.3f} | bate a {n_beaten}/{len(PSEUDO_MATS)} pseudo-Venus")

print(f"\nVenus bate a TODOS los pseudo-Venus en {(venus_rank_per_fold == len(PSEUDO_MATS)).sum()}/8 folds")
print(f"Venus ocupa rango #1 en media: {means['Venus'] == max(means.values())}")

# Δ entre Venus y el mejor pseudo-Venus
best_pseudo_mean = max(means[n] for n in PSEUDO_MATS)
best_pseudo_name = max(PSEUDO_MATS, key=lambda n: means[n])
delta_venus_vs_best = means['Venus'] - best_pseudo_mean
print(f"\nMejor pseudo-Venus: {best_pseudo_name}  (media={best_pseudo_mean:+.4f})")
print(f"Ventaja Venus sobre mejor pseudo: Δ={delta_venus_vs_best:+.4f}")

# ──────────────────────────────────────────────────────────────────────────────
# 6. TEST DE SIGNIFICACIÓN BOOTSTRAP (sobre los 8 folds)
# ──────────────────────────────────────────────────────────────────────────────
# Pregunta: ¿es la ventaja media de Venus sobre el mejor pseudo-Venus
# estadísticamente distinguible de 0?
# Con solo 8 puntos usamos bootstrap sobre los folds.

N_BOOT = 99999
rng_boot = np.random.default_rng(RANDOM_SEED_4E)

# Diferencia observada: Venus - mejor pseudo-Venus, fold a fold
best_pseudo_deltas = results_ll[best_pseudo_name]
diff_obs = venus_delta - best_pseudo_deltas    # (8,) diferencia por fold
diff_mean_obs = diff_obs.mean()

# Bootstrap bajo H0: Venus no mejor → centrar en 0
diff_centered = diff_obs - diff_obs.mean()
boot_means = np.array([
    rng_boot.choice(diff_centered, size=N_ROWS, replace=True).mean()
    for _ in range(N_BOOT)
])
p_bootstrap = float(np.mean(np.abs(boot_means) >= np.abs(diff_mean_obs)))

print(f"\nTest bootstrap (n_boot={N_BOOT}):")
print(f"  Diferencia media Venus−mejor_pseudo = {diff_mean_obs:+.4f}")
print(f"  p-valor bootstrap (bilateral)       = {p_bootstrap:.4f}")

if p_bootstrap < 0.05:
    print("  → Venus supera significativamente al mejor pseudo-Venus (p<0.05)")
elif p_bootstrap < 0.10:
    print("  → Señal marginal (0.05 ≤ p < 0.10). No concluyente.")
else:
    print("  → Venus NO supera significativamente a los pseudo-Venus (p≥0.10).")
    print("    La señal del Test 1 no es específica del período Venus.")

# ──────────────────────────────────────────────────────────────────────────────
# 7. FIGURA
# ──────────────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(15, 10))
gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.38, wspace=0.32)

colors_pseudo = plt.cm.tab10(np.linspace(0.1, 0.9, len(PSEUDO_MATS)))
venus_color   = '#c0392b'

# Panel A — Δlog-lik por fold para cada familia
ax0 = fig.add_subplot(gs[0, :])
x_folds = np.arange(N_ROWS)
width   = 0.08
offsets = np.linspace(-0.36, 0.36, len(family_names))

for i, name in enumerate(family_names):
    color  = venus_color if name == 'Venus' else colors_pseudo[i-1]
    lw     = 2.0 if name == 'Venus' else 0.6
    zorder = 5 if name == 'Venus' else 2
    alpha  = 1.0 if name == 'Venus' else 0.7
    ax0.bar(x_folds + offsets[i], results_ll[name],
            width=width, color=color, alpha=alpha,
            linewidth=lw, edgecolor='white', zorder=zorder,
            label=name)

ax0.axhline(0, color='black', lw=0.8, linestyle='-')
ax0.set_xlabel('Fila retenida (fold LORO)', fontsize=10)
ax0.set_ylabel('Δ log-lik en fila retenida', fontsize=10)
ax0.set_title('Ganancia predictiva fuera de muestra por fold: Venus vs pseudo-Venus',
              fontsize=10)
ax0.set_xticks(x_folds)
ax0.set_xticklabels([f'F{r+1}' for r in range(N_ROWS)])
ax0.legend(fontsize=8, ncol=3, loc='upper right')

# Panel B — Media ± std por familia
ax1 = fig.add_subplot(gs[1, 0])
sorted_names = sorted(family_names, key=lambda n: means[n], reverse=True)
colors_sorted = []
for n in sorted_names:
    colors_sorted.append(venus_color if n == 'Venus' else '#7f8c8d')

bars = ax1.bar(range(len(sorted_names)),
               [means[n] for n in sorted_names],
               yerr=[stds[n]/np.sqrt(N_ROWS) for n in sorted_names],
               color=colors_sorted, alpha=0.85, capsize=4,
               edgecolor='white', linewidth=0.5)
ax1.axhline(0, color='black', lw=0.8)
ax1.set_xticks(range(len(sorted_names)))
ax1.set_xticklabels(sorted_names, rotation=35, ha='right', fontsize=8)
ax1.set_ylabel('Δ log-lik medio (±SE)', fontsize=10)
ax1.set_title('Ganancia media fuera de muestra (8 folds)', fontsize=10)

# Panel C — Ventaja Venus vs mejor pseudo-Venus (diferencia por fold)
ax2 = fig.add_subplot(gs[1, 1])
ax2.bar(x_folds, diff_obs,
        color=[venus_color if d > 0 else '#7f8c8d' for d in diff_obs],
        alpha=0.85, edgecolor='white', linewidth=0.5)
ax2.axhline(0, color='black', lw=0.8)
ax2.axhline(diff_mean_obs, color=venus_color, lw=1.5, linestyle='--',
            label=f'Media = {diff_mean_obs:+.3f}')
ax2.set_xlabel('Fila retenida', fontsize=10)
ax2.set_ylabel(f'Δlog-lik Venus − {best_pseudo_name}', fontsize=9)
ax2.set_title(f'Venus vs mejor pseudo ({best_pseudo_name})\n'
              f'p_bootstrap={p_bootstrap:.4f}', fontsize=10)
ax2.set_xticks(x_folds)
ax2.set_xticklabels([f'F{r+1}' for r in range(N_ROWS)])
ax2.legend(fontsize=9)

fig.suptitle(
    f'Fase 4e — Especificidad Venus | LORO 8-fold | '
    f'p_bootstrap={p_bootstrap:.4f} | '
    f'Venus rango #{ranking.index("Venus")+1} de {len(family_names)}',
    fontsize=11, y=1.01
)

plt.savefig('../results/fig28_fase4e_LORO_specificity.png',
            dpi=150, bbox_inches='tight')
plt.show()
print("\nFigura guardada: results/fig28_fase4e_LORO_specificity.png")

# ──────────────────────────────────────────────────────────────────────────────
# 8. GUARDAR
# ──────────────────────────────────────────────────────────────────────────────
resultados_4e = {
    'delta_ll_per_fold': results_ll,
    'means':             means,
    'stds':              stds,
    'ranking':           ranking,
    'p_bootstrap':       p_bootstrap,
    'diff_mean_obs':     diff_mean_obs,
    'best_pseudo_name':  best_pseudo_name,
    'delta_venus_vs_best': delta_venus_vs_best,
    'venus_rank_per_fold': venus_rank_per_fold,
}
np.save('../results/fase4e_resultados.npy', resultados_4e)
print("Resultados guardados: results/fase4e_resultados.npy")

# ──────────────────────────────────────────────────────────────────────────────
# 9. RESUMEN FINAL COMBINADO (Fases 4d + 4e)
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("SÍNTESIS FASES 4d + 4e — Hipótesis Venus")
print("="*65)
print(f"  Fase 4d: Venus supera nulo fixed-margin   p = 0.0341  ✓")
print(f"  Fase 4e: ranking Venus vs pseudo-Venus    #{ranking.index('Venus')+1}"
      f" de {len(family_names)}")
print(f"           p_bootstrap Venus>mejor_pseudo   {p_bootstrap:.4f}")
if p_bootstrap < 0.05:
    print("\n  CONCLUSIÓN: La señal es estadísticamente significativa Y específica")
    print("  del período Venus. Evidencia astronómica moderada-fuerte.")
elif p_bootstrap < 0.10:
    print("\n  CONCLUSIÓN: La señal supera el nulo (4d) pero la especificidad")
    print("  venusina es marginal. Compatible con Venus pero no exclusivo.")
else:
    print("\n  CONCLUSIÓN: La señal supera el nulo estructurado (4d) pero NO")
    print("  es específica del período Venus. Cualquier señal periódica")
    print("  comparable produce resultados similares. Venus queda como")
    print("  hipótesis compatible, no apoyada específicamente.")
print("="*65)
