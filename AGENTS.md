# 🤖 LeadGen AI — Agent Reference

This document describes each agent in the LeadGen AI CrewAI system.

---

## 1. Lead Research Agent
**File:** `src/leadgen_ai/agents/lead_research_agent.py`

| Property | Value |
|----------|-------|
| Role | Lead Research Specialist |
| Tools | Serper Search Tool |
| Delegation | Disabled |

**Responsibility:**
Searches the web for potential business leads matching the user's query.
Finds 3–5 relevant companies with website URLs and brief descriptions.

---

## 2. Company Research Agent
**File:** `src/leadgen_ai/agents/company_research_agent.py`

| Property | Value |
|----------|-------|
| Role | Company Intelligence Analyst |
| Tools | Website Scraper Tool |
| Delegation | Disabled |

**Responsibility:**
Visits each company's website and extracts key business intelligence —
products, services, target audience, company stage, and recent activity.

---

## 3. Personalization Agent
**File:** `src/leadgen_ai/agents/personalization_agent.py`

| Property | Value |
|----------|-------|
| Role | Outreach Personalization Strategist |
| Tools | None (reasoning-only) |
| Delegation | Disabled |

**Responsibility:**
Analyzes company research to craft personalized outreach hooks,
identify pain points, and define a value proposition and tone for each lead.

---

## 4. Outreach Agent
**File:** `src/leadgen_ai/agents/outreach_agent.py`

| Property | Value |
|----------|-------|
| Role | Cold Outreach Copywriter |
| Tools | Email Saver Tool |
| Delegation | Disabled |

**Responsibility:**
Writes professional, personalized cold emails for each lead (under 150 words).
Saves all generated outreach content to the `data/` folder.

---

## Agent Execution Order