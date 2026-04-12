from message_bus import create_message, send_message, get_messages
from llm import call_llm
import json
import re

class CEOAgent:
    def __init__(self, idea):
        self.idea = idea
        self.revision_count = 0
        self.max_revisions = 2

    def send_task_to_product(self):
        print(f"\n[CEO] Received Startup Idea: {self.idea}")

        msg = create_message(
            from_agent="ceo",
            to_agent="product",
            message_type="task",
            payload={
                "idea": self.idea,
                "task": "Create product specification"
            }
        )
        send_message(msg)
        print("[CEO] Task sent to Product Agent.")

    def receive_product_response(self):
        messages = get_messages("ceo")

        for msg in messages:
            if msg["from_agent"] != "product" or msg["message_type"] != "result":
                continue

            spec = msg.get("payload") or {}

            # Stop infinite loops
            if self.revision_count >= self.max_revisions:
                print("\n[CEO] ⚠️ Max revisions reached. Forcing approval.")
                self._delegate_to_agents()
                return True

            print("\n[CEO] Reviewing product spec using LLM reasoning...")

            review_prompt = f"""
            You are a professional Startup CEO.

            Review this product specification for 'TaskTriage':
            {json.dumps(spec, indent=2)}

            Criteria:
            - Exactly 5 features
            - Must clearly support micro-tasking
            - Strong value for stressed students

            Return ONLY JSON:
            {{
                "decision": "approve" or "revise",
                "feedback": "..."
            }}
            """

            llm_output = call_llm(review_prompt)

            try:
                match = re.search(r"\{.*\}", llm_output, re.DOTALL)
                review = json.loads(match.group())
            except Exception as e:
                print(f"⚠️ Parsing failed ({e}), approving by default")
                self._delegate_to_agents()
                return True

            if review.get("decision") == "revise":
                self.revision_count += 1
                print(f"[CEO] Decision: REVISE ❌ ({self.revision_count}/{self.max_revisions})")

                revision_msg = create_message(
                    from_agent="ceo",
                    to_agent="product",
                    message_type="revision_request",
                    payload={
                        "feedback": review.get("feedback", "Improve features")
                    },
                    parent_id=msg["message_id"]
                )
                send_message(revision_msg)
                return False

            else:
                print("[CEO] Decision: APPROVED ✅")
                self._delegate_to_agents()
                return True

    def _delegate_to_agents(self):
        """Send tasks to BOTH Engineer and Marketing"""

        # ENGINEER
        print("[CEO] Delegating to Engineer...")
        engineer_msg = create_message(
            from_agent="ceo",
            to_agent="engineer",
            message_type="task",
            payload={"action": "build landing page"}
        )
        send_message(engineer_msg)

        # MARKETING (🔥 NEW)
        print("[CEO] Delegating to Marketing...")
        marketing_msg = create_message(
            from_agent="ceo",
            to_agent="marketing",
            message_type="task",
            payload={
                "startup_name": "TaskTriage",
                "goal": "Create launch message, tagline, and social content"
            }
        )
        send_message(marketing_msg)

    def send_final_summary(self):
        print("[CEO] Startup process complete.")