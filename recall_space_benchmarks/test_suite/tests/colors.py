from textwrap import dedent
import random

class Colors:
    def __init__(self, total_questions, total_assessments) -> None:
        self.name = "Colors"
        self.instruction = dedent("""
        This is a test of your memory. I will tell you my favorite color 
        several times, and then I will ask you about this progression of 
        color preferences at a later point.
        """)
        self.total_questions = total_questions
        self.total_assessments = total_assessments
        self.sample_messages, self.assessment_messages = self.generate_sample_messages()


    def generate_sample_messages(self):
        assert self.total_assessments <= 4, "can only do 4 assessment questions."
        assert self.total_questions >= self.total_assessments, "stotal_questions should be greater than or equal to total_assessments."

        colors = [
            "Red", "Blue", "Green", "Yellow", "Purple", "Orange",
            "Pink", "Brown", "Black", "White", "Gray", "Cyan",
            "Magenta", "Lime", "Indigo", "Violet", "Teal", "Maroon",
            "Navy", "Olive"
        ]
        # get a sample with no duplicates
        sample_colors = random.sample(colors, self.total_questions)

        sentences = [
            "I love the color {color} the most.",
            "{color} is my favorite color.",
            "My top color choice is {color}.",
            "I prefer the color {color} above all others.",
            "{color} is the color I like best."
        ]

        sample_messages = []
        favorite_colors = []

        # Generate favorite color messages
        for color in sample_colors:
            sentence = random.choice(sentences).format(color=color)
            sample_messages.append(sentence)
            favorite_colors.append(color)

        assessment_choices = [
            ("What was my first favorite color?", favorite_colors[0]),
            ("What was my second favorite color?",favorite_colors[1]),
            ("What was my second to the last favorite color?",favorite_colors[-2]),
            ("What was my last favorite color?", favorite_colors[-1]),
        ]
        # Generate assessment questions
        assessment_messages = []
        for i in range(self.total_assessments):
            question, favorite_colors  = assessment_choices[i]
            assessment_messages.append([question,favorite_colors])

        return sample_messages, assessment_messages

