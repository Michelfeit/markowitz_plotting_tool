import pandas as pd
import re
from data_cache.dax_wiki.dax_marketcap_data import dax_data
from data_cache.dax_wiki.dax_ticker_data import dax_ticker_data
from logger import log_dataframe


def longest_common_prefix_len(a, b):
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    return i

# Function to find the best match from df2 for each row in df1
def match_by_longest_prefix(row, df2):
    best_match = None
    best_len = 0
    for idx, name in df2['Name'].items():
        lcp_len = longest_common_prefix_len(row['Company'], name)
        if lcp_len > best_len:
            best_len = lcp_len
            best_match = df2.loc[idx]
    return pd.Series(best_match)

  # Replace with your full string
def extract_df_from_wikidata():
    pd.set_option('expand_frame_repr', True)
    pd.set_option('display.max_colwidth', 150)
    # Extract rows using regex
    pattern = r'\|\sstyle="text-align:left"\s\|\s(.*?)\s<!--.*?-->\s\|\|\s[\d,]+,\d+\s<!--.*?-->\s\|\|\s([\d,.]+)'
    matches = re.findall(pattern, dax_data)
    # Convert to DataFrame
    df = pd.DataFrame(matches, columns=["Company", "MarketCap (€Mio)"])

    # Convert German-style numbers to float (comma as decimal, dot as thousands separator)
    df["MarketCap (€Mio)"] = df["MarketCap (€Mio)"].str.replace('.', '', regex=False)
    df["MarketCap (€Mio)"] = df["MarketCap (€Mio)"].str.replace(',', '.', regex=False).astype(float)
    df.replace('DHL Group (ex Deutsche Post)', 'DHL Group', inplace=True)
    df.replace('adidas', 'Adidas', inplace=True)

    # Use regex to extract (name, ticker) pairs
    pattern = r"\|\s*\[\[(?:[^\]|]+\|)?([^\]]+)\]\]\s*\n\|\s*([A-Z0-9]+)"
    matches = re.findall(pattern, dax_ticker_data)
    # Create a DataFrame for mapping
    ticker_df = pd.DataFrame(matches, columns=["Name", "Ticker"])
    # Optional: clean names to match original DataFrame if needed
    ticker_df["Name"] = ticker_df["Name"].str.strip()
    ticker_df.replace('Deutsche Post', 'DHL Group', inplace=True)

    matched_df = df.apply(lambda row: match_by_longest_prefix(row, ticker_df), axis=1)

    # Combine matched rows
    merged = pd.concat([df.reset_index(drop=True), matched_df.reset_index(drop=True)], axis=1)
    df = merged[["Name","Ticker", "MarketCap (€Mio)"]]

    n = df["MarketCap (€Mio)"].sum()
    share = df["MarketCap (€Mio)"].to_numpy()
    assert (share/n).sum() == 1
    df["Share"] = (share/n)
    df.columns = ["Company","Ticker", "MarketCap (€Mio)", "Share"]
    log_dataframe(df)