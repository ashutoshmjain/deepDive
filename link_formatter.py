import re

def create_markdown_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    works_cited_heading = "#### Works cited"
    if works_cited_heading not in content:
        print("'Works cited' section not found.")
        return

    before_works_cited, works_cited_raw = content.split(works_cited_heading, 1)
    works_cited_raw = works_cited_raw.strip()

    # Split into individual citation lines, more robustly
    citations = re.split(r'\n\s*\d+\.', works_cited_raw)
    # The first split item is often empty or just a newline
    if not citations[0].strip():
        citations.pop(0)

    # Re-add the numbers to the beginning of each citation
    numbered_citations = []
    for i, citation_text in enumerate(citations, 1):
        # Clean up each citation text
        citation_text = citation_text.strip()
        if citation_text:
            numbered_citations.append(f"{i}. {citation_text}")

    formatted_links = []
    for entry in numbered_citations:
        # First, remove any internal newlines to merge broken URLs
        entry = re.sub(r'\s*\n\s*', '', entry).strip()

        # Match the number, title, and URL
        match = re.match(r'(\d+)\.\s+(.*?),?\s+(https?://.*)', entry)
        if match:
            number = match.group(1)
            title = match.group(2).strip()
            url = match.group(3).strip()

            # Clean up trailing characters from title if they exist
            if title.endswith(','):
                title = title[:-1]

            # Format as a markdown link
            formatted_links.append(f"{number}. [{title}]({url})")
        else:
            # If regex fails, append the original entry to see what went wrong
            formatted_links.append(entry)
    
    # Rebuild the final content
    new_content = before_works_cited + works_cited_heading + "\n\n" + "\n\n".join(formatted_links)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Formatted 'Works cited' section with markdown links.")

create_markdown_links('src/GlobalStrategicRetrospective2025.md')
