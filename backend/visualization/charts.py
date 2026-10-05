import json

import matplotlib.pyplot as plt
import seaborn as sns

with open(
    "backend/data/analytics_report.json",
    "r",
    encoding="utf-8"
) as f:
    report = json.load(f)

content_analysis = report["content_analysis"]


def format_content_type(content_type):
    if content_type == "clips":
        return "Clips"
    if content_type == "carousel_container":
        return "Carousel"
    if content_type == "feed":
        return "Feed"
    return content_type.replace("_", " ").title()


def format_number(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if value >= 1_000:
        return f"{value / 1_000:.0f}K"
    return f"{value:.0f}"


labels = []
post_counts = []
average_likes = []

for item in content_analysis:
    labels.append(format_content_type(item["content_type"]))
    post_counts.append(item["posts"])
    average_likes.append(item["average_likes"])


sns.set_theme(
    style="whitegrid",
    font_scale=1.05
)


# --------------------------------------------------
# 1. CONTENT DISTRIBUTION
# --------------------------------------------------

plt.figure(figsize=(9, 7))

plt.pie(
    post_counts,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90,
    pctdistance=0.75,
    labeldistance=1.08,
    wedgeprops={
        "edgecolor": "white",
        "linewidth": 2
    },
    textprops={
        "fontsize": 11
    }
)

plt.title(
    "Content Distribution",
    fontsize=18,
    fontweight="bold",
    pad=20
)

plt.axis("equal")
plt.tight_layout()

plt.savefig(
    "backend/visualization/content_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# --------------------------------------------------
# 2. AVERAGE LIKES BY CONTENT TYPE
# --------------------------------------------------

plt.figure(figsize=(10, 6))

bars = plt.barh(
    labels,
    average_likes,
    height=0.55
)

plt.title(
    "Average Likes by Content Type",
    fontsize=18,
    fontweight="bold",
    pad=20
)

plt.xlabel(
    "Average Likes",
    fontsize=12
)

plt.ylabel("")

plt.grid(
    axis="x",
    linestyle="--",
    alpha=0.25
)

plt.grid(
    axis="y",
    visible=False
)

plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)
plt.gca().spines["left"].set_visible(False)

plt.tick_params(
    axis="y",
    length=0,
    labelsize=12
)

plt.tick_params(
    axis="x",
    labelsize=10
)

max_value = max(average_likes)

plt.xlim(
    0,
    max_value * 1.18
)

for bar, value in zip(bars, average_likes):

    plt.text(
        value + max_value * 0.015,
        bar.get_y() + bar.get_height() / 2,
        format_number(value),
        va="center",
        fontsize=11,
        fontweight="bold"
    )

plt.tight_layout()

plt.savefig(
    "backend/visualization/average_likes_content_type.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# --------------------------------------------------
# 3. POSTING TIME PERFORMANCE
# --------------------------------------------------

posting_analysis = report["posting_analysis"]

reliable_hours = []

for item in posting_analysis:
    if item["posts"] >= 5:
        reliable_hours.append(item)

reliable_hours.sort(
    key=lambda item: item["hour"]
)

posting_times = []
posting_average_likes = []
posting_counts = []

for item in reliable_hours:
    posting_times.append(
        f"{item['hour']:02d}:00"
    )
    posting_average_likes.append(
        item["average_likes"]
    )
    posting_counts.append(
        item["posts"]
    )


plt.figure(figsize=(10, 6))

bars = plt.barh(
    posting_times,
    posting_average_likes,
    height=0.55
)

plt.title(
    "Posting Time Performance",
    fontsize=18,
    fontweight="bold",
    pad=20
)

plt.xlabel(
    "Average Likes",
    fontsize=12
)

plt.ylabel(
    "Posting Time",
    fontsize=12
)

plt.grid(
    axis="x",
    linestyle="--",
    alpha=0.25
)

plt.grid(
    axis="y",
    visible=False
)

plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)
plt.gca().spines["left"].set_visible(False)

plt.tick_params(
    axis="y",
    length=0,
    labelsize=11
)

plt.tick_params(
    axis="x",
    labelsize=10
)

max_value = max(posting_average_likes)

plt.xlim(
    0,
    max_value * 1.20
)

for bar, value, count in zip(
    bars,
    posting_average_likes,
    posting_counts
):

    plt.text(
        value + max_value * 0.015,
        bar.get_y() + bar.get_height() / 2,
        f"{format_number(value)}  ({count} posts)",
        va="center",
        fontsize=10,
        fontweight="bold"
    )

plt.tight_layout()

plt.savefig(
    "backend/visualization/posting_time_performance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# --------------------------------------------------
# 4. TOP 3 PERFORMING POSTS
# --------------------------------------------------

top_posts = report["top_posts"]

post_labels = []
post_likes = []

for post in top_posts:
    post_labels.append(
        post["short_code"]
    )
    post_likes.append(
        post["likes"]
    )


plt.figure(figsize=(10, 6))

bars = plt.bar(
    post_labels,
    post_likes,
    width=0.55
)

plt.title(
    "Top 3 Performing Posts",
    fontsize=18,
    fontweight="bold",
    pad=20
)

plt.xlabel(
    "Post",
    fontsize=12
)

plt.ylabel(
    "Likes",
    fontsize=12
)

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.25
)

plt.grid(
    axis="x",
    visible=False
)

plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)
plt.gca().spines["left"].set_visible(False)

plt.tick_params(
    axis="x",
    length=0,
    labelsize=11
)

plt.tick_params(
    axis="y",
    labelsize=10
)

max_value = max(post_likes)

plt.ylim(
    0,
    max_value * 1.18
)

for bar, value in zip(
    bars,
    post_likes
):

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + max_value * 0.025,
        format_number(value),
        ha="center",
        va="bottom",
        fontsize=11,
        fontweight="bold"
    )

plt.tight_layout()

plt.savefig(
    "backend/visualization/top_3_posts.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()