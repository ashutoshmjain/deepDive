import re

with open("src/SUMMARY.md", "r") as f:
    content = f.read()

# Completely reset SUMMARY.md to a known clean top state
top_state = """# Summary

- [Deep Dive with Gemini](./cover.md)
"""

# Find everything after <!-- RECENT_END --> (thematic stuff)
parts = content.split("<!-- RECENT_END -->")
thematic_part = parts[1] if len(parts) > 1 else ""

with open("src/SUMMARY.md", "w") as f:
    f.write(top_state + thematic_part)

