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

    window.AuraFX = AuraFX;

    document.addEventListener('DOMContentLoaded', () => {
        AuraFX.initCardGlow();
    });
})(window);
