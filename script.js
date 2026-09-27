async function analyzeIncident() {

    const problem = document.getElementById("problem").value.trim();

    const result = document.getElementById("result");
    const loading = document.getElementById("loading");
    const error = document.getElementById("error");

    if (!problem) {
        error.textContent = "Please describe the incident first.";
        error.classList.remove("hidden");
        result.classList.add("hidden");
        return;
    }

    error.classList.add("hidden");
    result.classList.add("hidden");
    loading.classList.remove("hidden");

    try {

        const response = await fetch("/analyze", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                problem: problem
            })

        });

        const data = await response.json();

        loading.classList.add("hidden");

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }

        const memoriesContainer =
            document.getElementById("memories");

        memoriesContainer.innerHTML = "";

        if (data.memories && data.memories.length > 0) {

            data.memories.forEach((memory, index) => {

                const div = document.createElement("div");

                div.className = "memory";

                div.innerHTML =
                    `<strong>Memory ${index + 1}</strong><br>${memory}`;

                memoriesContainer.appendChild(div);

            });

        }

        document.getElementById("recommendation").textContent =
            data.recommendation;

        result.classList.remove("hidden");

    } catch (err) {

        loading.classList.add("hidden");

        error.textContent = "Error: " + err.message;

        error.classList.remove("hidden");
    }
}