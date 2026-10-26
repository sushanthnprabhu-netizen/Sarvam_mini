import math
import statistics
from dataclasses import dataclass

from scipy import stats


@dataclass
class Result:
    n: int
    mean: float
    sd: float
    t: float
    p: float
    ci_low: float
    ci_high: float
    d: float
    power: float
    n_needed: int | None
    remaining: int | None


def _power(d: float, n: int, alpha: float) -> float:
    df = n - 1
    nc = d * math.sqrt(n)
    tcrit = stats.t.ppf(1 - alpha / 2, df)
    return float(1 - stats.nct.cdf(tcrit, df, nc) + stats.nct.cdf(-tcrit, df, nc))


def analyze(scores, mu0=3.0, alpha=0.05, target_power=0.8):
    n = len(scores)
    if n < 2:
        return None
    mean = statistics.mean(scores)
    sd = statistics.stdev(scores)
    if sd == 0:
        return None  # all identical answers: test is undefined
    se = sd / math.sqrt(n)
    t_stat, p = stats.ttest_1samp(scores, mu0)
    lo, hi = stats.t.interval(0.95, n - 1, loc=mean, scale=se)
    d = abs(mean - mu0) / sd
    power = _power(d, n, alpha) if d > 0 else alpha
    n_needed = None
    if d >= 0.05:
        for k in range(2, 2001):
            if _power(d, k, alpha) >= target_power:
                n_needed = k
                break
    remaining = max(0, n_needed - n) if n_needed else None
    return Result(n, mean, sd, float(t_stat), float(p), float(lo), float(hi),
                  d, power, n_needed, remaining)