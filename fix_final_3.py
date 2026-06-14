with open("src/SUMMARY.md", "r") as f:
    content = f.read()

# Completely clean summary to pristine state
clean = """# Summary

- [Deep Dive with Gemini](./cover.md)
"""
with open("src/SUMMARY.md", "w") as f:
    f.write(clean)
