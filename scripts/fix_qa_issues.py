import os
import re

base_dir = r"c:\Users\Ali Raza Bhatti\Desktop\AuraToolKit 360"

# 1. Fix broken localized cover-letter-maker links
fixed_links = 0
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith(".html"):
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8") as fp:
                c = fp.read()
            
            # replace /ar/cover-letter-maker/ -> /cover-letter-maker/ etc.
            new_c = re.sub(r'href=["\']/(ar|de|es|fr|pt)/cover-letter-maker/?["\']', 'href="/cover-letter-maker/"', c)
            if new_c != c:
                with open(p, "w", encoding="utf-8") as fp:
                    fp.write(new_c)
                print(f"Fixed localized cover-letter link in: {os.path.relpath(p, base_dir)}")
                fixed_links += 1

print(f"Total files updated for localized links: {fixed_links}")

# 2. Fix [Your Name] placeholder in how-to-write-ats-cover-letter-step-by-step
blog_files = [
    os.path.join(base_dir, "blogs", "how-to-write-ats-cover-letter-step-by-step", "index.html"),
    os.path.join(base_dir, "templates", "blog", "how-to-write-ats-cover-letter-step-by-step.html")
]

for bf in blog_files:
    if os.path.exists(bf):
        with open(bf, "r", encoding="utf-8") as fp:
            c = fp.read()
        
        c_fixed = c.replace("[Your Name]", "Alex Morgan\nalex.morgan@email.com | (555) 019-2834")
        if c_fixed != c:
            with open(bf, "w", encoding="utf-8") as fp:
                fp.write(c_fixed)
            print(f"Fixed placeholder in: {os.path.relpath(bf, base_dir)}")

