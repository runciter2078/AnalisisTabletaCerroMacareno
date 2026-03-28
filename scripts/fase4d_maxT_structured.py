# =============================================================================
# FASE 4d — Test maxT con nulo estructurado (fila + columna)
# Pregunta: ¿añade Venus mejora de deviance MÁS ALLÁ del gradiente conocido?
#
# Diseño:
#   - Estadístico: max Δdeviance (score test) sobre ~236 anchors Venus
#   - Nulo: H0 = "solo gradiente fila+columna; sin Venus"
#   - Nulo implementado con matrices fixed-margin (Curveball, Strona et al. 2014)
#   - 9 999 réplicas permutacionales → p-valor FWER sin asumir independencia
#
# Coste computacional optimizado:
#   - Score test (Rao LM test) en lugar de LRT completo en el loop nulo
#   - Todas las secuencias Venus precomputadas como matriz (112 × K)
#   - sklearn LogisticRegression (saga) para velocidad en el loop
#   - ~2-5 min en total en hardware moderno
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings('ignore')

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from scipy.special import expit  # = sigmoid

RANDOM_SEED_4D = 42 + 400   # offset independiente del resto de fases

# ──────────────────────────────────────────────────────────────────────────────
# 0. CARGA DE DATOS
# ──────────────────────────────────────────────────────────────────────────────
# Intentamos usar las variables del kernel (si el notebook ya fue ejecutado).
# Si no están disponibles, recargamos desde disco.
try:
    y_obs = M_bin.values.astype(float).ravel()          # (112,)
    print("M_bin cargado desde kernel.")
except NameError:
    import openpyxl
    df_raw = pd.read_excel('../data/tableta.xlsx', header=None)
    y_obs = (df_raw.values == 1).astype(float).ravel()
    print("M_bin recargado desde disco (tableta.xlsx).")

M_obs_2d = y_obs.reshape(8, 14).astype(int)
N = len(y_obs)  # 112
rows_idx = np.repeat(np.arange(8), 14)    # índice de fila para cada celda
cols_idx = np.tile(np.arange(14), 8)      # índice de columna

print(f"Matriz: {M_obs_2d.shape}, total eventos = {M_obs_2d.sum()}")

# ──────────────────────────────────────────────────────────────────────────────
# 1. MATRIZ DE DISEÑO BASE (fila + columna, codificación one-hot)
# ──────────────────────────────────────────────────────────────────────────────
# Creamos X_base: one-hot para fila (8 categorías, drop first) +
#                  one-hot para columna (14 categorías, drop first)
# = 7 + 13 = 20 columnas + interceptro implícito en sklearn

ohe = OneHotEncoder(drop='first', sparse_output=False)
feat_base = np.column_stack([rows_idx, cols_idx])
X_base = ohe.fit_transform(feat_base)       # (112, 20)

print(f"X_base shape: {X_base.shape}  (7 dummies fila + 13 dummies columna)")

# ──────────────────────────────────────────────────────────────────────────────
# 2. MODELO BASE LOGIT: y ~ fila + columna
# ──────────────────────────────────────────────────────────────────────────────
def fit_logit_base(y, X):
    """Ajusta logit y ~ X. Devuelve (probabilidades ajustadas, log-verosimilitud)."""
    clf = LogisticRegression(
        penalty=None, solver='lbfgs', fit_intercept=True,
        max_iter=1000, tol=1e-8
    )
    clf.fit(X, y)
    mu = clf.predict_proba(X)[:, 1]
    mu = np.clip(mu, 1e-10, 1 - 1e-10)
    ll = np.sum(y * np.log(mu) + (1 - y) * np.log(1 - mu))
    return mu, ll, clf

mu_base, ll_base, clf_base = fit_logit_base(y_obs, X_base)
print(f"\nModelo base: log-lik = {ll_base:.4f}")
print(f"Predicciones base — rango mu: [{mu_base.min():.3f}, {mu_base.max():.3f}]")

# ──────────────────────────────────────────────────────────────────────────────
# 3. GRID DENSO DE ELONGACIONES VENUS (precálculo único con Skyfield)
# ──────────────────────────────────────────────────────────────────────────────
SYNODIC_MONTH = 29.53058867   # días
ELONG_THRESHOLD = 35.0        # grados; Venus visible ≈ elongación > 35°

try:
    # Intentar reutilizar objetos Skyfield del kernel (Fase 4b/4c)
    _ts   = ts
    _eph  = eph
    _earth = earth
    _venus = venus
    _sun  = sun
    print("\nObjetos Skyfield reutilizados del kernel.")
    _skyfield_from_kernel = True
