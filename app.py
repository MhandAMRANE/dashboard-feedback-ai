import os
import pandas as pd
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "data"
ALLOWED_EXTENSIONS = {"csv"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload_page():
    preview_data = None
    columns = []
    error = None
    success = None
    file_info = None

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
    )


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)