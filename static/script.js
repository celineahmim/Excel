function uploadFiles() {
    let files = document.getElementById("file-input").files;
    let motsCles = document.getElementById("mots-cles").value.trim();

    if (files.length === 0 || motsCles === "") {
        alert("Veuillez sélectionner des fichiers et entrer des mots-clés.");
        return;
    }

    if (files.length > 50 || motsCles.split(",").length > 50) {
        alert("Vous ne pouvez pas télécharger plus de 50 fichiers et mots-clés.");
        return;
    }

    document.getElementById("progress").style.display = "block";

    let formData = new FormData();
    let motsClesArray = motsCles.split(",").map(mot => mot.trim()); // Séparer les mots-clés

    if (files.length !== motsClesArray.length) {
        alert("Le nombre de mots-clés ne correspond pas au nombre de fichiers.");
        document.getElementById("progress").style.display = "none";
        return;
    }

    // Ajouter les fichiers et les mots-clés au formData
    for (let i = 0; i < files.length; i++) {
        formData.append("fichiers", files[i]);
        formData.append("mots_cles", motsClesArray[i]);
    }

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
