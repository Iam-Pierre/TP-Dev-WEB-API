const form = document.getElementById("formulaire");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    document.getElementById("formulaire").style.display = "none";
    document.getElementById("resultats").style.display = "block";
    
    const formData = Object.fromEntries(new FormData(form));
    
    const response = await fetch("/api/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(formData)
    });
    
    const data = await response.json();
    

    
    const bar = document.getElementById("myBar");
    bar.style.width = data.proba * 100 + "%";
    bar.style.backgroundColor = data.proba > 0.5 ? "red" : "green";
    bar.textContent = Math.round(data.proba * 100) + "%";

    const params = new URLSearchParams(formData);
    const response2 = await fetch(`/api/waterfall?${params}`);

    const blob = await response2.blob();
    const imgUrl = URL.createObjectURL(blob);
    const img = document.getElementById("waterfall");
    img.src = imgUrl;
    img.style.display = "block";
});

document.getElementById("dashboard").addEventListener("click", () => {
    window.location.href = "/dashboard";
});

document.getElementById("backForm").addEventListener("click", () => {
    document.getElementById("resultats").style.display = "none";
    document.getElementById("formulaire").style.display = "block";
});

document.getElementById("explication").addEventListener("click", () => {
    document.getElementById("shapValues").style.display = "block";
    document.getElementById("explication").style.display = "none";
});