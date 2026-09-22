with open('website/template/index-03.html', encoding='utf-8') as f:
    lines = f.readlines()

sections = []
for idx, line in enumerate(lines, 1):
    if any(k in line for k in ['id="home"', 'id="about"', 'id="service"', 'id="portfolio"', 'id="blog"', 'id="resume"', 'id="contacts"', '<footer']):
        sections.append((idx, line.strip()))

for s in sections:
    print(f"Line {s[0]}: {s[1]}")
