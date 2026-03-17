import os
import pandas as pd
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import io
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from src.storage import (
    init_db,
    insert_feedback,
    count_feedbacks,
    get_all_feedbacks,
    get_unanalyzed_feedbacks,
    update_feedback_analysis,
)
from src.utils import clean_text, generate_text_hash, normalize_date
from src.llm import analyze_feedback_with_llm
from src.analytics import compute_sentiment_stats, compute_theme_stats

app = Flask(__name__)

UPLOAD_FOLDER = "data"
ALLOWED_EXTENSIONS = {"csv"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

init_db()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def fetch_feedback_dicts():
    rows = get_all_feedbacks()
    return [
        {
            "id": row[0],
            "feedback_date": row[1],
            "text": row[2],
            "text_hash": row[3],
            "sentiment": row[4],
            "themes": row[5],
            "confidence": row[6],
            "created_at": row[7],
        }
        for row in rows
    ]


def apply_filters(feedbacks, sentiment_filter=None, theme_filter=None, date_filter=None):
    filtered = feedbacks

    if sentiment_filter:
        filtered = [
            feedback for feedback in filtered
            if feedback.get("sentiment") == sentiment_filter
        ]

    if theme_filter:
        filtered = [
            feedback for feedback in filtered
            if feedback.get("themes") and theme_filter in [t.strip() for t in feedback["themes"].split(",")]
        ]

    if date_filter:
        filtered = [
            feedback for feedback in filtered
            if feedback.get("feedback_date") == date_filter
        ]

    return filtered


def get_available_themes(feedbacks):
    theme_set = set()
    for feedback in feedbacks:
        themes = feedback.get("themes")
        if themes:
            for theme in themes.split(","):
                theme_set.add(theme.strip())
    return sorted(theme_set)


@app.route("/")
def home():
    total_feedbacks = count_feedbacks()
    return render_template("index.html", total_feedbacks=total_feedbacks)


@app.route("/upload", methods=["GET", "POST"])
def upload_page():
    preview_data = None
    columns = []
    error = None
    success = None
    file_info = None
    import_summary = None

    if request.method == "POST":
        if "file" not in request.files:
            error = "Aucun fichier n'a été envoyé."
            return render_template(
                "upload.html",
                error=error,
                preview_data=preview_data,
                columns=columns,
                success=success,
                file_info=file_info,
                import_summary=import_summary,
            )

        file = request.files["file"]

        if file.filename == "":
            error = "Aucun fichier sélectionné."
            return render_template(
                "upload.html",
                error=error,
                preview_data=preview_data,
                columns=columns,
                success=success,
                file_info=file_info,
                import_summary=import_summary,
            )

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
            file.save(filepath)

            try:
                df = pd.read_csv(filepath)

                if df.empty:
                    error = "Le fichier CSV est vide."
                else:
                    columns = df.columns.tolist()
                    preview_data = df.head(5).to_dict(orient="records")
                    success = "Fichier importé avec succès."
                    file_info = {
                        "filename": filename,
                        "rows": len(df),
                        "columns_count": len(df.columns),
                    }

                    if "text" not in df.columns:
                        error = "Le CSV doit contenir une colonne 'text'."
                    else:
                        inserted_count = 0
                        duplicate_count = 0

                        for _, row in df.iterrows():
                            text = clean_text(row.get("text"))
                            if not text:
                                continue

                            feedback_date = normalize_date(row.get("date"))
                            text_hash = generate_text_hash(text)

                            inserted = insert_feedback(feedback_date, text, text_hash)
                            if inserted:
                                inserted_count += 1
                            else:
                                duplicate_count += 1

                        import_summary = {
                            "inserted": inserted_count,
                            "duplicates": duplicate_count,
                            "total_in_db": count_feedbacks(),
                        }

            except Exception as e:
                error = f"Erreur lors de la lecture du CSV : {str(e)}"
        else:
            error = "Format invalide. Veuillez envoyer un fichier CSV."

    return render_template(
        "upload.html",
        error=error,
        preview_data=preview_data,
        columns=columns,
        success=success,
        file_info=file_info,
        import_summary=import_summary,
    )


@app.route("/analyze", methods=["POST"])
def analyze_feedbacks():
    unanalyzed_feedbacks = get_unanalyzed_feedbacks()
    analyzed_count = 0
    error_messages = []

    for feedback_id, text in unanalyzed_feedbacks:
        try:
            result = analyze_feedback_with_llm(text)
            update_feedback_analysis(
                feedback_id=feedback_id,
                sentiment=result["sentiment"],
                themes=", ".join(result["themes"]),
                confidence=result["confidence"],
            )
            analyzed_count += 1
        except Exception as e:
            error_messages.append(f"Feedback ID {feedback_id}: {str(e)}")

    feedbacks = fetch_feedback_dicts()
    sentiment_stats = compute_sentiment_stats(feedbacks)
    theme_stats = compute_theme_stats(feedbacks)
    available_themes = get_available_themes(feedbacks)

    return render_template(
        "dashboard.html",
        feedbacks=feedbacks,
        analyzed_count=analyzed_count,
        error_messages=error_messages,
        sentiment_stats=sentiment_stats,
        theme_stats=theme_stats,
        available_themes=available_themes,
        current_sentiment="",
        current_theme="",
        current_date="",
    )


@app.route("/dashboard")
def dashboard():
    feedbacks = fetch_feedback_dicts()

    sentiment_filter = request.args.get("sentiment", "").strip()
    theme_filter = request.args.get("theme", "").strip()
    date_filter = request.args.get("date", "").strip()

    filtered_feedbacks = apply_filters(
        feedbacks,
        sentiment_filter=sentiment_filter if sentiment_filter else None,
        theme_filter=theme_filter if theme_filter else None,
        date_filter=date_filter if date_filter else None,
    )

    sentiment_stats = compute_sentiment_stats(filtered_feedbacks)
    theme_stats = compute_theme_stats(filtered_feedbacks)
    available_themes = get_available_themes(feedbacks)

    return render_template(
        "dashboard.html",
        feedbacks=filtered_feedbacks,
        analyzed_count=None,
        error_messages=[],
        sentiment_stats=sentiment_stats,
        theme_stats=theme_stats,
        available_themes=available_themes,
        current_sentiment=sentiment_filter,
        current_theme=theme_filter,
        current_date=date_filter,
    )


@app.route("/export", methods=["GET"])
def export_feedbacks():
    feedbacks = fetch_feedback_dicts()
    sentiment_filter = request.args.get("sentiment", "").strip()
    theme_filter = request.args.get("theme", "").strip()
    date_filter = request.args.get("date", "").strip()

    filtered_feedbacks = apply_filters(
        feedbacks,
        sentiment_filter=sentiment_filter if sentiment_filter else None,
        theme_filter=theme_filter if theme_filter else None,
        date_filter=date_filter if date_filter else None,
    )

    # Préparer le CSV en mémoire
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=[
        "id", "feedback_date", "text", "sentiment", "themes", "confidence", "created_at"
    ])
    writer.writeheader()
    for fb in filtered_feedbacks:
        writer.writerow({
            "id": fb["id"],
            "feedback_date": fb["feedback_date"],
            "text": fb["text"],
            "sentiment": fb["sentiment"],
            "themes": fb["themes"],
            "confidence": fb["confidence"],
            "created_at": fb["created_at"],
        })
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="feedbacks_export.csv"
    )


