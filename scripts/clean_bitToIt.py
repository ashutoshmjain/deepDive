import re

def clean_works_cited(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove [^n] from inside footnote definitions
    # Match [^n]: ... [^m] ...
    lines = content.split('\n')
    new_lines = []
    in_works_cited = False
    for line in lines:
        if "#### **Works cited**" in line:
            in_works_cited = True
            new_lines.append(line)
            continue
        if in_works_cited:
            # If line starts with [^n]:
            if line.startswith('[^'):
                # Remove any OTHER [^m] from this line
                # But keep the starting one!
                parts = line.split(':', 1)
                if len(parts) > 1:
                    prefix = parts[0] + ':'
                    rest = parts[1]
                    rest = re.sub(r'\[\^\d+\]', '', rest)
                    new_lines.append(prefix + rest)
                    continue
        new_lines.append(line)
    
    content = '\n'.join(new_lines)

    # 2. Add spaces between adjacent footnotes in text
    content = content.replace('][^', '] [^')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Cleaned up {file_path}")

clean_works_cited("src/bitToIt.md")
