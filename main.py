import time
from agents.ceo_agent import CEOAgent
from agents.product_agent import ProductAgent
from agents.engineer_agent import EngineerAgent
from agents.marketing_agent import MarketingAgent

idea = "TaskTriage: A platform that breaks large assignments into small manageable tasks to reduce student stress"

ceo = CEOAgent(idea)
product = ProductAgent()
engineer = EngineerAgent()
marketing = MarketingAgent()

ceo.send_task_to_product()

print("\n🚀 Startup launched. Agents are now autonomous...")

while True:
    product.run()
    ceo.receive_product_response()
    engineer.run()
    marketing.run()
    break