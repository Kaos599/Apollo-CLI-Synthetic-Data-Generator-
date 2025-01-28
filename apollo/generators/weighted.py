import random

class WeightedGenerator:
    def __init__(self, choices_str):
        self.choices = self._parse_choices(choices_str)

    def _parse_choices(self, choices_str):
        choices = {}
        for choice_pair in choices_str.split(','):
            if ':' not in choice_pair:
                raise ValueError(f"Invalid choice format: '{choice_pair}'. Use 'choice:probability'.")
            choice, probability_str = choice_pair.split(':')
            try:
                probability = float(probability_str)
                if not 0 <= probability <= 1:
                    raise ValueError(f"Probability for '{choice}' must be between 0 and 1.")
                choices[choice] = probability
            except ValueError:
                raise ValueError(f"Invalid probability value for '{choice}': '{probability_str}'. Must be a float between 0 and 1.")
        return choices

    def generate_record(self):
        rand_val = random.random()
        cumulative_probability = 0.0
        for choice, probability in self.choices.items():
            cumulative_probability += probability
            if rand_val < cumulative_probability:
                return choice
        # Fallback in case of rounding errors, should rarely happen
        return list(self.choices.keys())[-1] if self.choices else None


    def generate_data(self, num_entries):
        return [{'response': self.generate_record()} for _ in range(num_entries)]