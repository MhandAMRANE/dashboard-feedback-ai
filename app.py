import os
import pandas as pd
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from src.storage import init_db, insert_feedback, count_feedbacks, get_all_feedbacks
from src.utils import clean_text, generate_text_hash, normalize_date

app = Flask(__name__)

UPLOAD_FOLDER = "data"
ALLOWED_EXTENSIONS = {"csv"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

init_db()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


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


@app.route("/dashboard")
def dashboard():
    rows = get_all_feedbacks()
    feedbacks = [
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
    return render_template("dashboard.html", feedbacks=feedbacks)


if __name__ == "__main__":
    app.run(debug=True)