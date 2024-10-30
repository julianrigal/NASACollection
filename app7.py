from flask import Flask, jsonify
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

app = Flask(__name__)

# Function to scrape the heading and status from a specific mission website
def scrape_mission_details(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the heading if present
            heading_element = soup.find('h1', class_='page-heading-md display-block width-full margin-0')
            heading = heading_element.text.strip() if heading_element else "Heading not found"

            # Find the mission status if present
            status_element = soup.find('div', class_='label tag tag-mission mission-status-spacer')
            status = status_element.find('span').text.strip() if status_element else "Status not found"

            return heading, status
    except requests.exceptions.RequestException as e:
        print("Error:", e)
    return "Heading not found", "Status not found"

# Function to scrape all mission headings and statuses from the NASA missions page
def scrape_nasa_mission_headings(urls):
    all_headings_and_statuses = []

    for url in urls:
        # Set up the ChromeDriver (ensure chromedriver is installed and in your PATH)
        driver = webdriver.Chrome()
        driver.get(url)
        page_source = driver.page_source
        driver.quit()

        soup = BeautifulSoup(page_source, 'html.parser')
        mission_results_div = soup.find('div', {'id': 'mission-terms-results-list'})

        if mission_results_div:
            for link in mission_results_div.find_all('a'):
                href = link.get('href')
                if href:
                    absolute_url = urljoin(url, href)
                    heading, status = scrape_mission_details(absolute_url)
                    all_headings_and_statuses.append((heading, status))
        else:
            print("Div with id 'mission-terms-results-list' not found on the page.")

    return all_headings_and_statuses

# Endpoint to scrape mission data
@app.route('/nasa_scrape', methods=['GET'])
def nasa_scrape():
    # URLs to scrape
    urls = [
        "https://www.nasa.gov/missions/?terms=10828%2C10873%2C12882",
        "https://www.nasa.gov/missions/?terms=10828%2C10873%2C12882&page=2",
        "https://www.nasa.gov/missions/?terms=10828%2C10873%2C12882&page=3",
        "https://www.nasa.gov/missions/?terms=10828%2C10873%2C12882&page=4"
    ]

    # Scrape mission headings and statuses
    headings_and_statuses = scrape_nasa_mission_headings(urls)

    # Prepare response data
    response_data = [{'heading': heading, 'status': status} for heading, status in headings_and_statuses]

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
