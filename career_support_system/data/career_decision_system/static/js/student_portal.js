function buildRoleChart(payload) {
    const canvas = document.getElementById("roleChart");
    if (!canvas || typeof Chart === "undefined") {
        return;
    }

    new Chart(canvas, {
        type: "bar",
        data: {
            labels: payload.role_labels,
            datasets: [
                {
                    label: "Matching Score",
                    data: payload.role_scores,
                    backgroundColor: ["#ef4444", "#0f766e", "#4f46e5"],
                    borderRadius: 12,
                },
            ],
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                },
            },
        },
    });
}

function buildScoreChart(payload) {
    const canvas = document.getElementById("scoreChart");
    if (!canvas || typeof Chart === "undefined") {
        return;
    }

    new Chart(canvas, {
        type: "line",
        data: {
            labels: ["Before Reupload", "After Reupload"],
            datasets: [
                {
                    label: "Resume Score",
                    data: payload.score_compare,
                    borderColor: "#0f766e",
                    backgroundColor: "rgba(15, 118, 110, 0.15)",
                    fill: true,
                    tension: 0.35,
                },
            ],
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                },
            },
        },
    });
}

function buildProgressChart(payload) {
    const canvas = document.getElementById("progressChart");
    if (!canvas || typeof Chart === "undefined") {
        return;
    }

    new Chart(canvas, {
        type: "scatter",
        data: {
            datasets: [
                {
                    label: "Progress Points",
                    data: payload.progress_points,
                    showLine: true,
                    borderColor: "#4f46e5",
                    backgroundColor: "#4f46e5",
                    tension: 0,
                },
            ],
        },
        options: {
            responsive: true,
            parsing: false,
            scales: {
                x: {
                    min: 1,
                    max: payload.progress_labels.length,
                    ticks: {
                        callback(value) {
                            return payload.progress_labels[value - 1] || value;
                        },
                    },
                },
                y: {
                    min: 0,
                    max: 3,
                    ticks: {
                        stepSize: 1,
                        callback(value) {
                            if (value === 1) {
                                return "Started";
                            }
                            if (value === 2) {
                                return "Learning";
                            }
                            if (value === 3) {
                                return "Completed";
                            }
                            return "Idle";
                        },
                    },
                },
            },
        },
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const payload = window.studentPortalCharts;
    if (!payload) {
        return;
    }

    buildRoleChart(payload);
    buildScoreChart(payload);
    buildProgressChart(payload);
});
