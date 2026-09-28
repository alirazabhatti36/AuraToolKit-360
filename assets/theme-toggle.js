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
            btn.innerHTML = isDark 
                ? '<span class="theme-icon">☀️</span><span class="theme-label">Light</span>' 
                : '<span class="theme-icon">🌙</span><span class="theme-label">Dark</span>';
            btn.setAttribute('aria-label', isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode');
            btn.setAttribute('title', isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode');
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
