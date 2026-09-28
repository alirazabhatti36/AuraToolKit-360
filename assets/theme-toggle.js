/**
 * AuraToolkit360 - Global Theme Toggle Controller
 * Supports persistent Light & Dark modes across all toolkit pages
 */
(function() {
    function initTheme() {
        const savedTheme = localStorage.getItem('atk_theme');
        if (savedTheme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
        }
        updateThemeButtons();
    }

    function updateThemeButtons() {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
            btn.innerHTML = isDark ? '<span>☀️</span> Light' : '<span>🌙</span> Dark';
            btn.setAttribute('aria-label', isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode');
        });
    }

    window.toggleAuraTheme = function() {
        const current = document.documentElement.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('atk_theme', next);
        updateThemeButtons();
    };

    // Run on load and DOMContentLoaded
    initTheme();
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', updateThemeButtons);
    } else {
        updateThemeButtons();
    }
})();
