# core/math_translator.py
import re
import sympy

class EnhancedMathTranslator:
    def __init__(self):
        self.translation_rules = {
            "=": "equals",
            "+": "plus",
            "-": "minus",
            "*": "times",
            "/": "divided by",
            "^": "to the power of",
            "'": "prime",
            "∫": "the integral of",
            "∂": "the partial derivative of",
            "Σ": "the sum of",
        }
        self.whitespace_re = re.compile(r'\s+')

    def translate(self, formula, level="intermediate"):
        formula = self.whitespace_re.sub(' ', formula.strip())
        tokens = self._tokenize(formula)
        translated = []
        for token in tokens:
            if token.endswith("'") and len(token) > 1:
                base = token[:-1]
                translated.append(f"{base} prime")
            else:
                translated.append(self.translation_rules.get(token, token))
        result = " ".join(translated).strip()

        try:
            numeric_result = sympy.sympify(formula)
            if numeric_result.is_number:
                if not result:
                    result = str(numeric_result)
                else:
                    result += f" = {numeric_result}"
        except Exception:
            pass

        return result if result else "(no translation available)"

    def _tokenize(self, formula):
        return re.findall(r"(\d+\.?\d*|\w+|\S)", formula)

    def calculate_complexity(self, formula):
        return min(1.0, len(formula) / 20.0)

    # ✅ FIXED: return "general" for non-math so routing works
    def identify_domain(self, text: str) -> str:
        t = (text or "").strip()
        if any(sym in t for sym in ["∫", "∂"]):
            return "calculus"
        math_symbols = set("+-*/=^()[]{}√Σπ")
        if any(ch in math_symbols for ch in t):
            return "algebra"
        kw = ["equation","solve","factor","derivative","integral","matrix","vector",
              "probability","statistics","geometry","trig","algebra"]
        if any(k in t.lower() for k in kw):
            return "algebra"
        return "general"
