// AuraToolkit360 PWA Registration & 1-Click Install System
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').catch(() => {});
    });
}

let deferredPrompt = null;

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    document.querySelectorAll('.pwa-install-btn').forEach(btn => {
        if (btn.classList.contains('mobile-nav-item')) {
            btn.style.display = 'flex';
        } else {
            btn.style.display = 'inline-block';
        }
    });
});

// Hide install options if app is already running in standalone PWA mode
if (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true) {
    document.querySelectorAll('.pwa-install-btn').forEach(btn => btn.style.display = 'none');
}

window.installPwaApp = async function() {
    if (!deferredPrompt) {
        alert('To install AuraToolkit360 on your device:\n\n• Chrome/Edge (Desktop): Click the install icon in the URL address bar.\n• Android: Tap the three dots (⋮) and select "Install app" or "Add to Home Screen".\n• iPhone/iPad: Tap the Share button (⎋) and select "Add to Home Screen".');
        return;
    }
    deferredPrompt.prompt();
    const choiceResult = await deferredPrompt.userChoice;
    if (choiceResult.outcome === 'accepted') {
        document.querySelectorAll('.pwa-install-btn').forEach(btn => btn.style.display = 'none');
    }
    deferredPrompt = null;
};
