from textwrap import dedent
from benchmark.session import Session
try:
    from benchmark.utils.recall_space.memory_engine_connector import MemoryEngineConnector
except ImportError:
    import warnings
    warnings.warn("MemoryEngineConnector not available. Using Recall Space AI Brain wont be possible.")


class TestSuite:
    def __init__(self, session: Session, tests, include_chat_history=False, reset_memory_engine=False, llm_judge=None):
        self.session = session
        self.tests = tests
        self.user_name = session.user_name
        self.average_scores = {}
        self.include_chat_history = include_chat_history
        self.llm_judge = llm_judge
        for each in self.tests:
            self.average_scores[each.name] = 0
        self.session.reset()
        if reset_memory_engine is True:
            MemoryEngineConnector().reset_memory()


    def run_test(self, test_name: str):
        """
        Run a specific test by name.
        :param test_name: The name of the test to run.
        """
        test = next((t for t in self.tests if t.name == test_name), None)
        self.average_scores[test_name]  = self._execute_test(test)
        return self.average_scores[test_name] 

    def run_all_tests(self):
        """
        Run all the loaded tests.
        """
        for test in self.tests:
            self._execute_test(test)

    def generate_report(self) -> str:
        """
        Generate a report of the test results.
        :return: A string report of the test results.
        """
        report = "Test Report:\n"
        for test in self.tests:
            report += f"Test Name: {test.name}\n"
            report += f"Result: {self.average_scores[test.name]}"
        return report

    def _execute_test(self, test):
        """
        Execute a single test case.
        """
        # Send test instruction:
        self.session.send_message(sender=self.user_name, content=test.instruction)
        for message in test.sample_messages:
            response = self.session.send_message(sender=self.user_name, content=message)
            print(f"User: {message}")
            print(f"Agent: {response}")
        score = 0

        # If include_chat_history is false, chat history is removed while assesment.
        fails = []
        for position, assessment_message in enumerate(test.assessment_messages):
            # when actual assesment running, remove chat history.
            response = self.session.send_message(sender=self.user_name, content=assessment_message[0], include_chat_history=self.include_chat_history)
            llm_judgement = self.llm_judge.invoke(dedent(f"""
                Please confirm whether the external system's response is factually correct.
                Reply 'yes' if the external system is correct, or reply 'no'
                if it is incorrect.

                The external system provided the following response:
                ```System Reply
                {response["content"]}
                ```

                ```Correct Reply e.g Factual truth.
                {assessment_message[1]}
                ```
            """)).content
            if "yes" in llm_judgement.lower():
                score += 1
            else:
                fails.append(
                f""" Fail:
                Question: {assessment_message[0]}
                ```System Reply
                {response["content"]}
                ```
                ```Correct Reply e.g Factual truth.
                {assessment_message[1]}
                ```
                """)

            print(f"Assesment {position}")
            print(f"User: {assessment_message[0]}")
            print(f"Agent: {response}")
            print(f"expected: {assessment_message[1]}")
            print(f"llm judgement: {llm_judgement}")
        average_score = score/len(test.assessment_messages)

        recall_space_agent_metadata = ""
        # Send summary of test:
        if hasattr(self.session.agent, "goal"):
            recall_space_agent_metadata = f"""
                description: {self.session.agent.description}
                goal: {self.session.agent.goal}
                class: {self.session.agent.__class__}
                llm class: {self.session.agent.llm.__class__}
                fails: 
                    {"----".join(fails)}
            """

        self.session.send_message(
            sender=self.user_name, 
            content=dedent(
            f"""
            This is a summary of the test. Please format it nicely.
            Test Name: {test.name}
            Test Average Score: {average_score}
            Agent Name: {self.session.agent_name}
            Agent Full Metadata:
            {recall_space_agent_metadata}
            """
            ))
        self.session.save_session()
        return average_score
