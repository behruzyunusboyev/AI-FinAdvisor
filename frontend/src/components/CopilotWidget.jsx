import { useState } from 'react'
import { Sparkles } from 'lucide-react'
import { dailyCheck } from '../api/businessPlan'

export default function CopilotWidget({ projectId }) {
  const [revenue, setRevenue] = useState('2400000'); const [expense, setExpense] = useState('1700000'); const [result, setResult] = useState(null); const [error, setError] = useState(''); const [loading, setLoading] = useState(false)
  const submit = async (event) => { event.preventDefault(); setLoading(true); setError(''); try { const response = await dailyCheck({ project_id: projectId, daily_revenue: Number(revenue), daily_expense: Number(expense) }); setResult(response.data) } catch (err) { setError(err.response?.data?.detail || 'Copilot bilan bog‘lanib bo‘lmadi.') } finally { setLoading(false) } }
  return <aside className="copilot"><div className="copilot-title"><Sparkles size={19} /><div><span>AI BUSINESS COPILOT</span><strong>Bugungi kassa tekshiruvi</strong></div></div><form onSubmit={submit}><label>Bugungi tushum<input type="number" min="0" value={revenue} onChange={(e) => setRevenue(e.target.value)} /></label><label>Bugungi xarajat<input type="number" min="0" value={expense} onChange={(e) => setExpense(e.target.value)} /></label><button className="button primary" disabled={loading}>{loading ? 'Tahlil qilinmoqda…' : 'Tahlil qilish'}</button></form>{error && <p className="error">{error}</p>}{result && <div className="copilot-result"><b>{Number(result.daily_profit).toLocaleString('uz-UZ')} so‘m sof foyda</b><span>BEP progress: {result.bep_progress_pct}%</span><p>{result.insight}</p></div>}</aside>
}
