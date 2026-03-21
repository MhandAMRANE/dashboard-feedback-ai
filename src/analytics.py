def detect_negative_peak(feedbacks, theme="livraison", threshold=5):
    """
    Retourne une liste de semaines où le nombre de feedbacks négatifs sur le thème donné dépasse le seuil.
    """
    if not feedbacks:
        return []
    df = pd.DataFrame(feedbacks)
    if 'feedback_date_raw' not in df.columns or 'themes' not in df.columns or 'sentiment' not in df.columns:
        return []
    df['date'] = pd.to_datetime(df['feedback_date_raw'], errors='coerce')
    df = df.dropna(subset=['date'])
    df['week'] = df['date'].dt.to_period('W').astype(str)
    # Harmoniser les labels de sentiment
    df['sentiment'] = df['sentiment'].replace({
        'positif': 'positive',
        'neutre': 'neutral',
        'négatif': 'negative',
        'négative': 'negative',
        'negatif': 'negative',
        'positive': 'positive',
        'neutral': 'neutral',
        'negative': 'negative',
    })
    # Filtrer les feedbacks négatifs contenant le thème
    mask = (
        df['sentiment'] == 'negative'
    ) & (
        df['themes'].fillna('').apply(lambda t: theme.lower() in [th.strip().lower() for th in t.split(',')])
    )
    df_neg = df[mask]
    # Compter par semaine
    counts = df_neg.groupby('week').size()
    # Retourner les semaines où le seuil est dépassé
    return [week for week, count in counts.items() if count > threshold]
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


# --- Ajout pour l'évolution temporelle des sentiments ---
import pandas as pd

def compute_weekly_sentiment(feedbacks):
    if not feedbacks:
        return [], [], [], []
    df = pd.DataFrame(feedbacks)
    if 'feedback_date_raw' not in df.columns:
        return [], [], [], []
    df['date'] = pd.to_datetime(df['feedback_date_raw'], errors='coerce')
    df = df.dropna(subset=['date'])
    df['week'] = df['date'].dt.to_period('W').astype(str)
    # Harmoniser les labels de sentiment
    df['sentiment'] = df['sentiment'].replace({
        'positif': 'positive',
        'neutre': 'neutral',
        'négatif': 'negative',
        'négative': 'negative',
        'negatif': 'negative',
        'positive': 'positive',
        'neutral': 'neutral',
        'negative': 'negative',
    })
    weekly_counts = df.groupby('week')['sentiment'].value_counts().unstack(fill_value=0).reset_index()
    labels = weekly_counts['week'].tolist()
    data_positifs = weekly_counts.get('positive', pd.Series([0]*len(labels))).tolist()
    data_neutres = weekly_counts.get('neutral', pd.Series([0]*len(labels))).tolist()
    data_negatifs = weekly_counts.get('negative', pd.Series([0]*len(labels))).tolist()
    return labels, data_positifs, data_neutres, data_negatifs