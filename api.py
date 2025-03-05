from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import os

app = FastAPI()

# Créer le dossier de destination pour les fichiers uploadés
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Monter le dossier "static" pour servir l'interface
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=JSONResponse)
async def get_homepage():
    """Retourner l'interface."""
    return {"message": "Page d'accueil"}

@app.post("/upload")
async def upload_files(fichiers: list[UploadFile] = File(...), mots_cles: str = Form(...)):
    try:
        fichiers_sauvegardes = []
        mots_cles_liste = [mot.strip() for mot in mots_cles.split(",")]

        if len(fichiers) > 50 or len(mots_cles_liste) > 50:
            return JSONResponse({"error": "Tu ne peux pas envoyer plus de 50 fichiers et mots-clés."}, status_code=400)

        if len(fichiers) != len(mots_cles_liste):
            return JSONResponse({"error": "Le nombre de fichiers ne correspond pas au nombre de mots-clés."}, status_code=400)

        dataframes = []

        for fichier, mot_cle in zip(fichiers, mots_cles_liste):
            filepath = os.path.join(UPLOAD_FOLDER, fichier.filename)
            with open(filepath, "wb") as buffer:
                buffer.write(await fichier.read())

            df = pd.read_excel(filepath)
            df.insert(0, "Mot Clé", mot_cle)  # Ajouter la colonne "Mot Clé"
            dataframes.append(df)

        # Fusionner les fichiers
        result_df = pd.concat(dataframes, ignore_index=True)
        result_path = os.path.join(UPLOAD_FOLDER, "fusion_resultats.xlsx")
        result_df.to_excel(result_path, index=False)

        return {"message": "Fichier fusionné avec succès.", "download_url": f"/download/{os.path.basename(result_path)}"}

    except Exception as e:
        return {"error": str(e)}

@app.get("/download/{file_name}")
def download_file(file_name: str):
    """Permet de télécharger le fichier fusionné."""
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=file_name)
    return JSONResponse({"message": "Fichier non trouvé."}, status_code=404)
