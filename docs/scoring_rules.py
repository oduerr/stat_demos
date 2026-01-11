import numpy as np
import math
import argparse

"""
Scoring Rules Verification Script

Usage Examples:
1. Normal Distribution (NLL):
   python3 scoring_rules.py --dist normal --rule nll

2. Right Triangular Distribution (Linear Score):
   python3 scoring_rules.py --dist triangular --rule linear

3. Symmetric Triangular (Linear Score):
   python3 scoring_rules.py --dist sym_triangular --rule linear

4. Custom Prediction:
   python3 scoring_rules.py --dist triangular --mu 0.8 --sigma 0.5 --rule crps
"""

# --- Math Helpers ---
def erf(x):
    return math.erf(x)

def pdf_normal_scalar(x, mu, sigma):
    return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma)**2)

def cdf_normal_scalar(x, mu, sigma):
    return 0.5 * (1 + erf((x - mu) / (sigma * np.sqrt(2))))

# Vectorize for numpy arrays
pdf_normal = np.vectorize(pdf_normal_scalar)
cdf_normal = np.vectorize(cdf_normal_scalar)

def pdf_skew(x, xi=-1, omega=2, alpha=4):
    # Skew Normal PDF
    z = (x - xi) / omega
    return (2 / omega) * pdf_normal(z, 0, 1) * cdf_normal(alpha * z, 0, 1)

def pdf_student(x, nu=3):
    # Student-t PDF (nu degrees of freedom)
    # Gamma((nu+1)/2) / (sqrt(nu*pi) * Gamma(nu/2)) * (1 + x^2/nu)^(-(nu+1)/2)
    # For nu=3: Gamma(2)=1, Gamma(1.5)=0.5*sqrt(pi). Factor = 1 / (sqrt(3pi) * 0.5*sqrt(pi)) = 1 / (0.5 * pi * sqrt(3))
    # Gamma(2) = 1
    # Gamma(1.5) = 0.8862269
    # coeff = 1 / (sqrt(3)*beta(0.5, 3/2)) ... simplifying
    # T-dist PDF:
    factor = math.gamma((nu + 1) / 2) / (np.sqrt(nu * np.pi) * math.gamma(nu / 2))
    return factor * (1 + (x**2) / nu)**(-(nu + 1) / 2)


def pdf_triangular(x):
    # Right Triangular on [0, 1], peak at 1
    # PDF = 2x for x in [0, 1], else 0
    return np.where((x >= 0) & (x <= 1), 2 * x, 0.0)

def pdf_sym_triangular(x):
    # Symmetric Triangular on [0, 2], peak at 1
    # PDF = x for x in [0, 1]
    # PDF = 2 - x for x in [1, 2]
    val = np.zeros_like(x)
    mask1 = (x >= 0) & (x <= 1)
    mask2 = (x > 1) & (x <= 2)
    val[mask1] = x[mask1]
    val[mask2] = 2 - x[mask2]
    return val

def pdf_mixture(x):
    # 0.6 * N(-1.5, 0.8) + 0.4 * N(2.5, 0.6)
    return 0.6 * pdf_normal(x, -1.5, 0.8) + 0.4 * pdf_normal(x, 2.5, 0.6)

def get_true_pdf(y, dist_type):
    if dist_type == 'normal':
        return pdf_normal(y, 1.0, 1.5)
    elif dist_type == 'mixture':
        return pdf_mixture(y)
    elif dist_type == 'skewed':
        return pdf_skew(y)
    elif dist_type == 'heavy':
        return pdf_student(y)
    elif dist_type == 'triangular':
        return pdf_triangular(y)
    elif dist_type == 'sym_triangular':
        return pdf_sym_triangular(y)
    else:
        raise ValueError(f"Unknown distribution: {dist_type}")

def score_nll(y, mu, sigma):
    # S(p, y) = -log p(y)
    # NLL = 0.5*log(2pi) + log(sigma) + 0.5*((y-mu)/sigma)^2
    z = (y - mu) / sigma
    return 0.5 * np.log(2 * np.pi) + np.log(sigma) + 0.5 * z**2

def score_linear(y, mu, sigma):
    # S(p, y) = -p(y)
    return -pdf_normal(y, mu, sigma)

