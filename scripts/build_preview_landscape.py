from generate_landscape_logos import get_landscape_banner

sample_slugs = ["ppt-to-pdf", "word-to-pdf", "pdf-to-word", "excel-to-pdf", "merge-pdf", "compress-pdf", "jpg-to-pdf", "split-pdf", "age-calculator"]

html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Landscape Banners Preview</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet">
<style>
body { background: #0f172a; padding: 40px; font-family: 'Plus Jakarta Sans', sans-serif; color: #f8fafc; }
h1 { text-align: center; margin-bottom: 30px; font-weight: 800; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; max-width: 1200px; margin: 0 auto; }
.tool-card {
    background: #ffffff;
    border-radius: 20px;
    padding: 1.4rem;
    border: 1px solid #e2e8f0;
    color: #0f172a;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    transition: transform 0.2s, box-shadow 0.2s;
}
.tool-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 32px rgba(37,99,235,0.15);
}
.banner-container {
    width: 100%;
    height: 78px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem;
    overflow: hidden;
}
h3 { margin: 0 0 0.5rem; font-size: 1.15rem; font-weight: 800; color: #0f172a; }
p { color: #64748b; font-size: 0.85rem; line-height: 1.45; margin: 0 0 1rem; }
.btn {
    background: linear-gradient(135deg, #1d4ed8, #2563eb);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px;
    font-weight: 700;
    font-size: 0.88rem;
    text-align: center;
    text-decoration: none;
    display: block;
    margin-top: auto;
}
</style>
</head>
<body>
<h1>AuraToolKit 360 - Landscape Tool Banners (Matching User Reference)</h1>
<div class="grid">
"""

for slug in sample_slugs:
    title = slug.replace("-", " ").title()
    svg = get_landscape_banner(slug, title)
    html += f"""
    <div class="tool-card">
        <div class="banner-container">
            {svg}
        </div>
        <h3>{title}</h3>
        <p>100% private in-browser conversion with zero server uploads.</p>
        <a href="#" class="btn">Convert Now ⚡</a>
    </div>
    """

html += """
</div>
</body>
</html>
"""

with open("scratch/preview_landscape.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Generated scratch/preview_landscape.html successfully!")
