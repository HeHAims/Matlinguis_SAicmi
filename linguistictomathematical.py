import re
import random

class CausalReasoner:
    def __init__(self):
        # Core cause-effect patterns
        self.rules = {
            "laundry": {
                "keywords": ["boiler", "dryer", "clothes", "wash", "clean"],
                "next": ["fold the clothes", "put them in the closet"]
            },
            "cooking": {
                "keywords": ["stove", "pan", "cook", "boil", "oven"],
                "next": ["serve the food", "wash the dishes"]
            },
            "study": {
                "keywords": ["book", "study", "test", "homework"],
                "next": ["review notes", "take a break"]
            },
            "math": {
                "keywords": ["add", "subtract", "equation", "solve", "result"],
                "next": ["check your answer", "graph the function"]
            },
            "cleaning": {
                "keywords": ["vacuum", "clean", "mop", "dust"],
                "next": ["organize the room", "relax and enjoy the space"]
            }
        }

    def infer_context(self, text):
        text = text.lower()
        for context, data in self.rules.items():
            if any(k in text for k in data["keywords"]):
                return context
        return "general"

    def infer_next_action(self, text):
        context = self.infer_context(text)
        if context != "general":
            next_steps = self.rules[context]["next"]
            return random.choice(next_steps)
        else:
            return "Reflect on what you just did and decide your next step."

    def process(self, text):
        # Extract verbs (roughly)
        verbs = re.findall(r"\b\w+ed\b|\bto\s\w+\b", text)
        next_action = self.infer_next_action(text)
        return {
            "input": text,
            "detected_verbs": verbs,
            "context": self.infer_context(text),
            "predicted_next_action": next_action
        }

# Example usage
if __name__ == "__main__":
    cr = CausalReasoner()

    sentences = [
        "I turned on the boiler and got clean clothes in the bed.",
        "I finished solving the math problem.",
        "I cooked dinner on the stove.",
        "I was cleaning the living room.",
        "I studied for my test last night."
    ]

    for s in sentences:
        result = cr.process(s)
        print(result)
