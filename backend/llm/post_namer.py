import json
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:latest"


def generate_post_name(post):

    caption = post.get("caption") or ""
    hashtags = post.get("hashtags") or []
    post_type = post.get("type") or "Post"

    if isinstance(hashtags, list):
        hashtag_text = " ".join(hashtags)
    else:
        hashtag_text = str(hashtags)

    prompt = f"""
Generate a short, human-readable English name for this Instagram post.

Post data:

Caption:
{caption}

Hashtags:
{hashtag_text}

Post type:
{post_type}

Rules:

1. Return exactly one short, natural English post name.
2. The name must contain 2 to 4 meaningful English words and Do not add the word "Post" unless it is actually meaningful.
3. Use meaningful words from the caption when available.
4. If the caption contains only emojis or meaningless text, use meaningful hashtags.
5. Hashtags can be converted into normal English words.
6. Prefer specific meaningful hashtags over generic hashtags such as:
   #like, #post, #share, #trendingnow, #trends.
7. For example, #brothers and #trendingsongs can support a name such as:
   "Brothers Trending Song Post"
8. Never include the technical post type such as Sidecar, Image, Video,
   Carousel, Clips, or Feed in the generated name.
9. Do not assume what is shown in the image or video.
10. Do not infer an event, location, person, activity, or story unless explicitly supported.
11. If neither caption nor hashtags contain meaningful information,
    use a generic name based on the post type.
12. Do not include emojis.
13. Do not include hashtags.
14. Do not include quotation marks.
15. Do not explain your answer.
16. Return ONLY the post name.

"""
    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=data,
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    name = result.get("response", "").strip()
    name = name.replace('"', "").replace("'", "").strip()

    return name