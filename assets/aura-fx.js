/**
 * AuraToolkit360 — Luxury Animation & Micro-Interactions FX Engine
 * Lightweight, zero-dependency, 60fps hardware accelerated
 */
(function(window) {
    'use strict';

    const AuraFX = {
        /**
         * Smooth CountUp Number Animation (Ease-out Quart)
         */
        animateCount: function(el, target, duration = 800, prefix = '', suffix = '', decimals = 0) {
            if (!el) return;
            const targetNum = typeof target === 'number' ? target : parseFloat(String(target).replace(/[^0-9.-]+/g, '')) || 0;
            const startNum = 0;
            const startTime = performance.now();

            function easeOutQuart(x) {
                return 1 - Math.pow(1 - x, 4);
            }

            function update(now) {
                const elapsed = now - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const currentVal = startNum + (targetNum - startNum) * easeOutQuart(progress);

                const formatted = decimals > 0 
                    ? currentVal.toFixed(decimals) 
                    : Math.round(currentVal).toLocaleString();

                el.textContent = `${prefix}${formatted}${suffix}`;

                if (progress < 1) {
                    requestAnimationFrame(update);
                } else {
                    const finalFormatted = decimals > 0 
                        ? targetNum.toFixed(decimals) 
                        : Math.round(targetNum).toLocaleString();
                    el.textContent = `${prefix}${finalFormatted}${suffix}`;
                }
            }

            requestAnimationFrame(update);
        },

        /**
         * High-Performance Canvas Confetti Burst
         */
        confetti: function() {
            let canvas = document.getElementById('auraConfettiCanvas');
            if (!canvas) {
                canvas = document.createElement('canvas');
                canvas.id = 'auraConfettiCanvas';
                document.body.appendChild(canvas);
            }
            const ctx = canvas.getContext('2d');
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;

            const particles = [];
            const colors = ['#38bdf8', '#818cf8', '#c084fc', '#34d399', '#fbbf24', '#f472b6'];

            for (let i = 0; i < 70; i++) {
                particles.push({
                    x: canvas.width / 2 + (Math.random() - 0.5) * 200,
                    y: canvas.height * 0.45,
                    vx: (Math.random() - 0.5) * 14,
                    vy: (Math.random() - 1) * 12 - 4,
                    size: Math.random() * 8 + 4,
                    color: colors[Math.floor(Math.random() * colors.length)],
                    tilt: Math.random() * 10,
                    tiltAngle: 0,
                    tiltSpeed: Math.random() * 0.1 + 0.05,
                    opacity: 1
                });
            }

            let animId;
            function render() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                let alive = 0;

                particles.forEach(p => {
                    p.x += p.vx;
                    p.y += p.vy;
                    p.vy += 0.35; // gravity
                    p.tiltAngle += p.tiltSpeed;
                    p.tilt = Math.sin(p.tiltAngle) * 12;
                    p.opacity -= 0.012;

                    if (p.opacity > 0) {
                        alive++;
                        ctx.fillStyle = p.color;
                        ctx.globalAlpha = Math.max(0, p.opacity);
                        ctx.beginPath();
                        ctx.ellipse(p.x, p.y, p.size, Math.abs(p.tilt), p.tiltAngle, 0, 2 * Math.PI);
                        ctx.fill();
                    }
                });

                if (alive > 0) {
                    animId = requestAnimationFrame(render);
                } else {
                    cancelAnimationFrame(animId);
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                }
            }

            render();
        },

        /**
         * Dynamic Mouse-Follower Radial Border Glow (Linear/Raycast style)
         */
        initCardGlow: function() {
            document.querySelectorAll('.aura-glow-card, .tool-card, .trending-card').forEach(card => {
                card.addEventListener('mousemove', function(e) {
                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    card.style.setProperty('--mouse-x', `${x}px`);
                    card.style.setProperty('--mouse-y', `${y}px`);
                });
            });
        },

        /**
         * Slick Toast Notification
         */
        toast: function(msg, icon = '✨') {
            let container = document.getElementById('auraToastBox');
            if (!container) {
                container = document.createElement('div');
                container.id = 'auraToastBox';
                container.style.cssText = 'position:fixed;bottom:24px;right:24px;display:flex;flex-direction:column;gap:8px;z-index:999999;pointer-events:none;';
                document.body.appendChild(container);
            }

            const toast = document.createElement('div');
            toast.style.cssText = 'background:rgba(15,23,42,0.92);backdrop-filter:blur(12px);border:1px solid rgba(56,189,248,0.3);color:#f8fafc;padding:0.75rem 1.25rem;border-radius:12px;font-size:0.88rem;font-weight:600;display:flex;align-items:center;gap:0.5rem;box-shadow:0 12px 30px rgba(0,0,0,0.35);transform:translateY(20px);opacity:0;transition:all 0.3s cubic-bezier(0.16,1,0.3,1);';
            toast.innerHTML = `<span>${icon}</span><span>${msg}</span>`;
            container.appendChild(toast);

            requestAnimationFrame(() => {
                toast.style.transform = 'translateY(0)';
                toast.style.opacity = '1';
            });

            setTimeout(() => {
                toast.style.transform = 'translateY(10px)';
                toast.style.opacity = '0';
                setTimeout(() => toast.remove(), 300);
            }, 2500);
        }
    };

    // Global Mobile Navigation Toggle
    window.toggleMobileMenu = function() {
        const drawer = document.getElementById('mobileNavDrawer');
        const hamburger = document.getElementById('navHamburger');
        if (drawer) {
            drawer.classList.toggle('open');
            const isOpen = drawer.classList.contains('open');
            if (hamburger) {
                hamburger.classList.toggle('active', isOpen);
                hamburger.setAttribute('aria-expanded', isOpen);
            }
        }
    };

    // Global Bookmark Handler
    window.bookmarkSite = function() {
        if (navigator.userAgent.toLowerCase().indexOf('mac') !== -1) {
            alert('Press Cmd + D to bookmark AuraToolkit360!');
        } else {
            alert('Press Ctrl + D to bookmark AuraToolkit360!');
        }
    };

    // Global Language Switcher Toggle
    window.toggleLangDropdown = function(e) {
        if (e) e.stopPropagation();
        const menu = document.getElementById('langDropdownMenu');
        const btn = document.getElementById('langSwitcherBtn');
        if (menu) {
            menu.classList.toggle('show');
            if (btn) btn.setAttribute('aria-expanded', menu.classList.contains('show'));
        }
    };

    document.addEventListener('click', function(e) {
        const menu = document.getElementById('langDropdownMenu');
        const btn = document.getElementById('langSwitcherBtn');
        if (menu && menu.classList.contains('show')) {
            if (!menu.contains(e.target) && (!btn || !btn.contains(e.target))) {
                menu.classList.remove('show');
                if (btn) btn.setAttribute('aria-expanded', 'false');
            }
        }
        const drawer = document.getElementById('mobileNavDrawer');
        const hamburger = document.getElementById('navHamburger');
        if (drawer && drawer.classList.contains('open')) {
            if (!drawer.contains(e.target) && (!hamburger || !hamburger.contains(e.target))) {
                drawer.classList.remove('open');
                if (hamburger) {
                    hamburger.classList.remove('active');
                    hamburger.setAttribute('aria-expanded', 'false');
                }
            }
        }
    });

    // Global Language Dropdown Fallback
    if (!window.toggleLangDropdown) {
        window.toggleLangDropdown = function(e) {
            if (e) e.stopPropagation();
            const dropdown = document.getElementById('langDropdownMenu');
            if (dropdown) {
                const isOpen = dropdown.classList.toggle('show');
                dropdown.style.display = isOpen ? 'flex' : 'none';
                const btn = document.getElementById('langSwitcherBtn');
                if (btn) btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
            }
        };
    }

    // Global Theme Toggle Fallback
    if (!window.toggleAuraTheme) {
        window.toggleAuraTheme = function() {
            const current = document.documentElement.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            try { localStorage.setItem('atk_theme', next); } catch(e) {}
            document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
                btn.innerHTML = next === 'dark' 
                    ? '<span class="theme-icon">☀️</span><span class="theme-label">Light</span>' 
                    : '<span class="theme-icon">🌙</span><span class="theme-label">Dark</span>';
                btn.setAttribute('aria-label', next === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode');
                btn.setAttribute('title', next === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode');
            });
        };
    }

    // PWA Install Fallback
    if (!window.installPwaApp) {
        window.installPwaApp = function() {
            alert('To install AuraToolkit360 on your device:\n\n• Chrome/Edge (Desktop): Click the install icon in the URL address bar.\n• Android: Tap the three dots (⋮) and select "Install app" or "Add to Home Screen".\n• iPhone/iPad: Tap the Share button (⎋) and select "Add to Home Screen".');
        };
    }

    // Highlight Active Navigation Link Automatically
    function highlightActiveNav() {
        const path = window.location.pathname;
        const normalized = path.replace(/\/$/, '') || '/';

        document.querySelectorAll('.navbar .nav-link, .mobile-nav-item').forEach(link => {
            const href = link.getAttribute('href');
            if (!href) return;
            const linkNorm = href.replace(/\/$/, '') || '/';
            if (linkNorm === '/' && normalized === '/') {
                link.classList.add('active');
            } else if (linkNorm !== '/' && (normalized === linkNorm || normalized.startsWith(linkNorm + '/'))) {
                link.classList.add('active');
            } else if (linkNorm === '/' && normalized !== '/') {
                link.classList.remove('active');
            }
        });
    }

    window.AuraFX = AuraFX;

    document.addEventListener('DOMContentLoaded', () => {
        AuraFX.initCardGlow();
        highlightActiveNav();
    });
})(window);

