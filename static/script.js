function uploadFiles() {
    let files = document.getElementById("file-input").files;
    let motsCles = document.getElementById("mots-cles").value.trim();

    if (files.length === 0 || motsCles === "") {
        alert("Veuillez sélectionner des fichiers et entrer des mots-clés.");
        return;
    }

    // Ajouter des numéros devant chaque mot-clé
    let motsClesListe = motsCles.split('\n').filter(Boolean);  // Divise par ligne et enlève les vides
    let motsClesNumerotes = motsClesListe.map((mot, index) => `${index + 1}. ${mot}`).join('\n');

    // Mettre à jour la valeur de l'input pour refléter les changements
    document.getElementById("mots-cles").value = motsClesNumerotes;

    document.getElementById("progress").style.display = "block";

    let formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append("fichiers", files[i]);
    }
    formData.append("mots_cles", motsClesNumerotes);

    fetch("/upload", { 
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("progress").style.display = "none";
        if (data.download_url) {
            let link = document.getElementById("download-link");
            link.href = data.download_url;
            link.style.display = "block";
        } else {
            alert("Erreur : " + data.error);
        }
    });
}
