document.getElementById("logout").addEventListener("click", async () => {
    const response = await fetch('/api/logout', {
        method: 'POST',
        });

    const data = await response.json();
    if (data.ok) {
        window.location.href = "/";  
    }
});

const api = document.getElementById("create_api");
api?.addEventListener("click", async(e) => {
    e.preventDefault();

    const apiName = document.getElementById("api_key_name").value;

    const response = await fetch("/api/keys", {
        method : "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ apiName })
    });

});

