from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

from utils import parse_table_to_df


ESMA_PROS_URL = 'https://registers.esma.europa.eu/publication/searchRegister?core=esma_registers_priii_documents'
ESMA_DOC_DOWNLOAD_BASE_URL = 'https://registers.esma.europa.eu/publication/'


# Function to click the "next" page if it's active
def click_next_page(driver):
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
    except:
        print("No more active 'next' button found.")
        return False



def main():
    driver = webdriver.Firefox()

    try:
        driver.get(ESMA_PROS_URL)

        # Wait for the page to load completely
        time.sleep(2)

        # select doctype 
        dropdown_doc_type = Select(driver.find_element(By.NAME, "document_type"))
        dropdown_doc_type.select_by_value("BPWO") # Base prospectus without Final terms
        # select home member state
        dropdown_home_member_state = Select(driver.find_element(By.NAME, "home_member_state_code"))
        dropdown_home_member_state.select_by_value("NL") # Netherlands 

        # Click the search button
        search_button = driver.find_element(By.ID, "searchSolrButton")
        search_button.click()

        time.sleep(1)

        # Select the dropdown element by its id and choose the option "100"
        n_items_dropdown = Select(driver.find_element(By.ID, "tablePageSize"))
        n_items_dropdown.select_by_value("100")

        time.sleep(3)

        # Loop through all pages until "next" is inactive
        while click_next_page(driver):
            # Add logic here to parse each page's content
            pass


        # # Get doc download links
        # page_source = driver.page_source
        # soup = BeautifulSoup(page_source, 'html.parser')
        # # Find all document links in the table with id "T01"
        # table = soup.find("table", {"id": "T01"})

        # table_df = parse_table_to_df(table)
        # # creat working download link
        # table_df['physical_doc_downl_url'] = ESMA_DOC_DOWNLOAD_BASE_URL + table_df['Physical Document'].astype(str)

  

        print(table_df.head())
        print(table_df['physical_doc_downl_url'].iloc[0])
        print(table_df.columns)

    finally:
        # Close the browser
        driver.quit()



if __name__ == '__main__':
    main()


