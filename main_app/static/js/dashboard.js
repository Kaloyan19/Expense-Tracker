document.addEventListener("DOMContentLoaded", function () {
    try {
        const categoryElement = document.getElementById("categoryData");
        const monthlyLabelsElement = document.getElementById("monthlyLabels");
        const monthlyValuesElement = document.getElementById("monthlyValues");

        if (!categoryElement || !monthlyLabelsElement || !monthlyValuesElement) {
            console.error("Error: JSON script elements not found in the DOM.");
            return;
        }

        const categoryDataText = categoryElement.textContent.trim();
        const monthlyLabelsText = monthlyLabelsElement.textContent.trim();
        const monthlyValuesText = monthlyValuesElement.textContent.trim();

        if (!categoryDataText || !monthlyLabelsText || !monthlyValuesText) {
            console.error("Error: JSON data is empty or invalid.");
            return;
        }

        try {
            const categoryData = JSON.parse(categoryDataText);
            const monthlyLabels = JSON.parse(monthlyLabelsText);
            const monthlyValues = JSON.parse(monthlyValuesText);

            console.log("DEBUG: categoryData =", categoryData);
            console.log("DEBUG: monthlyLabels =", monthlyLabels);
            console.log("DEBUG: monthlyValues =", monthlyValues);
        } catch (jsonError) {
            console.error("Error parsing JSON data:", jsonError);
        }
    } catch (error) {
        console.error("Unexpected error:", error);
    }
});