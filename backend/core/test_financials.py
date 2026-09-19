from financials import compare_loans, evaluate_expansion


def test_compare_loans():
    offers = [
        {'name': 'Bank A', 'principal': 100000, 'annual_rate': 0.18, 'term_months': 12, 'type': 'annuity', 'fees': 500},
        {'name': 'Bank B', 'principal': 100000, 'annual_rate': 0.16, 'term_months': 12, 'type': 'differential', 'fees': 1000},
    ]
    res = compare_loans(offers)
    assert isinstance(res, list)
    assert len(res) == 2
    # cheapest total_payment should be first
    assert res[0]['total_payment'] <= res[1]['total_payment']


def test_evaluate_expansion():
    r = evaluate_expansion(50000, 20000, 5000, max_payback_months=12)
    assert 'can_self_fund' in r
    assert r['shortfall'] == 30000.00
    assert r['payback_months'] == 10.0


if __name__ == '__main__':
    print('Running financials tests...')
    test_compare_loans()
    test_evaluate_expansion()
    print('OK')