def score_crps_gaussian(y, mu, sigma):
    # Exact CRPS for Gaussian prediction
    z = (y - mu) / sigma
    pdf_z = pdf_normal(z, 0, 1)
    cdf_z = cdf_normal(z, 0, 1)
    return sigma * (z * (2 * cdf_z - 1) + 2 * pdf_z - 1 / np.sqrt(np.pi))

def calculate_losses(dist_type, pred_mu, pred_sigma, rule, grid_step=0.0001):
    y_grid = np.arange(-7, 7 + grid_step, grid_step)
    
    # 1. True Distribution g(y)
    g_pdf = get_true_pdf(y_grid, dist_type)
    
    # Check normalization
    normalization = np.sum(g_pdf) * grid_step
    # print(f"Normalization check: {normalization:.5f}")

    # 2. Compute Expected Loss E_g[S(p)]
    # S(p, y) for each y in grid
    if rule == 'nll':
        s_vals = score_nll(y_grid, pred_mu, pred_sigma)
    elif rule == 'linear':
        s_vals = score_linear(y_grid, pred_mu, pred_sigma)
    elif rule == 'crps':
        s_vals = score_crps_gaussian(y_grid, pred_mu, pred_sigma)
    else:
        raise ValueError(f"Unknown rule: {rule}")
        
    expected_loss = np.sum(g_pdf * s_vals * grid_step)
    
    # 3. Compute Baseline Loss E_g[S(g)] ("Entropy")
    # Note: S(g) depends on the rule. 
    # For NLL: -log g(y)
    # For Linear: -g(y)
    # For CRPS: Integral (G(z) - 1(z>y))^2 dz
    
    baseline_loss = 0
    
    if rule == 'nll':
        # Avoid log(0)
        safe_g = np.maximum(g_pdf, 1e-12)
        s_g = -np.log(safe_g)
        baseline_loss = np.sum(g_pdf * s_g * grid_step)
        
    elif rule == 'linear':
        s_g = -g_pdf
        baseline_loss = np.sum(g_pdf * s_g * grid_step)
        
    elif rule == 'crps':
        # Numerical approach for generic g
        # Precompute CDF G
        G_cdf = np.cumsum(g_pdf) * grid_step
        
        # S(g, y) = Integral (G(z) - 1(z>y))^2 dz
        # This is expensive: O(N^2)
        # Verify if there's a faster way? 
        # E[S(g, Y)] = 0.5 * E[|Y - Y'|] where Y, Y' ~ g independent
        #           = Integral G(x)(1-G(x)) dx
        # This is much faster! O(N)
        
        # Let's use the identity: E_g[S(g, Y)] = Integral_{-inf}^{inf} G(x) * (1 - G(x)) dx
        term = G_cdf * (1 - G_cdf)
        baseline_loss = np.sum(term * grid_step)
        
    return expected_loss, baseline_loss

def main():
    parser = argparse.ArgumentParser(description='Replicate Scoring Rules Calculations')
    parser.add_argument('--dist', type=str, default='normal', 
                        choices=['normal', 'mixture', 'skewed', 'heavy', 'triangular', 'sym_triangular'],
                        help='True distribution g(y)')
    parser.add_argument('--mu', type=float, default=0.5, help='Predictive Mean')
    parser.add_argument('--sigma', type=float, default=1.0, help='Predictive Std Dev')
    parser.add_argument('--rule', type=str, default='nll', choices=['nll', 'linear', 'crps'],
                        help='Scoring Rule')
    
    args = parser.parse_args()
    
    print(f"--- Configuration ---")
    print(f"True Dist: {args.dist}")
    print(f"Prediction: N({args.mu}, {args.sigma}^2)")
    print(f"Rule: {args.rule}")
    print(f"---------------------")
    
    loss, baseline = calculate_losses(args.dist, args.mu, args.sigma, args.rule)
    regret = loss - baseline
    
    print(f"Baseline Loss E[S(g)]: {baseline:.4f}")
    print(f"Your Loss     E[S(p)]: {loss:.4f}")
    print(f"Regret        (Gap)  : {regret:.4f}")

if __name__ == "__main__":
    main()
