import re
import os

def fix_markdown_formatting(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    original_content = content

    # --- Heading Replacements ---
    # Remove bolding from main headings and ensure single newline
    content = re.sub(r'# \*\*(.*?)\*\*', r'# \1', content)
    # Ensure blank lines around main headings (level 1)
    content = re.sub(r'(\n|^)([IVX]+\. [^\n:]+):([^\n]*)', r'\n# \2:\3\n\n', content, flags=re.MULTILINE)
    content = re.sub(r'(\n|^)([IVX]+\. [^\n:]+)([^\n]*)', r'\n# \2\3\n\n', content, flags=re.MULTILINE)

    # Ensure blank lines around sub-headings (level 2)
    content = re.sub(r'(\n|^)(\d+\.\d+ [^\n]+)', r'\n## \2\n\n', content, flags=re.MULTILINE)
    
    # Remove "## ---" lines
    content = content.replace("## ---", "")

    # --- Dollar Sign Replacements (excluding URLs) ---
    # Function to replace dollar amounts outside URLs
    def replace_dollars_outside_urls(match):
        text = match.group(0)
        # Check if the match is inside a URL (heuristic: starts with http or https)
        if re.search(r'https?://', text):
            return text
        
        # Original dollar replacement logic
        text = re.sub(r'\$(\d+(\.\d+)?)\s*billion', r'USD \1 billion', text)
        text = re.sub(r'\$(\d+(\.\d+)?)\s*million', r'USD \1 million', text)
        text = re.sub(r'\$(\d+)', r'USD \1', text)
        return text

    # Use a negative lookbehind assertion to avoid matching '$' within a URL
    # This is a complex regex, so I'll try to refine it by splitting the content
    # and processing parts outside URLs. A simpler approach is to process URLs first,
    # then the rest.

    # Temporarily hide URLs to prevent dollar sign replacement within them
    url_pattern = re.compile(r'(https?://[^\s\]\)]+)', re.IGNORECASE)
    urls_found = {}
    
    def hide_url(match):
        url_id = f"__URL_PLACEHOLDER_{len(urls_found)}__"
        urls_found[url_id] = match.group(0)
        return url_id
    
    content_with_hidden_urls = url_pattern.sub(hide_url, content)

    # Replace dollar amounts in the remaining content
    content_with_hidden_urls = re.sub(r'\$(\d+(\.\d+)?)\s*billion', r'USD \1 billion', content_with_hidden_urls)
    content_with_hidden_urls = re.sub(r'\$(\d+(\.\d+)?)\s*million', r'USD \1 million', content_with_hidden_urls)
    content_with_hidden_urls = re.sub(r'\$(\d+)', r'USD \1', content_with_hidden_urls)

    # Restore URLs
    for url_id, url in urls_found.items():
        content_with_hidden_urls = content_with_hidden_urls.replace(url_id, url)
    content = content_with_hidden_urls


    # Clean up multiple blank lines introduced by previous replacements
    content = re.sub(r'\n\s*\n+', r'\n\n', content)


    # --- Works Cited Formatting ---
    works_cited_start_pattern = re.compile(r"#### \*\*Works cited\*\*")
    works_cited_start_match = works_cited_start_pattern.search(content)

    if works_cited_start_match:
        before_works_cited = content[:works_cited_start_match.end()]
        works_cited_raw = content[works_cited_start_match.end():]

        # Split by citation number and re-attach numbers
        parts = re.split(r'(\d+\.\s+)', works_cited_raw)
        reconstructed_citations = []
        start_idx = 1 if parts[0].strip() == "" else 0

        for i in range(start_idx, len(parts), 2):
            if i + 1 < len(parts):
                citation_entry = parts[i] + parts[i+1].strip()
                reconstructed_citations.append(citation_entry)
            elif parts[i].strip():
                    reconstructed_citations.append(parts[i].strip())

        works_cited_formatted = "\n\n".join(reconstructed_citations)
        new_content = before_works_cited + "\n\n" + works_cited_formatted.strip()
        content = new_content

    # Final cleanup of multiple blank lines
    content = re.sub(r'\n\s*\n+', r'\n\n', content)

    # Write the modified content back to the file only if it has changed
    if content != original_content:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"File {file_path} modified successfully.")
    else:
        print(f"No changes were made to {file_path}.")

fix_markdown_formatting("src/the-great-fragmentation.md")
