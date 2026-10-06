def build_recommendations(report):

    insights = report.get("llm_insights", [])

    recommendations = []

    for insight in insights:

        insight_type = insight.get("type")
        evidence = insight.get("evidence", {})

        if insight_type == "top_post":

            post_name = evidence.get("post_name")
            likes = evidence.get("likes")
            comments = evidence.get("comments")

            if post_name and likes is not None:

                recommendations.append({
                    "type": "top_post",
                    "action": (
                        f'Use "{post_name}" as a performance reference '
                        "when evaluating future posts."
                    ),
                    "evidence": {
                        "post_name": post_name,
                        "likes": likes,
                        "comments": comments
                    }
                })

        elif insight_type == "video_performance":

            short_code = evidence.get("short_code")
            interaction_rate = evidence.get("interaction_rate")

            if short_code and interaction_rate is not None:

                recommendations.append({
                    "type": "video_performance",
                    "action": (
                        f"Test future videos and compare their "
                        f"interaction rates with the observed "
                        f"{interaction_rate}% rate from {short_code}."
                    ),
                    "evidence": {
                        "short_code": short_code,
                        "interaction_rate": interaction_rate
                    }
                })

    return recommendations