import re

def fix_unreferenced_footnotes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Manually insert missing footnote references
    content = content.replace('Particle Psychology', 'Particle Psychology[^9]')
    content = content.replace('semantic gravity', 'semantic gravity[^12]', 1) # only first occurrence
    content = content.replace('Neural Representation Manifold', 'Neural Representation Manifold[^13]')
    content = content.replace('representational dimensionality', 'representational dimensionality[^14]')
    content = content.replace("Vopson's Principle", "Vopson's Principle[^15]")
    content = content.replace('[^20]', '[^17][^20]')
    content = content.replace('"It from Bit" doctrine', '"It from Bit" doctrine[^18]')
    content = content.replace('signified in semiotics.', 'signified in semiotics.[^23]')
    content = content.replace('Mirror the Human Brain', 'Mirror the Human Brain[^25]')
    content = content.replace('Universal Latent Space', 'Universal Latent Space[^30]')
    content = content.replace('Sāńkhya', 'Sāńkhya[^31]')
    content = content.replace('Pre-Geometric Gravity', 'Pre-Geometric Gravity[^32][^33]')

    # Also fix the interpretation of atomic theory.[^29]
    # In original it was Particle Psychology" and "Sāńkhya" interpretations of atomic theory.[^29]
    # But 29 is Latent space. It should probably be 9 and 31.
    content = content.replace('interpretations of atomic theory.[^29]', 'interpretations of atomic theory.[^9][^31]')

    # Final cleanup of multiple insertions if any
    content = content.replace('Sāńkhya[^31][^31]', 'Sāńkhya[^31]')
    content = content.replace('Particle Psychology[^9][^9]', 'Particle Psychology[^9]')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed unreferenced footnotes in {file_path}")

fix_unreferenced_footnotes("src/bitToIt.md")
