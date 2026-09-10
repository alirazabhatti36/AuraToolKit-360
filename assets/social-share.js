/**
 * AuraToolkit360 - 1-Click Viral Social Sharing Component
 * Allows instant sharing to WhatsApp, LinkedIn, X (Twitter), and Clipboard
 */
(function() {
    'use strict';

    window.AuraShare = {
        getDefaultUrl: function() {
            var canonical = document.querySelector('link[rel="canonical"]');
            return canonical ? canonical.href : window.location.href.split('#')[0];
        },

        getDefaultText: function() {
            var title = document.title.split('|')[0].trim();
            return "Check out " + title + " on AuraToolkit360 — 100% Free, No Sign-up & Zero Watermarks:";
        },

        whatsapp: function(customText, customUrl) {
            var url = customUrl || this.getDefaultUrl();
            var text = (customText || this.getDefaultText()) + " " + url;
            var waUrl = "https://api.whatsapp.com/send?text=" + encodeURIComponent(text);
            window.open(waUrl, '_blank', 'noopener,noreferrer');
        },

        linkedin: function(customUrl) {
            var url = customUrl || this.getDefaultUrl();
            var liUrl = "https://www.linkedin.com/sharing/share-offsite/?url=" + encodeURIComponent(url);
            window.open(liUrl, '_blank', 'noopener,noreferrer,width=600,height=600');
        },

        twitter: function(customText, customUrl) {
            var url = customUrl || this.getDefaultUrl();
            var text = customText || this.getDefaultText();
            var twUrl = "https://twitter.com/intent/tweet?text=" + encodeURIComponent(text) + "&url=" + encodeURIComponent(url);
            window.open(twUrl, '_blank', 'noopener,noreferrer,width=600,height=500');
        },

        copyLink: function(buttonElement, customUrl) {
            var url = customUrl || this.getDefaultUrl();
            var originalHtml = buttonElement.innerHTML;

            var performSuccess = function() {
                buttonElement.classList.add('copied');
                buttonElement.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg><span>Copied Link!</span>';
                setTimeout(function() {
                    buttonElement.classList.remove('copied');
                    buttonElement.innerHTML = originalHtml;
                }, 2500);
            };

            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(url).then(performSuccess).catch(function() {
                    fallbackCopy(url, performSuccess);
                });
            } else {
                fallbackCopy(url, performSuccess);
            }

            function fallbackCopy(text, cb) {
                var textArea = document.createElement("textarea");
                textArea.value = text;
                textArea.style.position = "fixed";
                textArea.style.left = "-9999px";
                document.body.appendChild(textArea);
                textArea.focus();
                textArea.select();
                try {
                    document.execCommand('copy');
                    cb();
                } catch (err) {
                    prompt("Copy link to share:", text);
                }
                document.body.removeChild(textArea);
            }
        },

        renderWidgets: function() {
            var containers = document.querySelectorAll('.aura-share-container:not([data-rendered])');
            if (!containers.length) return;

            var self = this;
            containers.forEach(function(container) {
                container.setAttribute('data-rendered', 'true');
                var shareUrl = container.getAttribute('data-url') || self.getDefaultUrl();
                var shareTitle = container.getAttribute('data-title') || "Love this free tool? Share it with job seekers & friends!";
                var shareSubtitle = container.getAttribute('data-subtitle') || "Help colleagues build ATS resumes, convert documents, and land their dream jobs with 100% free private tools.";

                var html = `
                <div class="aura-share-card">
                    <div class="aura-share-header">
                        <div>
                            <span class="aura-share-badge">❤️ 100% Free &amp; Private</span>
                            <div class="aura-share-title">${shareTitle}</div>
                            <p class="aura-share-subtitle">${shareSubtitle}</p>
                        </div>
                    </div>
                    <div class="aura-share-buttons">
                        <button type="button" class="aura-btn-share aura-btn-whatsapp" title="Share via WhatsApp">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2m.01 1.67c2.2 0 4.26.86 5.82 2.42a8.225 8.225 0 0 1 2.41 5.83c0 4.54-3.7 8.24-8.24 8.24-1.48 0-2.93-.4-4.2-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.196 8.196 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.24-8.24m4.52 11.66c-.25-.13-1.47-.72-1.7-.81-.23-.09-.39-.13-.56.13-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.13-1.06-.39-2.03-1.25-.75-.67-1.26-1.5-1.41-1.75-.15-.25-.02-.39.11-.51.11-.11.25-.29.37-.44.13-.15.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.13-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43h-.48c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1s.9 2.43 1.02 2.6c.13.17 1.77 2.7 4.28 3.79.6.26 1.07.41 1.43.53.6.19 1.15.16 1.58.1.48-.07 1.47-.6 1.68-1.18.21-.58.21-1.07.15-1.18-.07-.1-.23-.17-.48-.29z"/></svg>
                            <span>WhatsApp</span>
                        </button>
                        <button type="button" class="aura-btn-share aura-btn-linkedin" title="Share on LinkedIn">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 8.76a1.64 1.64 0 0 0 1.66-1.63 1.65 1.65 0 1 0-3.31 0c0 .9.74 1.63 1.65 1.63M7.86 18.5v-8.37H5.07v8.37h2.79z"/></svg>
                            <span>LinkedIn</span>
                        </button>
                        <button type="button" class="aura-btn-share aura-btn-twitter" title="Share on X">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                            <span>Post on X</span>
                        </button>
                        <button type="button" class="aura-btn-share aura-btn-copy" title="Copy Direct Link">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
                            <span>Copy Link</span>
                        </button>
                    </div>
                </div>
                `;
                container.innerHTML = html;

                var waBtn = container.querySelector('.aura-btn-whatsapp');
                var liBtn = container.querySelector('.aura-btn-linkedin');
                var twBtn = container.querySelector('.aura-btn-twitter');
                var cpBtn = container.querySelector('.aura-btn-copy');

                if (waBtn) waBtn.addEventListener('click', function() { self.whatsapp(null, shareUrl); });
                if (liBtn) liBtn.addEventListener('click', function() { self.linkedin(shareUrl); });
                if (twBtn) twBtn.addEventListener('click', function() { self.twitter(null, shareUrl); });
                if (cpBtn) cpBtn.addEventListener('click', function() { self.copyLink(cpBtn, shareUrl); });
            });
        }
    };

    // Initialize automatically when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            window.AuraShare.renderWidgets();
        });
    } else {
        window.AuraShare.renderWidgets();
    }
})();
