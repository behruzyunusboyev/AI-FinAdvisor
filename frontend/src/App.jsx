import { useState } from 'react'
import { BrowserRouter, Link, Route, Routes, useNavigate } from 'react-router-dom'
import { ArrowRight, Calculator, Clock3, FileText, Gauge, PiggyBank, Sparkles } from 'lucide-react'
import BusinessWizard from './components/Wizard/BusinessWizard'
import CompareResults from './components/CompareResults'
import Dashboard from './components/Dashboard/Dashboard'
import { submitBusinessPlan } from './api/businessPlan'
import './App.css'
import './dark-theme.css'
import './wizard-layout.css'

const readCompareResults = () => { try { return JSON.parse(sessionStorage.getItem('finadvisor-compare-results') || '{}') } catch { return {} } }
const features = [[FileText, 'Dinamik Biznes-reja', '6 bosqichli so‘rovnoma asosida moliyaviy model.'], [Calculator, '2026 Soliq Kalkulyatori', 'YaTT va MChJ soliq yuklamasini solishtiring.'], [Gauge, 'Bankka Tayyorlik Indeksi', 'Kredit ehtimolini aniq ko‘rsatkichlar bilan biling.'], [Sparkles, 'AI Business Copilot', 'Kunlik kassa monitoringi va tezkor tahlil.']]

function Layout({ children }) { return <div className="app-shell"><header className="topbar"><Link to="/" className="brand"><span className="brand-icon"><Calculator size={20} /></span><span><b>AI FinAdvisor</b><small>O'ZBEKISTON KOB PLATFORMASI — 2026</small></span></Link><nav><Link to="/">Bosh sahifa</Link><Link to="/create">Biznes-reja</Link><Link className="nav-cta" to="/create">Yangi reja</Link></nav></header>{children}<footer>© 2026 AI FinAdvisor · O'zbekiston KOB bizneslari uchun moliyaviy rejalashtirish</footer></div> }
function Home() { return <main className="home"><section className="hero"><span className="hero-pill"><i />2026-yilgi moliyaviy model</span><h1>Biznesingiz uchun 2 daqiqada <em>bank talabiga mos</em> biznes-reja</h1><p>O‘zbekistondagi KOB, YaTT va startaplar uchun aniq moliyaviy hisob, soliq taqqoslash va bankka tayyor PDF.</p><div className="hero-actions"><Link to="/create" className="button primary">Biznes-reja tuzishni boshlash<ArrowRight size={18} /></Link><Link to="/compare" className="button gold">2 ta g‘oyani solishtirish<ArrowRight size={18} /></Link></div></section><section className="quick-stats"><article><Clock3 /><b>2 daqiqa</b><span>hisoblash vaqti</span></article><article><PiggyBank /><b>1.5–5 mln so‘m</b><span>konsalting tejami</span></article><article><FileText /><b>Bank andozasi</b><span>PDF formatda</span></article></section><section className="feature-section"><header><h2>Platforma imkoniyatlari</h2><p>Biznesingizni to‘liq tahlil qilish uchun to‘rtta vosita.</p></header><div className="feature-grid">{features.map(([Icon, title, text]) => <article key={title}><span><Icon size={24} /></span><h3>{title}</h3><p>{text}</p></article>)}</div></section></main> }
function Create() { const navigate = useNavigate(); const [busy, setBusy] = useState(false); const [error, setError] = useState(''); const submit = async data => { setBusy(true); setError(''); try { const response = await submitBusinessPlan(data); sessionStorage.setItem('finadvisor-result', JSON.stringify({ ...response.data, request: data })); navigate('/dashboard') } catch (err) { setError(err.response?.data?.detail || 'Server bilan bog‘lanib bo‘lmadi. Backend ishlayotganini tekshiring.') } finally { setBusy(false) } }; return <main className="create-page"><Link className="back-link" to="/">← Bosh sahifa</Link><BusinessWizard onSubmit={submit} busy={busy} />{error && <p className="form-error">{error}</p>}</main> }

