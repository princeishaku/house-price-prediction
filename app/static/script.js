// ============================================
// House Price Prediction App
// ============================================

document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("form");
    const button = document.querySelector("button");

    if (form && button) {

        form.addEventListener("submit", () => {

            button.disabled = true;

            button.innerHTML = "Predicting...";

        });

    }

    const inputs = document.querySelectorAll("input");

    inputs.forEach(input => {

        input.addEventListener("focus", () => {

            input.style.borderColor = "#2563eb";

        });

        input.addEventListener("blur", () => {

            input.style.borderColor = "#cccccc";

        });

    });

});