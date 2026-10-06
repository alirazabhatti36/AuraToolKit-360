import os
import re

base_dir = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360"

TOOL_SUGGESTIONS = {
    "resume-score-checker/index.html": """
        <!-- Related Tools Section -->
        <div class="info-card" style="margin-top: 2.5rem; max-width: 1200px; margin-left: auto; margin-right: auto; padding: 2rem; background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 20px;">
            <h2 style="font-size: 1.45rem; font-weight: 800; color: #38bdf8; margin-bottom: 1.2rem; border-left: 4px solid #38bdf8; padding-left: 0.75rem;">Explore Related Career &amp; HR Tools</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-top: 1.2rem;">
                <a href="/resume-cv-maker/" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1.2rem; text-decoration: none; color: #f8fafc; text-align: center; display: block; transition: all 0.25s;" onmouseover="this.style.borderColor='#38bdf8'; this.style.transform='translateY(-3px)'" onmouseout="this.style.borderColor='rgba(255, 255, 255, 0.08)'; this.style.transform='none'">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">📝</div>
                    <h4 style="font-size: 0.98rem; font-weight: 700; margin-bottom: 0.35rem; color: #fff;">ATS Resume Builder</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.45; margin: 0;">Create single-page ATS-formatted CVs</p>
                </a>
                <a href="/cover-letter-maker/" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1.2rem; text-decoration: none; color: #f8fafc; text-align: center; display: block; transition: all 0.25s;" onmouseover="this.style.borderColor='#38bdf8'; this.style.transform='translateY(-3px)'" onmouseout="this.style.borderColor='rgba(255, 255, 255, 0.08)'; this.style.transform='none'">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">✉️</div>
                    <h4 style="font-size: 0.98rem; font-weight: 700; margin-bottom: 0.35rem; color: #fff;">Cover Letter Maker</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.45; margin: 0;">Generate targeted job cover letters</p>
                </a>
                <a href="/converter/pdf-to-word/" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1.2rem; text-decoration: none; color: #f8fafc; text-align: center; display: block; transition: all 0.25s;" onmouseover="this.style.borderColor='#38bdf8'; this.style.transform='translateY(-3px)'" onmouseout="this.style.borderColor='rgba(255, 255, 255, 0.08)'; this.style.transform='none'">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">📕➔📝</div>
                    <h4 style="font-size: 0.98rem; font-weight: 700; margin-bottom: 0.35rem; color: #fff;">PDF to Word</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.45; margin: 0;">Reconstruct editable DOCX from PDF</p>
                </a>
                <a href="/hr-helper/" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1.2rem; text-decoration: none; color: #f8fafc; text-align: center; display: block; transition: all 0.25s;" onmouseover="this.style.borderColor='#38bdf8'; this.style.transform='translateY(-3px)'" onmouseout="this.style.borderColor='rgba(255, 255, 255, 0.08)'; this.style.transform='none'">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">👥</div>
                    <h4 style="font-size: 0.98rem; font-weight: 700; margin-bottom: 0.35rem; color: #fff;">HR Bulk Screener</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.45; margin: 0;">Screen 100+ candidates in minutes</p>
                </a>
            </div>
        </div>
    """,
    "hr-helper/index.html": """
        <!-- Related Tools Section -->
        <div class="info-card" style="margin-top: 2.5rem; max-width: 1200px; margin-left: auto; margin-right: auto; padding: 2rem; background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 20px;">
            <h2 style="font-size: 1.45rem; font-weight: 800; color: #38bdf8; margin-bottom: 1.2rem; border-left: 4px solid #38bdf8; padding-left: 0.75rem;">Explore Related HR &amp; Career Tools</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-top: 1.2rem;">
                <a href="/resume-score-checker/" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1.2rem; text-decoration: none; color: #f8fafc; text-align: center; display: block; transition: all 0.25s;" onmouseover="this.style.borderColor='#38bdf8'; this.style.transform='translateY(-3px)'" onmouseout="this.style.borderColor='rgba(255, 255, 255, 0.08)'; this.style.transform='none'">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
                    <h4 style="font-size: 0.98rem; font-weight: 700; margin-bottom: 0.35rem; color: #fff;">ATS Score Checker</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.45; margin: 0;">Scan candidate CVs against job criteria</p>
                </a>
                <a href="/resume-cv-maker/" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1.2rem; text-decoration: none; color: #f8fafc; text-align: center; display: block; transition: all 0.25s;" onmouseover="this.style.borderColor='#38bdf8'; this.style.transform='translateY(-3px)'" onmouseout="this.style.borderColor='rgba(255, 255, 255, 0.08)'; this.style.transform='none'">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">📝</div>
                    <h4 style="font-size: 0.98rem; font-weight: 700; margin-bottom: 0.35rem; color: #fff;">ATS Resume Builder</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.45; margin: 0;">Create 100% compliant resume templates</p>
                </a>
                <a href="/saas/" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1.2rem; text-decoration: none; color: #f8fafc; text-align: center; display: block; transition: all 0.25s;" onmouseover="this.style.borderColor='#38bdf8'; this.style.transform='translateY(-3px)'" onmouseout="this.style.borderColor='rgba(255, 255, 255, 0.08)'; this.style.transform='none'">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚡🏢</div>
                    <h4 style="font-size: 0.98rem; font-weight: 700; margin-bottom: 0.35rem; color: #fff;">AuraHR 360 Enterprise</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.45; margin: 0;">Local HR, payroll &amp; attendance portal</p>
                </a>
                <a href="/converter/pdf-to-word/" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1.2rem; text-decoration: none; color: #f8fafc; text-align: center; display: block; transition: all 0.25s;" onmouseover="this.style.borderColor='#38bdf8'; this.style.transform='translateY(-3px)'" onmouseout="this.style.borderColor='rgba(255, 255, 255, 0.08)'; this.style.transform='none'">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">📕➔📝</div>
                    <h4 style="font-size: 0.98rem; font-weight: 700; margin-bottom: 0.35rem; color: #fff;">PDF to Word</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.45; margin: 0;">Convert resumes from PDF to Word</p>
                </a>
            </div>
        </div>
    """,
    "paraphrasing-tool/index.html": """
        <!-- Related Tools Section -->
        <div class="info-card" style="margin-top: 2.5rem; max-width: 1200px; margin-left: auto; margin-right: auto; padding: 2rem; background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 20px;">
            <h2 style="font-size: 1.45rem; font-weight: 800; color: #38bdf8; margin-bottom: 1.2rem; border-left: 4px solid #38bdf8; padding-left: 0.75rem;">Explore Related Writing &amp; Document Tools</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-top: 1.2rem;">
                <a href="/converter/word-counter/" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1.2rem; text-decoration: none; color: #f8fafc; text-align: center; display: block; transition: all 0.25s;" onmouseover="this.style.borderColor='#38bdf8'; this.style.transform='translateY(-3px)'" onmouseout="this.style.borderColor='rgba(255, 255, 255, 0.08)'; this.style.transform='none'">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔤</div>
                    <h4 style="font-size: 0.98rem; font-weight: 700; margin-bottom: 0.35rem; color: #fff;">Word Counter</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.45; margin: 0;">Count words, characters &amp; reading time</p>
                </a>
                <a href="/cover-letter-maker/" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1.2rem; text-decoration: none; color: #f8fafc; text-align: center; display: block; transition: all 0.25s;" onmouseover="this.style.borderColor='#38bdf8'; this.style.transform='translateY(-3px)'" onmouseout="this.style.borderColor='rgba(255, 255, 255, 0.08)'; this.style.transform='none'">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">✉️</div>
                    <h4 style="font-size: 0.98rem; font-weight: 700; margin-bottom: 0.35rem; color: #fff;">Cover Letter Maker</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.45; margin: 0;">Create targeted ATS job letters</p>
                </a>
                <a href="/converter/case-converter/" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1.2rem; text-decoration: none; color: #f8fafc; text-align: center; display: block; transition: all 0.25s;" onmouseover="this.style.borderColor='#38bdf8'; this.style.transform='translateY(-3px)'" onmouseout="this.style.borderColor='rgba(255, 255, 255, 0.08)'; this.style.transform='none'">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔠</div>
                    <h4 style="font-size: 0.98rem; font-weight: 700; margin-bottom: 0.35rem; color: #fff;">Case Converter</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.45; margin: 0;">Transform text case styles instantly</p>
                </a>
                <a href="/converter/word-to-pdf/" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1.2rem; text-decoration: none; color: #f8fafc; text-align: center; display: block; transition: all 0.25s;" onmouseover="this.style.borderColor='#38bdf8'; this.style.transform='translateY(-3px)'" onmouseout="this.style.borderColor='rgba(255, 255, 255, 0.08)'; this.style.transform='none'">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">📝➔📕</div>
                    <h4 style="font-size: 0.98rem; font-weight: 700; margin-bottom: 0.35rem; color: #fff;">Word to PDF</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.45; margin: 0;">Convert Word docs to clean PDF</p>
                </a>
            </div>
        </div>
    """,
    "resume-cv-maker/index.html": """
        <!-- Related Tools Section -->
        <div class="info-card" style="margin-top: 2.5rem; max-width: 1200px; margin-left: auto; margin-right: auto; padding: 2rem; background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 20px;">
            <h2 style="font-size: 1.45rem; font-weight: 800; color: #38bdf8; margin-bottom: 1.2rem; border-left: 4px solid #38bdf8; padding-left: 0.75rem;">Explore Related Career &amp; Writing Tools</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-top: 1.2rem;">
                <a href="/resume-score-checker/" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1.2rem; text-decoration: none; color: #f8fafc; text-align: center; display: block; transition: all 0.25s;" onmouseover="this.style.borderColor='#38bdf8'; this.style.transform='translateY(-3px)'" onmouseout="this.style.borderColor='rgba(255, 255, 255, 0.08)'; this.style.transform='none'">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
                    <h4 style="font-size: 0.98rem; font-weight: 700; margin-bottom: 0.35rem; color: #fff;">ATS Score Checker</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.45; margin: 0;">Scan CV against ATS parsers &amp; keywords</p>
                </a>
                <a href="/cover-letter-maker/" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1.2rem; text-decoration: none; color: #f8fafc; text-align: center; display: block; transition: all 0.25s;" onmouseover="this.style.borderColor='#38bdf8'; this.style.transform='translateY(-3px)'" onmouseout="this.style.borderColor='rgba(255, 255, 255, 0.08)'; this.style.transform='none'">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">✉️</div>
                    <h4 style="font-size: 0.98rem; font-weight: 700; margin-bottom: 0.35rem; color: #fff;">Cover Letter Maker</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.45; margin: 0;">Create matching ATS cover letters</p>
                </a>
                <a href="/paraphrasing-tool/" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1.2rem; text-decoration: none; color: #f8fafc; text-align: center; display: block; transition: all 0.25s;" onmouseover="this.style.borderColor='#38bdf8'; this.style.transform='translateY(-3px)'" onmouseout="this.style.borderColor='rgba(255, 255, 255, 0.08)'; this.style.transform='none'">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">✍️</div>
                    <h4 style="font-size: 0.98rem; font-weight: 700; margin-bottom: 0.35rem; color: #fff;">Paraphrasing Tool</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.45; margin: 0;">Polish bullet points with strong action verbs</p>
                </a>
                <a href="/converter/pdf-to-word/" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1.2rem; text-decoration: none; color: #f8fafc; text-align: center; display: block; transition: all 0.25s;" onmouseover="this.style.borderColor='#38bdf8'; this.style.transform='translateY(-3px)'" onmouseout="this.style.borderColor='rgba(255, 255, 255, 0.08)'; this.style.transform='none'">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">📕➔📝</div>
                    <h4 style="font-size: 0.98rem; font-weight: 700; margin-bottom: 0.35rem; color: #fff;">PDF to Word</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.45; margin: 0;">Convert resumes from PDF to DOCX</p>
                </a>
            </div>
        </div>
    """,
    "cover-letter-maker/index.html": """
        <!-- Related Tools Section -->
        <div class="info-card" style="margin-top: 2.5rem; max-width: 1200px; margin-left: auto; margin-right: auto; padding: 2rem; background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 20px;">
            <h2 style="font-size: 1.45rem; font-weight: 800; color: #38bdf8; margin-bottom: 1.2rem; border-left: 4px solid #38bdf8; padding-left: 0.75rem;">Explore Related Career &amp; Writing Tools</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-top: 1.2rem;">
                <a href="/resume-cv-maker/" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1.2rem; text-decoration: none; color: #f8fafc; text-align: center; display: block; transition: all 0.25s;" onmouseover="this.style.borderColor='#38bdf8'; this.style.transform='translateY(-3px)'" onmouseout="this.style.borderColor='rgba(255, 255, 255, 0.08)'; this.style.transform='none'">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">📝</div>
                    <h4 style="font-size: 0.98rem; font-weight: 700; margin-bottom: 0.35rem; color: #fff;">ATS Resume Builder</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.45; margin: 0;">Build ATS-compliant resumes fast</p>
                </a>
                <a href="/resume-score-checker/" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1.2rem; text-decoration: none; color: #f8fafc; text-align: center; display: block; transition: all 0.25s;" onmouseover="this.style.borderColor='#38bdf8'; this.style.transform='translateY(-3px)'" onmouseout="this.style.borderColor='rgba(255, 255, 255, 0.08)'; this.style.transform='none'">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
                    <h4 style="font-size: 0.98rem; font-weight: 700; margin-bottom: 0.35rem; color: #fff;">ATS Score Checker</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.45; margin: 0;">Scan resumes against job descriptions</p>
                </a>
                <a href="/paraphrasing-tool/" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1.2rem; text-decoration: none; color: #f8fafc; text-align: center; display: block; transition: all 0.25s;" onmouseover="this.style.borderColor='#38bdf8'; this.style.transform='translateY(-3px)'" onmouseout="this.style.borderColor='rgba(255, 255, 255, 0.08)'; this.style.transform='none'">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">✍️</div>
                    <h4 style="font-size: 0.98rem; font-weight: 700; margin-bottom: 0.35rem; color: #fff;">Paraphrasing Tool</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.45; margin: 0;">Enhance tone &amp; rephrase sentences</p>
                </a>
                <a href="/converter/word-counter/" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1.2rem; text-decoration: none; color: #f8fafc; text-align: center; display: block; transition: all 0.25s;" onmouseover="this.style.borderColor='#38bdf8'; this.style.transform='translateY(-3px)'" onmouseout="this.style.borderColor='rgba(255, 255, 255, 0.08)'; this.style.transform='none'">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔤</div>
                    <h4 style="font-size: 0.98rem; font-weight: 700; margin-bottom: 0.35rem; color: #fff;">Word Counter</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; line-height: 1.45; margin: 0;">Check character &amp; paragraph count</p>
                </a>
            </div>
        </div>
    """
}

for rel_path, snippet in TOOL_SUGGESTIONS.items():
    p = os.path.join(base_dir, rel_path.replace("/", os.sep))
    if not os.path.exists(p):
        continue
    with open(p, "r", encoding="utf-8") as f:
        c = f.read()
    
    if "Explore Related" in c or "related-grid" in c:
        continue
    
    if "<footer" in c:
        c = c.replace("<footer", snippet.strip() + "\n\n    <footer", 1)
        with open(p, "w", encoding="utf-8") as f:
            f.write(c)
        print(f"Injected suggestions into {rel_path}")

print("Done injecting suggestions into primary tools.")
