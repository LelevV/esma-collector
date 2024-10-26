import pandas as pd 
from bs4 import BeautifulSoup
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def click_next_page(driver):
    """Function to click the "next" page if it's active"""
    try:
        # Locate the "next" page element
        wait_sec = 3
        next_button = WebDriverWait(driver, wait_sec).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.next a.active"))
        )
        if next_button:
            next_button.click()
            time.sleep(2)  # Allow time for the page to load
            return True
    except Exception as e:
        print(f"Error occurred: {e}")
        print("No more active 'next' button found.")
        return False


def scrape_esma_table(driver):
    """Scrape table from ESMA prospects register and transform to df""" 
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    # Find all document links in the table with id "T01"
    table = soup.find("table", {"id": "T01"})
    table_df = parse_table_to_df(table)
    return table_df


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