function ComparePage() {
  const navigate = useNavigate()
  const [drafts, setDrafts] = useState({ A: null, B: null })
  const [states, setStates] = useState({ A: 'idle', B: 'idle' })
  const [errors, setErrors] = useState({ A: '', B: '' })
  const [busy, setBusy] = useState(false)
  const runComparison = async () => {
    if (!drafts.A || !drafts.B) return
    const results = {}
    setBusy(true); setStates({ A: 'loading', B: 'loading' }); setErrors({ A: '', B: '' })
    const requestIdea = async idea => {
      try {
        const response = await submitBusinessPlan(drafts[idea])
        results[idea] = { ...response.data, request: drafts[idea] }
        setStates(previous => ({ ...previous, [idea]: 'success' }))
      } catch (error) {
        setStates(previous => ({ ...previous, [idea]: 'error' }))
        setErrors(previous => ({ ...previous, [idea]: error.response?.data?.detail || 'Xatolik yuz berdi, qayta urinib ko‘ring.' }))
      }
    }
    await Promise.all([requestIdea('A'), requestIdea('B')])
    setBusy(false)
    sessionStorage.setItem('finadvisor-compare-results', JSON.stringify(results))
    if (results.A && results.B) navigate('/compare/results')
  }
  const statusText = idea => states[idea] === 'loading' ? 'Yuklanmoqda…' : states[idea] === 'success' ? 'Natija tayyor' : states[idea] === 'error' ? errors[idea] : drafts[idea] ? 'Tayyor' : 'Hali to‘ldirilmagan'
  return <main className="compare-page"><header className="compare-header"><div><Link className="back-link" to="/">← Bosh sahifa</Link><h1>G‘oyalarni solishtirish</h1><p>Har ikki g‘oyani to‘ldiring, keyin bitta tugma bilan birga hisoblang.</p></div></header><section className="compare-grid"><div className="compare-card"><BusinessWizard variantName="A" wizardTitle="G‘oya A" onReady={data => setDrafts(previous => ({ ...previous, A: data }))} ready={!!drafts.A} /><p className={`compare-request-status ${states.A}`}>G‘oya A: {statusText('A')}</p></div><div className="compare-card"><BusinessWizard variantName="B" wizardTitle="G‘oya B" onReady={data => setDrafts(previous => ({ ...previous, B: data }))} ready={!!drafts.B} /><p className={`compare-request-status ${states.B}`}>G‘oya B: {statusText('B')}</p></div></section><div className="compare-submit-wrap"><p>{drafts.A && drafts.B ? 'Ikkala g‘oya tayyor. Hisoblashni boshlashingiz mumkin.' : `Tayyor holat: G‘oya A ${drafts.A ? '✓' : '—'} · G‘oya B ${drafts.B ? '✓' : '—'}`}</p><button type="button" className="button gold compare-submit" disabled={!drafts.A || !drafts.B || busy} onClick={runComparison}>{busy ? 'Ikkala g‘oya hisoblanmoqda…' : 'Ikkala g‘oyani solishtirish'}</button></div></main>
}

function DashboardRoute() { const navigate = useNavigate(); let result = null; try { result = JSON.parse(sessionStorage.getItem('finadvisor-result') || 'null') } catch { result = null } return result ? <Dashboard result={result} onReset={() => { sessionStorage.removeItem('finadvisor-result'); navigate('/create') }} /> : <main className="empty"><h1>Natija topilmadi</h1><Link className="button primary" to="/create">Hisoblashni boshlash</Link></main> }
function CompareResultsRoute() { const results = readCompareResults(); return results.A && results.B ? <CompareResults results={results} /> : <main className="empty"><h1>Taqqoslash yakunlanmadi</h1><p>Bir yoki ikkala g‘oya xato bilan yakunlangan bo‘lishi mumkin.</p><Link className="button primary" to="/compare">Qayta urinib ko‘ring</Link></main> }
export default function App() { return <BrowserRouter><Layout><Routes><Route path="/" element={<Home />} /><Route path="/create" element={<Create />} /><Route path="/compare" element={<ComparePage />} /><Route path="/compare/results" element={<CompareResultsRoute />} /><Route path="/dashboard" element={<DashboardRoute />} /><Route path="*" element={<Home />} /></Routes></Layout></BrowserRouter> }