@app.route("/export_pdf", methods=["GET"])
def export_pdf():
    feedbacks = fetch_feedback_dicts()
    sentiment_filter = request.args.get("sentiment", "").strip()
    theme_filter = request.args.get("theme", "").strip()
    date_filter = request.args.get("date", "").strip()

    filtered_feedbacks = apply_filters(
        feedbacks,
        sentiment_filter=sentiment_filter if sentiment_filter else None,
        theme_filter=theme_filter if theme_filter else None,
        date_filter=date_filter if date_filter else None,
    )

    sentiment_stats = compute_sentiment_stats(filtered_feedbacks)
    theme_stats = compute_theme_stats(filtered_feedbacks)

    # Création du PDF en mémoire
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Titre
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "Rapport d'Analyse des Feedbacks")
    
    p.setFont("Helvetica", 10)
    p.drawString(50, height - 70, f"Filtres appliqués - Sentiment: {sentiment_filter or 'Tous'}, Thème: {theme_filter or 'Tous'}, Date: {date_filter or 'Toutes'}")

    # Statistiques
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 100, "Statistiques Globales :")
    p.setFont("Helvetica", 10)
    p.drawString(70, height - 120, f"Total Feedbacks: {sentiment_stats['total']}")
    p.drawString(70, height - 135, f"Positifs: {sentiment_stats['positive']}")
    p.drawString(70, height - 150, f"Neutres: {sentiment_stats['neutral']}")
    p.drawString(70, height - 165, f"Négatifs: {sentiment_stats['negative']}")

    # Top Thèmes
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 200, "Top 10 Thèmes :")
    y = height - 220
    for theme, count in theme_stats:
        p.setFont("Helvetica", 10)
        p.drawString(70, y, f"- {theme}: {count}")
        y -= 15
        if y < 50:
            p.showPage()
            y = height - 50

    # Liste des Feedbacks
    y -= 25
    if y < 100:
        p.showPage()
        y = height - 50

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Détails des Feedbacks :")
    y -= 20

    for fb in filtered_feedbacks:
        p.setFont("Helvetica-Bold", 9)
        date_str = fb['feedback_date'] or "N/A"
        sentiment_str = (fb['sentiment'] or "N/A").upper()
        p.drawString(50, y, f"[{date_str}] - {sentiment_str}")
        y -= 12
        
        p.setFont("Helvetica", 9)
        text = fb['text']
        # Découpage rudimentaire du texte pour éviter de déborder de la page
        max_chars = 90
        lines = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
        for line in lines:
            p.drawString(70, y, line)
            y -= 12
            if y < 50:
                p.showPage()
                y = height - 50
        
        y -= 8
        if y < 50:
            p.showPage()
            y = height - 50

    p.showPage()
    p.save()

    buffer.seek(0)
    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="rapport_feedbacks.pdf"
    )


if __name__ == "__main__":
    app.run(debug=True)