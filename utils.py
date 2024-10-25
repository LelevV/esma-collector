import pandas as pd 
from bs4 import BeautifulSoup


def parse_table_to_df(table):
    """
    Parses an HTML table (as a BeautifulSoup object) into a pandas DataFrame.

    Args:
        table (bs4.element.Tag): BeautifulSoup element containing the HTML table.

    Returns:
        pd.DataFrame: DataFrame with table data and document links.
    """
    # Extract headers
    headers = [header.text for header in table.find_all("th")]
    
    # Extract rows
    rows = []
    for row in table.find_all("tr")[1:]:  # Skip header row
        cells = row.find_all("td")
        row_data = []  
        for cell in cells:
            # Check for an anchor link in the cell
            link = cell.find("a", href=True)
            # Use link URL if no text is present, else None
            cell_text = cell.get_text(strip=True) or (link['href'] if link else None)
            row_data.append(cell_text)
        rows.append(row_data)
    
    # Create and return DataFrame
    return pd.DataFrame(rows, columns=headers)