except NameError:
    from skyfield.api import load as sky_load
    _ts   = sky_load.timescale()
    _eph  = sky_load('de406.bsp')          # debe estar en el path de trabajo
    _earth = _eph['earth']
    _venus = _eph['venus']
    _sun  = _eph['sun']
    print("\nObjetos Skyfield cargados (de406.bsp).")
    _skyfield_from_kernel = False

# Grid 5-día: 900 aC – 100 aC
# JD de -900 a.C.: año -899 (astronómico) ~ JD 1288438.5
# JD de -100 a.C.: año -99 (astronómico)  ~ JD 1577874.5
JD_START = 1228400.0    # ~ 1050 aC (margen extra)
JD_END   = 1640000.0    # ~  200 dC (margen extra)
STEP_DAYS = 5

print(f"Precalculando elongaciones Venus [{JD_START:.0f} – {JD_END:.0f}]"
      f" con paso {STEP_DAYS} días...")

jd_dense_full = np.arange(JD_START, JD_END, STEP_DAYS)
elong_dense   = np.empty(len(jd_dense_full))

BLOCK = 2000
for i in range(0, len(jd_dense_full), BLOCK):
    jd_block = jd_dense_full[i:i+BLOCK]
    t_block  = _ts.tt_jd(jd_block)
    astrometric = (_earth + _eph['earth-moon-barycenter'] -
                   _earth).at(t_block).observe(_venus) if False else \
                  _earth.at(t_block).observe(_venus).apparent()
    # elongación desde el Sol
    sun_pos    = _earth.at(t_block).observe(_sun).apparent()
    elong_block = astrometric.separation_from(sun_pos).degrees
    elong_dense[i:i+len(jd_block)] = elong_block

print(f"Grid denso listo: {len(jd_dense_full)} puntos.")

# ──────────────────────────────────────────────────────────────────────────────
# 4. ANCHORS VENUS: reutilizar jd_elong_refinados o recomputar
# ──────────────────────────────────────────────────────────────────────────────
try:
    anchors_jd = jd_elong_refinados.copy()
    print(f"\nAnchors reutilizados del kernel: {len(anchors_jd)} máximos.")
except NameError:
    from scipy.signal import find_peaks
    # Recomputar máximos de elongación entre 800 aC y 150 aC
    mask = (jd_dense_full >= 1370000) & (jd_dense_full <= 1620000)
    jd_search   = jd_dense_full[mask]
    elong_search = elong_dense[mask]
    peaks_idx, _ = find_peaks(elong_search, height=35.0, distance=50)
    # Refinamiento a 1-día
    refined_jds = []
    for idx in peaks_idx:
        lo = max(0, idx - 30)
        hi = min(len(jd_search) - 1, idx + 30)
        jd_fine = np.arange(jd_search[lo], jd_search[hi], 1.0)
        t_fine  = _ts.tt_jd(jd_fine)
        ap_fine = _earth.at(t_fine).observe(_venus).apparent()
        sp_fine = _earth.at(t_fine).observe(_sun).apparent()
        el_fine = ap_fine.separation_from(sp_fine).degrees
        refined_jds.append(jd_fine[np.argmax(el_fine)])
    anchors_jd = np.array(refined_jds)
    print(f"\nAnchors recomputados: {len(anchors_jd)} máximos de elongación.")

# ──────────────────────────────────────────────────────────────────────────────
# 5. PRECOMPUTAR TODAS LAS SECUENCIAS BINARIAS VENUS (112 × K)
# ──────────────────────────────────────────────────────────────────────────────
K = len(anchors_jd)

def build_venus_sequence(anchor_jd):
    """
    Secuencia binaria (112,) para un ancla dada.
    Celda m = (i*14 + j) → JD_celda = anchor_jd + m * SYNODIC_MONTH
    Marca 1 si elongación > ELONG_THRESHOLD.
    """
    months    = np.arange(112)
    jd_cells  = anchor_jd + months * SYNODIC_MONTH
    elong_cells = np.interp(jd_cells, jd_dense_full, elong_dense,
                            left=np.nan, right=np.nan)
    return (elong_cells > ELONG_THRESHOLD).astype(float)

print(f"\nPrecomputando {K} secuencias Venus (112 × {K})...")
VENUS_MATRIX = np.zeros((N, K))   # (112, K)
for k, ajd in enumerate(anchors_jd):
    VENUS_MATRIX[:, k] = build_venus_sequence(ajd)

