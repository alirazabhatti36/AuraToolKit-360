from generate_landscape_logos import get_landscape_banner

# mp3-converter
p_mp3 = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360\converter\mp3-converter\index.html"
with open(p_mp3, "r", encoding="utf-8") as f:
    c = f.read()
if "tool-hero-banner" not in c:
    svg = get_landscape_banner("mp3-converter")
    banner_div = f'<div class="tool-hero-banner" style="width: 180px; max-width: 100%; height: 76px; margin: 0 auto 1.4rem; background: rgba(15,23,42,0.6); border: 1px solid rgba(255,255,255,0.12); border-radius: 16px; display: flex; align-items: center; justify-content: center; padding: 2px; box-shadow: 0 8px 24px rgba(0,0,0,0.3); overflow: hidden;">{svg}</div>\n        '
    c = c.replace('<div class="tool-box">', banner_div + '<div class="tool-box">', 1)
    with open(p_mp3, "w", encoding="utf-8") as f:
        f.write(c)
    print("Injected banner into mp3-converter")

# percentage-calculator
p_pct = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360\converter\percentage-calculator\index.html"
with open(p_pct, "r", encoding="utf-8") as f:
    c = f.read()
if "tool-hero-banner" not in c:
    svg = get_landscape_banner("percentage-calculator")
    banner_div = f'<div class="tool-hero-banner" style="width: 180px; max-width: 100%; height: 76px; margin: 0 auto 1.4rem; background: rgba(15,23,42,0.6); border: 1px solid rgba(255,255,255,0.12); border-radius: 16px; display: flex; align-items: center; justify-content: center; padding: 2px; box-shadow: 0 8px 24px rgba(0,0,0,0.3); overflow: hidden;">{svg}</div>\n        '
    c = c.replace('<div class="calc-sections-grid">', banner_div + '<div class="calc-sections-grid">', 1)
    with open(p_pct, "w", encoding="utf-8") as f:
        f.write(c)
    print("Injected banner into percentage-calculator")
