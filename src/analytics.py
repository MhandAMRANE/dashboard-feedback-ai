from collections import Counter


def compute_sentiment_stats(feedbacks):
    stats = {
        "total": len(feedbacks),
        "positive": 0,
        "neutral": 0,
        "negative": 0,
        "not_analyzed": 0,
    }

    for feedback in feedbacks:
        sentiment = feedback.get("sentiment")
        if sentiment == "positive":
            stats["positive"] += 1
        elif sentiment == "neutral":
            stats["neutral"] += 1
        elif sentiment == "negative":
            stats["negative"] += 1
        else:
            stats["not_analyzed"] += 1

    return stats


def compute_theme_stats(feedbacks):
    counter = Counter()

    for feedback in feedbacks:
        themes = feedback.get("themes")
        if not themes:
            continue

        if isinstance(themes, str):
            split_themes = [theme.strip() for theme in themes.split(",") if theme.strip()]
            counter.update(split_themes)

    return counter.most_common(10)