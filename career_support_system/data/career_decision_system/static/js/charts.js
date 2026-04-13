function initThemeToggle() {
    const toggleBtn = document.getElementById("themeToggle");
    if (!toggleBtn) {
        return;
    }

    const savedTheme = localStorage.getItem("careerTheme");
    if (savedTheme === "dark") {
        document.body.classList.add("dark");
    }

    toggleBtn.addEventListener("click", () => {
        document.body.classList.toggle("dark");
        const active = document.body.classList.contains("dark") ? "dark" : "light";
        localStorage.setItem("careerTheme", active);
    });
}

function commonScaleOptions() {
    return {
        y: {
            beginAtZero: true,
            max: 100,
        },
    };
}

function renderCharts() {
    if (typeof Chart === "undefined" || !window.chartPayload) {
        return;
    }

    const payload = window.chartPayload;

    const roleCanvas = document.getElementById("roleChart");
    if (roleCanvas) {
        new Chart(roleCanvas, {
            type: "bar",
            data: {
                labels: payload.role_labels,
                datasets: [
                    {
                        label: "Skill Match Score (%)",
                        data: payload.role_scores,
                        backgroundColor: "rgba(217, 72, 65, 0.78)",
                        borderRadius: 12,
                    },
                ],
            },
            options: {
                responsive: true,
                scales: commonScaleOptions(),
            },
        });
    }

    const improvementCanvas = document.getElementById("improvementChart");
    if (improvementCanvas) {
        new Chart(improvementCanvas, {
            type: "line",
            data: {
                labels: ["Before Learning", "After Progress Update"],
                datasets: [
                    {
                        label: "Readiness Score (%)",
                        data: payload.before_after,
                        borderColor: "rgba(15, 118, 110, 1)",
                        backgroundColor: "rgba(15, 118, 110, 0.22)",
                        tension: 0.35,
                        fill: true,
                    },
                ],
            },
            options: {
                responsive: true,
                scales: commonScaleOptions(),
            },
        });
    }

    const readinessCanvas = document.getElementById("readinessChart");
    if (readinessCanvas) {
        new Chart(readinessCanvas, {
            type: "line",
            data: {
                labels: ["Current", "Midpoint", "Improved"],
                datasets: [
                    {
                        label: "Career Readiness Trend (%)",
                        data: payload.readiness_trend,
                        borderColor: "rgba(245, 158, 11, 1)",
                        backgroundColor: "rgba(245, 158, 11, 0.18)",
                        pointRadius: 5,
                        fill: true,
                        tension: 0.4,
                    },
                ],
            },
            options: {
                responsive: true,
                scales: commonScaleOptions(),
            },
        });
    }

    const progressCanvas = document.getElementById("progressChart");
    if (progressCanvas) {
        new Chart(progressCanvas, {
            type: "line",
            data: {
                labels: payload.progress_labels,
                datasets: [
                    {
                        label: "Progress Points",
                        data: payload.progress_values.map((value) => value * 50),
                        borderColor: "rgba(79, 70, 229, 1)",
                        backgroundColor: "rgba(79, 70, 229, 0.12)",
                        pointRadius: 6,
                        pointHoverRadius: 8,
                        fill: false,
                        tension: 0,
                    },
                ],
            },
            options: {
                responsive: true,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label(context) {
                                const detail = payload.progress_tasks?.[context.dataIndex] || "";
                                return detail;
                            },
                        },
                    },
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback(value) {
                                if (value === 0) {
                                    return "Not Started";
                                }
                                if (value === 50) {
                                    return "In Progress";
                                }
                                if (value === 100) {
                                    return "Completed";
                                }
                                return value;
                            },
                        },
                    },
                },
            },
        });
    }
}

document.addEventListener("DOMContentLoaded", () => {
    initThemeToggle();
    renderCharts();
});
