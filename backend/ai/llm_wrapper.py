"""
Modul 1: LLM Wrapper — OpenAI va Groq uchun
"""

import os

try:
    from .system_prompt import get_system_prompt, prepend_context_to_prompt
except ImportError:  # Faylni bevosita ishga tushirishdagi import uchun
    from system_prompt import get_system_prompt, prepend_context_to_prompt


class AIClient:
    """OpenAI va Groq uchun unified wrapper"""
    
    def __init__(self, use_groq: bool = False):
        """
        LLM clientini boshlash
        
        Args:
            use_groq (bool): True bo'lsa Groq ishlatadi, False bo'lsa OpenAI (default)
        """
        self.use_groq = use_groq
        self.openai_api_key = os.getenv("PLATFORM_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        
        if not use_groq and not self.openai_api_key:
            raise ValueError("PLATFORM_OPENAI_API_KEY yoki OPENAI_API_KEY environment variable yo'q")
        if use_groq and not self.groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable yo'q")
    
    def ask_ai(self, user_query: str, context: str = "") -> str:
        """
        AI'ga savol beradi va javob qaytaradi
        
        Args:
            user_query (str): Foydalanuvchi savoli
            context (str): RAG'dan kelgan kontekst (opsional)
        
        Returns:
            str: AI javob (o'zbek tilida)
        """
        full_prompt = prepend_context_to_prompt(user_query, context)

        # 1) Try Gemini (Google Generative API) if available and key is set
        try:
            gemini_resp = self._ask_gemini(full_prompt)
            if gemini_resp:
                return gemini_resp
        except Exception:
            pass

        # 2) Try Groq if configured
        try:
            if self.groq_api_key:
                try:
                    return self._ask_groq(full_prompt)
                except Exception:
                    # fall through to OpenAI
                    pass
        except Exception:
            pass

        # 3) Finally, try OpenAI
        return self._ask_openai(full_prompt)
    
    def _ask_openai(self, prompt: str) -> str:
        """
        OpenAI gpt-4o-mini ga savol beradi
        
        Args:
            prompt (str): To'liq prompt (kontekst + savol)
        
        Returns:
            str: Javob
        """
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.openai_api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Hallucination oldinini olish uchun tushir
                max_tokens=2000
            )
            content = response.choices[0].message.content
            if not content:
                raise RuntimeError("OpenAI bo'sh javob qaytardi")
            return content
        except ImportError:
            raise ImportError("openai kutubxonasi o'rnatilmagan. Ishqar: pip install openai")
    
    def _ask_groq(self, prompt: str) -> str:
        """
        Groq llama-3.1-70b ga savol beradi (zaxira)
        
        Args:
            prompt (str): To'liq prompt
        
        Returns:
            str: Javob
        """
        try:
            from groq import Groq
            
            client = Groq(api_key=self.groq_api_key)
            response = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {"role": "system", "content": get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            content = response.choices[0].message.content
            if not content:
                raise RuntimeError("Groq bo'sh javob qaytardi")
            return content
        except ImportError:
            raise ImportError("groq kutubxonasi o'rnatilmagan. Ishqar: pip install groq")

    def _ask_gemini(self, prompt: str) -> str:
        """
        Try Google Generative / Gemini via available client wrappers or REST.
        Returns response text or raises/returns None on failure.
        """
        gemini_key = os.getenv('GEMINI_API_KEY') or os.getenv('GEMINI_API_KEY2')
        if not gemini_key:
            return None

        # Try google.generativeai wrapper
        try:
            try:
                import google.generativeai as genai
            except Exception:
                import google as genai_pkg
                genai = getattr(genai_pkg, 'generativeai', None)

            # configure if available
            try:
                genai.configure(api_key=gemini_key)
            except Exception:
                pass

            if hasattr(genai, 'generate_text'):
                resp = genai.generate_text(model="text-bison-001", input=prompt)
                if isinstance(resp, dict):
                    return resp.get('candidates', [{}])[0].get('content') if resp.get('candidates') else resp.get('output')
                return getattr(resp, 'text', str(resp))

            if hasattr(genai, 'TextGenerationClient'):
                client = genai.TextGenerationClient()
                resp = client.generate(model="text-bison-001", prompt=prompt)
                return getattr(resp, 'text', None) or str(resp)
        except Exception:
            # fall through to REST attempt
            pass

        # Fallback: simple REST call (gemini_wrapper handles status codes)
        try:
            from .gemini_wrapper import test_key as _test_key
        except Exception:
            try:
                from gemini_wrapper import test_key as _test_key
            except Exception:
                _test_key = None

        if _test_key:
            ok, resp = _test_key(gemini_key, prompt)
            if ok:
                # try to extract text
                if isinstance(resp, dict):
                    # try common shapes
                    if 'candidates' in resp:
                        return resp['candidates'][0].get('content')
                    if 'output' in resp:
                        return resp['output']
                return str(resp)

        return None


async def ask_ai_async(
    user_query: str,
    context: str = "",
    use_groq: bool = False
) -> str:
    """
    Async versiya (keyinchalik FastAPI'da ishlatiladi)
    
    Args:
        user_query (str): Savol
        context (str): Kontekst
        use_groq (bool): Groq ishlatishmi?
    
    Returns:
        str: Javob
    """
    client = AIClient(use_groq=use_groq)
    return client.ask_ai(user_query, context)
