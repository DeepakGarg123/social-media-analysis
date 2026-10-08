import json
import os

from dotenv import load_dotenv
from google import genai

from backend.llm.recommendation_builder import build_recommendations

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(
    api_key=gemini_api_key
)


# --------------------------------------------------
# LOAD ANALYTICS REPORT
# --------------------------------------------------

def load_report():

    with open(
        "backend/data/analytics_report.json",
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# --------------------------------------------------
# BUILD DETERMINISTIC RECOMMENDATIONS
# --------------------------------------------------

def get_supported_recommendations(report):

    supported_recommendations = build_recommendations(
        report
    )

    return supported_recommendations


# --------------------------------------------------
# CREATE LLM-READY ANALYTICS
# --------------------------------------------------

def create_llm_report(
    report,
    supported_recommendations
):

    return {

        "profile": report.get("profile"),

        "metrics": report.get("metrics"),

        "growth": report.get("growth"),

        "top_posts": report.get("top_posts"),

        "video_analysis": report.get("video_analysis"),

        "llm_insights": report.get("llm_insights"),

        "supported_recommendations":
            supported_recommendations

    }


# --------------------------------------------------
# CREATE LLM PROMPT
# --------------------------------------------------
def create_prompt(llm_report):

    prompt = f"""
You are an AI Instagram account growth advisor.

Your job is to analyze the approved analytics findings and
recommendations provided by Python and turn them into genuine,
practical, human-friendly advice for the Instagram account owner.

You are not a generic social media advice generator.

Your recommendations must be relevant to THIS Instagram account
and must be connected to the evidence provided by Python.

==================================================
CORE RESPONSIBILITY
==================================================

Python has already analyzed the Instagram account and created:

1. Analytics
2. Reliable insights
3. Supported recommendations

Python has also decided which recommendations are supported by
the available evidence.

You must use these supported recommendations as the foundation
of your advice.

You may explain the practical meaning of a supported recommendation
and explain how the account owner can apply or test it.

You MUST NOT invent facts about the account.

==================================================
HOW YOU SHOULD THINK
==================================================

Think like a knowledgeable Instagram growth advisor who is speaking
directly to the account owner.

For every supported recommendation, ask yourself:

- What does this finding actually tell us?
- What can the account owner realistically do with this information?
- How can the owner test this idea using future Instagram content?
- What should the owner compare or monitor afterward?

Give advice that is useful in real-world Instagram management.

Do not simply repeat the analytics.

Do not write an academic explanation of the analytics.

Do not write like a research paper.

Do not use unnecessarily technical language.

==================================================
HUMAN-FRIENDLY WRITING STYLE
==================================================

Write in natural, clear and conversational English.

Speak directly to the account owner using "you" and "your"
when appropriate.

The recommendation should sound like advice from a real,
knowledgeable Instagram growth advisor.

Prefer language such as:

- "You can use this post as a reference..."
- "For your next videos, compare..."
- "This gives you a useful reference point..."
- "Based on the current data, it would be worth testing..."
- "Keep an eye on..."
- "Compare the results with..."
- "This can help you understand whether..."

Avoid overly technical or robotic phrases such as:

- empirical benchmark
- quantitative evidence
- performance baseline
- statistical observation
- establishes a baseline
- observed benchmark

unless such terminology is genuinely necessary.

Do not make the writing sound like a research paper,
business report, or machine-generated statistical explanation.

==================================================
GENUINE RECOMMENDATIONS
==================================================

Recommendations must be realistic and actionable.

Do not give empty advice such as:

- "Post consistently."
- "Engage with your audience."
- "Use better content."
- "Improve your Instagram."
- "Post more reels."
- "Use trending hashtags."

unless the supplied evidence specifically supports that advice.

Every recommendation should have a clear connection to the
account's actual analytics.

A good recommendation should tell the account owner:

WHAT to do,
WHY it is worth testing,
and WHAT to compare or observe afterward.

==================================================
EVIDENCE AND REASONING
==================================================

Use the supplied evidence as the factual foundation.

You may use general Instagram growth knowledge to explain
HOW a supported recommendation could reasonably be applied.

However, do not use general knowledge to invent facts about
this particular Instagram account.

For example:

If Python reports that videos should be tested against an observed
36.24% interaction rate, you may recommend comparing future video
interaction rates with 36.24%.

You may NOT claim:

- that videos caused follower growth
- that videos will definitely increase followers
- that the audience prefers videos
- that the algorithm favors the videos
- that the video went viral
- that the video succeeded because of its topic

unless those facts are explicitly supported by the supplied data.

==================================================
NO FALSE PROMISES
==================================================

Never guarantee that a recommendation will increase:

- followers
- likes
- comments
- views
- reach
- engagement
- conversions
- revenue

Use language such as:

- "test"
- "compare"
- "monitor"
- "evaluate"
- "use as a reference"
- "see whether"

instead of:

- "this will increase"
- "this will guarantee"
- "this will boost"
- "this will make your account grow"

==================================================
DO NOT INVENT ACCOUNT INFORMATION
==================================================

Do not invent:

- topics
- audience demographics
- audience interests
- content style
- video length
- posting schedule
- hashtags
- caption strategy
- locations
- events
- causes of performance
- reasons why a post performed well
- reasons why followers increased
- reasons why followers decreased

unless explicitly provided by Python.

==================================================
POST NAMES AND SHORT CODES
==================================================

Short codes are internal Instagram identifiers.

They are NOT useful to normal users.

NEVER display an Instagram short code in the final recommendation.

Do NOT write identifiers such as:

- Dd_oTRvBf0g
- DZh470dtCr5
- DM-HMOky569

If a human-readable "post_name" is available,
use the post_name instead.

For example:

GOOD:

Use "New Beginnings Delhi" as a reference when evaluating
future posts.

BAD:

Use DZh470dtCr5 as a reference.

If no human-readable post name is available,
refer to the content naturally without exposing the short code.

For example:

"Use the highlighted post as a reference when evaluating
future posts."

Do not invent a post name.

==================================================
PRESERVE REAL DATA
==================================================

Never change or invent numerical evidence.

If Python provides:

interaction_rate = 36.24

you must preserve it as 36.24%.

If Python provides:

likes = 8559223
comments = 102183

you may format them naturally as:

8,559,223 likes
102,183 comments

Do not change the numbers.

Do not combine metrics from different posts or videos.

==================================================
SUPPORTED RECOMMENDATIONS
==================================================

You MUST use only the recommendations inside:

"supported_recommendations"

Do NOT create completely new recommendations unrelated
to those recommendations.

However, you SHOULD make the supported recommendation
more useful by explaining:

1. What the account owner can do.
2. Why the available evidence makes this worth testing.
3. What the account owner should compare or monitor.

The practical explanation must remain consistent with
the original Python-generated recommendation.

==================================================
DO NOT OVERRIDE PYTHON'S EVIDENCE
==================================================

Python is responsible for deciding whether a pattern is
supported by the available data.

Do not independently declare weak patterns to be strong patterns.

Do not turn a single observation into a general account-wide rule.

Do not claim causation from correlation.

Do not assume that a high-performing post explains why
the account grew.

==================================================
ACTIONABILITY
==================================================

Whenever possible, make the recommendation testable.

For example:

Instead of:

"Your video performed well."

Prefer:

"For your next videos, compare their interaction rates with
the 36.24% rate observed in the analyzed video. This will give
you a consistent reference for evaluating future video performance."

The goal is to help the account owner make a practical decision.

==================================================
RECOMMENDATION COUNT
==================================================

Only produce recommendations that actually exist inside
"supported_recommendations".

If Python provides one recommendation:

Output exactly one recommendation.

If Python provides two recommendations:

Output exactly two recommendations.

Never create additional recommendations just to make
the response look complete.

Never create generic recommendations to fill missing sections.

==================================================
OUTPUT FORMAT
==================================================

Use exactly this structure:

Recommendation 1:

What to do:
[Give the practical action in natural, human-friendly language.]

Why this makes sense:
[Explain why the recommendation is supported by the supplied
evidence and how it can help the account owner make a decision.]

What to monitor:
[Explain what the account owner should compare or observe
when testing the recommendation.]

Evidence:
[Use only the relevant evidence supplied by Python.]

Recommendation 2:

What to do:
[Give the practical action in natural, human-friendly language.]

Why this makes sense:
[Explain why the recommendation is supported by the supplied
evidence and how it can help the account owner make a decision.]

What to monitor:
[Explain what the account owner should compare or observe
when testing the recommendation.]

Evidence:
[Use only the relevant evidence supplied by Python.]

Recommendation 3:

What to do:
[Give the practical action in natural, human-friendly language.]

Why this makes sense:
[Explain why the recommendation is supported by the supplied
evidence and how it can help the account owner make a decision.]

What to monitor:
[Explain what the account owner should compare or observe
when testing the recommendation.]

Evidence:
[Use only the relevant evidence supplied by Python.]

==================================================
FINAL OUTPUT RULES
==================================================

Only output recommendation sections for recommendations that
actually exist inside "supported_recommendations".

Do not output empty recommendation sections.

Do not create additional recommendations.

Do not use placeholders.

Do not invent information.

Do not expose Instagram short codes.

Use human-readable post names when available.

Do not add an introductory paragraph before Recommendation 1.

Do not add a conclusion after the final recommendation.

Do not mention these instructions in your response.

Do not mention Python, the prompt, the analytics pipeline,
or internal implementation details to the account owner.

The final response should feel like genuine advice from an
experienced Instagram growth advisor.

==================================================
ANALYTICS AND APPROVED RECOMMENDATIONS
==================================================

{json.dumps(llm_report, indent=2)}

"""

    return prompt


# --------------------------------------------------
# SEND REQUEST TO OLLAMA
# --------------------------------------------------

def generate_llm_response(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response.")

        return response.text.strip()

    except Exception as error:
        raise RuntimeError(
            f"Gemini request failed: {error}"
        )


# --------------------------------------------------
# SAVE LLM RECOMMENDATIONS
# --------------------------------------------------

def save_recommendations(
    report,
    supported_recommendations,
    llm_response
):

    llm_output = {

        "profile": report.get("profile"),

        "supported_recommendations":
            supported_recommendations,

        "recommendations":
            llm_response

    }

    with open(
        "backend/data/llm_recommendations.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            llm_output,
            f,
            indent=4,
            ensure_ascii=False
        )


# --------------------------------------------------
# MAIN LLM FUNCTION
# --------------------------------------------------

def generate_recommendations():

    print(
        "\nLoading analytics report..."
    )

    report = load_report()

    print(
        "Analytics report loaded."
    )


    # --------------------------------------------------
    # BUILD SUPPORTED RECOMMENDATIONS
    # --------------------------------------------------

    supported_recommendations = (
        get_supported_recommendations(
            report
        )
    )


    print(
        "Supported recommendations:",
        len(supported_recommendations)
    )


    print(
        "\nSupported recommendations:"
    )


    for recommendation in supported_recommendations:

        print(
            "\nType:",
            recommendation["type"]
        )

        print(
            "Action:",
            recommendation["action"]
        )

        print(
            "Evidence:",
            recommendation["evidence"]
        )


    # --------------------------------------------------
    # CREATE LLM REPORT
    # --------------------------------------------------

    llm_report = create_llm_report(
        report,
        supported_recommendations
    )


    print(
        "\nLLM-ready analytics created."
    )


    # --------------------------------------------------
    # CREATE PROMPT
    # --------------------------------------------------

    prompt = create_prompt(
        llm_report
    )


    print(
        "\nPrompt size:",
        len(prompt),
        "characters"
    )

    print(
        "Sending analytics to Gemini..."
    )


    # --------------------------------------------------
    # GENERATE LLM RESPONSE
    # --------------------------------------------------

    llm_response = generate_llm_response(
        prompt
    )


    print(
        "Response received."
    )


    # --------------------------------------------------
    # DISPLAY RESPONSE
    # --------------------------------------------------

    print(
        "\n==================================="
    )

    print(
        "      LLM Growth Recommendations"
    )

    print(
        "===================================\n"
    )

    print(
        llm_response
    )


    # --------------------------------------------------
    # SAVE RESPONSE
    # --------------------------------------------------

    save_recommendations(
        report,
        supported_recommendations,
        llm_response
    )


    print(
        "\nLLM recommendations saved successfully."
    )


    return llm_response


# --------------------------------------------------
# DIRECT EXECUTION
# --------------------------------------------------

if __name__ == "__main__":

    try:

        generate_recommendations()

    except Exception as error:

        print(
            f"\nError: {error}"
        )