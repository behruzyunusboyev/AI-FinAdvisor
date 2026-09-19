from typing import List, Dict, Tuple
import math


def annuity_monthly_payment(principal: float, annual_rate: float, months: int) -> float:
    r = annual_rate / 12.0
    if r == 0:
        return principal / months
    return principal * (r / (1 - (1 + r) ** (-months)))


def differential_monthly_payments(principal: float, annual_rate: float, months: int) -> List[float]:
    r = annual_rate / 12.0
    payments = []
    for m in range(months):
        remaining = principal - (principal * m / months)
        interest = remaining * r
        principal_part = principal / months
        payments.append(principal_part + interest)
    return payments


def compare_loans(offers: List[Dict], months: int = None) -> List[Dict]:
    """
    Compare loan offers.

    offers: list of dicts with keys: 'name', 'principal', 'annual_rate' (as decimal, e.g. 0.18),
            'term_months' (int), 'type' ('annuity'|'differential'), 'fees' (float, optional)

    Returns list with computed 'avg_monthly', 'total_payment', 'total_interest', 'details'
    """
    results = []
    for o in offers:
        P = float(o['principal'])
        n = int(o.get('term_months', o.get('term', 12)))
        rate = float(o.get('annual_rate', 0.0))
        typ = o.get('type', 'annuity')
        fees = float(o.get('fees', 0.0))

        if months is None:
            months = n

        if typ == 'annuity':
            mpay = annuity_monthly_payment(P, rate, n)
            total = mpay * n + fees
            total_interest = total - P - fees
            details = {'monthly_schedule': None}
        else:
            sched = differential_monthly_payments(P, rate, n)
            total = sum(sched) + fees
            total_interest = total - P - fees
            mpay = sum(sched) / len(sched) if sched else 0.0
            details = {'monthly_schedule': sched}

        results.append({
            'name': o.get('name', ''),
            'principal': P,
            'term_months': n,
            'type': typ,
            'avg_monthly': round(mpay, 2),
            'total_payment': round(total, 2),
            'total_interest': round(total_interest, 2),
            'fees': fees,
            'details': details,
        })

    # sort by total_payment ascending
    results.sort(key=lambda x: x['total_payment'])
    return results


def evaluate_expansion(capital_needed: float,
                       current_reserve: float,
                       expected_monthly_incremental_profit: float,
                       max_payback_months: int = 24) -> Dict:
    """
    Simple expansion feasibility check.

    Returns dict with 'can_self_fund', 'shortfall', 'payback_months' (if financed),
    and 'recommendation'.
    """
    res = {}
    res['can_self_fund'] = current_reserve >= capital_needed
    res['shortfall'] = round(max(0.0, capital_needed - current_reserve), 2)

    if expected_monthly_incremental_profit <= 0:
        res['payback_months'] = None
        res['recommendation'] = 'No projected incremental profit; do not expand without better plan.'
        return res

    payback = capital_needed / expected_monthly_incremental_profit
    res['payback_months'] = round(payback, 1)

    if payback <= max_payback_months and (res['can_self_fund'] or res['shortfall'] > 0):
        res['recommendation'] = 'Feasible: payback within threshold.'
    else:
        res['recommendation'] = 'Not feasible within desired payback; consider smaller pilot or external financing.'

    return res
