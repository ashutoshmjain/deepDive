import re
import os
import sys

LIGHTNING_WIDGET = """
---

### Tips and Donations

If you enjoyed this deep dive, consider supporting the project with a tip in **Sats**. It's a simple, global way to support independent research.

<lightning-widget
  name='Thanks for supporting the publication'
  accent='#f9ce00'
  to='shutosha@primal.net'
  image='https://nostrcheck.me/media/5af0794606a15b5641e25aa23d04af4cb0d7d5e68b11cacb47e56a4698fca8c4/49ff6d00cb5bc819cd19f77783d4815fbd46a5b99b6fbdead1eaecfab798187b.webp'
/>
<script src='https://embed.twentyuno.net/js/app.js'></script>

To send Sats, you'll need a [lightning wallet](https://lightningaddress.com/). 

---
"""

KATEX_MAP = {
    "![][image1]": r"$\mathcal{P} = (\mathcal{S}, \mathcal{A}, \rho, \mathcal{R})$",
    "![][image2]": r"$\mathcal{S}$",
    "![][image3]": r"$\mathcal{A}$",
    "![][image4]": r"$\rho$",
    "![][image5]": r"$\mathcal{R}$",
    "![][image6]": r"$G_N$",
    "![][image7]": r"$SU(3) \times SU(2) \times U(1)$",
    "![][image8]": r"$S^2$",
    "![][image9]": r"$SL(2, \mathbb{C})$",
    "![][image10]": r"$SO(3,1)$",
    "![][image11]": r"$10^{120}$",
    "![][image12]": r"$T_{\mu\nu} l^\mu l^\nu = 0$",
}

EPISODE_229_MAP = {
    "![][image1]": r"$E = mc^2$",
    "![][image2]": r"$10-15$",
    "![][image3]": r"$100$",
    "![][image4]": r"$500-1000$",
    "![][image5]": r"$I$",
    "![][image6]": r"$\eta$",
    "![][image7]": r"$E$",
    "![][image8]": r"$\Delta S$",
    "![][image9]": r"$$I = \eta \frac{\Delta S \cdot k_B T}{E}$$",
    "![][image10]": r"$\Delta S$",
    "![][image11]": r"$T$",
    "![][image12]": r"$W \ge k_B T \ln 2$",
    "![][image13]": r"$$T = \kappa E$$",
    "![][image14]": r"$\kappa$",
    "![][image15]": r"$E$",
    "![][image16]": r"$2E/\pi\hbar$",
    "![][image17]": r"$E = mc^2$",
    "![][image18]": r"$10^{50}$",
    "![][image19]": r"$L$",
    "![][image20]": r"$C$",
    "![][image21]": r"$N$",
    "![][image22]": r"$1/C^\alpha$",
    "![][image23]": r"$1/N^\beta$",
    "![][image24]": r"$1/D^\gamma$",
    "![][image25]": r"$\rho_s$",
    "![][image26]": r"$P_s$",
    "![][image27]": r"$\mathcal{M}$",
    "![][image28]": r"$G_{\mu\nu}$",
    "![][image29]": r"$$G_{\mu\nu} + \Lambda g_{\mu\nu} = \kappa T_{\mu\nu}$$",
    "![][image30]": r"$a$",
    "![][image31]": r"$\Phi$",
    "![][image32]": r"$4 \times 10^{26}$",
    "![][image33]": r"$$I \propto \frac{\Delta S}{E}$$"
}

EPISODE_230_MAP = {
    "![][image1]": r"$mNAV < 1$"
}

EPISODE_234_MAP = {
    "![][image1]": r"$P = F \left(1 - \frac{d \cdot t}{360}\right)$"
}

def extract_episode(filename):
    m = re.match(r'^(\d+)\.md$', filename)
    if m:
        val = int(m.group(1))
        if val < 1000: return str(val)
    return None

