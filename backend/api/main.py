from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.financials import annuity_monthly_payment, compare_loans, evaluate_expansion
from ai.llm_wrapper import AIClient

app = FastAPI(title='AI FinAdvisor API', version='0.1.0')

# ✅ CORS configuration — allow frontend localhost:5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'http://127.0.0.1:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


class LoanInput(BaseModel):
    principal: float = Field(..., gt=0)
    annual_rate: float = Field(..., ge=0)
    term_months: int = Field(..., gt=0)
    payment_type: str = Field(default='annuity', pattern='^(annuity|differential)$')
    fees: float = Field(default=0.0, ge=0)


class LoanReply(BaseModel):
    monthly_payment: float
    total_payment: float
    total_interest: float
    payment_type: str


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)
    context: Optional[str] = ""


class ChatResponse(BaseModel):
    answer: str


@app.get('/')
def root():
    return {'message': 'AI FinAdvisor API is running'}


@app.post('/api/v1/loan/calculate', response_model=LoanReply)
def calculate_loan(payload: LoanInput):
    if payload.payment_type == 'annuity':
        monthly = annuity_monthly_payment(payload.principal, payload.annual_rate, payload.term_months)
        total = monthly * payload.term_months + payload.fees
        total_interest = total - payload.principal - payload.fees
    else:
        schedules = []
        r = payload.annual_rate / 12.0
        principal_remaining = payload.principal
        for month in range(payload.term_months):
            principal_part = payload.principal / payload.term_months
            interest = principal_remaining * r
            total_month = principal_part + interest
            schedules.append(total_month)
            principal_remaining -= principal_part
        monthly = sum(schedules) / len(schedules)
        total = sum(schedules) + payload.fees
        total_interest = total - payload.principal - payload.fees

    return LoanReply(
        monthly_payment=round(monthly, 2),
        total_payment=round(total, 2),
        total_interest=round(total_interest, 2),
        payment_type=payload.payment_type,
    )


@app.post('/api/v1/loan/compare', response_model=List[Dict[str, Any]])
def compare_loans_endpoint(offers: List[Dict[str, Any]]):
    return compare_loans(offers)


@app.post('/api/v1/chat', response_model=ChatResponse)
def chat_with_ai(payload: ChatRequest):
    try:
        try:
            client = AIClient(use_groq=False)
            answer = client.ask_ai(payload.question, payload.context or '')
        except ValueError:
            answer = (
                'AI API kaliti mavjud emasligi sababli real model ishlamadi. '
                'Ammo murojaat bo\'yicha men quyidagi umumiy moliyaviy yo\'riqnoma beraman: '
                'kreditni olishdan oldin oylik to\'lov, foiz stavkasi, muddat, va oylik zaxira pulni tekshiring; '
                'foiz va to\'lovlar Python hisob-kitobi orqali aniq hisoblansin, AI esa faqat tushuntirish va tavsiyalar berishi kerak.'
            )
        return ChatResponse(answer=answer)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f'AI error: {str(exc)}')


@app.post('/api/v1/financial/expansion-check')
def expansion_check(payload: Dict[str, Any]):
    required = float(payload.get('capital_needed', 0))
    reserve = float(payload.get('current_reserve', 0))
    profit = float(payload.get('expected_monthly_incremental_profit', 0))
    payback_limit = int(payload.get('max_payback_months', 24))
    result = evaluate_expansion(required, reserve, profit, payback_limit)
    return result

@app.post('/api/v1/business-plan/generate')
def generate_business_plan(payload: Dict[str, Any]):
    """Generate a complete business plan from user input"""
    try:
        project_name = payload.get('project_name', 'New Project')
        monthly_revenue = float(payload.get('monthly_revenue', 0))
        monthly_expenses = float(payload.get('monthly_expenses', 0))
        investment_amount = float(payload.get('investment_amount', 0))
        employees_count = int(payload.get('employees_count', 1))
        
        monthly_profit = monthly_revenue - monthly_expenses
        payback_months = int(investment_amount / monthly_profit) if monthly_profit > 0 else 0
        
        # Generate mock business plan (AI integration would happen here)
        business_plan = {
            'executive_summary': {
                'title': f'{project_name} - Biznes-reja',
                'description': f'{project_name} loyihasi {employees_count} nafar xodim bilan boshlanadi. '
                               f'Monthly daromad: {monthly_revenue:,.0f} so\'m, xarajat: {monthly_expenses:,.0f} so\'m'
            },
            'financial_plan': {
                'monthly_profit': f'{monthly_profit:,.0f} so\'m',
                'payback_period': f'{payback_months} oy' if payback_months > 0 else 'Hisoblanmoqda'
            },
            'swot': {
                'strengths': ['Aniq biznes yo\'nalishi', 'Raqamli bozor'],
                'weaknesses': ['Boshlang\'ich xarajatlarni nazorat qilish'],
                'opportunities': ['O\'sish imkoniyatlari']
            },
            'credit': {
                'monthly_payment': f'{monthly_profit * 0.3:,.0f} so\'m' if monthly_profit > 0 else '—',
                'risk_level': 'O\'rta'
            },
            'tax': {
                'monthly_estimate': f'{monthly_revenue * 0.04:,.0f} so\'m',
                'regime': '4% aylanma solig\'i'
            }
        }
        return business_plan
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Business plan error: {str(e)}')


@app.post('/api/v1/pdf/export')
def export_business_plan_pdf(payload: Dict[str, Any]):
    """Export business plan as PDF"""
    try:
        # Simple mock PDF response (WeasyPrint integration would happen here)
        import io
        from datetime import datetime
        
        project_name = payload.get('project_name', 'Business Plan')
        
        # Create a simple PDF-like response
        pdf_content = f"""
        AI FinAdvisor Business Plan
        ==========================
        Project: {project_name}
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        
        This is a placeholder PDF. 
        In production, WeasyPrint would generate a full PDF here.
        """.encode('utf-8')
        
        return io.BytesIO(pdf_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'PDF export error: {str(e)}')