# Eliminar columnas constantes (Venus nunca / siempre activo en las 112 celdas)
col_var = VENUS_MATRIX.var(axis=0)
valid_mask = col_var > 0
VENUS_MATRIX = VENUS_MATRIX[:, valid_mask]
anchors_jd_valid = anchors_jd[valid_mask]
K_valid = VENUS_MATRIX.shape[1]
print(f"Secuencias válidas (varianza > 0): {K_valid} de {K}")

# ──────────────────────────────────────────────────────────────────────────────
# 6. SCORE TEST VECTORIZADO (Rao LM test)
#
# Para añadir covariable x a logit y ~ X_base con parámetros ajustados β:
#   W_i = mu_i (1 - mu_i)           pesos de información
#   r_i = y_i - mu_i                 residuos de Pearson
#   Numerador^2  = (x^T r)^2
#   Denominador  = x^T W x - x^T W X (X^T W X)^{-1} X^T W x
#   Score stat   = Num^2 / Denom  ~  chi^2(1) bajo H0
#
# Con VENUS_MATRIX (N × K_valid) aplicamos todo en una sola operación.
# ──────────────────────────────────────────────────────────────────────────────
def score_stats_vectorized(y, mu, X_base, VENUS):
    """
    Calcula K estadísticos de score (Rao LM) simultáneamente.
    Devuelve array (K,) con score stat para cada columna de VENUS.
    """
    W = mu * (1.0 - mu)                              # (N,)
    r = y - mu                                        # (N,)

    # X^T W X y su inversa (solo una vez por modelo base)
    WX   = W[:, None] * X_base                        # (N, p)
    XtWX = X_base.T @ WX                              # (p, p)
    XtWX_inv = np.linalg.solve(XtWX, np.eye(XtWX.shape[0]))

    # Numeradores: (V^T r)^2  →  (K,)
    num2 = (VENUS.T @ r) ** 2                         # (K,)

    # Denominador parte 1: diag(V^T W V)  →  (K,)
    d1   = (VENUS ** 2).T @ W                         # (K,)

    # Denominador parte 2: V^T W X (X^T W X)^{-1} X^T W V  →  (K,)
    # = ||X^T W V||^2_{(XtWX)^{-1}}
    VtWX = VENUS.T @ WX                               # (K, p)
    d2   = np.sum((VtWX @ XtWX_inv) * VtWX, axis=1)  # (K,)

    denom = d1 - d2                                   # (K,)
    scores = np.where(denom > 1e-12, num2 / denom, 0.0)
    return scores                                     # (K,)


# Estadístico observado
scores_obs   = score_stats_vectorized(y_obs, mu_base, X_base, VENUS_MATRIX)
T_obs        = np.max(scores_obs)
best_k       = np.argmax(scores_obs)
best_anchor  = anchors_jd_valid[best_k]
# Año aproximado del mejor ancla
best_year    = int((best_anchor - 1721425.5) / 365.25)

print(f"\n{'─'*55}")
print(f"T_obs (max score stat)    = {T_obs:.4f}")
print(f"Mejor anchor              = JD {best_anchor:.1f}  (~{abs(best_year)} a.C.)")
print(f"Score chi² df=1 p asint.  = {1 - float(__import__('scipy').stats.chi2.cdf(T_obs, 1)):.4f}  "
      "(IGNORAR: no corregido por búsqueda múltiple)")
print(f"{'─'*55}")

# ──────────────────────────────────────────────────────────────────────────────
# 7. GENERADOR DE MATRICES CON MÁRGENES FIJOS (Curveball)
# ──────────────────────────────────────────────────────────────────────────────
def curveball_swap(mat, n_swaps=None, rng=None):
    """
    Strona et al. (2014). Genera matriz binaria con mismos totales fila/columna.
    n_swaps: número de operaciones Curveball (default: 10 × n_unos)
    """
    mat = mat.copy()
    n_rows = mat.shape[0]
    n_ones = mat.sum()
    if n_swaps is None:
        n_swaps = max(2000, 10 * int(n_ones))
    if rng is None:
        rng = np.random.default_rng()

    for _ in range(n_swaps):
        r1, r2 = rng.choice(n_rows, size=2, replace=False)
        set1 = np.where(mat[r1])[0]
        set2 = np.where(mat[r2])[0]
        if len(set1) == 0 or len(set2) == 0:
            continue
        only1 = np.setdiff1d(set1, set2, assume_unique=True)
        only2 = np.setdiff1d(set2, set1, assume_unique=True)
        if len(only1) == 0 or len(only2) == 0:
            continue
        n_trade = rng.integers(1, min(len(only1), len(only2)) + 1)
        t1 = rng.choice(only1, size=n_trade, replace=False)
        t2 = rng.choice(only2, size=n_trade, replace=False)
        mat[r1, t1] = 0;  mat[r1, t2] = 1
        mat[r2, t2] = 0;  mat[r2, t1] = 1

    return mat

