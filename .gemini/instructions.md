## Fix Markdown Instructions

When the user says 'fix markdown', the automation flow is:

1.  Fix the markdown syntax (headings, tables, etc.).
2.  Check and fix KaTeX and math-related rendering issues. This includes:
    *   Escaping all dollar signs (\$) that are not used as math delimiters. Any \$ intended to represent currency or other non-math meanings must be escaped as \\\$ to prevent the KaTeX renderer from misinterpreting it.
    *   Ensuring all math blocks (both inline `$...$` and block `$$...$$`) are properly opened and closed.
    *   Avoiding the use of KaTeX for styling currency. Use standard markdown for formatting currency amounts (e.g., `**$1,000**`).
3.  Check for and fix "Truncated" lines, and improve the readability of the surrounding text.
4.  Check and fix citations and footnotes. This includes:
    *   Ensuring all footnotes are numbered sequentially.
    *   Ensuring every footnote defined in the reference list is used in the text, and that there are no unreferenced footnotes.
5.  Identify all data points and claims in the paper, find references for them through a quick web search, and add them to a "References" section at the end of the document.
6.  Do a final check for readability and break the text into more paragraphs if needed.
7.  Add a catchy five-word title to `SUMMARY.md` and a link to the modified file.
