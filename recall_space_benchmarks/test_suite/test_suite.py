from textwrap import dedent
from recall_space_benchmarks.session import Session
try:
    from recall_space_benchmarks.utils.recall_space.memory_engine_connector import (
        MemoryEngineConnector,
    )
except ImportError:
    import warnings

    warnings.warn(
        "MemoryEngineConnector not available. Using Recall Space AI Brain wont be possible."
    )


class TestSuite:
    def __init__(
        self,
        session: Session,
        tests,
        include_chat_history=False,
        reset_memory_engine=False,
        llm_judge=None,
    ):
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
        self.average_scores[test_name] = self._execute_test(test)
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
        for assessment_message in test.assessment_messages:
            # when actual assesment running, remove chat history.
            response = self.session.send_message(
                sender=self.user_name,
                content=assessment_message[0],
                include_chat_history=self.include_chat_history,
            )
            print(f"Assessment ")
            print(f"---------- ")
            print(f"User: {assessment_message[0]}")
            print(f"Agent: {response['content']}")
            llm_judgement = self.llm_judge.invoke(dedent(
                    f"""
                Please assess if the external system's response contains the correct answer as a factual element.
                Focus only on confirming if the answer factually matches the expected truth provided below.

                Question: {assessment_message[0]}
                The external system provided this response:
                ```
                System Reply: {response["content"]}
                ```

                The correct factual answer should be:
                ```
                Correct Answer: {assessment_message[1]}
                ```

                Reply with 'yes' if the system's answer is correct based on the factual answer provided, or 'no' if it is incorrect.
            """
                )).content
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
                """
                )
        average_score = score / len(test.assessment_messages)

        recall_space_agent_metadata = ""
        # Send summary of test:
        if hasattr(self.session.agent, "goal"):
            recall_space_agent_metadata = f"""
                description: {self.session.agent.description}
                goal: {self.session.agent.goal}
                class: {self.session.agent.__class__}
                llm class: {self.session.agent.llm.__class__}
            """
        temp_report_messsage = dedent(
        f"""
            This is a summary of the test. Please format it nicely.
            Test Name: {test.name}
            Test Average Score: {average_score}
            Agent Name: {self.session.agent_name}
            Agent Full Metadata:
            {recall_space_agent_metadata}
            fails: 
            {"----".join(fails)}
        """
        )

        response = self.session.send_message(
            sender=self.user_name,
            content=temp_report_messsage,
        )
        print(f"Summary: {response['content']}")
        self.session.save_session()
        return average_score
