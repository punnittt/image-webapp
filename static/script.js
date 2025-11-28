let selectedFile = null;

document.getElementById("upload").addEventListener("change", function(e) {
    selectedFile = e.target.files[0];
});

document.getElementById("generateBtn").addEventListener("click", async function() {
    if (!selectedFile) {
        alert("Please upload an image first!");
        return;
    }

    const text = document.getElementById("textInput").value;
    if (!text) {
        alert("Enter text first!");
        return;
    }

    document.getElementById("loading").classList.remove("hidden");

    const formData = new FormData();
    formData.append("image", selectedFile);
    formData.append("text", text);

    const response = await fetch("/generate", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    document.getElementById("loading").classList.add("hidden");

    const zipLink = document.getElementById("downloadZip");
    zipLink.href = data.zip_url;
    zipLink.classList.remove("hidden");
});
