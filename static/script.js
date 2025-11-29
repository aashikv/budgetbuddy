// Toast Notification
function showToast(message, type = 'success') {
    Toastify({
        text: message,
        duration: 3000,
        gravity: "top",
        position: "right",
        style: {
            background: type === 'success' ? "linear-gradient(to right, #10b981, #059669)" : "linear-gradient(to right, #ef4444, #dc2626)",
            borderRadius: "0.5rem",
            boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)"
        }
    }).showToast();
}

// Handle Flash Messages & Initialization
document.addEventListener('DOMContentLoaded', () => {
    // Flash Messages
    const flashContainer = document.getElementById('flash-messages');
    if (flashContainer) {
        try {
            const messages = JSON.parse(flashContainer.dataset.messages);
            messages.forEach(([category, message]) => {
                showToast(message, category);
                if (category === 'success' && message.toLowerCase().includes('income')) {
                    confetti({
                        particleCount: 100,
                        spread: 70,
                        origin: { y: 0.6 }
                    });
                }
            });
        } catch (e) {
            console.error("Error parsing flash messages:", e);
        }
    }

    // Onboarding
    if (!localStorage.getItem('onboardingShown')) {
        const modal = document.getElementById('onboardingModal');
        if (modal) {
            modal.style.display = 'flex';
        }
    }

    // Initialize Charts
    const pieCanvas = document.getElementById('pieChart');
    const lineCanvas = document.getElementById('lineChart');

    if (pieCanvas && lineCanvas) {
        try {
            const categoryData = JSON.parse(pieCanvas.dataset.chart || '{}');
            const trendData = JSON.parse(lineCanvas.dataset.chart || '{}');
            initCharts(categoryData, trendData);
        } catch (e) {
            console.error("Error parsing chart data:", e);
        }
    }

    // Dark Mode Toggle
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    const icon = themeToggle ? themeToggle.querySelector('i') : null;

    // Check local storage
    if (localStorage.getItem('darkMode') === 'enabled') {
        enableDarkMode();
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            if (body.classList.contains('dark-mode')) {
                disableDarkMode();
            } else {
                enableDarkMode();
            }
        });
    }

    function enableDarkMode() {
        body.classList.add('dark-mode');
        localStorage.setItem('darkMode', 'enabled');
        if (icon) {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        }
    }

    function disableDarkMode() {
        body.classList.remove('dark-mode');
        localStorage.setItem('darkMode', 'disabled');
        if (icon) {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        }
    }
});

function closeOnboarding() {
    const modal = document.getElementById('onboardingModal');
    if (modal) {
        modal.style.display = 'none';
        localStorage.setItem('onboardingShown', 'true');
        confetti({
            particleCount: 150,
            spread: 100,
            origin: { y: 0.6 }
        });
    }
}

function initCharts(categoryData, trendData) {
    // Pie Chart
    const pieCtx = document.getElementById('pieChart').getContext('2d');
    new Chart(pieCtx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(categoryData),
            datasets: [{
                data: Object.values(categoryData),
                backgroundColor: [
                    '#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right'
                }
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });

    // Line Chart
    const lineCtx = document.getElementById('lineChart').getContext('2d');
    const months = Object.keys(trendData);
    const incomeData = months.map(m => trendData[m].income);
    const expenseData = months.map(m => trendData[m].expense);

    new Chart(lineCtx, {
        type: 'line',
        data: {
            labels: months,
            datasets: [
                {
                    label: 'Income',
                    data: incomeData,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Expense',
                    data: expenseData,
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index',
            },
            plugins: {
                tooltip: {
                    enabled: true
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
