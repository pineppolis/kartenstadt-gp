// --- 1. THEME TOGGLE LOGIC ---
const setupTheme = () => {
    const toggleBtn = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme');

    // Apply saved theme on load
    if (currentTheme === 'light') {
        document.body.classList.add('light-mode');
    }

    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            document.body.classList.toggle('light-mode');

            // Save preference
            const theme = document.body.classList.contains('light-mode') ? 'light' : 'dark';
            localStorage.setItem('theme', theme);
        });
    }
};

// --- 2. SCROLL ANIMATION LOGIC (Intersection Observer) ---
const setupAnimations = () => {
    const observerOptions = { threshold: 0.15 };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("appear");
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll(".article-card").forEach((card) => {
        observer.observe(card);
    });
};

// Initialize everything once the DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    setupTheme();
    setupAnimations();
});
