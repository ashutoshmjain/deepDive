with open("src/SUMMARY.md", "r") as f:
    lines = f.readlines()

seen = set()
unique_lines = []
for line in lines:
    link_match = None
    if "(" in line and ")" in line:
        link = line.split("(")[1].split(")")[0]
        if link in seen:
            continue
        seen.add(link)
    unique_lines.append(line)

with open("src/SUMMARY.md", "w") as f:
    f.writelines(unique_lines)
