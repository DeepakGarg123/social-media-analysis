import os
import json
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

token = os.getenv("APIFY_API_TOKEN")

client = ApifyClient(token)

instagram_url = input("Enter Instagram profile URL: ")

run_input = {
    "addParentData": False,
    "directUrls": [instagram_url],
    "resultsLimit": 5,
    "resultsType": "posts",
    "searchLimit": 10,
    "searchType": "hashtag"
}

print("\nScraping Instagram posts...")

run = client.actor("apify/instagram-scraper").call(
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
    json.dump(items, f, indent=4)

print(f"Posts collected: {len(items)}")
print("Post data saved successfully.")


from urllib.parse import urlparse

parsed_url = urlparse(instagram_url)
username = parsed_url.path.strip("/").split("/")[0]

profile_input = {
    "usernames": [username]
}

print("\nScraping Instagram profile...")

profile_run = client.actor(
    "apify/instagram-profile-scraper"
).call(
    run_input=profile_input
)

profile_items = client.dataset(
    profile_run.default_dataset_id
).list_items().items

with open(
    "backend/data/instagram_profile.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(profile_items, f, indent=4)

print(f"Profiles collected: {len(profile_items)}")
print("Profile data saved successfully.")