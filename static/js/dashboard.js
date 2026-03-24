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

    const data = await response.json();
    document.getElementById("raw_key").style.display = "block";
    document.querySelector("#raw_key label").textContent = data.raw_key;

});

 for (const deleteApi of document.querySelectorAll('button[data-id-key]')) {
    
     deleteApi.addEventListener("click", async(e) => {
        
        e.preventDefault();

        const key_id = deleteApi.dataset.idKey

        const response = await fetch(`/api/keys/${key_id}`,{
            method : "DELETE",
            headers : {"Content-type": "application/json"}
        });

        window.location.reload()

    
     });
 }
 

