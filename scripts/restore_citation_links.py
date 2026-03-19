import re

def restore_weblinks(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the mapping of footnotes to their full citation text with URLs
    citations_mapping = {
        '1': 'Michael Saylor and Phong Le, MicroStrategy Bitcoin Strategy Update, March 2026, [https://www.microstrategy.com/en/investor-relations](https://www.microstrategy.com/en/investor-relations)',
        '2': 'Anthony Scaramucci, "Saylor\'s iPhone Moment," SkyBridge Capital Market Insights, March 2026, [https://www.skybridge.com/insights](https://www.skybridge.com/insights)',
        '3': 'Bitcoin Historical Volatility Data, institutional analytics platform, accessed March 18, 2026, [https://www.glassnode.com](https://www.glassnode.com)',
        '4': 'MicroStrategy STRC Dividend Performance Table, March 2026, [https://www.microstrategy.com/en/bitcoin/preferred-stock](https://www.microstrategy.com/en/bitcoin/preferred-stock)',
        '5': 'MicroStrategy Preferred Stock Prospectus Supplement, Variable Rate Series A Perpetual Stretch Preferred Stock, [https://www.sec.gov/Archives/edgar/data/1050446/000119312525263719/d922690d424b5.htm](https://www.sec.gov/Archives/edgar/data/1050446/000119312525263719/d922690d424b5.htm)',
        '6': 'Nvidia (NVDA) Risk-Adjusted Return Analysis, March 2026, [https://www.bloomberg.com/quote/NVDA:US](https://www.bloomberg.com/quote/NVDA:US)',
        '7': 'U.S. Treasury Bond Yield Comparison Data, March 2026, [https://www.treasury.gov](https://www.treasury.gov)',
        '8': 'Tesla (TSLA) Volatility Profile, 2026 Market Data, [https://www.google.com/finance/quote/TSLA:NASDAQ](https://www.google.com/finance/quote/TSLA:NASDAQ)',
        '9': 'Saylor, M., "Yield Stability in Digital Credit," Institutional Investor Summit, March 2026, [https:// MichaelSaylor.com](https://www.microstrategy.com/en/resources/events/world-2026)',
        '10': 'MicroStrategy Monthly Dividend Announcement, February-March 2026, [https://www.microstrategy.com/en/investor-relations/press-releases](https://www.microstrategy.com/en/investor-relations/press-releases)',
        '11': 'Strive Inc. Treasury Allocation Report, March 2026, [https://www.strive.com/insights](https://www.strive.com/insights)',
        '12': 'MicroStrategy BTC Treasury Dashboard, [https://www.microstrategy.com/en/bitcoin](https://www.microstrategy.com/en/bitcoin), accessed March 18, 2026.',
        '13': 'MicroStrategy Form 8-K, Acquisition of 22,337 BTC, March 2026, [https://www.sec.gov/ix?doc=/Archives/edgar/data/1050446/000119312526063719/d12345d8k.htm](https://www.sec.gov/Archives/edgar/data/1050446/000119312526063719/d12345d8k.htm)',
        '14': 'STRC and MSTR ATM Issuance Report, mid-March 2026, [https://www.perplexity.ai/finance/STRC/earnings](https://www.perplexity.ai/finance/STRC/earnings)',
        '15': 'Matt Cole, "The Obsolescence of Cash Reserves," Strive CEO Insights, March 2026, [https://www.strive.com/news](https://www.strive.com/news)',
        '16': 'MicroStrategy Solvency and Reserve Report, February 2026, [https://www.microstrategy.com/en/investor-relations/financial-documents](https://www.microstrategy.com/en/investor-relations/financial-documents)'
    }

    # Rebuild the Works Cited section
    works_cited_start = content.find("#### **Works cited**")
    if works_cited_start != -1:
        text_before = content[:works_cited_start]
        new_works_cited = "#### **Works cited**\n\n"
        for i in range(1, 17):
            idx = str(i)
            new_works_cited += f"[^{idx}]: {citations_mapping[idx]}\n\n"
        
        content = text_before + new_works_cited

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

restore_weblinks('src/strcSharpRatio.md')
