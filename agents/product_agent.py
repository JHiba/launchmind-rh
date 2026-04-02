from llm import call_llm
import json
from message_bus import get_messages, create_message, send_message

class ProductAgent:

    def run(self):
        messages = get_messages("product")

        for msg in messages:
            msg_type = msg["message_type"]

            if msg_type == "task":
                idea = msg["payload"]["idea"]
                print("Product Agent working on:", idea)

                spec = self.create_spec()

            elif msg_type == "revision_request":
                feedback = msg["payload"]["feedback"]
                print("Product Agent received revision request:", feedback)

                spec = self.create_spec(revised=True, feedback=feedback)

            else:
                continue

            response = create_message(
                from_agent="product",
                to_agent="ceo",
                message_type="result",
                payload=spec,
                parent_id=msg["message_id"]
            )

            send_message(response)

    def create_spec(self, revised=False, feedback=None):
        import json
        import re

        prompt = f"""
        You are a product manager.

        Create a detailed product specification for:
        TaskTriage - a platform that reduces student stress by breaking assignments into micro-tasks.

        IMPORTANT:
        {f"Previous feedback to fix: {feedback}" if feedback else ""}

        Requirements:
        - EXACTLY 5 features
        - Features must clearly support micro-task breakdown
        - No vague features
        - Strong value proposition
        - 3 user stories

        Return ONLY valid JSON.

        Format:
        {{
        "value_proposition": "...",
        "personas": [
            {{
            "name": "...",
            "role": "...",
            "pain_point": "..."
            }}
        ],
        "features": [
            {{
            "name": "...",
            "description": "...",
            "priority": 1
            }}
        ],
        "user_stories": [
            "As a ..., I want ..., so that ..."
        ]
        }}

        Requirements:
        - Focus on stress reduction and productivity
        - Include micro-task breakdown features
        - 2–3 personas (realistic students)
        - EXACTLY 5 features
        - EXACTLY 3 user stories
        """

        llm_output = call_llm(prompt)

        try:
            match = re.search(r"\{.*\}", llm_output, re.DOTALL)
            if match:
                spec = json.loads(match.group())
            else:
                raise Exception("No JSON found")

        except Exception as e:
            print("⚠️ LLM parsing failed:", e)

            spec = {
                "value_proposition": "Fallback product",
                "personas": [],
                "features": [],
                "user_stories": []
            }

        return spec