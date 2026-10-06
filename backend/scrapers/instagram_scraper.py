import os
import json
from urllib.parse import urlparse
from datetime import datetime

from dotenv import load_dotenv
from apify_client import ApifyClient

from backend.logs.logs import logger


load_dotenv()

token = os.getenv("APIFY_API_TOKEN")

if not token:
    raise ValueError("APIFY_API_TOKEN not found in .env file")

client = ApifyClient(token)


def scrape_instagram(instagram_url):

    parsed_url = urlparse(instagram_url)
    username = parsed_url.path.strip("/").split("/")[0]

    if not username:
        print("Invalid Instagram profile URL.")
        logger.error("Invalid Instagram profile URL.")
        return None

    profile_input = {
        "usernames": [username]
    }

    print("\nScraping Instagram profile...")
    logger.info(
        f"Instagram profile scraping started for: {username}"
    )

    profile_run = client.actor(
        "apify/instagram-profile-scraper"
    ).call(
        run_input=profile_input
    )

    profile_items = client.dataset(
        profile_run.default_dataset_id
    ).list_items().items

    if not profile_items:
        print("Instagram profile not found.")
        logger.error(
            f"Instagram profile not found: {username}"
        )
        return None

    profile = profile_items[0]

    total_posts = profile["postsCount"]
    analysis_limit = min(total_posts, 50)

    print(f"Total posts on profile: {total_posts}")
    print(
        f"Posts selected for analysis: {analysis_limit}"
    )

    logger.info(
        f"Profile {username} has {total_posts} posts. "
        f"Analysis limit set to {analysis_limit}."
    )

    run_input = {
        "addParentData": False,
        "directUrls": [instagram_url],
        "resultsLimit": analysis_limit,
        "resultsType": "posts",
        "searchLimit": 10,
        "searchType": "hashtag"
    }

    print("\nScraping Instagram posts...")
    logger.info("Instagram post scraping started")

    run = client.actor(
        "apify/instagram-scraper"
    ).call(
        run_input=run_input
    )

    items = client.dataset(
        run.default_dataset_id
    ).list_items().items

    with open(
        "backend/data/instagram_data.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            items,
            f,
            indent=4
        )

    print(f"Posts collected: {len(items)}")

    logger.info(
        f"Instagram posts collected: {len(items)}"
    )

    print("Post data saved successfully.")

    history_file = "backend/data/profile_history.json"

    try:
        with open(
            history_file,
            "r",
            encoding="utf-8"
        ) as f:
            profile_history = json.load(f)

    except FileNotFoundError:
        profile_history = []

    today = datetime.now().strftime("%Y-%m-%d")

    existing_snapshot = any(
        item.get("username") == profile["username"]
        and item.get("date") == today
        for item in profile_history
    )

    if not existing_snapshot:

        snapshot = {
            "username": profile["username"],
            "date": today,
            "followers": profile["followersCount"]
        }

        profile_history.append(snapshot)

        logger.info(
            f"Follower snapshot saved for "
            f"{profile['username']}: "
            f"{profile['followersCount']}"
        )

        print("New follower history snapshot saved.")

    else:

        print(
            "Follower snapshot for today already exists."
        )

    with open(
        history_file,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            profile_history,
            f,
            indent=4
        )

    with open(
        "backend/data/instagram_profile.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            profile_items,
            f,
            indent=4
        )

    print(
        f"Profiles collected: {len(profile_items)}"
    )

    logger.info(
        f"Instagram profiles collected: "
        f"{len(profile_items)}"
    )

    print("Profile data saved successfully.")

    return profile