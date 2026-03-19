## Animation 1 — Sampling Distribution (`sampling_distribution.py`)

### How it was made

1. Talked to NotebookLM (with all my slides) to create the storyboard (`story_board.md`).
2. Used Claude Code (Sonnet 4.6) to generate the Manim code.
- Prompt:
```text
is there a mcp server or better a skill for manim. I want to create a animation like in story_board.md
```

Answer:
```text
There's no dedicated manim skill installed, but there are MCP servers available
(like abhiemj/manim-mcp-server). However, the simplest path is to just write
the Manim Python code directly — I can do that now without any extra tooling.
```

- Me: "ok go for option one" — animation was finished in ~7 minutes.

### What it shows

Split-screen animation: **Mother Nature** (Probability Land, left) holds the true model with secret parameter μ = 42. She generates random samples that fall into **Data Land** (right) where **Fred Stanton** uses Maximum Likelihood to estimate μ. Repeated sampling (15 rounds, accelerating) accumulates red stars near the true parameter. In the final scene the stars morph into a histogram and then into the **sampling distribution** bell curve, centred exactly on the truth.

### Render

```bash
manim -pqh sampling_distribution.py SamplingDistribution
```

### Reproduce the key idea in code

**Python**
```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

mu, sigma, n, n_reps = 42, 0.7, 10, 1000

rng = np.random.default_rng(42)

# build the sampling distribution with an explicit loop
sample_means = []
for _ in range(n_reps):
    sample = rng.normal(mu, sigma, n)   # draw one fresh sample of size n
    sample_means.append(sample.mean())  # compute and store the estimate

# compact one-liner equivalent:
# sample_means = [rng.normal(mu, sigma, n).mean() for _ in range(n_reps)]

fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(sample_means, bins=40, density=True, alpha=0.6,
        color='steelblue', label='Sample means')
x = np.linspace(mu - 4*sigma/np.sqrt(n), mu + 4*sigma/np.sqrt(n), 300)
ax.plot(x, norm.pdf(x, mu, sigma/np.sqrt(n)), 'r-', lw=2,
        label=r'$\mathcal{N}(\mu,\,\sigma/\sqrt{n})$')
ax.axvline(mu, color='gold', linestyle='--', label='True μ = 42')
ax.set(xlabel='Sample mean', ylabel='Density',
       title='Sampling Distribution of the Mean')
ax.legend()
plt.tight_layout()
plt.show()
```

**R**
```r
library(ggplot2)

mu <- 42; sigma <- 0.7; n <- 10; n_reps <- 1000
set.seed(42)

# build the sampling distribution with an explicit loop
sample_means <- numeric(n_reps)
for (i in seq_len(n_reps)) {
  sample          <- rnorm(n, mu, sigma)  # draw one fresh sample of size n
  sample_means[i] <- mean(sample)         # compute and store the estimate
}

# compact one-liner equivalent:
# sample_means <- replicate(n_reps, mean(rnorm(n, mu, sigma)))

x_seq   <- seq(mu - 4*sigma/sqrt(n), mu + 4*sigma/sqrt(n), length.out = 300)
theory  <- data.frame(x = x_seq, y = dnorm(x_seq, mu, sigma/sqrt(n)))

ggplot(data.frame(x = sample_means), aes(x)) +
  geom_histogram(aes(y = after_stat(density)), bins = 40,
                 fill = "steelblue", alpha = 0.6) +
  geom_line(data = theory, aes(x, y), color = "red", linewidth = 1.2) +
  geom_vline(xintercept = mu, color = "gold", linetype = "dashed") +
  labs(title = "Sampling Distribution of the Mean",
       x = "Sample mean", y = "Density") +
  theme_minimal()
```

---

## Animation 2 — Three Estimators (`three_estimators.py`)

### How it was made

1. Storyboard from `story_board_mean_med_biased.md` (created by Claude / NotebookLM).
2. Used Claude Code (Sonnet 4.6) in the same session as Animation 1 — iterative tweaks over ~3 prompts (rename Pi-X labels, fix clutter, adjust colors, move labels below axis).

### What it shows

Same split-screen setup as Animation 1, but now with **three estimators** in Data Land — each time Mother Nature drops a sample all three compute their estimate simultaneously and throw a coloured star back:

