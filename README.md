# LaunchMind / TaskTriage Multi-Agent Startup System

A multi-agent startup automation system built for an Agentic AI assignment. The system simulates a startup team where AI agents collaborate to design, review, build, and market a product called **TaskTriage**.

## Project Idea

**TaskTriage** is a platform that helps students reduce stress by breaking large assignments into small manageable micro-tasks.

## Agents in the System

### 1. CEO Agent
- Receives the startup idea
- Sends the task to the Product Agent
- Reviews the generated product specification using an LLM
- Approves or requests revision
- Delegates work to Engineer and Marketing agents

### 2. Product Agent
- Generates product specification
- Creates value proposition
- Creates features
- Creates personas
- Creates user stories
- Revises output based on CEO feedback

### 3. Engineer Agent
- Generates landing page code
- Creates a real GitHub issue
- Commits code to the repository
- Works with the PR branch flow

### 4. Marketing Agent
- Generates launch content
- Creates Slack announcement
- Creates email subject and email body
- Creates social media style post
- Sends a real Slack message
- Sends a real Gmail email

## Real Integrations

This system performs real actions on real platforms:

- **GitHub**
  - Issue creation
  - Code commit
  - PR workflow branch support

- **Slack**
  - Real Slack message via Incoming Webhook

- **Gmail**
  - Real email sending using Gmail SMTP and App Password

## Current Workflow

1. CEO receives startup idea
2. CEO sends task to Product Agent
3. Product Agent generates product specification
4. CEO reviews and either approves or requests revision
5. CEO delegates to Engineer Agent
6. CEO delegates to Marketing Agent
7. Engineer Agent creates issue and commits landing page code
8. Marketing Agent generates launch content
9. Marketing Agent sends Slack message
10. Marketing Agent sends email

## Tech Stack

- Python
- Groq API
- GitHub REST API
- Slack Incoming Webhooks
- Gmail SMTP
- dotenv

## Project Structure

```text
launchmind-rh/
│
├── agents/
│   ├── ceo_agent.py
│   ├── product_agent.py
│   ├── engineer_agent.py
│   └── marketing_agent.py
│
├── llm.py
├── message_bus.py
├── slack_utils.py
├── email_utils.py
├── main.py
├── requirements.txt
├── .env.example
└── README.md