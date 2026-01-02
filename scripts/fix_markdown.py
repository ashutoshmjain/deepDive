import re

def format_works_cited(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    works_cited_heading = "#### **Works cited**"
    if works_cited_heading not in content:
        return "'Works cited' section not found."

    before_works_cited, works_cited_raw = content.split(works_cited_heading, 1)

    # Split by citation number and re-attach numbers
    parts = re.split(r'(\d+\.\s+)', works_cited_raw)
    reconstructed_citations = []
    start_idx = 1 if parts[0].strip() == "" else 0

    for i in range(start_idx, len(parts), 2):
        if i + 1 < len(parts):
            citation_entry = parts[i] + parts[i+1].strip()
            reconstructed_citations.append(citation_entry)
        elif parts[i].strip():
                reconstructed_citations.append(parts[i].strip())

    works_cited_formatted = "\n\n".join(reconstructed_citations)
    new_content = before_works_cited + works_cited_heading + "\n\n" + works_cited_formatted.strip()

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return "Works cited section formatted successfully."

def fix_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix headings
    content = re.sub(r'^# \*\*(.*)\*\*$', r'# \1', content, flags=re.MULTILINE)
    content = re.sub(r'^## \*\*(.*)\*\*$', r'## \1', content, flags=re.MULTILINE)
    content = re.sub(r'^### \*\*(.*)\*\*$', r'### \1', content, flags=re.MULTILINE)
    content = re.sub(r'^#### \*\*(.*)\*\*$', r'#### \1', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.*)', r'## \1', content, flags=re.MULTILINE)
    
    # Fix dollar signs
    content = content.replace('$38.50', 'USD 38.50')
    content = content.replace('$248', 'USD 248')
    
    # Add citations
    content = content.replace("S&P 500 delivering returns in the 17% to 20% range ", "S&P 500 delivering returns in the 17% to 20% range [19] ")
    content = content.replace("staggering return of nearly 600% by year-end.", "staggering return of nearly 600% by year-end [2].")
    content = content.replace("mispriced the standalone entity at approximately USD 38.50 per share.", "mispriced the standalone entity at approximately USD 38.50 per share [4].")
    content = content.replace("driving the price to nearly USD 248 by year-end.", "driving the price to nearly USD 248 by year-end [4].")
    content = content.replace("expanding gross margins from the low 20s to 36%.", "expanding gross margins from the low 20s to 36% [4].")
    content = content.replace("Silver prices surged by approximately 160% in 2025,", "Silver prices surged by approximately 160% in 2025 [8, 9],")
    content = content.replace("obliterating the returns of Gold (~75%)", "obliterating the returns of Gold (~75%) [11]")
    content = content.replace("Hyperliquid (HYPE)**\n\n**Performance:** ~86% Return (Year-to-Date)", "Hyperliquid (HYPE)**\n\n**Performance:** ~86% Return (Year-to-Date) [12]")
    content = content.replace("78% acknowledging the necessity of this trade-off.", "78% acknowledging the necessity of this trade-off [13].")
    content = content.replace("71% of business leaders reported they did not expect a recession in 2025,", "71% of business leaders reported they did not expect a recession in 2025 [14],")
    content = content.replace("over half of mid-market executives planning to introduce new products or services.", "over half of mid-market executives planning to introduce new products or services [14].")
    content = content.replace("43% of business leaders planned to explore strategic partnerships to drive growth.", "43% of business leaders planned to explore strategic partnerships to drive growth [14].")
    content = content.replace("51% of mid-market leaders planned to expand their workforce.", "51% of mid-market leaders planned to expand their workforce [14].")
    content = content.replace("IBM noting that AI creates an \"automation advantage\" that empowers bankers to reimagine their contributions.", "IBM noting that AI creates an \"automation advantage\" that empowers bankers to reimagine their contributions [13].")
    content = content.replace("nearly two-thirds expecting the national economy to improve.", "nearly two-thirds expecting the national economy to improve [14].")
    content = content.replace("31% of businesses considered M&A as a means to achieve growth in 2025.", "31% of businesses considered M&A as a means to achieve growth in 2025 [14].")
    content = content.replace("A consortium of nine major European banks, including ING and Deutsche Bank, united to launch a Euro-backed stablecoin.", "A consortium of nine major European banks, including ING and Deutsche Bank, united to launch a Euro-backed stablecoin [16].")
    content = content.replace("multi-asset funds delivered average returns of nearly 17%,", "multi-asset funds delivered average returns of nearly 17% [7],")
    content = content.replace("driven by the 76% surge in gold and 155% surge in silver.", "driven by the 76% surge in gold and 155% surge in silver [7].")
    content = content.replace("Sectors like Utilities performed surprisingly well (+20.17%)", "Sectors like Utilities performed surprisingly well (+20.17%) [19],")
    content = content.replace("SIP inflows hit record highs, with 97% of mutual fund schemes delivering positive returns.", "SIP inflows hit record highs, with 97% of mutual fund schemes delivering positive returns [20].")
    content = content.replace("Russia announced plans to establish a nuclear power plant on the moon within the next decade.", "Russia announced plans to establish a nuclear power plant on the moon within the next decade [21].")
    content = content.replace("successful \"First Light\" of the Vera C. Rubin Observatory", "successful \"First Light\" of the Vera C. Rubin Observatory [24]")
    content = content.replace("gene therapy. Researchers at University College London successfully used an adeno-associated virus vector to deliver the LGI1 gene,", "gene therapy. Researchers at University College London successfully used an adeno-associated virus vector to deliver the LGI1 gene [22],")
    content = content.replace("MIT researchers revolutionized energy storage by turning one of the world’s most common materials—cement—into a battery.", "MIT researchers revolutionized energy storage by turning one of the world’s most common materials—cement—into a battery [23].")
    content = content.replace("\"Cat Qubit\" breakthrough by researchers at AWS and Caltech,", "\"Cat Qubit\" breakthrough by researchers at AWS and Caltech [25],")
    content = content.replace("generative AI was used to design novel antibiotics capable of killing drug-resistant bacteria.", "generative AI was used to design novel antibiotics capable of killing drug-resistant bacteria [22].")
    content = content.replace("ancient DNA to solve the origins of the Uralic languages", "ancient DNA to solve the origins of the Uralic languages [24]")
    content = content.replace("earliest evidence of Neanderthals using fire-making technology (400,000 years ago) in Suffolk, England.", "earliest evidence of Neanderthals using fire-making technology (400,000 years ago) in Suffolk, England [21].")
    content = content.replace("Antarctic ozone layer is healing as a direct result of the global ban on CFCs.", "Antarctic ozone layer is healing as a direct result of the global ban on CFCs [24].")
    content = content.replace("device using hydrogels that can harvest fresh drinking water from the air,", "device using hydrogels that can harvest fresh drinking water from the air [29],")
    content = content.replace("captured the first images of \"free-range\" atoms interacting in space", "captured the first images of \"free-range\" atoms interacting in space [23]")
    content = content.replace("MoM-z14 Galaxy, one of the earliest and most distant galaxies ever observed.", "MoM-z14 Galaxy, one of the earliest and most distant galaxies ever observed [21].")
    content = content.replace("** Hudson Tunnel Project ** in New York", "** Hudson Tunnel Project ** in New York [26]")
    content = content.replace("**Delta Conveyance Project** in California", "**Delta Conveyance Project** in California [26]")
    content = content.replace("The **Khavda Solar Park** in India", "The **Khavda Solar Park** in India [27]")
    content = content.replace("the **Omkareshwar Floating Solar Park**", "the **Omkareshwar Floating Solar Park** [27]")
    content = content.replace("MIT engineers developed a bionic knee that allows amputees to walk faster", "MIT engineers developed a bionic knee that allows amputees to walk faster [23]")
    content = content.replace("NEOM project... The excavation of the \"B3 Tunnel\" at the Trojena ski resort", "NEOM project... The excavation of the \"B3 Tunnel\" at the Trojena ski resort [27]")
    content = content.replace("The **Brightline West** project", "The **Brightline West** project [26]")
    content = content.replace("the **California High-Speed Railway**", "the **California High-Speed Railway** [26]")
    content = content.replace("the **Chuo Shinkansen** (Maglev line) in Japan", "the **Chuo Shinkansen** (Maglev line) in Japan [10]")
    content = content.replace("the **FutureFeed Asparagopsis Supplement**", "the **FutureFeed Asparagopsis Supplement** [22]")
    content = content.replace("**RootWave** that use electricity instead of chemicals.", "**RootWave** that use electricity instead of chemicals [22].")
    content = content.replace("China’s **South-North Water Transfer Project**", "China’s **South-North Water Transfer Project** [10]")
    content = content.replace("**Flocean** gained traction.", "**Flocean** gained traction [22].")
    content = content.replace("**AST SpaceMobile's BlueBird**", "**AST SpaceMobile's BlueBird** [10]")
    content = content.replace("the **Glass City Metropark**", "the **Glass City Metropark** [28]")
    content = content.replace("**Bois d'Arc Lake**", "**Bois d'Arc Lake** [28]")
    content = content.replace("film cameras (Pentax 17)", "film cameras (Pentax 17) [29]")
    content = content.replace("Sales of \"dumb phones\" (like the Light Phone III)", "Sales of \"dumb phones\" (like the Light Phone III) [29]")
    content = content.replace("Americans increasingly moved away from a biblical, authoritarian God toward a deity perceived as more accepting and less demanding.", "Americans increasingly moved away from a biblical, authoritarian God toward a deity perceived as more accepting and less demanding [32].")
    content = content.replace("the rapid growth of the \"Nones\" (those claiming no religious affiliation) appeared to plateau globally.", "the rapid growth of the \"Nones\" (those claiming no religious affiliation) appeared to plateau globally [31].")
    content = content.replace("\"Forest Bathing\" and \"Immersive Nature Retreats\" became top wellness trends.", "\"Forest Bathing\" [33] and \"Immersive Nature Retreats\" [34] became top wellness trends.")
    content = content.replace("Interest in genealogy moved beyond DNA percentages to \"Ancestral Healing\"", "Interest in genealogy moved beyond DNA percentages to \"Ancestral Healing\" [35]")
    content = content.replace("\"Sound Baths\" and \"Vibration Therapy\" moved from the fringe to the center of wellness culture.", "\"Sound Baths\" and \"Vibration Therapy\" moved from the fringe to the center of wellness culture [36].")
    content = content.replace("The Global Wellness Summit noted a surge in \"Pilgrimage Trails\" and \"Wellness Retreats\".", "The Global Wellness Summit noted a surge in \"Pilgrimage Trails\" and \"Wellness Retreats\" [15].")
    content = content.replace("Barna trends highlight a return to questions about \"human design\" and purpose.", "Barna trends highlight a return to questions about \"human design\" and purpose [37].")

    # Fix Works Cited section by removing extra backslashes around . in the numbered list
    content = re.sub(r'(\d+)\\.', r'\1.', content)

    # Remove extra backslashes from URLs
    content = re.sub(r'http(s?):\\/\\/([^ \n\\]+)', r'http\1://\2', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    format_works_cited(file_path)


fix_markdown('src/GlobalStrategicRetrospective2025.md')
