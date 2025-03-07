from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import os
import shutil
from typing import List

app = FastAPI()

# 📂 Création du dossier d'upload
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 📂 Monter le dossier "static" pour servir l'interface
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_homepage():
    """Retourne l'interface web."""
    with open("static/index.html", "r", encoding="utf-8") as file:
        return file.read()

@app.post("/upload")
async def upload_files(
    fichiers: List[UploadFile] = File(...),
    mots_cles: str = Form(...),
    outputFileName: str = Form(...)
):
    fichiers_sauvegardes = []
    mots_cles_liste = [mot.strip() for mot in mots_cles.split(",")]

    if len(fichiers) > 50 or len(mots_cles_liste) > 50:
        return {"error": "Tu ne peux pas envoyer plus de 50 fichiers et mots-clés à la fois."}

    if len(fichiers) != len(mots_cles_liste):
        return {"error": "Le nombre de fichiers ne correspond pas au nombre de mots-clés."}

    dataframes = []

    for fichier, mot_cle in zip(fichiers, mots_cles_liste):
        filepath = os.path.join(UPLOAD_FOLDER, fichier.filename)
        with open(filepath, "wb") as buffer:
            buffer.write(await fichier.read())

        df = pd.read_excel(filepath)
        df.insert(0, "Mot Clé", mot_cle)  # Ajout de la colonne "Mot Clé"

        # Vérification si une colonne de résultats SERP existe (ex: colonne 3)
        if df.shape[1] >= 3:
            df.rename(columns={df.columns[2]: "Résultats SERP"}, inplace=True)

        dataframes.append(df)

    # 🔄 Fusionner les fichiers en un seul
    result_df = pd.concat(dataframes, ignore_index=True)
    resultat_path = os.path.join(UPLOAD_FOLDER, outputFileName + ".xlsx")
    result_df.to_excel(resultat_path, index=False)

    return {"message": "Fichier fusionné avec succès.", "download_url": f"/download/{outputFileName}.xlsx"}

@app.get("/download/{file_name}")
def download_file(file_name: str):
    """Permet de télécharger le fichier fusionné."""
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=file_name)
    return {"message": "Fichier non trouvé."}, 404
