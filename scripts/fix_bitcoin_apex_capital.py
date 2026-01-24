
import re
import os
import sys

def fix_markdown_formatting(file_path):
    # Read the entire content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # --- Heading Replacements ---
    # Ensure blank lines around main headings (level 1)
    content = re.sub(r'(\n|^)([IVX]+\. [^\n:]+):([^\n]*)', r'\n# \2:\3\n\n', content, flags=re.MULTILINE)
    content = re.sub(r'(\n|^)([IVX]+\. [^\n:]+)([^\n]*)', r'\n# \2\3\n\n', content, flags=re.MULTILINE)

    # Ensure blank lines around sub-headings (level 2)
    content = re.sub(r'(\n|^)(\d+\.\d+ [^\n]+)', r'\n## \2\n\n', content, flags=re.MULTILINE)

    # Clean up multiple blank lines introduced by previous replacements
    content = re.sub(r'\n\s*\n+', r'\n\n', content)

    # --- KaTeX and Dollar Sign Fixes ---
    # Replace '$' with 'USD' or 'dollars' if not part of a math environment
    # This is a simplified approach, a more robust solution would require parsing Markdown.
    # For now, let's target specific instances based on context if identifiable.
    # Given the context, we will replace '$' signs that are clearly currency and not math.
    # Example: If '$50,000' appears, it becomes 'USD50,000' or '50,000 dollars'
    content = re.sub(r'\$(\d[\d,\.]*)', r'USD\1', content) # Replaces $1,000,000 with USD1,000,000

    # Replace '&' with 'and' if not part of a math environment or HTML entity
    # This is also a simplification. Assuming non-math '&' are meant as 'and'.
    content = re.sub(r'(\s)&\s', r'\1and ', content)


    # --- "Truncated" line fix ---
    # Remove "Truncated" and adjust surrounding text for flow
    # This pattern looks for "Truncated" followed by "]" and potentially some whitespace
    content = re.sub(r'\[truncated\]\s*', '', content, flags=re.IGNORECASE)


    # --- Table 1 Formatting (using original content as reference for replacement boundary) ---
    # Manually constructed markdown for Table 1 (using raw string literal)
    markdown_table_1 = r"""### Table 1: Comparative Scarcity Physics

| Feature | Gold | Bitcoin |
| :---- | :---- | :---- |
| **Total Supply Cap** | None (Geological Estimate) | 21,000,000 (Hard Coded) |
| **Supply Curve** | Elastic (Price up = Supply up) | Perfectly Inelastic (Vertical) |
| **Inflation Rate** | ~1.5 - 2.0% Annually | Programmatic Halving (Deflationary) |
| **Issuance Mechanism** | Mining & Refining | Algorithm (nSubsidy) |
| **Cost to Verify Supply** | Millions (Global Audit impossible) | ~$0 (Run a Node) |
| **Dilution Risk** | High (Paper Gold / Derivatives) | Zero (On-Chain) |
"""
    # Find the old table 1 content and replace it
    table_1_search_pattern = re.compile(
        r'### Table 1: Comparative Scarcity Physics.*?\| Dilution Risk \|\s*High \(Paper Gold \/ Derivatives\)\s*\|\s*Zero \(On-Chain\)\s*\|', re.DOTALL
    )
    content = table_1_search_pattern.sub(lambda match: markdown_table_1, content)


    # --- Table 2 Formatting (using original content as reference for replacement boundary) ---
    # Manually constructed markdown for Table 2 (using raw string literal)
    markdown_table_2 = r"""### Table 2: The Voltage Regulation Analogy

| Electrical Component | Financial Equivalent | Function |
| :---- | :---- | :---- |
| **Input Source (Mains)** | Bitcoin (Spot Asset) | Provides raw, high-energy value. Volatile. |
| **Transformer (Inductor)** | Treasury / Balance Sheet | Stores the value. |
| **Switch / Regulator** | Convertible Bond / Futures Short | "Strips" the volatility. Manages risk. |
| **Output (DC)** | Stable Credit / Fiat Loan | Consistent purchasing power for commerce. |
| **Waste Heat** | Equity Volatility / Leverage | Excess returns absorbed by speculators. |
"""

    # Find the old table 2 content and replace it
    table_2_search_pattern = re.compile(
        r'### Table 2: The Voltage Regulation Analogy.*?\| Waste Heat \|\s*Equity Volatility \/ Leverage\s*\|\s*Excess returns absorbed by speculators\.\s*\|', re.DOTALL
    )
    content = table_2_search_pattern.sub(lambda match: markdown_table_2, content)


    # --- Works Cited / References Formatting ---
    # Format the "Works cited" section as a numbered list with blank lines
    works_cited_start_pattern = r"#### \*\*Works cited\*\*"
    works_cited_start_match = re.search(works_cited_start_pattern, content)

    if works_cited_start_match:
        before_works_cited = content[:works_cited_start_match.start()]
        works_cited_raw = content[works_cited_start_match.end():]

        # Split by citation number and re-attach numbers
        parts = re.split(r'(\d+\.\s+)', works_cited_raw)
        reconstructed_citations = []
        # The first part might be empty if the split happens at the very beginning
        start_idx = 1 if parts[0].strip() == "" else 0

        current_citation_number = 1
        for i in range(start_idx, len(parts), 2):
            if i + 1 < len(parts):
                citation_text = parts[i+1].strip()
                # Remove backslashes from URLs
                citation_text = re.sub(r'\\([_.-])', r'\1', citation_text)
                reconstructed_citations.append(f"{current_citation_number}. {citation_text}")
                current_citation_number += 1
            elif parts[i].strip(): # Handle the last part if it exists and wasn't part of a pair
                citation_text = parts[i].strip()
                citation_text = re.sub(r'\\([_.-])', r'\1', citation_text)
                reconstructed_citations.append(f"{current_citation_number}. {citation_text}")
                current_citation_number += 1

        works_cited_formatted = "\n\n".join(reconstructed_citations)
        new_content_with_works_cited = before_works_cited + "\n\n#### **Works cited**\n\n" + works_cited_formatted.strip()
        content = new_content_with_works_cited


    # Final cleanup of multiple blank lines
    content = re.sub(r'\n\s*\n+', r'\n\n', content)

    # Write the modified content back to the file only if it has changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"File {file_path} modified successfully.")
    else:
        print(f"No changes were made to {file_path}.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_bitcoin_apex_capital.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    fix_markdown_formatting(file_path)
