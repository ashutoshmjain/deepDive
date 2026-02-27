import re
import os

def fix_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix headings (remove bolding from headers, ensure blank lines)
    content = re.sub(r'^# \*\*([^\*]+)\*\*', r'# \1', content, flags=re.MULTILINE)
    content = re.sub(r'^## \*\*(\d+\\?\.\s*[^\*]+)\*\*', r'## \1', content, flags=re.MULTILINE)
    content = re.sub(r'^### \*\*([^\*]+)\*\*', r'### \1', content, flags=re.MULTILINE)
    
    # Ensure blank lines around headings
    content = re.sub(r'\n(#+ .*)', r'\n\n\1', content)
    content = re.sub(r'(#+ .*)\n([^\n])', r'\1\n\n\2', content)

    # 2. Fix KaTeX and Math related rendering issues
    # Handle the specific math/image line: ![][image1]\\pm 2%$
    content = content.replace(r'![][image1]\\pm 2%$)', r'![][image1] $\pm 2\%$)')
    
    # Replace currency $ with USD or escape
    # Pattern to find $ followed by numbers (like $68.1 billion, $200 threshold)
    content = re.sub(r'(?<!\\)\$(\d)', r'USD \1', content)
    
    # 3. Fix citations in text
    # Match: word.N or word N
    # Using a more careful pattern to avoid capturing prices or dates
    # word[12] or word. [12]
    content = re.sub(r'(\w)\.?(\d{1,2})(?=\s|$|\n)', r'\1 [\2]', content)

    # 4. Fix "Works cited" section
    # Should be a numbered list with blank lines
    works_cited_match = re.search(r'#### \*\*Works cited\*\*', content)
    if works_cited_match:
        before = content[:works_cited_match.start()]
        after = content[works_cited_match.end():]
        
        # Split references by number
        parts = re.split(r'(\d+\.\s+)', after)
        formatted_refs = ["# References\n"]
        for i in range(1, len(parts), 2):
            num = parts[i].strip()
            text = parts[i+1].strip()
            # Remove backslashes from URLs
            text = re.sub(r'\\([_.-])', r'\1', text)
            formatted_refs.append(f"{num} {text}\n")
        
        content = before + "\n".join(formatted_refs)

    # 5. Final cleanup of multiple blank lines
    content = re.sub(r'\n\s*\n+', r'\n\n', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    fix_markdown('src/mag7split.md')
