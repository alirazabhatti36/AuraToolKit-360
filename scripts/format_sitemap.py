import re

with open("sitemap.xml", "r", encoding="utf-8") as f:
    c = f.read()

# Strip any namespace prefixes like ns0:
c = re.sub(r'</?ns0:', lambda m: '</' if m.group().startswith('</') else '<', c)
c = re.sub(r'xmlns:ns0="[^"]*"', '', c)
c = re.sub(r'<urlset[^>]*>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">', c)

urls = re.findall(r'<url>(.*?)</url>', c, re.DOTALL)
print(f"Parsed {len(urls)} URLs")

new_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    loc = re.search(r'<loc>(.*?)</loc>', u)
    lastmod = re.search(r'<lastmod>(.*?)</lastmod>', u)
    changefreq = re.search(r'<changefreq>(.*?)</changefreq>', u)
    priority = re.search(r'<priority>(.*?)</priority>', u)
    
    new_xml += "  <url>\n"
    if loc:
        new_xml += f"    <loc>{loc.group(1).strip()}</loc>\n"
    if lastmod:
        new_xml += f"    <lastmod>{lastmod.group(1).strip()}</lastmod>\n"
    if changefreq:
        new_xml += f"    <changefreq>{changefreq.group(1).strip()}</changefreq>\n"
    if priority:
        new_xml += f"    <priority>{priority.group(1).strip()}</priority>\n"
    new_xml += "  </url>\n"

new_xml += "</urlset>\n"

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(new_xml)

print(f"Successfully formatted sitemap.xml with {len(urls)} entries.")
