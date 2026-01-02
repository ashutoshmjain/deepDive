import re

def format_citations_as_links_very_carefully(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    works_cited_heading = "#### Works cited"
    if works_cited_heading not in content:
        print("'Works cited' section not found.")
        return

    before_works_cited, works_cited_section = content.split(works_cited_heading, 1)
    
    # Process the raw text of the works cited section
    # Replace multiple newlines with a single one to start, to handle odd spacing
    raw_text = works_cited_section.strip()
    
    # Split into entries based on the numbering. This is a key heuristic.
    # We assume each new citation starts with a number followed by a dot.
    # The lookahead `(?=\d+\.)` ensures we don't consume the delimiter.
    entries = re.split(r'\n(?=\d+\.)', raw_text)
    
    formatted_links = []
    for entry in entries:
        if not entry.strip():
            continue
            
        # Clean up the entry by removing newlines and extra whitespace
        single_line_entry = re.sub(r'\s+', ' ', entry.strip())
        
        # Match the number, title, and URL
        match = re.match(r'(\d+)\.\s+(.*?)(https?://.*)', single_line_entry)
        
        if match:
            number = match.group(1)
            title = match.group(2).strip()
            url = match.group(3).strip()

            # Clean up title
            if title.endswith(','):
                title = title[:-1]
            
            formatted_links.append(f"{number}. [{title}]({url})")
        else:
            # Fallback for entries that don't match the expected pattern
            formatted_links.append(single_line_entry)

    # Reconstruct the file content
    new_content = before_works_cited + works_cited_heading + "\n\n" + "\n\n".join(formatted_links)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Final attempt to format 'Works cited' section has completed.")

format_citations_as_links_very_carefully('src/GlobalStrategicRetrospective2025.md')
