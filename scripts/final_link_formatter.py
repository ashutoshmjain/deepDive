import re

def format_citations_as_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    works_cited_heading = "#### Works cited"
    if works_cited_heading not in content:
        print("'Works cited' section not found.")
        return

    # Isolate the content before and after the "Works cited" heading
    before_works_cited, works_cited_section = content.split(works_cited_heading, 1)
    works_cited_section = works_cited_section.strip()

    # Use a regex to find all citations, which might span multiple lines.
    # This pattern looks for a number followed by a period, then captures everything until the next numbered citation.
    citations = re.split(r'\n(?=\d+\.)', works_cited_section)
    
    formatted_links = []
    # Keep track of the correct citation number
    citation_counter = 1 

    for citation_text in citations:
        if not citation_text.strip():
            continue

        # Remove the original number and any leading whitespace
        cleaned_text = re.sub(r'^\d+\.\s*', '', citation_text.strip()).strip()

        # Remove newlines and extra spaces to merge broken lines
        single_line_text = re.sub(r'\s+', ' ', cleaned_text)

        # Find the last occurrence of http to correctly identify the start of the URL
        url_start_index = single_line_text.rfind('http')
        if url_start_index == -1:
            # If no URL, just add the text back (and maybe log it)
            formatted_links.append(f"{citation_counter}. {single_line_text}")
            citation_counter += 1
            continue

        # Separate title and URL
        title = single_line_text[:url_start_index].strip()
        url = single_line_text[url_start_index:].strip()

        # Clean up the title (e.g., remove trailing comma)
        if title.endswith(','):
            title = title[:-1]

        # Format as markdown link
        formatted_links.append(f"{citation_counter}. [{title}]({url})")
        citation_counter += 1

    # Reconstruct the file content
    new_content = before_works_cited + works_cited_heading + "\n\n" + "\n\n".join(formatted_links)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Successfully formatted 'Works cited' section with markdown links.")

format_citations_as_links('src/GlobalStrategicRetrospective2025.md')
