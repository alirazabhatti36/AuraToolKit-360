import glob, os, re

base_dir = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360"
dedicated_pages = glob.glob(os.path.join(base_dir, "converter", "*", "index.html"))

outlines_css_block = """
        /* Prominent Outlines & High-Contrast Visual Separation */
        .tool-card,
        .tool-box,
        .calc-card {
            border: 1.5px solid #cbd5e1 !important;
            box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.08), 0 2px 6px -1px rgba(15, 23, 42, 0.04) !important;
        }
        .file-upload-box,
        .upload-area,
        #dropZone {
            border: 2px dashed #94a3b8 !important;
            background: #f8fafc !important;
        }
        .file-upload-box:hover,
        .upload-area:hover,
        #dropZone:hover {
            border-color: #2563eb !important;
            background: #eff6ff !important;
        }
        .tool-hero-banner {
            border: 1.5px solid #cbd5e1 !important;
            background: #f1f5f9 !important;
            box-shadow: inset 0 1px 2px rgba(15, 23, 42, 0.04), 0 1px 2px rgba(15, 23, 42, 0.03) !important;
        }
        .info-card,
        .step-box,
        .related-card {
            border: 1.5px solid #cbd5e1 !important;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04) !important;
        }
        .related-card:hover {
            border-color: #2563eb !important;
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.12) !important;
        }
"""

updated_count = 0
for dp in dedicated_pages:
    slug = os.path.basename(os.path.dirname(dp))
    with open(dp, "r", encoding="utf-8") as f:
        c = f.read()

    if "/* Prominent Outlines & High-Contrast Visual Separation */" in c:
        continue

    # Insert before </style> in the page
    if "</style>" in c:
        c = c.replace("</style>", outlines_css_block + "\n    </style>", 1)
        with open(dp, "w", encoding="utf-8") as f:
            f.write(c)
        updated_count += 1

print(f"Injected prominent outlines CSS into {updated_count} dedicated tool pages!")
