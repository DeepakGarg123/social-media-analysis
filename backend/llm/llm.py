import json
import requests

print("Loading analytics report...")

with open(
    "backend/data/analytics_report.json",
    "r",
    encoding="utf-8"
) as f:
    report = json.load(f)

print("Analytics report loaded.")

llm_report = {
    "profile": report.get("profile"),
    "metrics": report.get("metrics"),
    "growth": report.get("growth"),
    "llm_insights": report.get("llm_insights")
}
print("LLM-ready analytics created.")

prompt = f"""
You are an AI social media growth advisor.

Your job is to provide practical strategies that can help the Instagram
account owner grow their account.

The analytics report contains reliable insights calculated by the analytics
system. Use these insights as the primary evidence for your recommendations.

Rules:

1. Give exactly 3 practical growth recommendations.
2. Every recommendation must be connected to one or more provided insights.
3. Turn the insight into a specific action the account owner can take.
4. You may use general social media strategy to explain how to act on an
   observed pattern, but do not claim unsupported facts.
5. Do not invent metrics, numbers, trends, causes, or performance results.
6. Do not claim that a strategy will definitely increase followers.
7. Do not treat follower growth as proof that a particular post or content
   type caused the growth.
8. Do not recommend a content type when the analytics say there is insufficient
   data for that conclusion.
9. Explain the evidence behind every recommendation.
10. Recommendations should focus on improving reach, engagement, content
    performance, or follower growth.
11. Avoid simply repeating the analytics. Convert the findings into actions.
12. If an insight is not strong enough to support a recommendation, do not use it.
13. Do not use words such as "maximize", "guarantee", "will increase",
or "will improve" unless the analytics directly prove such a relationship.
14. When an insight is based on a single post or possible outlier,
recommend studying and testing that pattern rather than making a
broad content strategy recommendation.
15. When comparing content types, treat the result as an observed
pattern and recommend testing the better-performing type rather
than claiming it will increase engagement.
16. Prefer recommendations that can be tested and measured using
future analytics.
17. Never use the phrase "statistically significant" or claim statistical
significance unless the analytics explicitly provide a statistical test
and its result.
18. Never imply causation from correlation or comparison. Use phrases such
as "observed higher", "performed better in the analyzed sample",
"test", or "evaluate" instead.


Use exactly this format:

Recommendation 1:
Action:
Why:
Evidence:

Recommendation 2:
Action:
Why:
Evidence:

Recommendation 3:
Action:
Why:
Evidence:

Analytics:

{json.dumps(llm_report, indent=2)}
"""

print("Prompt size:", len(prompt), "characters")
print("Sending analytics to llama...")

url = "http://localhost:11434/api/generate"

data = {
    "model": "llama3.2:latest",
    "prompt": prompt,
    "stream": False,
}

response = requests.post(url, json=data)

print("Response received.")

result = response.json()

print("\nLLM Growth Suggestions:\n")
print(result["response"])