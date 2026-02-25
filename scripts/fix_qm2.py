import re
import os

file_path = 'src/QM2-verification.md'

if not os.path.exists(file_path):
    print(f"Error: {file_path} not found")
    exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Split text and images
parts = content.split('\n[image1]:')
text = parts[0]
images = '\n[image1]:' + parts[1] if len(parts) > 1 else ''

# 1. Fix KaTeX/Math issues
text = text.replace('($ \\\\mu $)', '($ \mu $)')

# 2. Re-number and Integrate citations
text = text.replace('flavor-switching.1', 'flavor-switching. [1]')
text = text.replace('non-destructive validation.1', 'non-destructive validation. [1]')
text = text.replace('flavor-conserving.6', 'flavor-conserving. [2]')
text = text.replace('Zero-Knowledge Proof (ZKP).4', 'Zero-Knowledge Proof (ZKP). [3]')
text = text.replace('Weak Hypercharge (![][image6]).6', 'Weak Hypercharge (![][image6]). [4]')
text = text.replace('identity remain untouched.9', 'identity remain untouched. [5]')
text = text.replace('subatomic scale.', 'subatomic scale. [6]')
text = text.replace('end of the alphabet.', 'end of the alphabet. [7]')

# 3. New "Works cited"
works_cited_new = """#### **Works cited**

1. Weak interaction - Wikipedia, accessed February 19, 2026, [https://en.wikipedia.org/wiki/Weak_interaction](https://en.wikipedia.org/wiki/Weak_interaction)

2. Chiralsymmetry - UT Physics, accessed February 19, 2026, [https://web2.ph.utexas.edu/~coker2/index.files/chiralsb.htm](https://web2.ph.utexas.edu/~coker2/index.files/chiralsb.htm)

3. 23.1 The Four Fundamental Forces | Texas Gateway, accessed February 19, 2026, [https://texasgateway.org/resource/231-four-fundamental-forces](https://texasgateway.org/resource/231-four-fundamental-forces)

4. The Standard Model - The Physics Hypertextbook, accessed February 19, 2026, [https://physics.info/standard/](https://physics.info/standard/)

5. Are quantum fields in any way similar to classical fields? : r/askscience - Reddit, accessed February 19, 2026, [https://www.reddit.com/r/askscience/comments/fo4igl/are_quantum_fields_in_any_way_similar_to/](https://www.reddit.com/r/askscience/comments/fo4igl/are_quantum_fields_in_any_way_similar_to/)

6. DOE Explains...The Strong Force - Department of Energy, accessed February 19, 2026, [https://www.energy.gov/science/doe-explainsthe-strong-force](https://www.energy.gov/science/doe-explainsthe-strong-force)

7. Standard Model - Wikipedia, accessed February 19, 2026, [https://en.wikipedia.org/wiki/Standard_Model](https://en.wikipedia.org/wiki/Standard_Model)
"""

# Replace citation list
text = re.split(r'#### \*\*Works cited\*\*', text)[0] + works_cited_new

# Join
new_content = text.strip() + '\n\n' + images.strip()

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("File updated successfully.")
