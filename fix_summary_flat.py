with open("src/SUMMARY.md", "r") as f:
    content = f.read()

# 1. Rename The Tip of the Chain
content = content.replace("# The Tip of the Chain", "# Recent Blocks")

# 2. Remove The Network and promote Mempool and Deep Storage
old_structure = """# The Network

- [The Mempool (Unconfirmed)](mempool.md)
    - [242 : Triggering Cancer Self-Destruct Signal](_242.md)

- [Deep Storage (The Ledger)](archive.md)"""

new_structure = """# The Mempool (Unconfirmed)
- [WIP / Call for Participation](mempool.md)
  - [242 : Triggering Cancer Self-Destruct Signal](_242.md)

# Deep Storage (The Ledger)
- [The Archive](archive.md)"""

content = content.replace(old_structure, new_structure)

# Handle empty mempool case just in case
old_empty = """# The Network

- [The Mempool (Unconfirmed)](mempool.md)
    - [None at this moment. Join us on GitHub!](github.md)

- [Deep Storage (The Ledger)](archive.md)"""

new_empty = """# The Mempool (Unconfirmed)
- [WIP / Call for Participation](mempool.md)
  - [None at this moment. Join us on GitHub!](github.md)

# Deep Storage (The Ledger)
- [The Archive](archive.md)"""

content = content.replace(old_empty, new_empty)

with open("src/SUMMARY.md", "w") as f:
    f.write(content)

