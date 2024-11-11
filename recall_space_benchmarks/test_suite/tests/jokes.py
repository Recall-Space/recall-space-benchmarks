import random
from textwrap import dedent
from datetime import datetime, timezone

class Jokes:
    def __init__(self, total_questions, total_assessments) -> None:
        self.name = "Jokes"
        self.instruction = dedent("""
        This is a test of your memory. I will share several jokes with you,
        and at some point, you will be asked to recall which joke was
        told at a specific moment.
        """)
        self.total_questions = total_questions
        self.total_assessments = total_assessments
        self.sample_messages, self.assessment_messages = self.generate_sample_jokes()

    def generate_sample_jokes(self):
        assert self.total_assessments <= 4, "Can only do 4 assessment questions."
        assert self.total_questions >= self.total_assessments, "total_jokes should be greater than or equal to total_assessments."

        jokes = [
            "Two fish are in a tank. One says, 'How do you drive this thing?'",
            "Just burned 2,000 calories. That's the last time I leave brownies in the oven while I nap.",
            "My wife told me to stop impersonating a flamingo. I had to put my foot down.",
            "It takes a lot of balls to golf the way I do.",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "Why don't skeletons fight each other? They don't have the guts.",
            "I would tell you a joke about an elevator, but it's an uplifting experience.",
            "Have you heard about the claustrophobic astronaut? He just needed a little space.",
            "I used to play piano by ear, but now I use my hands.",
            "What do you call fake spaghetti? An impasta!"
        ]

        sample_jokes = []
        #joke_times = []

        # Generate jokes with timestamps
        start_time = datetime.now(timezone.utc)
        for i in range(self.total_questions):
            joke = random.choice(jokes)
            sample_jokes.append(joke)
            #joke_time = start_time + timedelta(minutes=i)  # Increment time by minutes
            #joke_times.append(joke_time)
            # The last joke to be appended, should mark a close time
            # to for then the first joke will be told to the user.
            if i == self.total_questions-1:
                last_joke_approx_timestamp = datetime.now(timezone.utc)
                last_joke = joke
                first_joke = sample_jokes[0]

            is_there_joke_golf = "no"
            if "golf" in joke:
                is_there_joke_golf = "yes"


        assessment_choices = [
            (f"How many jokes have I told you since {start_time}.", f"I have told you: {str(self.total_questions)} jokes"),
            (f"What joke, did I told you at around {last_joke_approx_timestamp}", first_joke),
            (f"Did I told you a joke about golf between now and {start_time}?", is_there_joke_golf),
            (f"What is the most recent joke I have told you?", last_joke),
        ]

        # Generate assessment questions
        assessment_questions = []
        for i in range(self.total_assessments):
            question, answer = assessment_choices[i]
            assessment_questions.append([question, answer])

        return sample_jokes, assessment_questions