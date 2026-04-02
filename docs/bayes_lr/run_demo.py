"""
Talk demo: 1D linear regression — MLE vs. Bayesian (Stan)

Generates simple data, computes MLE analytically, runs Stan for the
Bayesian posterior, and plots both side by side.

Outputs
-------
observed_data.csv          columns: x, y
posterior_samples.csv      columns: beta_0, beta_1, sigma
posterior_predictive.csv   columns: x_pred, y_pred_0, y_pred_1, ... (one col per draw)

Usage:
    python run_demo.py
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cmdstanpy

N_PRED_SAMPLES = 500   # posterior draws saved to CSV

# ── 1. Generate simple data ──────────────────────────────────────────────────
rng = np.random.default_rng(42)
N = 4
x = rng.uniform(0, 5, N)
beta_0_true, beta_1_true, sigma_true = 1.0, 0.8, 0.7
y = beta_0_true + beta_1_true * x + rng.normal(0, sigma_true, N)

x_pred = np.linspace(-5, 10, 200)

# ── 2. MLE (closed-form OLS) ─────────────────────────────────────────────────
X = np.column_stack([np.ones(N), x])
beta_mle = np.linalg.lstsq(X, y, rcond=None)[0]
beta_0_mle, beta_1_mle = beta_mle
y_mle = beta_0_mle + beta_1_mle * x_pred
sigma_mle = np.std(y - X @ beta_mle)

print(f"MLE:  beta_0={beta_0_mle:.3f}, beta_1={beta_1_mle:.3f}, sigma={sigma_mle:.3f}")

# ── 3. Bayesian inference via Stan ───────────────────────────────────────────
model = cmdstanpy.CmdStanModel(stan_file="model.stan")

stan_data = {
    "N": N,
    "x": x.tolist(),
    "y": y.tolist(),
    "N_pred": len(x_pred),
    "x_pred": x_pred.tolist(),
}

fit = model.sample(
    data=stan_data,
    chains=4,
    iter_warmup=500,
    iter_sampling=1000,
    show_progress=True,
    show_console=False,
)

print(fit.summary()[["Mean", "StdDev", "R_hat"]].loc[["beta_0", "beta_1", "sigma"]])

# Posterior samples of parameters
b0_samples    = fit.stan_variable("beta_0")    # (4000,)
b1_samples    = fit.stan_variable("beta_1")
sigma_samples = fit.stan_variable("sigma")
y_pred_all    = fit.stan_variable("y_pred")    # (4000, 200)

# ── 4. Save CSVs ─────────────────────────────────────────────────────────────

# observed data
pd.DataFrame({"x": x, "y": y}).to_csv("observed_data.csv", index=False)
print("Saved observed_data.csv")

# posterior samples (all draws)
pd.DataFrame({
    "beta_0": b0_samples,
    "beta_1": b1_samples,
    "sigma":  sigma_samples,
}).to_csv("posterior_samples.csv", index=False)
print("Saved posterior_samples.csv")

# posterior predictive — subsample to N_PRED_SAMPLES draws
idx = rng.choice(len(b0_samples), size=N_PRED_SAMPLES, replace=False)
y_pred_sub = y_pred_all[idx]                   # (N_PRED_SAMPLES, 200)
pp_df = pd.DataFrame(
    y_pred_sub.T,
    columns=[f"y_pred_{i}" for i in range(N_PRED_SAMPLES)],
)
pp_df.insert(0, "x_pred", x_pred)
pp_df.to_csv("posterior_predictive.csv", index=False)
print("Saved posterior_predictive.csv")

# ── 5. Quick matplotlib preview ──────────────────────────────────────────────
y_pred_mean = y_pred_sub.mean(axis=0)
y_pred_lo   = np.percentile(y_pred_sub, 5,  axis=0)
y_pred_hi   = np.percentile(y_pred_sub, 95, axis=0)

fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
fig.suptitle("1D Linear Regression: MLE vs. Bayesian", fontsize=14)

ax = axes[0]
ax.scatter(x, y, color="steelblue", zorder=3, label="data")
ax.plot(x_pred, y_mle, color="crimson", linewidth=2, label="MLE fit")
ax.fill_between(x_pred, y_mle - 2*sigma_mle, y_mle + 2*sigma_mle,
                color="crimson", alpha=0.15, label="±2σ (MLE)")
ax.set_title("Maximum Likelihood")
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.legend(fontsize=9)

ax = axes[1]
ax.scatter(x, y, color="steelblue", zorder=3, label="data")
for i in range(min(80, N_PRED_SAMPLES)):
    ax.plot(x_pred, b0_samples[idx[i]] + b1_samples[idx[i]] * x_pred,
            color="orange", alpha=0.06, linewidth=0.8)
ax.plot(x_pred, y_pred_mean, color="darkorange", linewidth=2, label="posterior mean")
ax.fill_between(x_pred, y_pred_lo, y_pred_hi,
                color="darkorange", alpha=0.25, label="90% posterior predictive")
ax.set_title("Bayesian (Stan)")
ax.set_xlabel("x"); ax.legend(fontsize=9)

plt.tight_layout()
plt.savefig("demo_mle_vs_bayes.png", dpi=150)
print("Saved demo_mle_vs_bayes.png")
plt.show()
