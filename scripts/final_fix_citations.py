import re

def final_fix(content):
    # 1. Tickers & Currency
    content = content.replace("$STRC", "\\$STRC")
    content = content.replace("$MSTR", "\\$MSTR")
    content = content.replace("$MNAV", "\\$MNAV")
    def curr(m): return f"{m.group(1)} USD"
    content = re.sub(r'(?<!\\)\$([\d\.,]+(?:\s*(?:billion|million|trillion))?)', curr, content)

    # 2. Citations in Text
    replacements = {
        '\\ [1]': ' [^1]',
        ' [2]': ' [^2]',
        ' [4]': ' [^3]',
        ' [3]': ' [^4]',
        ' [5]': ' [^5]',
        ' [6]': ' [^6]',
        ' [7]': ' [^7]',
        ' [8]': ' [^8]',
        ' [11]': ' [^9]',
        ' [12]': ' [^10]',
        ' [13]': ' [^11]',
        ' [14]': ' [^12]',
        ' [15]': ' [^13]',
        ' [16]': ' [^14]',
        ' [17]': ' [^15]',
        ' [18]': ' [^16]'
    }
    for old, new in replacements.items():
        content = content.replace(old, new)

    # 3. Works Cited entries (Manually added back because I keep losing them)
    citations = """
[^1]: Michael Saylor and Phong Le, MicroStrategy Bitcoin Strategy Update, March 2026.
[^2]: Anthony Scaramucci, "Saylor's iPhone Moment," SkyBridge Capital Market Insights, March 2026.
[^3]: Bitcoin Historical Volatility Data, institutional analytics platform, accessed March 18, 2026.
[^4]: MicroStrategy $STRC Dividend Performance Table, March 2026.
[^5]: MicroStrategy Preferred Stock Prospectus Supplement, Variable Rate Series A Perpetual Stretch Preferred Stock.
[^6]: Nvidia (NVDA) Risk-Adjusted Return Analysis, March 2026.
[^7]: U.S. Treasury Bond Yield Comparison Data, March 2026.
[^8]: Tesla (TSLA) Volatility Profile, 2026 Market Data.
[^9]: Saylor, M., "Yield Stability in Digital Credit," Institutional Investor Summit, March 2026.
[^10]: MicroStrategy Monthly Dividend Announcement, February-March 2026.
[^11]: Strive Inc. Treasury Allocation Report, March 2026.
[^12]: MicroStrategy BTC Treasury Dashboard, [https://www.microstrategy.com/en/bitcoin](https://www.microstrategy.com/en/bitcoin), accessed March 18, 2026.
[^13]: MicroStrategy Form 8-K, Acquisition of 22,337 BTC, March 2026.
[^14]: STRC and MSTR ATM Issuance Report, mid-March 2026.
[^15]: Matt Cole, "The Obsolescence of Cash Reserves," Strive CEO Insights, March 2026.
[^16]: MicroStrategy Solvency and Reserve Report, February 2026.
"""
    
    # 4. Remove existing Works Cited header and start from scratch
    content = re.sub(r'#### \*\*Works cited\*\*.*', '', content, flags=re.DOTALL)
    content = content.strip() + "\n\n#### **Works cited**\n" + citations
    
    return content

# Restore original
import subprocess
subprocess.run(["git", "checkout", "src/strcSharpRatio.md"])

with open('src/strcSharpRatio.md', 'r') as f:
    content = f.read()

# KaTeX first
content = content.replace("![][image1]", "$$S = \\frac{R_p - R_f}{\\sigma_p}$$")
content = content.replace("![][image2]", "$R_p$")
content = content.replace("![][image3]", "$R_f$")
content = content.replace("![][image4]", "$\\sigma_p$")

fixed = final_fix(content)

# Add header if missing
title = "MicroStrategy’s \\$STRC: The 5.37 Sharpe Ratio Benchmark"
cover_image = "![STRC Sharp Ratio](img/strcSharpRatio.png)"
podcast_links = '<center><a href="https://open.spotify.com/show/7doWf0GON9JsG6r8igc7RE" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Spotify</a><a href="https://podcasts.apple.com/us/podcast/deep-dive-with-gemini/id1844532251" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">Apple Podcasts</a><a href="https://music.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe&si=o534zFZsc7p5XA9Q" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube Music</a><a href="https://www.youtube.com/playlist?list=PLIX4sFsmu37qtJMlv-VzMYWM26M1QyXTe" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px; margin-right: 10px;">YouTube</a><a href="https://fountain.fm/show/7LBvZT6ffpGyubvk8aSF" target="_blank" style="background-color: #2E2E2E; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin-top: 10px;">Fountain.fm</a></center>'

if not fixed.startswith("# "):
    fixed = f"# {title}\n\n{cover_image}\n\n{podcast_links}\n\n" + fixed

with open('src/strcSharpRatio.md', 'w') as f:
    f.write(fixed)
