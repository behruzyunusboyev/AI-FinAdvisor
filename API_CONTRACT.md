# AI FinAdvisor — API Contract v2

Base URL: `/api/v1`. Monetary values are integer Uzbek so'm. Every financial field in responses is calculated by `core/financial_engine.py`, never by an LLM.

## `POST /business-plan/generate`

```json
{"region":"Xorazm","business_type":"Qahvaxona","own_capital":100000000,"need_credit":true,"requested_loan_amount":50000000,"loan_term_months":24,"employees_count":3,"average_salary_per_employee":3000000,"monthly_rent":8000000,"entity_type":"yatt"}
```

`entity_type` is either `yatt` or `mchj`. A credit amount is required only when `need_credit` is `true`; it must otherwise be zero.

Response `201`:

```json
{"financials":{"capex":{"equipment":0,"renovation":0,"furniture":0,"initial_stock":0,"marketing":0,"emergency_reserve":0,"total_capex":0},"opex_monthly":{"rent":0,"salaries":0,"utilities":0,"loan_payment":0,"total_fixed_opex":0},"break_even":{"monthly_break_even_revenue":0,"daily_break_even_revenue":0,"required_daily_customers":0},"tax_analysis":{"selected_regime":"string","estimated_monthly_tax":0,"alternative_regimes":{"yatt_1_percent":0,"mchj_4_percent":0,"vat_12_percent":0}},"bank_readiness":{"score":0,"status":"string","debt_service_ratio":0,"recommendation":"string"}},"ai_analysis":{"executive_summary":"string","swot":{"strengths":["string"],"weaknesses":["string"],"opportunities":["string"],"threats":["string"]},"marketing_strategy":"string"},"project_id":"uuid"}
```

## `POST /copilot/daily-check`

```json
{"project_id":"uuid","daily_revenue":2400000,"daily_expense":1700000}
```

Response `201`:

```json
{"daily_profit":700000,"bep_progress_pct":3.3,"insight":"Bugungi sof foyda ..."}
```

## `GET /export/pdf/{project_id}`

Response `200` is an `application/pdf` stream. The document has a project passport and Bank Readiness page, twelve-month cash-flow page, and SWOT/risk/disclaimer/QR page. Unknown projects return `404`.

## Operational responses

Validation failures return `422`. Projects and daily logs are stored in the local SQLite `finadvisor.db` file.
