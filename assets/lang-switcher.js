/**
 * AuraToolkit360 - Global Multilingual Language Switcher
 * Handles intelligent URL path resolution, persistence, and accessible dropdown.
 */
(function() {
    const SUPPORTED_LANGS = [
        { code: 'en', label: 'English', flag: '🇺🇸', dir: 'ltr' },
        { code: 'es', label: 'Español', flag: '🇪🇸', dir: 'ltr' },
        { code: 'fr', label: 'Français', flag: '🇫🇷', dir: 'ltr' },
        { code: 'de', label: 'Deutsch', flag: '🇩🇪', dir: 'ltr' },
        { code: 'pt', label: 'Português', flag: '🇧🇷', dir: 'ltr' },
        { code: 'ar', label: 'العربية', flag: '🇸🇦', dir: 'rtl' }
    ];

    function getCurrentLang() {
        const path = window.location.pathname;
        const match = path.match(/^\/(es|fr|de|pt|ar)(\/|$)/);
        return match ? match[1] : 'en';
    }

    function getCleanBasePath() {
        let path = window.location.pathname;
        path = path.replace(/^\/(es|fr|de|pt|ar)(\/|$)/, '/');
        if (!path.startsWith('/')) path = '/' + path;
        return path;
    }

    function buildLangUrl(targetCode) {
        const basePath = getCleanBasePath();
        if (targetCode === 'en') {
            return basePath;
        }
        return '/' + targetCode + (basePath === '/' ? '/' : basePath);
    }

    function initLangSwitcher() {
        const currentCode = getCurrentLang();
        const currentObj = SUPPORTED_LANGS.find(l => l.code === currentCode) || SUPPORTED_LANGS[0];

        // Update any current-lang indicator labels
        document.querySelectorAll('.lang-current-label').forEach(el => {
            el.textContent = currentObj.code.toUpperCase();
        });
        document.querySelectorAll('.lang-current-flag').forEach(el => {
            el.textContent = currentObj.flag;
        });

        // Set up links inside desktop and mobile dropdowns
        document.querySelectorAll('.lang-dropdown-menu a[data-lang], .mobile-lang-grid a[data-lang]').forEach(link => {
            const langCode = link.getAttribute('data-lang');
            link.href = buildLangUrl(langCode);
            if (langCode === currentCode) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    window.toggleLangDropdown = function(e) {
        if (e) e.stopPropagation();
        const dropdown = document.getElementById('langDropdownMenu');
        if (dropdown) {
            const isOpen = dropdown.classList.toggle('show');
            const btn = document.getElementById('langSwitcherBtn');
            if (btn) btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        }
    };

    // Close on outside click or ESC key
    document.addEventListener('click', function(e) {
        const dropdown = document.getElementById('langDropdownMenu');
        const btn = document.getElementById('langSwitcherBtn');
        if (dropdown && dropdown.classList.contains('show')) {
            if (!dropdown.contains(e.target) && (!btn || !btn.contains(e.target))) {
                dropdown.classList.remove('show');
                if (btn) btn.setAttribute('aria-expanded', 'false');
            }
        }
    });

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const dropdown = document.getElementById('langDropdownMenu');
            if (dropdown && dropdown.classList.contains('show')) {
                dropdown.classList.remove('show');
                const btn = document.getElementById('langSwitcherBtn');
                if (btn) btn.setAttribute('aria-expanded', 'false');
            }
        }
    });

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initLangSwitcher);
    } else {
        initLangSwitcher();
    }
})();
