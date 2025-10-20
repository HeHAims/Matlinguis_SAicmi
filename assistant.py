# core/assistant.py
from typing import Callable, Optional
from core.prompt_manager import PromptManager

class MathTutor:
    def __init__(self, memory, emotions, goals, self_model, translator,
                 llm_call: Optional[Callable[[str], str]] = None,
                 prompt_manager: Optional[PromptManager] = None):
        self.memory = memory
        self.emotions = emotions
        self.goals = goals
        self.self_model = self_model
        self.translator = translator
        self.llm_call = llm_call
        self.prompt_manager = prompt_manager or PromptManager()

    def explain_formula(self, formula):
        complexity = self.translator.calculate_complexity(formula)
        domain = self.translator.identify_domain(formula)

        self.emotions.update_stress(complexity * 0.5)
        self.self_model.update_engagement(domain)

        similar_formulas = self.memory.recall_similar(formula, domain)
        self.memory.consolidate(formula, {"domain": domain, "complexity": complexity})

        explanation = self.translator.translate(formula, level="intermediate")

        similar_text = ""
        if similar_formulas:
            unique_formulas = list(dict.fromkeys(similar_formulas))
            clean_examples = [
                f.replace('"', '^').replace('~', '').strip()
                for f in unique_formulas
            ]
            similar_text = "\nExamples you've seen:\n" + "\n".join(clean_examples)

        return explanation + similar_text

    # Prompt-pack path
    def respond_with_prompt(self, user_text: str, prompt_name: str) -> str:
        prompt = self.prompt_manager.get(prompt_name)
        if not prompt:
            return f"Prompt '{prompt_name}' not found."
        role = prompt.get("role", "")
        style = prompt.get("style", "")
        examples = ""
        ex_list = prompt.get("examples", [])
        if ex_list:
            pairs = []
            for ex in ex_list:
                u = ex.get("user", "")
                a = ex.get("assistant", "")
                pairs.append(f"User: {u}\nAssistant: {a}")
            examples = "\n\n".join(pairs)
        composed = (
            f"{role}\nStyle: {style}\n\n"
            f"Few-shot examples:\n{examples}\n\n"
            f"Now respond to the user:\nUser: {user_text}\nAssistant:"
        )
        if not self.llm_call:
            return "[LLM not configured]\n---\n" + composed
        return self.llm_call(composed)

class EmoBot(MathTutor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_formula = None
        self.last_raw_input = None
        self.last_prompt_name = "math_explainer_friendly"
        self.last_route = "MATH"  # or "PROMPT"

    def _looks_like_math(self, text: str) -> bool:
        if not text:
            return False
        math_symbols = set("+-*/=^()[]{}√Σπ∫∂Σ")
        return any(ch in math_symbols for ch in text)

    def explain_formula(self, formula):
        self.last_formula = formula
        self.last_raw_input = formula
        raw_explanation = super().explain_formula(formula)
        if not raw_explanation.strip():
            raw_explanation = "(no translation available)"
        return self._apply_emotional_style(raw_explanation)

    def respond(self, user_text: str, prompt_name: str = "math_explainer_friendly") -> str:
        self.last_raw_input = user_text
        self.last_prompt_name = prompt_name
        domain = self.translator.identify_domain(user_text)
        math_domains = ("algebra","calculus","geometry","trig","probability","statistics")

        if domain == "general" or domain not in math_domains:
            self.last_route = "PROMPT"
            out = self.respond_with_prompt(user_text, prompt_name)
            return self._apply_emotional_style(out)

        self.last_route = "MATH"
        return self.explain_formula(user_text)

    def handle_user_feedback(self, feedback):
        if not (self.last_raw_input or self.last_formula):
            return "I don't have context yet."

        f = (feedback or "").strip()

        # If last was MATH but user feedback looks non-math, flip to prompt path
        if self.last_route == "MATH" and not self._looks_like_math(f):
            # pick a sensible default if none set yet
            prompt = self.last_prompt_name or "ethics_coach_balanced"
            out = self.respond_with_prompt(f, prompt)
            self.last_route = "PROMPT"
            return self._apply_emotional_style(out)

        # PROMPT path refinements
        if self.last_route == "PROMPT":
            fl = f.lower()
            if "simpler" in fl or "simple" in fl or "más simple" in fl:
                hint = "Please simplify the explanation: shorter, clearer steps."
            elif "more" in fl or "detail" in fl or "más" in fl:
                hint = "Please add a bit more detail and one concrete example."
            else:
                hint = "Try a different analogy and end with one concrete action."
            composed = f"{self.last_raw_input}\n\nRefinement: {hint}"
            out = self.respond_with_prompt(composed, self.last_prompt_name or "ethics_coach_balanced")
            return self._apply_emotional_style(out)

        # default: stay in math mode
        fl = f.lower()
        if "simpler" in fl or "simple" in fl or "más simple" in fl:
            return f"I'll simplify...\n{self.explain_formula(self.last_formula)}"
        if "more" in fl or "detail" in fl or "más" in fl:
            return f"Here's more detail...\n{self.explain_formula(self.last_formula)}"
        return f"Let me try a different explanation...\n{self.explain_formula(self.last_formula)}"

    def _apply_emotional_style(self, explanation):
        mood = self.emotions.current_mood()
        if mood == "frustration":
            return f"\n*Sigh* Look, it's {explanation}. Got it?"
        elif mood == "confidence":
            return f"\nAbsolutely! {explanation.capitalize()}!"
        elif mood == "playfulness":
            return f"\n✨ Ta-da! {explanation} ✨"
        else:
            return f"\nHmm... {explanation}... interesting, right?"