| Creature | Estimator | Property |
|---|---|---|
| **Mean** (green) | $\hat{\mu} = \bar{x}$ | Unbiased, Low Variance |
| **Median** (teal) | $\hat{\mu} = \tilde{x}$ | Unbiased, High Variance |
| **Liar** (red 😈) | $\hat{\mu} = \bar{x}+5$ | Biased |

After 20 rounds the three piles of stars each morph into their own sampling distribution. The Liar's curve is visibly shifted — a bias arrow below the x-axis marks the systematic error.

### Render

```bash
manim -pqh three_estimators.py ThreeEstimators
```

### Reproduce the key idea in code

**Python**
```python
import numpy as np
import matplotlib.pyplot as plt

mu, sigma, n, n_reps = 42, 0.7, 10, 2000
bias = 5  # constant added by the biased estimator

rng = np.random.default_rng(42)

# build three sampling distributions with an explicit loop
est_mean, est_median, est_biased = [], [], []
for _ in range(n_reps):
    sample = rng.normal(mu, sigma, n)       # draw one fresh sample of size n
    est_mean.append(sample.mean())          # estimator 1: sample mean
    est_median.append(np.median(sample))    # estimator 2: sample median
    est_biased.append(sample.mean() + bias) # estimator 3: biased (mean + 5)

# compact vectorised equivalent:
# samples    = rng.normal(mu, sigma, (n_reps, n))
# est_mean   = samples.mean(axis=1)
# est_median = np.median(samples, axis=1)
# est_biased = est_mean + bias

fig, ax = plt.subplots(figsize=(10, 4))
for ests, col, lbl in [
    (est_mean,   'green', 'Mean'),
    (est_median, 'teal',  'Median'),
    (est_biased, 'red',   f'Liar (mean + {bias})'),
]:
    ax.hist(ests, bins=60, density=True, alpha=0.45, color=col, label=lbl)
ax.axvline(mu, color='gold', linestyle='--', linewidth=2, label='True μ = 42')
ax.set(xlabel='Estimate', ylabel='Density',
       title='Sampling Distributions: Mean vs Median vs Biased')
ax.legend()
plt.tight_layout()
plt.show()
```

**R**
```r
library(ggplot2)
library(tidyr)
library(dplyr)

mu <- 42; sigma <- 0.7; n <- 10; n_reps <- 2000; bias <- 5
set.seed(42)

# build three sampling distributions with an explicit loop
est_mean   <- numeric(n_reps)
est_median <- numeric(n_reps)
est_biased <- numeric(n_reps)

for (i in seq_len(n_reps)) {
  sample        <- rnorm(n, mu, sigma)    # draw one fresh sample of size n
  est_mean[i]   <- mean(sample)           # estimator 1: sample mean
  est_median[i] <- median(sample)         # estimator 2: sample median
  est_biased[i] <- mean(sample) + bias    # estimator 3: biased (mean + 5)
}

# compact vectorised equivalent:
# mat        <- matrix(rnorm(n_reps * n, mu, sigma), nrow = n_reps)
# est_mean   <- rowMeans(mat)
# est_median <- apply(mat, 1, median)
# est_biased <- est_mean + bias

df <- data.frame(Mean = est_mean, Median = est_median, Liar = est_biased) |>
  pivot_longer(everything(), names_to = "Estimator", values_to = "estimate") |>
  mutate(Estimator = factor(Estimator, levels = c("Mean", "Median", "Liar")))

ggplot(df, aes(estimate, fill = Estimator, colour = Estimator)) +
  geom_histogram(aes(y = after_stat(density)), bins = 60,
                 alpha = 0.45, position = "identity") +
  geom_vline(xintercept = mu, colour = "gold",
             linetype = "dashed", linewidth = 1.2) +
  scale_fill_manual(  values = c(Mean = "green4", Median = "darkcyan", Liar = "red3")) +
  scale_colour_manual(values = c(Mean = "green4", Median = "darkcyan", Liar = "red3")) +
  labs(title = "Sampling Distributions: Mean vs Median vs Biased Estimator",
       x = "Estimate", y = "Density") +
  theme_minimal()
```
