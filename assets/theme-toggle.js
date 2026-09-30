/**
 * AuraToolkit360 - Theme Enforcer
 * Enforces signature Dark Luxury mode across all pages
 */
(function() {
    try {
        localStorage.removeItem('atk_theme');
        document.documentElement.setAttribute('data-theme', 'dark');
    } catch(e) {}
    window.toggleAuraTheme = function() {};
})();