# Verificación de márgenes
M_test = curveball_swap(M_obs_2d, rng=np.random.default_rng(RANDOM_SEED_4D))
assert (M_test.sum(axis=1) == M_obs_2d.sum(axis=1)).all(), "Totales fila rotos"
assert (M_test.sum(axis=0) == M_obs_2d.sum(axis=0)).all(), "Totales columna rotos"
print("\nVerificación Curveball: márgenes conservados ✓")

# ──────────────────────────────────────────────────────────────────────────────
# 8. DISTRIBUCIÓN NULA: 9 999 réplicas
# ──────────────────────────────────────────────────────────────────────────────
N_PERM  = 9999
T_null  = np.zeros(N_PERM)
rng_main = np.random.default_rng(RANDOM_SEED_4D)

print(f"\nGenerando {N_PERM} matrices nulas y calculando max score stat...")
print("(estimación: 2-5 minutos)\n")

import time
t0 = time.time()

for perm in range(N_PERM):
    # Matriz nula con márgenes fijos
    M_null_2d = curveball_swap(M_obs_2d, rng=rng_main)
    y_null    = M_null_2d.ravel().astype(float)

    # Modelo base sobre la matriz nula
    mu_null, _, _ = fit_logit_base(y_null, X_base)

    # Max score stat sobre todos los anchors Venus (vectorizado)
    scores_null   = score_stats_vectorized(y_null, mu_null, X_base, VENUS_MATRIX)
    T_null[perm]  = np.max(scores_null)

    if (perm + 1) % 1000 == 0:
        elapsed = time.time() - t0
        eta = elapsed / (perm + 1) * (N_PERM - perm - 1)
        p_run = np.mean(T_null[:perm+1] >= T_obs)
        print(f"  {perm+1:5d}/{N_PERM} | T_null median={np.median(T_null[:perm+1]):.2f} "
              f"| p estimado={p_run:.4f} | ETA {eta/60:.1f} min")

elapsed_total = time.time() - t0
print(f"\nCompletado en {elapsed_total/60:.1f} minutos.")

# ──────────────────────────────────────────────────────────────────────────────
# 9. P-VALOR EMPÍRICO Y RESULTADO FINAL
# ──────────────────────────────────────────────────────────────────────────────
p_empirico = np.mean(T_null >= T_obs)
p_ci_lo    = p_empirico - 1.96 * np.sqrt(p_empirico * (1 - p_empirico) / N_PERM)
p_ci_hi    = p_empirico + 1.96 * np.sqrt(p_empirico * (1 - p_empirico) / N_PERM)

# Percentiles de la distribución nula
q95 = np.percentile(T_null, 95)
q99 = np.percentile(T_null, 99)

print(f"\n{'='*60}")
print(f"RESULTADO FASE 4d — Test maxT con nulo estructurado")
print(f"{'='*60}")
print(f"  Estadístico T_obs          = {T_obs:.4f}")
print(f"  Percentil 95 nulo          = {q95:.4f}")
print(f"  Percentil 99 nulo          = {q99:.4f}")
print(f"  p-valor FWER (empírico)    = {p_empirico:.4f}  "
      f"[IC 95%: {max(0,p_ci_lo):.4f} – {p_ci_hi:.4f}]")
print(f"  Mejor ancla Venus          = ~{abs(best_year)} a.C.")
print(f"  n_perms                    = {N_PERM}")
print()
if p_empirico < 0.05:
    print("  → Venus AÑADE mejora de deviance SIGNIFICATIVA más allá del")
    print("    gradiente fila+columna (p < 0.05, nulo fixed-margin).")
elif p_empirico < 0.10:
    print("  → Señal marginal (0.05 ≤ p < 0.10). Evidencia débil e insuficiente.")
else:
    print("  → Venus NO añade mejora significativa más allá del gradiente.")
    print("    La hipótesis astronómica de Venus queda debilitada.")
print(f"{'='*60}")

# ──────────────────────────────────────────────────────────────────────────────
# 10. FIGURA
# ──────────────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(14, 5))
gs  = gridspec.GridSpec(1, 3, figure=fig, wspace=0.35)

# Panel A: distribución nula vs T_obs
ax0 = fig.add_subplot(gs[0])
ax0.hist(T_null, bins=60, color='steelblue', alpha=0.75, edgecolor='white',
         linewidth=0.3, label=f'Nulo fixed-margin (n={N_PERM})')
ax0.axvline(T_obs, color='crimson', lw=2.0, linestyle='--',
            label=f'T_obs = {T_obs:.2f}')
