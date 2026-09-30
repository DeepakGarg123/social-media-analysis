data = [
    {
        "date": "2026-09-01",
        "views": 500,
        "likes": 20,
        "comments": 5,
        "shares": 2,
        "saves": 1,
        "followers": 600,
        "reposts": 0
    },
    {
        "date": "2026-09-15",
        "views": 5000,
        "likes": 180,
        "comments": 30,
        "shares": 20,
        "saves": 15,
        "followers": 670,
        "reposts": 8
    },
    {
        "date": "2026-09-30",
        "views": 13000,
        "likes": 415,
        "comments": 72,
        "shares": 87,
        "saves": 30,
        "followers": 707,
        "reposts": 26
    }
]

total_likes = 0
total_comments = 0
total_shares = 0
total_saves = 0
total_reposts = 0

for record in data:
    total_likes += record["likes"]
    total_comments += record["comments"]
    total_shares += record["shares"]
    total_saves += record['saves']
    total_reposts += record["reposts"]

print("Total likes:", total_likes)
print("Total comments:", total_comments)
print("Total shares:", total_shares)
print("Total saves:", total_saves)
print("Total reposts:", total_reposts)


