import re

def final_insertion(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 13 and 25
    content = content.replace('low-dimensional manifolds', 'low-dimensional manifolds[^13] [^25]', 1)
    
    # 30
    content = content.replace('point or a vector in a "latent space".', 'point or a vector in a "latent space".[^30]')
    
    # 33 (32 is already there)
    # Wait, check if 32 is there.
    # From previous grep: "composed of subatomic parts or words (particles).[^32]"
    content = content.replace('[^32]', '[^32] [^33]')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Final insertion done in {file_path}")

final_insertion("src/bitToIt.md")
