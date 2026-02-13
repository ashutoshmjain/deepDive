import re
import sys

def clean_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove the specific problematic Unicode character
    content = content.replace('\u0332', '')

    # Fix the escaped plus sign in the table
    content = content.replace(r'\+65%', '+65%')
    # Fix the escaped minus sign in the table
    content = content.replace(r'\-2% to \-5%', '-2% to -5%')


    # Re-apply dollar sign fixes, as they seem to have been reverted
    content = content.replace('$5,000', 'USD 5,000')
    content = content.replace('$3.8 trillion to $5 trillion', 'USD 3.8 trillion to USD 5 trillion')
    content = content.replace('$190 billion', 'USD 190 billion')
    content = content.replace('$3.3 trillion', 'USD 3.3 trillion')
    content = content.replace('$1,500–$2,000', 'USD 1,500–USD 2,000')
    content = content.replace('$5,400 and $6,000', 'USD 5,400 and USD 6,000')
    content = content.replace('₹15,000', 'INR 15,000')
    content = content.replace('₹1.2', 'INR 1.2')
    content = content.replace('₹3.6', 'INR 3.6')



    # Also, it seems one of the URLs has a stray dollar sign.
    # Let's read the file again to be sure.
    # The error was in this file: src/indoChinaGoldRace.md
    # The URL is: https://timesofindia.indiatimes.com/business/india-business/higher-than-indias-gdp-value-of-household-gold-at-record-high-of-over-$5-trillion-why-even-rbi-is-buying-the-yellow-metal/articleshow/128154264.cms
    # I will replace this URL with a corrected one.
    content = content.replace('https://timesofindia.indiatimes.com/business/india-business/higher-than-indias-gdp-value-of-household-gold-at-record-high-of-over-$5-trillion-why-even-rbi-is-buying-the-yellow-metal/articleshow/128154264.cms',
                              'https://timesofindia.indiatimes.com/business/india-business/higher-than-indias-gdp-value-of-household-gold-at-record-high-why-even-rbi-is-buying-the-yellow-metal/articleshow/128154264.cms')


    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return "File cleaned successfully."

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(clean_markdown(sys.argv[1]))
    else:
        print("Please provide a file path.")
