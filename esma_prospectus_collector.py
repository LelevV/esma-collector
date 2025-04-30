""" 
Run this script to collect metadata about prospectus document 
    from the ESMA register using Selenium
"""

import pandas as pd
import time
import os

from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utils import scrape_esma_table, click_next_page
from config import CONFIG_DICT


def apply_filters(driver, home_member_state_code=None) -> None:
        """Put all your filters for ESMA prospectus Register here"""
         
        # select doctype 
        dropdown_doc_type = Select(driver.find_element(By.NAME, "document_type"))
        dropdown_doc_type.select_by_value("BPWO") # Base prospectus without Final terms

        time.sleep(1)
        
        if home_member_state_code:
            # select home member state
            dropdown_home_member_state = Select(
                driver.find_element(By.NAME, home_member_state_code)
            )
            dropdown_home_member_state.select_by_value("NL") # Netherlands 

            time.sleep(1)

        #  add language as option 
        # Locate the dropdown element by its ID
        extra_filer_dropdown = Select(driver.find_element(By.ID, "ID005"))
        # Select the "Language" option by visible text
        extra_filer_dropdown.select_by_visible_text("Language")

        time.sleep(1)

        # select English
        dropdown_language = Select(driver.find_element(By.NAME, "document_language_code"))
        dropdown_language.select_by_value("en")  

        time.sleep(1)

        # add language as col in results 
        add_col_button = driver.find_element(By.CLASS_NAME, "displayColumn")
        add_col_button.click()

        time.sleep(1)

        # Locate the "Language" checkbox using its ID
        language_checkbox = driver.find_element(By.ID, "document_languages")
        # Click the checkbox
        language_checkbox.click()

        # click update
        # Locate the "Update" button using its class name
        update_button = driver.find_element(By.XPATH, "//button[text()='Update']")
        update_button.click()


def main():
    # create datafolder if does not exist
    os.makedirs(os.path.dirname(CONFIG_DICT['DATA_FOLDER']), exist_ok=True)

    driver = webdriver.Firefox()

    try:
        driver.get(CONFIG_DICT['ESMA_PROS_REGISTER_URL'])

        # Wait for the page to load completely
        time.sleep(2)

        # apply filters for ESMA Prospectus Register
        apply_filters(driver)

        time.sleep(2)

        # Click the search button
        search_button = driver.find_element(By.ID, "searchSolrButton")
        search_button.click()

        time.sleep(2)

        # Select the dropdown element by its id and choose the option "100"
        n_items_dropdown = Select(driver.find_element(By.ID, "tablePageSize"))
        n_items_dropdown.select_by_value("100")

        time.sleep(2)

        # scrape table 
        table_df = scrape_esma_table(driver)
        table_df_list = [table_df]

        # Loop through all pages until "next" is inactive
        while click_next_page(driver):
            table_df = scrape_esma_table(driver)
            table_df_list.append(table_df)

        # concat all table dfs
        final_df = pd.concat(table_df_list, ignore_index=True)

        # add working download link 
        final_df['physical_doc_downl_url'] = (
             CONFIG_DICT['ESMA_DOC_DOWNLOAD_BASE_URL'] + final_df['Physical Document'].astype(str)
        )

        # add file name
        final_df['file_name'] = (
            (
                final_df['Issuer(s) Name / LEI'].str.replace(' ', '_')
                + '__' + final_df['Prospectus Type'].str.replace(' ', '_') 
                + '__' + final_df['Approval or filing date'].str.replace(' ', '_').replace('/', '-', regex=True)
            ).replace([r'\.', ','], '', regex=True)
            + '.pdf'
        )

        # write result to csv 
        final_df.to_csv(
             CONFIG_DICT['DATA_FOLDER'] + CONFIG_DICT['METADATA_RESULT_CSV'], 
             index=False, encoding="utf-8", sep=";"
        )

    finally:
        # Close the browser
        driver.quit()


if __name__ == '__main__':
    main()


