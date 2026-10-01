import json

from pathlib import Path

from datetime import datetime

from collections import defaultdict


report = {
    "profile": {},
    "metrics": {},
    "top_posts": [],
    "posting_analysis": {},
    "content_analysis": {},
    "video_analysis": {},
    "growth": {},
    "suggestions": []
}


# -------------------- Load Data --------------------

data_file = Path("backend/data/instagram_data.json")

with open(data_file, "r", encoding="utf-8") as f:
    data = json.load(f)


profile_file = Path("backend/data/instagram_profile.json")

with open(profile_file, "r", encoding="utf-8") as f:
    profile_data = json.load(f)

profile = profile_data[0]


report["profile"] = {
    "username": profile["username"],
    "followers": profile["followersCount"],
    "following": profile["followsCount"],
    "total_posts": profile["postsCount"],
    "verified": profile["verified"],
    "private": profile["private"]
}


# -------------------- Profile History --------------------

history_file = Path("backend/data/profile_history.json")

with open(history_file, "r", encoding="utf-8") as f:
    profile_history = json.load(f)


today = datetime.now().strftime("%Y-%m-%d")

existing_dates = [
    snapshot["date"]
    for snapshot in profile_history
]


if today not in existing_dates:

    snapshot = {
        "date": today,
        "followers": profile["followersCount"]
    }

    profile_history.append(snapshot)


with open(history_file, "w", encoding="utf-8") as f:
    json.dump(profile_history, f, indent=4)


# -------------------- Follower Growth --------------------

if len(profile_history) >= 2:

    previous_snapshot = profile_history[-2]
    current_snapshot = profile_history[-1]

    previous_followers = previous_snapshot["followers"]
    current_followers = current_snapshot["followers"]

    follower_growth = current_followers - previous_followers

    growth_rate = (
        follower_growth / previous_followers
    ) * 100

    print("\nFollower Growth:")

    print(f"Previous followers: {previous_followers}")

    print(f"Current followers: {current_followers}")

    print(f"Growth: {follower_growth:+d}")

    print(f"Growth rate: {growth_rate:+.2f}%")


    report["growth"] = {
        "previous_followers": previous_followers,
        "current_followers": current_followers,
        "follower_growth": follower_growth,
        "growth_rate": round(growth_rate, 2)
    }


else:

    print("\nFollower Growth:")

    print("Not enough historical data to calculate growth.")

    report["growth"] = {
        "status": "insufficient_data"
    }


# -------------------- Instagram Profile --------------------

print("\nInstagram Profile:")

print(f"Username: {profile['username']}")

print(f"Followers: {profile['followersCount']}")

print(f"Following: {profile['followsCount']}")

print(f"Total posts: {profile['postsCount']}")

print(f"Verified: {profile['verified']}")

print(f"Scraped posts analyzed: {len(data)}")


# -------------------- Basic Metrics --------------------

valid_likes = [
    post.get("likesCount")
    for post in data
    if post.get("likesCount") is not None
    and post.get("likesCount") >= 0
]


total_comments = sum(
    post.get("commentsCount", 0)
    for post in data
)


average_comments = (
    total_comments / len(data)
    if data
    else 0
)


total_likes = sum(valid_likes)


average_likes = (
    total_likes / len(valid_likes)
    if valid_likes
    else 0
)


# -------------------- Engagement Metrics --------------------

total_interactions = total_likes + total_comments

average_interactions = (
    total_interactions / len(data)
    if data
    else 0
)


print(f"Total interactions: {total_interactions}")

print(f"Average interactions per post: {average_interactions}")


video_views = [
    post.get("videoViewCount")
    for post in data
    if post.get("videoViewCount") is not None
    and post.get("videoViewCount") >= 0
]


total_video_views = sum(video_views)


average_video_views = (
    total_video_views / len(video_views)
    if video_views
    else 0
)


report["metrics"] = {
    "total_interactions": total_interactions,
    "average_interactions_per_post": average_interactions,
    "total_comments": total_comments,
    "average_comments": average_comments,
    "total_likes": total_likes,
    "average_likes": average_likes,
    "total_video_views": total_video_views,
    "average_video_views": average_video_views
}


print(f"Total comments: {total_comments}")

print(f"Average comments: {average_comments}")

print(f"Total likes: {total_likes}")

print(f"Average likes: {average_likes}")

print(f"Total video views: {total_video_views}")

print(f"Average video views: {average_video_views}")


# -------------------- Best Performing Post --------------------

posts_with_likes = [
    post
    for post in data
    if post.get("likesCount") is not None
    and post.get("likesCount") >= 0
]


if posts_with_likes:

    best_post = max(
        posts_with_likes,
        key=lambda post: post.get("likesCount")
    )

    print("\nBest performing post:")

    print(f"URL: {best_post.get('url')}")

    print(f"Likes: {best_post.get('likesCount')}")

    print(f"Comments: {best_post.get('commentsCount')}")

    print(f"Views: {best_post.get('videoViewCount')}")

    print(f"Timestamp: {best_post.get('timestamp')}")


# -------------------- Top Performing Posts --------------------

top_posts = sorted(
    posts_with_likes,
    key=lambda post: post.get("likesCount"),
    reverse=True
)[:3]


report["top_posts"] = []


for post in top_posts:

    report["top_posts"].append({
        "short_code": post.get("shortCode"),
        "likes": post.get("likesCount"),
        "comments": post.get("commentsCount", 0),
        "views": post.get("videoViewCount"),
        "url": post.get("url"),
        "timestamp": post.get("timestamp")
    })


print("\nTop Performing Posts:")


for index, post in enumerate(top_posts, start=1):

    print(f"\n{index}. {post.get('shortCode')}")

    print(f"Likes: {post.get('likesCount')}")

    print(f"Comments: {post.get('commentsCount')}")

    print(f"Views: {post.get('videoViewCount')}")

    print(f"URL: {post.get('url')}")


