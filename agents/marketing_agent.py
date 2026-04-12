import re
from message_bus import get_messages, create_message, send_message
from llm import call_llm
from slack_utils import send_slack_message
from email_utils import send_email


class MarketingAgent:
    def run(self):
        messages = get_messages("marketing")

        for msg in messages:
            print("\n[Marketing] Received task")

            startup_name = msg["payload"].get("startup_name", "TaskTriage")
            goal = msg["payload"].get("goal", "Create launch content")

            prompt = f"""
You are a startup marketing specialist.

Create launch content for this startup:
Startup Name: {startup_name}
Goal: {goal}

Return exactly in this format:

SLACK:
<short exciting slack launch message>

TAGLINE:
<short catchy tagline>

EMAIL_SUBJECT:
<professional launch email subject>

EMAIL_BODY:
<short professional launch email body>

SOCIAL_POST:
<short LinkedIn-style or Instagram-style launch post>

Make it polished, realistic, and concise.
"""

            output = call_llm(prompt)

            print("\n[Marketing Output]")
            print(output)

            parsed = self.parse_output(output)

            print("\n[Marketing Parsed]")
            print(parsed)

            # 🔥 REAL ACTIONS
            send_slack_message(parsed["slack"])
            send_email(parsed["email_subject"], parsed["email_body"])

            # Send result back to CEO
            result_msg = create_message(
                from_agent="marketing",
                to_agent="ceo",
                message_type="result",
                payload=parsed,
                parent_id=msg.get("message_id")
            )
            send_message(result_msg)

    def parse_output(self, text):
        def extract(section_name, next_section_names):
            if next_section_names:
                pattern = rf"{section_name}:\s*(.*?)(?=\n(?:{'|'.join(next_section_names)}):|\Z)"
            else:
                pattern = rf"{section_name}:\s*(.*)"
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            return match.group(1).strip() if match else ""

        return {
            "slack": extract("SLACK", ["TAGLINE", "EMAIL_SUBJECT", "EMAIL_BODY", "SOCIAL_POST"]),
            "tagline": extract("TAGLINE", ["EMAIL_SUBJECT", "EMAIL_BODY", "SOCIAL_POST"]),
            "email_subject": extract("EMAIL_SUBJECT", ["EMAIL_BODY", "SOCIAL_POST"]),
            "email_body": extract("EMAIL_BODY", ["SOCIAL_POST"]),
            "social_post": extract("SOCIAL_POST", [])
        }