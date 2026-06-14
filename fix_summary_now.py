with open("src/SUMMARY.md", "r") as f:
    content = f.read()

# 1. Fix block template logic
content = content.replace("- [block template](current.md)\n<!-- RECENT_START -->", "<!-- RECENT_START -->\n- [block template](current.md)")

# 2. Fix genesis tree rendering
# Ensure genesis has its children correctly indented.
# I will just write a pristine summary top part to be sure.
pristine_top = """# Summary

- [deepDive](./cover.md)

- [mempool](mempool.md)
    - [242 : Triggering Cancer Self-Destruct Signal](_242.md)

<!-- RECENT_START -->
- [block template](current.md)
    - [241 : What exactly is Immutability?](241.md)
<!-- RECENT_END -->

- [chain](archive.md)
    - [block 1]()
        - [240 : Rise of the Observer](240.md)
        - [239 : Unification of #Resurrection and #Reincarnation](239.md)
        - [238 : Calculus of Liberation.](238.md)
        - [237 : SATA - The daily dividend company](237.md)
        - [236 : AGI Vs GAI](236.md)
        - [235 : Future of Sovereign Credit](235.md)
        - [234 : Satoshi Dividends via Lightning Network](234.md)
        - [233 : what exactly is NOT consciousness !](233.md)
        - [232 : The Orthogonal Manifold](232.md)
        - [231 : Why don't LLMs self-prompt ?](231.md)
        - [230 : STRC - derivatives and inflows](230.md)
        - [229 : The Energy-Intelligence Equivalence Principle](229.md)
        - [228 : What is Google Worth?](228.md)
        - [227 : 60 billion call option](227.md)
        - [226 : Root access to self \-](226.md)
        - [225 : BTC: Global Pristine Collateral Network](225.md)
        - [224 : TPUs vs GPUs: AI Commodification](224.md)
        - [223 : Observer Patch Holography](223.md)
        - [222 : Homeownership - American Dream!](222.md)
        - [221 : The perfect playbook](221.md)
        - [220 : AI Made Me a Believer](220.md)
    - [genesis](genesis.md)
"""

# Find where the thematic research starts (bitcoin)
thematic_start = content.find("        - [bitcoin]()")
if thematic_start != -1:
    summary = pristine_top + content[thematic_start:]
else:
    summary = pristine_top

with open("src/SUMMARY.md", "w") as f:
    f.write(summary)
