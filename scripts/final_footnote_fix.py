import sys
import re

def finalize_footnotes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    in_works_cited = False
    
    # Define the mapping of replacements based on the text we saw
    replacements = {
        "force.1": "force.[1](#1)",
        "leptons.1": "leptons.[1](#1)",
        "transmutation.3": "transmutation.[3](#3)",
        "matrices.4": "matrices.[4](#4)",
        "one.7": "one.[7](#7)",
        "matter.1": "matter.[1](#1)",
        "interactions.1": "interactions.[1](#1)",
        "field.1": "field.[1](#1)",
        "disappear.9": "disappear.[9](#9)",
        'puzzle".9': 'puzzle".[9](#9)',
        "flavor.3": "flavor.[3](#3)",
        "electron.4": "electron.[4](#4)",
        "bosons.5": "bosons.[5](#5)",
        "involved.4": "involved.[4](#4)",
        "boson.5": "bosons.[5](#5)",
        "boson.13": "boson.[13](#13)",
        "conservation.11": "conservation.[11](#11)",
        "antineutrino.11": "antineutrino.[11](#11)",
        "quarks.5": "quarks.[5](#5)",
        "obeyed.13": "obeyed.[13](#13)",
        "charge.13": "charge.[13](#13)",
        "lepton.13": "lepton.[13](#13)",
        "constant.17": "constant.[17](#17)",
        "doublets.10": "doublets.[10](#10)",
        "exchanges.14": "exchanges.[14](#14)",
        "antineutrino.14": "antineutrino.[14](#14)",
        "process.14": "process.[14](#14)",
        "numbers.16": "numbers.[16](#16)",
        "value.16": "value.[16](#16)",
        "leptons.2": "leptons.[2](#2)",
        "decay.22": "decay.[22](#22)",
        "antineutrino.18": "antineutrino.[18](#18)",
        "mass.21": "mass.[21](#21)",
        "mixing.6": "mixing.[6](#6)",
        "isolation.1": "isolation.[1](#1)",
        "baryon.24": "baryon.[24](#24)",
        "oscillations).6": "oscillations).[6](#6)",
        "matrix.6": "matrix.[6](#6)",
        "generation.1": "generation.[1](#1)",
        "time.6": "time.[6](#6)",
        "transition.12": "transition.[12](#12)",
        "doublet.12": "doublet.[12](#12)",
        "generation.26": "generation.[26](#26)",
        "small.6": "small.[6](#6)",
        "it.26": "it.[26](#26)",
        "name.5": "name.[5](#5)",
        "force.2": "force.[2](#2)",
        "boson.4": "boson.[4](#4)",
        "energy.8": "energy.[8](#8)",
        "fermion.1": "fermion.[1](#1)",
        "directly.14": "directly.[14](#14)",
        "decay.13": "decay.[13](#13)",
        "exist).6": "exist).[6](#6)",
        "baryon.1": "baryon.[1](#1)",
        "constraint.1": "constraint.[1](#1)",
        "Lagrangian.1": "Lagrangian.[1](#1)",
        "fermions.9": "fermions.[9](#9)",
        "interactions.11": "interactions.[11](#11)",
        "generations.5": "generations.[5](#5)",
        'Universality".6': 'Universality".[6](#6)',
        "identical.6": "identical.[6](#6)",
        "differences.6": "differences.[6](#6)",
        "decay 11": "decay [11](#11)",
        "dependence 16": "dependence [16](#16)",
        "same.16": "same.[16](#16)",
        "universe.11": "universe.[11](#11)",
        "predicted.31": "predicted.[31](#31)",
        "energy.9": "energy.[9](#9)",
        "Model.31": "Model.[31](#31)",
        "generations.31": "generations.[31](#31)",
        "number.16": "number.[16](#16)",
        "B-decay).20": "B-decay).[20](#20)",
        "travel.18": "travel.[18](#18)",
        "structure.18": "structure.[18](#18)",
        "force.4": "force.[4](#4)",
        "charge.5": "charge.[5](#5)",
        "neutrinos.12": "neutrinos.[12](#12)",
        "lines.6": "lines.[6](#6)",
        "world.1": "world.[1](#1)",
        "occupy.2": "occupy.[2](#2)",
        "Model.1": "Model.[1](#1)"
    }

    for line in lines:
        if "#### **Works cited**" in line:
            in_works_cited = True
            new_lines.append(line)
            continue
        
        if in_works_cited:
            # Reformat "N. Text" to "<a name="N"></a>N. Text"
            # Looking for "1. Text"
            match = re.match(r'^(\d+)\.\s+(.*)', line.strip())
            if match:
                num = match.group(1)
                text = match.group(2)
                new_lines.append(f'<a name="{num}"></a>{num}. {text}\n')
            else:
                new_lines.append(line)
        else:
            # Replace citations in text
            modified_line = line
            # Sort by length of 'old' string descending to avoid partial matches
            sorted_keys = sorted(replacements.keys(), key=len, reverse=True)
            for old in sorted_keys:
                modified_line = modified_line.replace(old, replacements[old])
            new_lines.append(modified_line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    finalize_footnotes(sys.argv[1])
