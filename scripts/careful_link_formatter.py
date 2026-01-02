import re

def format_citations_as_links_carefully(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    works_cited_heading = "#### Works cited"
    if works_cited_heading not in content:
        print("'Works cited' section not found.")
        return

    before_works_cited, works_cited_section = content.split(works_cited_heading, 1)
    
    # Start with a clean slate for the "Works cited" content
    lines = works_cited_section.strip().split('\n')
    
    merged_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # If a line does not start with a number, merge it with the previous line.
        if re.match(r'^\d+\.', line) or not merged_lines:
            merged_lines.append(line)
        else:
            merged_lines[-1] += line

    formatted_links = []
    for i, line in enumerate(merged_lines, 1):
        # Remove the original numbering to avoid confusion
        text_without_number = re.sub(r'^\d+\.\s*', '', line).strip()
        
        # Find the URL
        url_match = re.search(r'https?://[^\s]+', text_without_number)
        
        if url_match:
            url = url_match.group(0)
            # The title is everything before the URL
            title = text_without_number[:url_match.start()].strip()
            
            # Clean up title
            if title.endswith(','):
                title = title[:-1]
            
            # Format as markdown link with new, correct numbering
            formatted_links.append(f"{i}. [{title}]({url})")
        else:
            # If for some reason no URL is found, keep the original line with new numbering
            formatted_links.append(f"{i}. {text_without_number}")

    # Reconstruct the file content
    new_content = before_works_cited + works_cited_heading + "\n\n" + "\n\n".join(formatted_links)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Successfully and carefully formatted 'Works cited' section with markdown links.")

format_citations_as_links_carefully('src/GlobalStrategicRetrospective2025.md')