def fix_footnotes(content):
    parts = re.split(r'(#### \*\*Works cited\*\*|#### \*\*References\*\*)', content, flags=re.IGNORECASE)
    if len(parts) < 3: return content
    
    header = parts[1]
    refs_raw = parts[2]
    body = parts[0]
    
    ref_map = {}
    ref_lines = re.findall(r'^\[\^(\d+)\]:\s*(.*)$', refs_raw, re.MULTILINE)
    ref_lines += re.findall(r'^(\d+)\.\s*(.*)$', refs_raw, re.MULTILINE)
    ref_lines += re.findall(r'^(\d+)\s+([^\d].*)$', refs_raw, re.MULTILINE)

    for num, text in ref_lines:
        if num not in ref_map: ref_map[num] = text.strip()
    
    if not ref_map: return content

    def replacer(match):
        punct = match.group(1)
        nums_str = match.group(2)
        
        parts = re.split(r'[\s,]+', nums_str)
        valid_footnotes = []
        for p in parts:
            if not p: continue
            if p in ref_map: valid_footnotes.append(f"[^{p}]")
            else: return match.group(0)
        return f"{punct}{''.join(valid_footnotes)}"

    # Only match numbers immediately following specific punctuation
    body = re.sub(r'([.,;")\]])(\d+(?:[\s,]+\d+)*)(?![.\d])', replacer, body)
    
    def table_repl(match):
        pre, num, post = match.groups()
        if num in ref_map: return f"{pre}[^{num}]{post}"
        return match.group(0)
    # Be more careful with tables - only single numbers that match refs
    body = re.sub(r'(\|[^|]*?\s+)(\d+)(\s*\|)', table_repl, body)

    used_numbers = re.findall(r'\[\^(\d+)\]', body)
    unique_used = sorted(list(set(used_numbers)), key=int)
    
    num_map = {old: str(i+1) for i, old in enumerate(unique_used)}
    
    def final_repl(match):
        old_num = match.group(1)
        return f"[^{num_map[old_num]}]"
    
    body = re.sub(r'\[\^(\d+)\]', final_repl, body)

    new_refs = [f"\n\n{header}\n"]
    for old_num in unique_used:
        new_refs.append(f"[^{num_map[old_num]}]: {ref_map[old_num]}\n")
    
    return body + "".join(new_refs)

def process_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('\u0332', '')
    content = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', content)
    content = re.sub(r'(\\)([_.-])', r'\2', content)

    ep_num = extract_episode(os.path.basename(file_path))
    
    math_blocks = []
    def save_math(match):
        math_blocks.append(match.group(0))
        return f"__MATH_BLOCK_{len(math_blocks)-1}__"
    
    content = re.sub(r'\$\$.*?\$\$', save_math, content, flags=re.DOTALL)
    content = re.sub(r'\$.*?\$', save_math, content)
    
    content = fix_footnotes(content)

    content = re.sub(r'\$([\d\.,]+)\s*(million|billion|trillion|k|m|b|t)?(?=[^0-9\^]|$)', r'\1 \2 USD ', content, flags=re.IGNORECASE)
    content = content.replace('  ', ' ')
    content = content.replace('$', r'\$')
    
    cur_map = KATEX_MAP
    if ep_num == "229": cur_map = EPISODE_229_MAP
    elif ep_num == "230": cur_map = EPISODE_230_MAP
    elif ep_num == "234": cur_map = EPISODE_234_MAP
    for placeholder, symbol in cur_map.items():
        content = content.replace(placeholder, symbol)

    for idx, block in enumerate(math_blocks):
        content = content.replace(f"__MATH_BLOCK_{idx}__", block)

    if "lightning-widget" not in content:
        content = content.strip() + "\n" + LIGHTNING_WIDGET

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Processed markdown for {file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fix_markdown.py <episode_number_or_file_path>")
        sys.exit(1)
    
    input_arg = sys.argv[1]
    
    if input_arg.isdigit():
        file_path = f"src/{input_arg}.md"
        if not os.path.exists(file_path) and os.path.exists(f"deepDive/src/{input_arg}.md"):
            file_path = f"deepDive/src/{input_arg}.md"
    else:
        file_path = input_arg
        
    process_markdown(file_path)
