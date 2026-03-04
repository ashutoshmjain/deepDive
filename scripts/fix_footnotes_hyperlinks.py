import re
import sys

def fix_footnotes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Identify sections
    works_cited_start_pattern = r"#### \*\*Works cited\*\*"
    works_cited_match = re.search(works_cited_start_pattern, content)
    if not works_cited_match: return

    # Identify image definitions start
    image_start_pattern = r'\[image1\]:'
    image_match = re.search(image_start_pattern, content)
    
    if image_match:
        works_cited_raw = content[works_cited_match.end():image_match.start()]
        images_content = content[image_match.start():]
    else:
        works_cited_raw = content[works_cited_match.end():]
        images_content = ""

    # 2. Extract citations
    citation_definitions = {}
    parts = re.split(r'(\n\d+\.\s+)', "\n" + works_cited_raw.strip())
    for i in range(1, len(parts), 2):
        num_match = re.search(r'(\d+)', parts[i])
        if num_match:
            num = num_match.group(1)
            citation_definitions[num] = parts[i+1].strip()

    # 3. Replace references in main text with [N](#N)
    main_text = content[:works_cited_match.start()]
    sorted_nums = sorted(citation_definitions.keys(), key=lambda x: int(x), reverse=True)
    
    # Protect images
    main_text = re.sub(r'\[image(\d+)\]', r'__IMAGE__\1__', main_text)
    
    # Simple replacement: look for "N" that's preceded by non-digit and not followed by digit
    for num in sorted_nums:
        # Match num if it's preceded by word/punctuation or space
        pattern = r'(?<=[a-zA-Z.,\)\]! ])' + re.escape(num) + r'(?!\d)'
        main_text = re.sub(pattern, f"[<sup>{num}</sup>](#{num})", main_text)
    
    # Restore images
    main_text = re.sub(r'__IMAGE__(\d+)__', r'[image\1]', main_text)

    # 4. Reconstruct "Works cited" with anchors
    new_works_cited = "#### **Works cited**\n\n"
    for num in sorted(citation_definitions.keys(), key=lambda x: int(x)):
        # Add an HTML anchor for the link to jump to
        new_works_cited += f"<a name=\"{num}\"></a>{num}. {citation_definitions[num]}\n\n"

    final_content = main_text.strip() + "\n\n" + new_works_cited.strip() + "\n\n" + images_content.strip()

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print(f"Footnotes in {file_path} hyperlinked using internal anchors.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        fix_footnotes(sys.argv[1])
