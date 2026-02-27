import re
import os

def fix_invincible_dollar(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix headings (remove bolding and clean up)
    content = re.sub(r'^## \*\*([^\*]+)\*\*', r'## \1', content, flags=re.MULTILINE)
    content = re.sub(r'^# \*\*([^\*]+)\*\*', r'# \1', content, flags=re.MULTILINE)
    content = re.sub(r'## ([IVX]+)\\?\.', r'## \1.', content)

    # 2. Sequential Footnotes
    content = content.replace('(Eichengreen, 2011)', '[2]')
    content = content.replace('(Pettis, 2011)', '[3]')
    content = content.replace('(Bown, 2021)', '[1]')
    content = content.replace('(Prasad, 2016)', '[4]')
    content = re.sub(r'(Triffin Dilemma)', r'\1 [5]', content, count=1)

    # 3. References Section
    references_text = """# References

1. Bown, C. P. (2021). "Anatomy of a Flop: Why Trump’s US-China Phase One Trade Deal Fell Short." Peterson Institute for International Economics. [https://www.piie.com/publications/policy-briefs/anatomy-flop-why-trumps-us-china-phase-one-trade-deal-fell-short](https://www.piie.com/publications/policy-briefs/anatomy-flop-why-trumps-us-china-phase-one-trade-deal-fell-short)

2. Eichengreen, B. (2011). "Exorbitant Privilege: The Rise and Fall of the Dollar and the Future of the International Monetary System." Oxford University Press. [https://global.oup.com/academic/product/exorbitant-privilege-9780199753765](https://global.oup.com/academic/product/exorbitant-privilege-9780199753765)

3. Pettis, M. (2011). "The Volatility Machine: Emerging Economies and the Threat of Financial Collapse." Oxford University Press. [https://global.oup.com/academic/product/the-volatility-machine-9780199763740](https://global.oup.com/academic/product/the-volatility-machine-9780199763740)

4. Prasad, E. S. (2016). "Gaining Ground: The Rise of the Renminbi." Brookings Institution Press. [https://www.brookings.edu/book/gaining-ground/](https://www.brookings.edu/book/gaining-ground/)

5. Triffin, R. (1960). "Gold and the Dollar Crisis: The Future of Convertibility." Yale University Press. [https://research.stlouisfed.org/publications/review/1961/01/01/gold-and-the-dollar-crisis-the-future-of-convertibility/](https://research.stlouisfed.org/publications/review/1961/01/01/gold-and-the-dollar-crisis-the-future-of-convertibility/)
"""
    # Remove old References section and bibliography
    parts = re.split(r'---?\n\n## References|\n\n---\n\n## References', content)
    content = parts[0].strip()
    content = content + "\n\n" + references_text

    content = re.sub(r'\n\s*\n+', r'\n\n', content)
    content = content.replace('\u0332', '')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def update_summary(summary_path, file_link):
    with open(summary_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Check if already present
    for line in lines:
        if file_link in line:
            return
            
    # Insert at second spot (directly below cover.md)
    lines.insert(3, f"- {file_link}\n")
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

if __name__ == "__main__":
    file_path = 'src/invincibleDollar.md'
    summary_path = 'src/SUMMARY.md'
    file_link = "[Invincible Dollar: Triffin's Dilemma Explained](./invincibleDollar.md)"
    
    fix_invincible_dollar(file_path)
    update_summary(summary_path, file_link)
