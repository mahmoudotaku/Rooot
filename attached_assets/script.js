async function fetchInfo() {
    const url = document.getElementById("url").value;
    if (!url) return alert("ادخل رابط فيديو يا شيطان 👿");
    const res = await fetch(`/info?url=${encodeURIComponent(url)}`);
    const data = await res.json();

    document.getElementById("video-title").innerText = data.title;
    document.getElementById("thumb").src = data.thumbnail;

    const qualitySelect = document.getElementById("quality");
    qualitySelect.innerHTML = "";

    data.formats.forEach(format => {
        const option = document.createElement("option");
        option.value = format.format_id;
        option.textContent = `${format.resolution} - ${format.filesize} MB`;
        qualitySelect.appendChild(option);
    });

    document.getElementById("download-section").style.display = "block";
}

function downloadVideo() {
    const url = document.getElementById("url").value;
    const quality = document.getElementById("quality").value;
    const link = `/download?url=${encodeURIComponent(url)}&quality=${quality}`;
    window.open(link, "_blank");
}
