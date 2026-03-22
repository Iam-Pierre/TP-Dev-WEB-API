// Afficher le formulaire register
document.getElementById("btnShowRegister").addEventListener("click", () => {
    document.getElementById("loginfields").style.display = "none";
    document.getElementById("registerfields").style.display = "block";
});

// Afficher le formulaire login
document.getElementById("btnShowLogin").addEventListener("click", () => {
    document.getElementById("registerfields").style.display = "none";
    document.getElementById("loginfields").style.display = "block";
});

// Login
const form = document.getElementById("formulaireLogin");
form?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    if (data.ok) {
        window.location.href = "/";
    }

});

// Register
const formRegister = document.getElementById("formulaireRegister");
formRegister?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("usernameRegister").value;
    const password = document.getElementById("passwordRegister").value;

    const response = await fetch("/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    if (data.ok) {
        window.location.href = "/";
    } else {
        document.getElementById("error").style.display = "block";
        document.getElementById("error").textContent = data.error;
    }
});