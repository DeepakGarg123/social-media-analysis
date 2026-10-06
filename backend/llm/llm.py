import json

import requests

from backend.llm.recommendation_builder import build_recommendations


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
You are an AI social media growth advisor.

Your job is to convert the already-approved recommendations
into clear, practical recommendations for the Instagram
account owner.

IMPORTANT:

Python has already analyzed the analytics and created a list
called "supported_recommendations".

You MUST use only these supported recommendations.

Do NOT create new recommendations.

Do NOT create recommendations directly from raw analytics.

Do NOT create recommendations directly from top_posts.

Do NOT create recommendations directly from video_analysis.

The Python recommendation builder has already decided which
recommendations are supported by the available evidence.


RULES:

1. Rewrite the supported recommendations clearly and naturally.

2. Preserve the meaning of every Python-generated Action.

3. Do not add a new action.

4. Do not remove an important restriction from an action.

5. Do not invent metrics, numbers, trends, causes, or results.

6. Do not claim that a strategy will definitely increase followers,
   engagement, reach, views, or any other metric.

7. Do not imply causation.

8. Do not introduce information that is not present in the
   supported recommendation or its evidence.

9. Preserve actual post names and short codes exactly as provided.

10. Never replace an actual identifier with:
    - Post A
    - Post B
    - Video A
    - Video B
    - Post 1
    - Video 1
    - the top post
    - the top video

11. If a post_name is provided, preserve that exact post name.

12. If a short_code is provided, preserve that exact short code.

13. Do not invent a post name or identifier.

14. Do not combine metrics from different posts or videos.

15. If a metric is unavailable, do not invent it.

16. Do not infer:
    - video length
    - content style
    - topic
    - posting time
    - caption style
    - hashtags
    - audience behavior
    - location
    - event
    - cause of performance

17. Do not recommend:
    - copying content
    - changing content style
    - changing posting time
    - copying hashtags
    - copying captions
    - pinning a post
    - reposting a post
    - changing video length
    - changing frequency

    unless the supported recommendation explicitly says so.

18. Do not introduce new numeric targets.

19. Do not introduce posting-frequency targets.

20. Do not introduce engagement benchmarks.

21. Keep recommendations testable.

22. If Python provides only one supported recommendation,
    output only one recommendation.

23. Never create a second or third recommendation simply
    to make the output look complete.

24. The Evidence section must use only the evidence supplied
    by Python.

25. The Why section should explain the supported recommendation
    without introducing new facts.

26. The Action section must preserve the Python-generated action.

27. Do not describe a result as "promising", "strong", "successful",
    "effective", or similar unless that exact conclusion is explicitly
    present in the supplied evidence.

28. Do not introduce subjective interpretations of performance.

29. Keep the Why section factual and directly connected to the
    supplied evidence.

30. If Python provides an action, do not replace it with a different
    marketing strategy.

31. Do not add generic social-media advice.

32. Do not add recommendations that are not present in
    supported_recommendations.


USE EXACTLY THIS FORMAT:

Recommendation 1:

Action:

[Python-supported action rewritten clearly.]

Why:

[Explain why this action is supported using only the provided evidence.]

Evidence:

[Use only the supplied evidence.]


Recommendation 2:

Action:

[Python-supported action rewritten clearly.]

Why:

[Explain why this action is supported using only the provided evidence.]

Evidence:

[Use only the supplied evidence.]


Recommendation 3:

Action:

[Python-supported action rewritten clearly.]

Why:

[Explain why this action is supported using only the provided evidence.]

Evidence:

[Use only the supplied evidence.]


IMPORTANT:

Only output recommendation sections for recommendations
that actually exist inside "supported_recommendations".

Do not output empty recommendation sections.

Do not create additional recommendations.

Do not use placeholders.

Do not invent information.

Do not add an introductory paragraph before Recommendation 1.

Do not add a conclusion after the final recommendation.


ANALYTICS AND APPROVED RECOMMENDATIONS:

{json.dumps(llm_report, indent=2)}

"""

    return prompt


# --------------------------------------------------
# SEND REQUEST TO OLLAMA
# --------------------------------------------------

def generate_llm_response(prompt):

    url = "http://localhost:11434/api/generate"

    data = {

        "model": "llama3.2:latest",

        "prompt": prompt,

        "stream": False

    }

    try:

        response = requests.post(
            url,
            json=data,
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        if "response" not in result:

            raise ValueError(
                "Unexpected Ollama response."
            )

        return result["response"].strip()


    except requests.exceptions.ConnectionError:

        raise ConnectionError(
            "Could not connect to Ollama. "
            "Make sure the Ollama server is running."
        )


    except requests.exceptions.Timeout:

        raise TimeoutError(
            "Ollama request timed out."
        )


    except requests.exceptions.RequestException as error:

        raise RuntimeError(
            f"Ollama request failed: {error}"
        )


    except json.JSONDecodeError:

        raise ValueError(
            "Invalid JSON response received from Ollama."
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
        "Sending analytics to llama..."
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