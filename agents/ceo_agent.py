from message_bus import create_message, send_message, get_messages
from llm import call_llm
import json
import re

class CEOAgent:
    def __init__(self, idea):
        self.idea = idea
        self.revision_count = 0  # Internal state to track loops [cite: 179, 181]
        self.max_revisions = 2

    def send_task_to_product(self):
        """Initial spark to start the startup process[cite: 43, 45]."""
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
        """Polls for product results and autonomously decides next steps[cite: 48, 49]."""
        messages = get_messages("ceo")

        for msg in messages:
            # We only care about results from the Product Agent here
            if msg["from_agent"] != "product" or msg["message_type"] != "result":
                continue

            spec = msg.get("payload") or {}
            
            # --- AUTONOMOUS REVISION CHECK ---
            # If we've reached the limit, force approval to move the demo forward [cite: 141, 302, 306]
            if self.revision_count >= self.max_revisions:
                print("\n[CEO] ⚠️ Max revisions reached. Autonomously forcing approval for Engineer.")
                self._delegate_to_engineer()
                return True

            print("\n[CEO] Reviewing product spec using LLM reasoning...")

            review_prompt = f"""
            You are a professional Startup CEO. 
            Review this product specification for 'TaskTriage':
            {json.dumps(spec, indent=2)}

            Criteria for Approval:
            - Exactly 5 features.
            - Features must be specific and support micro-tasking.
            - Strong value proposition for stressed students.

            If it is reasonably good, respond with "approve". 
            If it is vague or missing features, respond with "revise" and provide feedback.

            Return ONLY JSON:
            {{
                "decision": "approve" or "revise",
                "feedback": "Your detailed feedback here"
            }}
            """

            llm_output = call_llm(review_prompt)

            try:
                # Use regex to find JSON in case LLM adds conversational text [cite: 64, 323]
                match = re.search(r"\{.*\}", llm_output, re.DOTALL)
                review = json.loads(match.group())
            except Exception as e:
                print(f"⚠️ [CEO] Review parsing failed ({e}), approving by default to prevent crash.")
                self._delegate_to_engineer()
                return True

            if review.get("decision") == "revise":
                self.revision_count += 1
                print(f"[CEO] Decision: REVISE ❌ (Attempt {self.revision_count}/{self.max_revisions})")
                
                revision_msg = create_message(
                    from_agent="ceo",
                    to_agent="product",
                    message_type="revision_request",
                    payload={
                        "feedback": review.get("feedback", "Improve the features and specificity.")
                    },
                    parent_id=msg["message_id"]
                )
                send_message(revision_msg)
                return False
            else:
                print("[CEO] Decision: APPROVED ✅")
                self._delegate_to_engineer()
                return True

    def _delegate_to_engineer(self):
        """Autonomously hands off the project to the Engineer Agent[cite: 46, 47]."""
        print("[CEO] Delegating task to Engineer: Build Landing Page.")
        task_msg = create_message(
            from_agent="ceo",
            to_agent="engineer",
            message_type="task",
            payload={"action": "build landing page"}
        )
        send_message(task_msg)

    def send_final_summary(self):
        """Final required step: Post summary to Slack[cite: 51, 59]."""
        print("[CEO] Startup process complete. Sending final summary to Slack...")
        # In a full system, this would call the Slack API via Block Kit [cite: 122, 233]