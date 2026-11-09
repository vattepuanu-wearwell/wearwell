async function getRecommendations() {
    const button = document.getElementById("recommendBtn");
    const results = document.getElementById("outfitResults");

    const preferences = {
        gender: document.getElementById("gender").value,
        style: document.getElementById("style").value,
        category: document.getElementById("category").value,
        color: document.getElementById("color").value,
        weather: document.getElementById("weather").value,
        occasion: document.getElementById("occasion").value,
        budget: document.getElementById("budget").value
    };

    button.innerText = "Finding Your Style...";
    button.disabled = true;

    results.innerHTML = "<p class='empty-message'>Finding beautiful outfit ideas for you...</p>";

    try {
        const response = await fetch("/recommend", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(preferences)
        });

        if (!response.ok) {
            throw new Error("Recommendation failed");
        }

        const data = await response.json();

        results.innerHTML = data.outfits.map((outfit, index) => {
            return `
                <div class="outfit-card">

                    <div class="outfit-placeholder">
                        <span>✦</span>
                        <h3>${outfit.name}</h3>
                        <p>Style inspiration #${index + 1}</p>
                    </div>

                    <h3>${outfit.name}</h3>

                    <p><strong>Gender:</strong> ${outfit.gender}</p>
                    <p><strong>Style:</strong> ${outfit.style}</p>
                    <p><strong>Category:</strong> ${outfit.category}</p>
                    <p><strong>Colour:</strong> ${outfit.color}</p>
                    <p><strong>Weather:</strong> ${outfit.weather}</p>
                    <p><strong>Occasion:</strong> ${outfit.occasion}</p>
                    <p><strong>Budget:</strong> ${outfit.budget}</p>
                    <p><strong>Accessories:</strong> ${outfit.accessories}</p>

                    <button class="save-btn"
                        onclick="saveOutfit(this, '${outfit.name.replace(/'/g, "\\'")}')">
                        ♡ Save Favourite
                    </button>

                </div>
            `;
        }).join("");

        document.getElementById("results").scrollIntoView({
            behavior: "smooth"
        });

    } catch (error) {
        results.innerHTML =
            "<p class='empty-message'>Something went wrong. Please try again.</p>";
    } finally {
        button.innerText = "Discover My Outfits →";
        button.disabled = false;
    }
}


function saveOutfit(button, name) {
    let saved = JSON.parse(
        localStorage.getItem("wearwell_saved") || "[]"
    );

    if (saved.includes(name)) {
        button.innerText = "✓ Already Saved";
        return;
    }

    saved.push(name);

    localStorage.setItem(
        "wearwell_saved",
        JSON.stringify(saved)
    );

    button.innerText = "♥ Saved";
}