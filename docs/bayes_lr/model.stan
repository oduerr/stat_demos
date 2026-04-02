data {
  int<lower=0> N;
  vector[N] x;
  vector[N] y;
  int<lower=0> N_pred;
  vector[N_pred] x_pred;
}
parameters {
  real beta_0;
  real beta_1;
  real<lower=0> sigma;
}
model {
  // Priors
  beta_0 ~ normal(0, 10);
  beta_1 ~ normal(0, 10);
  sigma  ~ exponential(1);

  // Likelihood
  y ~ normal(beta_0 + beta_1 * x, sigma);
}
generated quantities {
  // Log-likelihood of the training data
  real log_lik = normal_lpdf(y | beta_0 + beta_1 * x, sigma);

  // Posterior predictive samples at prediction grid
  vector[N_pred] y_pred;
  for (i in 1:N_pred)
    y_pred[i] = normal_rng(beta_0 + beta_1 * x_pred[i], sigma);
}
