/**
 * AuraToolkit360 - Global Navbar Search & Navigation Utilities
 * Provides instant live tool suggestions dropdown matching media_1790969611056.png
 */
(function() {
    const SITE_TOOLS = [
        { name: "PDF to Word Converter", url: "/converter/#pdf-to-word", cat: "Converter", icon: "📄" },
        { name: "Word to PDF Converter", url: "/converter/#word-to-pdf", cat: "Converter", icon: "📝" },
        { name: "Merge PDF Files", url: "/converter/#merge-pdf", cat: "Converter", icon: "📑" },
        { name: "Compress PDF", url: "/converter/#compress-pdf", cat: "Converter", icon: "🗜️" },
        { name: "PDF to JPG Image", url: "/converter/#pdf-to-jpg", cat: "Converter", icon: "🖼️" },
        { name: "JPG to PDF Converter", url: "/converter/#jpg-to-pdf", cat: "Converter", icon: "📄" },
        { name: "Excel to PDF Converter", url: "/converter/#excel-to-pdf", cat: "Converter", icon: "📊" },
        { name: "PowerPoint to PDF", url: "/converter/#ppt-to-pdf", cat: "Converter", icon: "📽️" },
        { name: "Resume & CV Maker", url: "/resume-cv-maker/", cat: "Resume", icon: "📄" },
        { name: "12 ATS Resume Templates", url: "/resume-cv-maker/#templates", cat: "Resume", icon: "🎨" },
        { name: "Cover Letter Builder", url: "/cover-letter-maker/", cat: "Cover Letter", icon: "✉️" },
        { name: "Resume ATS Score Checker", url: "/resume-score-checker/", cat: "Score Checker", icon: "🎯" },
        { name: "HR Bulk Resume Screener", url: "/hr-helper/", cat: "HR Bulk", icon: "👥" },
        { name: "AuraHR 360 Enterprise SaaS", url: "/saas/", cat: "Enterprise", icon: "⚡" },
        { name: "Career & Tech Blogs", url: "/blogs/", cat: "Blogs", icon: "📚" }
    ];

    window.handleNavSearch = function(val) {
        const resultsEl = document.getElementById('navSearchMenu');
        if (!resultsEl) return;
        const q = (val || '').trim().toLowerCase();
        if (!q) {
            resultsEl.style.display = 'none';
            resultsEl.innerHTML = '';
            return;
        }

        const matches = SITE_TOOLS.filter(t => 
            t.name.toLowerCase().includes(q) || 
            t.cat.toLowerCase().includes(q)
        ).slice(0, 6);

        if (!matches.length) {
            resultsEl.innerHTML = `
                <div style="padding: 0.6rem 0.85rem; font-size: 0.8rem; color: #64748b; text-align: center;">
                    No direct tools found. Press Enter to search All 59+ tools.
                </div>
            `;
            resultsEl.style.display = 'block';
            return;
        }

        resultsEl.innerHTML = matches.map(m => `
            <a href="${m.url}" class="nav-search-item">
                <span style="display:flex; align-items:center; gap:0.45rem;">
                    <span>${m.icon}</span>
                    <span style="font-weight:600; color:#0f172a;">${escapeHtml(m.name)}</span>
                </span>
                <span style="font-size:0.7rem; color:#64748b; background:#f1f5f9; padding:2px 6px; border-radius:5px;">${escapeHtml(m.cat)}</span>
            </a>
        `).join('') + `
            <div style="border-top:1px solid #f1f5f9; margin-top:4px; padding-top:4px; text-align:center;">
                <a href="/converter/?q=${encodeURIComponent(q)}" style="font-size:0.76rem; color:#2563eb; font-weight:600; text-decoration:none; display:block; padding:4px;">
                    Search all converters for "${escapeHtml(q)}" →
                </a>
            </div>
        `;
        resultsEl.style.display = 'block';
    };

    window.executeNavSearch = function() {
        const inp = document.getElementById('navGlobalSearch');
        if (!inp) return;
        const val = inp.value.trim();
        if (!val) return;

        // If on converter page, focus converter search
        const convInput = document.getElementById('toolSearchInput');
        if (convInput) {
            convInput.value = val;
            if (typeof filterTools === 'function') filterTools();
            convInput.scrollIntoView({ behavior: 'smooth' });
            const resultsEl = document.getElementById('navSearchMenu');
            if (resultsEl) resultsEl.style.display = 'none';
            return;
        }

        window.location.href = '/converter/?q=' + encodeURIComponent(val);
    };

    function escapeHtml(str) {
        return String(str || '')
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    // Close dropdown on outside click
    document.addEventListener('click', function(e) {
        const wrap = document.querySelector('.nav-search-wrap');
        const resultsEl = document.getElementById('navSearchMenu');
        if (resultsEl && wrap && !wrap.contains(e.target)) {
            resultsEl.style.display = 'none';
        }
    });
})();
