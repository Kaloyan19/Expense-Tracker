document.addEventListener("DOMContentLoaded", function () {
    try {
        // ✅ Ensure the elements exist before parsing
        const categoryElement = document.getElementById("categoryData");
        const monthlyLabelsElement = document.getElementById("monthlyLabels");
        const monthlyValuesElement = document.getElementById("monthlyValues");

        if (!categoryElement || !monthlyLabelsElement || !monthlyValuesElement) {
            console.error("Error: JSON script elements not found in the DOM.");
            return;
        }

        // ✅ Safely parse JSON data from Django templates
        const categoryData = JSON.parse(categoryElement.textContent);
        const monthlyLabels = JSON.parse(monthlyLabelsElement.textContent);
        const monthlyValues = JSON.parse(monthlyValuesElement.textContent);

        console.log("DEBUG: categoryData =", categoryData);
        console.log("DEBUG: monthlyLabels =", monthlyLabels);
        console.log("DEBUG: monthlyValues =", monthlyValues);

        // ✅ Ensure categoryData uses the correct field name
        const categoryLabels = categoryData.map(item => item["category__name"] || item["category"]);
        const categoryValues = categoryData.map(item => item["total"]);

        // ✅ Ensure Chart.js is correctly initialized
        if (typeof Chart !== "undefined") {
            new Chart(document.getElementById('categoryChart').getContext('2d'), {
                type: 'pie',
                data: {
                    labels: categoryLabels,
                    datasets: [{
                        data: categoryValues,
                        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#8AC24A', '#3F51B5'],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'right' },
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    return `${context.label}: $${context.raw.toFixed(2)}`;
                                }
                            }
                        }
                    }
                }
            });

            new Chart(document.getElementById('monthlyChart').getContext('2d'), {
                type: 'bar',
                data: {
                    labels: monthlyLabels,
                    datasets: [{
                        label: 'Amount ($)',
                        data: monthlyValues,
                        backgroundColor: '#36A2EB',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function (value) {
                                    return '$' + value;
                                }
                            }
                        }
                    }
                }
            });
        } else {
            console.error("Chart.js is not loaded correctly!");
        }
    } catch (error) {
        console.error("Error parsing JSON data:", error);
    }
});