ax0.axvline(q95,  color='darkorange', lw=1.2, linestyle=':',
            label=f'p=0.05 umbral = {q95:.2f}')
ax0.set_xlabel('max score stat (Venus sobre fila+col)', fontsize=10)
ax0.set_ylabel('Frecuencia', fontsize=10)
ax0.set_title(f'Distribución nula\np-valor = {p_empirico:.4f}', fontsize=10)
ax0.legend(fontsize=8)

# Panel B: perfil de score stat por anchor temporal
ax1 = fig.add_subplot(gs[1])
years_valid = (anchors_jd_valid - 1721425.5) / 365.25
ax1.plot(years_valid, scores_obs, color='steelblue', lw=0.9, alpha=0.85)
ax1.axhline(q95, color='darkorange', lw=1.2, linestyle=':',
            label=f'Umbral p=0.05')
ax1.axhline(q99, color='crimson', lw=1.0, linestyle=':',
            label=f'Umbral p=0.01')
ax1.axvline(best_year, color='crimson', lw=1.5, linestyle='--', alpha=0.7,
            label=f'Mejor ancla ~{abs(best_year)} a.C.')
ax1.set_xlabel('Año aproximado del ancla', fontsize=10)
ax1.set_ylabel('Score stat (Venus vs base)', fontsize=10)
ax1.set_title('Score stat por ancla temporal', fontsize=10)
ax1.legend(fontsize=8)
# Eje x: años a.C. (negativos → positivos en sentido histórico)
ax1_ticks = np.array([-800, -700, -600, -500, -400, -300, -200])
ax1.set_xticks(ax1_ticks)
ax1.set_xticklabels([f'{abs(y)} a.C.' for y in ax1_ticks], fontsize=7, rotation=30)

# Panel C: mejor secuencia Venus vs datos observados (heatmap comparativo)
ax2 = fig.add_subplot(gs[2])
best_venus_2d = VENUS_MATRIX[:, best_k].reshape(8, 14)
# Overlay: datos observados y predicción Venus
overlay = M_obs_2d * 2 + best_venus_2d.astype(int)
# 0 = ambos 0, 1 = solo Venus, 2 = solo observado, 3 = ambos 1
cmap_ov = plt.cm.colors.ListedColormap(
    ['#f0f0f0', '#aec6e8', '#e07070', '#2c7bb6'])
im = ax2.imshow(overlay, aspect='auto', cmap=cmap_ov, vmin=0, vmax=3)
ax2.set_xlabel('Columna', fontsize=10)
ax2.set_ylabel('Fila', fontsize=10)
ax2.set_title(f'Tableta vs Venus (mejor ancla ~{abs(best_year)} a.C.)', fontsize=10)
ax2.set_xticks(range(14)); ax2.set_xticklabels(range(1, 15), fontsize=7)
ax2.set_yticks(range(8));  ax2.set_yticklabels(range(1, 9), fontsize=7)
from matplotlib.patches import Patch
legend_elems = [
    Patch(facecolor='#f0f0f0', label='Ninguno'),
    Patch(facecolor='#aec6e8', label='Solo Venus'),
    Patch(facecolor='#e07070', label='Solo tableta'),
    Patch(facecolor='#2c7bb6', label='Coincidencia'),
]
ax2.legend(handles=legend_elems, fontsize=7, loc='lower right',
           framealpha=0.8, ncol=2)

fig.suptitle(
    f'Fase 4d — Test maxT con nulo fija+columna | '
    f'T_obs={T_obs:.2f} | p={p_empirico:.4f}',
    fontsize=11, y=1.02
)
plt.savefig('../results/fig27_fase4d_maxT_structured.png',
            dpi=150, bbox_inches='tight')
plt.show()
print("\nFigura guardada: results/fig27_fase4d_maxT_structured.png")

# ──────────────────────────────────────────────────────────────────────────────
# 11. GUARDAR RESULTADOS PARA USO POSTERIOR
# ──────────────────────────────────────────────────────────────────────────────
resultados_4d = {
    'T_obs':          T_obs,
    'p_empirico':     p_empirico,
    'p_ci':           (max(0, p_ci_lo), p_ci_hi),
    'q95_null':       q95,
    'q99_null':       q99,
    'best_anchor_jd': best_anchor,
    'best_year_aprox': best_year,
    'N_perm':         N_PERM,
    'K_valid_anchors': K_valid,
    'T_null':         T_null,
    'scores_obs':     scores_obs,
    'anchors_jd_valid': anchors_jd_valid,
}
np.save('../results/fase4d_resultados.npy', resultados_4d)
print("Resultados guardados: results/fase4d_resultados.npy")
