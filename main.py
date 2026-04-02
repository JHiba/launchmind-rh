# main.py
import time
from agents.ceo_agent import CEOAgent
from agents.product_agent import ProductAgent
from agents.engineer_agent import EngineerAgent

# 1. Initialize
idea = "TaskTriage: A platform that breaks large assignments into small manageable tasks to reduce student stress"
ceo = CEOAgent(idea)
product = ProductAgent()
engineer = EngineerAgent()

# 2. Start the first spark
ceo.send_task_to_product()

# 3. The "Engine" - All agents stay alive and check the bus
print("\n🚀 Startup launched. Agents are now autonomous...")
for _ in range(5):  # run 5 cycles max
    product.run()
    ceo.receive_product_response()
    engineer.run()
    
    # if approved:
    #     print("\n🎉 System completed successfully. Stopping...\n")
    #     break

    # time.sleep(2)
