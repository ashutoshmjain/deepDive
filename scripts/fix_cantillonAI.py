import re
import os

file_path = "src/cantillonAI.md"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace $ used for currency
content = re.sub(r'\$(\d+)', r'\1 USD', content)

# Separate main text and works cited
parts = re.split(r'#### \*\*Works cited\*\*', content)
main_text = parts[0]
works_cited = parts[1] if len(parts) > 1 else ""

# Extract URLs mapped to original numbers
url_map = {}
for line in works_cited.split('\n'):
    match = re.match(r'^(\d+)\.\s+.*?(https?://\S+)', line)
    if match:
        num = match.group(1)
        url = match.group(2).rstrip(')')
        url_map[num] = url

# Define all inline citation patterns we saw and replace with new sequential markers
inline_citations = re.findall(r'([a-zA-Z\."]+)\.(\d+)(?=\s|$)', main_text)
# Also need to handle \n1\n type of standalone table citations
standalone_citations = re.findall(r'\n(\d+)\n', main_text)
# And special cases like 2030\.2 -> 2030.2
main_text = main_text.replace(r'2030\.2', '2030.[^2]')

seq_num = 1
new_refs = []
seen_urls = {}
replacement_map = {} # original_num -> new_seq_num

def get_new_seq(orig_num):
    global seq_num
    url = url_map.get(str(orig_num), "")
    if not url: return None
    if url not in seen_urls:
        seen_urls[url] = seq_num
        new_refs.append((seq_num, url))
        seq_num += 1
    return seen_urls[url]

# Manual replacements for safety
replacements = [
    ("advisors.1", "advisors.[^1]"),
    ("chat box.1", "chat box.[^1]"),
    ("keyboard.4", "keyboard.[^4]"),
    ("reports.1", "reports.[^1]"),
    ("enterprise use.7", "enterprise use.[^7]"),
    ("tools and data.7", "tools and data.[^7]"),
    ("\n1\n", "\n[^1]\n"),
    ("scheduled tasks.6", "scheduled tasks.[^6]"),
    ("single session.6", "single session.[^6]"),
    ("autonomously.9", "autonomously.[^9]"),
    ("accordingly.10", "accordingly.[^10]"),
    ("recall.12", "recall.[^12]"),
    ("\n10\n", "\n[^10]\n"),
    ("productivity.3", "productivity.[^3]"),
    ("complexity.9", "complexity.[^9]"),
    ("strategy.14", "strategy.[^14]"),
    ("network.10", "network.[^10]"),
    ("proxy.11", "proxy.[^11]"),
    ("employee.1", "employee.[^1]"),
    ("another.15", "another.[^15]"),
    ("judgment.17", "judgment.[^17]"),
    ("needed.18", "needed.[^18]"),
    ("arise.18", "arise.[^18]"),
    ("independently.2", "independently.[^2]"),
    ("\n17\n", "\n[^17]\n"),
    ("integrations.5", "integrations.[^5]"),
    ("coordination.16", "coordination.[^16]"),
    ("cannot.21", "cannot.[^21]"),
    ("Engine\".8", "Engine\".[^8]"),
    ("provider.22", "provider.[^22]"),
    ("workflows.2", "workflows.[^2]"),
    ("transactions.8", "transactions.[^8]"),
    ("experience.8\"", "experience\".[^8]"),
    ("APIs.8", "APIs.[^8]"),
    ("\n5\n", "\n[^5]\n"),
    ("trails.8", "trails.[^8]"),
    ("platform.26", "platform.[^26]"),
    ("refined.8", "refined.[^8]"),
    ("benchmarks.27", "benchmarks.[^27]"),
    ("notes.2", "notes.[^2]"),
    ("annually.31", "annually.[^31]"),
    ("intelligence.31", "intelligence.[^31]"),
    ("\n30\n", "\n[^30]\n"),
    ("GDP.31", "GDP.[^31]"),
    ("yet.34", "yet.[^34]"),
    ("output.30", "output.[^30]"),
    ("(63%).30", "(63%).[^30]"),
    ("technology.30", "technology.[^30]"),
    ("slows.31", "slows.[^31]"),
    ("inflation.37", "inflation.[^37]"),
    ("prospects.37", "prospects.[^37]"),
    ("\"intelligence\".41", "\"intelligence\".[^41]"),
    ("partners.41", "partners.[^41]"),
    ("platforms.41", "platforms.[^41]"),
    ("inequality.42", "inequality.[^42]"),
    ("corporations.36", "corporations.[^36]"),
    ("\n42\n", "\n[^42]\n"),
    ("occurred.41", "occurred.[^41]"),
    ("systems.41", "systems.[^41]"),
    ("form.41", "form.[^41]"),
    ("latecomers.37", "latecomers.[^37]"),
    ("infrastructure.43", "infrastructure.[^43]"),
    ("immiseration.43", "immiseration.[^43]")
]

for old, new in replacements:
    main_text = main_text.replace(old, new)

# Now, we parse the text to find all [^X] and assign sequential numbering
new_main_text = ""
current_idx = 0
for match in re.finditer(r'\[\^(\d+)\]', main_text):
    old_num = match.group(1)
    new_seq = get_new_seq(old_num)
    if new_seq:
        new_main_text += main_text[current_idx:match.start()] + f"[^{new_seq}]"
        current_idx = match.end()
    else:
        new_main_text += main_text[current_idx:match.end()]
        current_idx = match.end()
new_main_text += main_text[current_idx:]

# Construct references
references_section = "\n## References\n\n"
for seq, url in new_refs:
    references_section += f"[^{seq}]: {url}\n"

# Add podcast links snippet
podcast_links = '\n\n<center><a href="https://open.spotify.com/show/7doWf0GON9JsG6r8igc7RE" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Spotify</a><a href="https://podcasts.apple.com/us/podcast/deep-dive-with-gemini/id1844532251" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Apple Podcasts</a><a href="https://music.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe&si=o534zFZsc7p5XA9Q" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube Music</a><a href="https://www.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube</a><a href="https://fountain.fm/show/7LBvZT6ffpGyubvk8aSF" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px;">Fountain.fm</a></center>\n\n'

# Split into lines to insert after heading
lines = new_main_text.split('\n')
out_lines = []
for i, line in enumerate(lines):
    out_lines.append(line)
    if line.startswith('# '):
        out_lines.append(podcast_links.strip('\n'))

final_text = '\n'.join(out_lines) + references_section

with open(file_path, "w", encoding="utf-8") as f:
    f.write(final_text)

# Verify all markdown files in src are in SUMMARY.md
summary_path = "src/SUMMARY.md"
with open(summary_path, "r", encoding="utf-8") as f:
    summary_content = f.read()

# Insert the new link
target_section = "# The AI Revolution & Machine Intelligence"
new_link = "- [Agentic AI: The Wealth Catalyst](./cantillonAI.md)"

if "cantillonAI.md" not in summary_content:
    parts = summary_content.split(target_section)
    if len(parts) == 2:
        new_summary = parts[0] + target_section + "\n" + new_link + parts[1]
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(new_summary)

