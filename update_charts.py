import os
import re

def update_file(filepath, symbol, height=450):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find the Symbol Overview widget script
    # It looks for the script tag with symbol-overview.js and captures until </script>
    # We also want to capture the surrounding div if possible? 
    # The previous edits replaced the whole container.
    # Pattern: <div class="tradingview-widget-container">...<script...symbol-overview.js...</script>...</div>
    # But matching across lines is tricky.
    
    # improved regex: find the script tag, and replace it and potentially the container if we want to be exact.
    # But the user wants to replace the widget.
    # The structure is:
    # <div class="tradingview-widget-container">
    #    <div class="tradingview-widget-container__widget"></div>
    #    <script ... symbol-overview.js ... > ... </script>
    # </div>
    
    # We can replace the inner part or the whole thing.
    
    # Let's search for the specific script tag src.
    pattern = r'<script type="text/javascript"\s+src="https://s3\.tradingview\.com/external-embedding/embed-widget-symbol-overview\.js"\s+async>\s*\{.*?\n\s*\}\s*</script>'
    
    # The JSON inside might contain newlines, so we use DOTALL.
    
    new_widget = f"""<script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
                            {{
                                "width": "100%",
                                "height": {height},
                                "symbol": "{symbol}",
                                "interval": "D",
                                "timezone": "Asia/Tokyo",
                                "theme": "light",
                                "style": "1",
                                "locale": "ja",
                                "allow_symbol_change": true,
                                "calendar": false,
                                "support_host": "https://www.tradingview.com"
                            }}
                            </script>"""
    
    # We need to preserve the indentation of the original script tag if possible, or just apply a standard one.
    # The previous `replace_file_content` replaced the whole `tradingview-widget-container` div content or the div itself.
    # Let's target the script tag.
    
    match = re.search(pattern, content, re.DOTALL)
    if match:
        print(f"Found match in {filepath}")
        # print("Match:", match.group(0))
        new_content = content[:match.start()] + new_widget + content[match.end():]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
    else:
        print(f"No match found in {filepath}")

# Update Palantir
update_file(r'c:\Users\daiki\.gemini\antigravity\scratch\stock-analysis-blog\Palantir_article.html', 'NASDAQ:PLTR')

# Update Western Digital
# WDC has two charts: SNDK and WDC.
# The script above only replaces the first one found.
# usage for WDC needs to handle multiple.

def update_file_all(filepath, replacements):
    # replacements is a list of symbols to use for consecutive matches
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'<script type="text/javascript"\s+src="https://s3\.tradingview\.com/external-embedding/embed-widget-symbol-overview\.js"\s+async>\s*\{.*?\n\s*\}\s*</script>'
    
    # Find all matches
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    if not matches:
        print(f"No matches in {filepath}")
        return

    if len(matches) != len(replacements):
        print(f"Warning: Found {len(matches)} widgets but provided {len(replacements)} symbols for {filepath}")
    
    # We replace from last to first to keep indices valid
    for match, symbol in zip(reversed(matches), reversed(replacements)):
         new_widget = f"""<script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
                            {{
                                "width": "100%",
                                "height": 450,
                                "symbol": "{symbol}",
                                "interval": "D",
                                "timezone": "Asia/Tokyo",
                                "theme": "light",
                                "style": "1",
                                "locale": "ja",
                                "allow_symbol_change": true,
                                "calendar": false,
                                "support_host": "https://www.tradingview.com"
                            }}
                            </script>"""
         content = content[:match.start()] + new_widget + content[match.end():]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")

update_file_all(r'c:\Users\daiki\.gemini\antigravity\scratch\stock-analysis-blog\WesternDigital_article.html', ['NASDAQ:SNDK', 'NASDAQ:WDC'])