# -------------------- Post Details --------------------

for post in data:

    product_type = post.get("productType")


    if product_type == "clips":

        post_type = "Video"

    elif product_type == "carousel_container":

        post_type = "Carousel"

    else:

        post_type = "Other"


    print("\n--------------------")

    print(f"Type: {post_type}")

    print(f"URL: {post.get('url')}")

    print(f"Likes: {post.get('likesCount')}")

    print(f"Comments: {post.get('commentsCount')}")

    print(f"Views: {post.get('videoViewCount')}")

    print(f"Timestamp: {post.get('timestamp')}")

    print(f"Content type: {product_type}")


# -------------------- Posting Time Analysis --------------------

hourly_likes = defaultdict(list)


for post in data:

    likes = post.get("likesCount")

    if likes is None or likes < 0:
        continue


    timestamp = post.get("timestamp")

    if timestamp:

        date = datetime.fromisoformat(
            timestamp.replace("Z", "+00:00")
        )

        hour = date.hour


        print(
            f"Post: {post.get('shortCode')} | "
            f"Hour: {hour} | "
            f"Likes: {likes}"
        )


        hourly_likes[hour].append(likes)


print("\nHourly likes:")


for hour, likes in hourly_likes.items():

    average = sum(likes) / len(likes)

    print(
        f"{hour:02d}:00 -> "
        f"Posts: {len(likes)} | "
        f"Average likes: {average}"
    )


posting_analysis = []


for hour, likes in hourly_likes.items():

    average = sum(likes) / len(likes)

    posting_analysis.append({
        "hour": hour,
        "posts": len(likes),
        "average_likes": average
    })


report["posting_analysis"] = posting_analysis


# -------------------- Content Type Analysis --------------------

content_likes = defaultdict(list)


for post in data:

    likes = post.get("likesCount")

    if likes is None or likes < 0:
        continue


    product_type = post.get("productType")


    if product_type == "clips":

        content_type = "video"

    elif product_type == "carousel_container":

        content_type = "carousel"

    else:

        content_type = "other"


    content_likes[content_type].append(likes)


print("\nContent type performance:")


for content_type, likes in content_likes.items():

    average = sum(likes) / len(likes)

    print(
        f"{content_type} -> "
        f"Posts: {len(likes)} | "
        f"Average likes: {average}"
    )


content_analysis = []


for content_type, likes in content_likes.items():

    average = sum(likes) / len(likes)

    content_analysis.append({
        "content_type": content_type,
        "posts": len(likes),
        "average_likes": average
    })


report["content_analysis"] = content_analysis


# -------------------- Video Interaction Rate --------------------

video_engagement = []


for post in data:

    views = post.get("videoViewCount")

    likes = post.get("likesCount")

    comments = post.get("commentsCount", 0)


    if likes is None or likes < 0:
        continue


    if views is None or views <= 0:
        continue


    interaction_rate = (
        (likes + comments) / views
    ) * 100


    video_engagement.append(
        (interaction_rate, post)
    )


print("\nVideo Interaction Rate:")


for interaction_rate, post in video_engagement:

    print(
        f"{post.get('shortCode')} -> "
        f"Interaction rate: {interaction_rate:.2f}%"
    )


video_analysis = []


for interaction_rate, post in video_engagement:

    video_analysis.append({
        "short_code": post.get("shortCode"),
        "views": post.get("videoViewCount"),
        "likes": post.get("likesCount"),
        "comments": post.get("commentsCount", 0),
        "interaction_rate": round(interaction_rate, 2)
    })


report["video_analysis"] = video_analysis


# -------------------- Growth Suggestions --------------------

print("\nGrowth Suggestions:")

suggestions = []


video_likes = content_likes.get("video", [])

carousel_likes = content_likes.get("carousel", [])


video_avg = (
    sum(video_likes) / len(video_likes)
    if video_likes
    else 0
)


carousel_avg = (
    sum(carousel_likes) / len(carousel_likes)
    if carousel_likes
    else 0
)


if video_likes and carousel_likes:

    if video_avg > carousel_avg:

        suggestion = (
            "Video posts have a higher average like count "
            "than carousel posts in the scraped sample. "
            "Consider testing more short-form video content."
        )

        suggestions.append(suggestion)

        print(f"- {suggestion}")


    elif carousel_avg > video_avg:

        suggestion = (
            "Carousel posts have a higher average like count "
            "than video posts in the scraped sample. "
            "Consider testing more carousel content."
        )

        suggestions.append(suggestion)

        print(f"- {suggestion}")


# -------------------- Best Posting Time Suggestion --------------------

if hourly_likes:

    best_hour = max(
        hourly_likes,
        key=lambda hour:
        sum(hourly_likes[hour]) /
        len(hourly_likes[hour])
    )


    suggestion = (
        f"The highest observed average like count "
        f"occurred at {best_hour:02d}:00."
    )


    suggestions.append(suggestion)

    print(f"- {suggestion}")


    suggestion = (
        "Consider testing this posting window with "
        "future posts and comparing the results."
    )


    suggestions.append(suggestion)

    print(f"- {suggestion}")


# -------------------- Best Video Engagement Suggestion --------------------

if video_engagement:

    best_engagement = max(
        video_engagement,
        key=lambda item: item[0]
    )


    suggestion = (
        f"The highest observed video interaction rate "
        f"was {best_engagement[0]:.2f}%."
    )


    suggestions.append(suggestion)

    print(f"- {suggestion}")


report["suggestions"] = suggestions


# -------------------- Final Report --------------------

print("\n\n========== FINAL REPORT ==========")

print(json.dumps(report, indent=4))