"""Run this file to check the IP selenium is using to perform requests."""

from selenium import webdriver
from bs4 import BeautifulSoup
import time


def check_ip() -> str:
    """Function to get current IP address using Selenium"""
    # Set up the Firefox driver
    driver = webdriver.Firefox()

    try:
        # Navigate to an IP-checking service
        driver.get("https://api.ipify.org?format=json")

        # Wait for the page to load completely
        time.sleep(3)

        # Extract the IP address from the page
        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')
        # Locate the element that contains the IP address
        ip_element = soup.find("tr", id="/ip").find("span", class_="objectBox-string")
        # Extract and clean the IP address text
        ip_address = ip_element.text.strip('"')

        print(f"Your current IP address is: {ip_address}")
        return ip_address

    finally:
        # Close the browser
        driver.quit()


if __name__ == '__main__':
    check_ip()
