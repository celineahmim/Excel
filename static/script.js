function uploadFiles() {
    let files = document.getElementById("file-input").files;
    let motsCles = document.getElementById("mots-cles").value;

    if (files.length === 0 || motsCles.trim() === "") {
        alert("Veuillez sélectionner des fichiers et entrer des mots-clés.");
        return;
    }

    document.getElementById("progress").style.display = "block";  // Afficher la barre de progrès

    let formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append("fichiers", files[i]);
    }
    formData.append("mots_cles", motsCles);

    fetch("/upload", { 
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("progress").style.display = "none";  // Cacher la barre de progrès
        if (data.download_url) {
            let link = document.getElementById("download-link");
            link.href = data.download_url;
            link.style.display = "block";
        } else {
            alert("Erreur: " + data.error);
        }
    })
    .catch(error => {
        document.getElementById("progress").style.display = "none";  // Cacher la barre de progrès
        alert("Erreur de communication avec le serveur.");
    });
}
