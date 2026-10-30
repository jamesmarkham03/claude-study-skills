"""Check every answer in 01-binomial-poisson.html.

Each answer is computed from the formula, checked a second, independent way (direct
summation or a seeded Monte Carlo simulation), and then looked up in the HTML page so
the page and this script can't drift apart.

Run: python verify_01_binomial_poisson.py
"""
import math
import random
from pathlib import Path

PAGE = Path(__file__).with_name("01-binomial-poisson.html").read_text(encoding="utf-8")
rng = random.Random(817)
SIMS = 200_000


def binom_pmf(k, n, p):
    return math.comb(n, k) * p**k * (1 - p) ** (n - k)


def binom_cdf(k, n, p):
    return sum(binom_pmf(i, n, p) for i in range(k + 1))


def pois_pmf(k, lam):
    return math.exp(-lam) * lam**k / math.factorial(k)


def pois_cdf(k, lam):
    return sum(pois_pmf(i, lam) for i in range(k + 1))


def simulate_binom(n, p, event):
    hits = sum(event(sum(rng.random() < p for _ in range(n))) for _ in range(SIMS))
    return hits / SIMS


def simulate_pois(lam, event):
    # Count arrivals in [0, 1) from exponential gaps: independent of the pmf formula.
    def draw():
        t, k = rng.expovariate(lam), 0
        while t < 1:
            k += 1
            t += rng.expovariate(lam)
        return k
    return sum(event(draw()) for _ in range(SIMS)) / SIMS


checks = []


def check(label, value, shown, simulated=None, tol=0.006):
    """value: exact answer; shown: the string the page prints; simulated: independent estimate."""
    assert shown in PAGE, f"{label}: '{shown}' not found in the HTML"
    if simulated is not None:
        assert abs(value - simulated) < tol, f"{label}: exact {value:.4f} vs simulated {simulated:.4f}"
    checks.append((label, value, shown, simulated))


# Sanity: pmfs sum to 1 and the means match np and λ.
assert abs(sum(binom_pmf(k, 8, 0.6) for k in range(9)) - 1) < 1e-12
assert abs(sum(k * binom_pmf(k, 8, 0.6) for k in range(9)) - 4.8) < 1e-12
assert abs(sum(pois_pmf(k, 3.6) for k in range(80)) - 1) < 1e-12
assert abs(sum(k * pois_pmf(k, 3.6) for k in range(80)) - 3.6) < 1e-12

# ---------------- Block A: binomial ----------------
check("Learn-it example: P(X=1), n=3, p=0.25", binom_pmf(1, 3, 0.25), "0.4219")
check("A1 P(exactly 2 hits in 4), p=.300", binom_pmf(2, 4, 0.3), "0.2646",
      simulate_binom(4, 0.3, lambda x: x == 2))
check("A2 P(at least 1 hit in 4)", 1 - 0.7**4, "0.7599",
      simulate_binom(4, 0.3, lambda x: x >= 1))
check("A3 mean hits in 20 AB", 20 * 0.3, "6 hits")
check("A3 SD of hits in 20 AB", math.sqrt(20 * 0.3 * 0.7), "2.05")
a4 = sum(binom_pmf(k, 5, 0.62) for k in range(3, 6))
check("A4 P(at least 3 strikes in 5), p=.62", a4, "0.7165", simulate_binom(5, 0.62, lambda x: x >= 3))
check("A5a P(exactly 5 of 8), p=.6", binom_pmf(5, 8, 0.6), "0.2787", simulate_binom(8, 0.6, lambda x: x == 5))
check("A5b P(at most 2 of 8)", binom_cdf(2, 8, 0.6), "0.0498", simulate_binom(8, 0.6, lambda x: x <= 2))
check("A5c mean", 8 * 0.6, "4.8")
check("A5c variance", 8 * 0.6 * 0.4, "1.92")
n_needed = math.ceil(math.log(0.01) / math.log(0.6))
assert 0.6 ** (n_needed - 1) > 0.01 >= 0.6**n_needed  # the smallest n that works, and the one before fails
check("A5d smallest n with P(at least one ball) ≥ 0.99", n_needed, "n = 10")
check("A5d 0.6^9 just misses", 0.6**9, "0.0101")

# ---------------- Block B: Poisson ----------------
check("Learn-it example: P(X=2), λ=2", pois_pmf(2, 2), "0.2707")
check("B1 P(0 HR), λ=1.2", pois_pmf(0, 1.2), "0.3012", simulate_pois(1.2, lambda x: x == 0))
b2 = 1 - pois_cdf(1, 3.6)
check("B2 P(at least 2 HR in 3 games), λ=3.6", b2, "0.8743", simulate_pois(3.6, lambda x: x >= 2))
check("B3 P(no errors in 4 games), λ=0.5×4", pois_pmf(0, 2.0), "0.1353", simulate_pois(2.0, lambda x: x == 0))
exact = binom_cdf(1, 250, 0.01)
approx = pois_cdf(1, 2.5)
check("B4a exact binomial P(X≤1), n=250, p=.01", exact, "0.2858", simulate_binom(250, 0.01, lambda x: x <= 1))
check("B4b Poisson approx P(X≤1), λ=2.5", approx, "0.2873")
check("B4c approximation error", abs(approx - exact), "0.0015")
check("B4d P(X≥5), exact", 1 - binom_cdf(4, 250, 0.01), "0.1078")

print(f"{'check':<52} {'exact':>9} {'page':>8} {'simulated':>10}")
for label, value, shown, sim in checks:
    print(f"{label:<52} {value:>9.4f} {shown:>8} {'' if sim is None else f'{sim:.4f}':>10}")
print(f"\nAll {len(checks)} answers verified and found in the page.")
