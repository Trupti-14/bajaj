form.addEventListener("submit", async function (e) {
    e.preventDefault(); // Prevent default form submission

    loading.style.display = "block";
    resultDiv.style.display = "none";
    errorDiv.textContent = "";
    clausesDiv.innerHTML = "";

    const formData = new FormData(form);

    try {
        const response = await fetch("http://127.0.0.1:8000/process", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        const data = await response.json();

        // Display matched clauses
        (data.matched_clauses || []).forEach(clause => {
            const div = document.createElement("div");
            div.className = "clause";
            div.textContent = clause;
            clausesDiv.appendChild(div);
        });

        // Show result section
        resultDiv.style.display = "block";

    } catch (error) {
        errorDiv.textContent = "Error: " + error.message;
    } finally {
        loading.style.display = "none";
    }
});