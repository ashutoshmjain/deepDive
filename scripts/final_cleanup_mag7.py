import re
import os

def final_cleanup(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Final targeted fixes
    content = content.replace('Siri 2 [0]', 'Siri 2.0')
    content = content.replace('August 20 [25]', 'August 2025')
    content = content.replace('late 20 [25]', 'late 2025')
    content = content.replace('Q [4] 20 [26]', 'Q4 2026')
    content = content.replace('Q [4] 20 [25]', 'Q4 2025')
    content = content.replace('USD 9 [35] Trillion', 'USD 9.35 Trillion')
    content = content.replace('USD 11 [66] Trillion', 'USD 11.66 Trillion')
    content = content.replace('USD 9 [58] Trillion', 'USD 9.58 Trillion')
    content = content.replace('USD 9 [06] Trillion', 'USD 9.06 Trillion')
    content = content.replace('Feb. 2 [5]', 'Feb. 25')
    
    # Also fix any remaining Q [N]
    content = re.sub(r'Q\s*\[(\d)\]', r'Q\1', content)
    
    # Ensure citations are space [N]
    content = re.sub(r'(\w)\[(\d{1,2})\]', r'\1 [\2]', content)
    content = re.sub(r'(\.)\[(\d{1,2})\]', r'\1 [\2]', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

final_cleanup('src/mag7split.md')
