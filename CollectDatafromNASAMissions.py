from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

# Function to scrape data from a specific mission website
def scrape_mission_details(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            # Find the heading if present
            heading_element = soup.find('h1', class_='page-heading-md display-block width-full margin-0')
            if heading_element:
                return heading_element.text.strip()
    except requests.exceptions.RequestException as e:
        print("Error:", e)
    return "Heading not found"


# Function to scrape data from the NASA website
def scrape_nasa_missions(urls):
    # Initialize empty lists for each data point
    all_headings = []
    all_launch_sites = []
    all_launch_vehicles = []
    all_objectives = []
    all_spacecrafts = []
    all_spacecraft_masses = []
    all_launch_dates = []
    all_scientific_instruments = []

    # Iterate over each URL
    for url in urls:
        # Set up the ChromeDriver (make sure to have chromedriver installed and in your PATH)
        driver = webdriver.Chrome()
        # Open the webpage
        driver.get(url)
        # Get the page source after dynamic content has loaded
        page_source = driver.page_source
        # Close the browser
        driver.quit()

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the div with id "mission-terms-results-list"
        mission_results_div = soup.find('div', {'id': 'mission-terms-results-list'})

        # Check if the div is found
        if mission_results_div:
            # Find all anchor tags (links) within the div and visit each link
            for link in mission_results_div.find_all('a'):
                href = link.get('href')
                if href:
                    # Construct the absolute URL if the href is relative
                    absolute_url = urljoin(url, href)
                    print("Visiting:", absolute_url)

                    # Get the heading from the mission website
                    heading = scrape_mission_details(absolute_url)
                    print("Heading found:", heading)

                    # Check the status of the link
                    try:
                        response = requests.get(absolute_url)
                        if response.status_code == 200:
                            print("Status: OK")

                            # Parse the HTML content of the visited page
                            visited_soup = BeautifulSoup(response.content, 'html.parser')

                            # Find the table if present
                            table = visited_soup.find('table')
                            if table:
                                # If table is found, extract and store information
                                rows = table.find_all('tr')
                                data = {}  # Store scraped data in a dictionary
                                for row in rows:
                                    columns = row.find_all('td')
                                    if len(columns) == 2:
                                        key = columns[0].get_text().strip()
                                        value = columns[1].get_text().strip()
                                        data[key] = value

                                # Extract data from the dictionary, handling missing keys
                                all_headings.append(heading)
                                all_launch_sites.append(data.get('Launch Site', ''))
                                all_launch_vehicles.append(data.get('Launch Vehicle', ''))
                                all_objectives.append(data.get('Objective(s)', ''))
                                all_spacecrafts.append(data.get('Spacecraft', ''))
                                all_spacecraft_masses.append(data.get('Spacecraft Mass', ''))
                                all_launch_dates.append(data.get('Launch Date and Time', ''))
                                all_scientific_instruments.append(data.get('Scientific Instruments', ''))

                            else:
                                print("No table found on this page.")

                        else:
                            print(f"Status: {response.status_code}")
                    except requests.exceptions.RequestException as e:
                        print("Error:", e)
        else:
            print("Div with id 'mission-terms-results-list' not found on the page.")

    return all_headings, all_launch_sites, all_launch_vehicles, all_objectives, all_spacecrafts, all_spacecraft_masses, all_launch_dates, all_scientific_instruments


# URLs to scrape
urls = [
    "https://www.nasa.gov/missions/?terms=12882",
    "https://www.nasa.gov/missions/?terms=12882&page=2",
    "https://www.nasa.gov/missions/?terms=12270%2C12882&page=3"
]

# Scrape data
headings, launch_sites, launch_vehicles, objectives, spacecrafts, spacecraft_masses, launch_dates, scientific_instruments = scrape_nasa_missions(urls)

# Print the scraped data
print("\nScraped Mission Data:\n")
for i in range(len(headings)):
    print(f"Heading: {headings[i]}")
    print(f"Launch Site: {launch_sites[i]}")
    print(f"Launch Vehicle: {launch_vehicles[i]}")
    print(f"Objective: {objectives[i]}")
    print(f"Spacecraft: {spacecrafts[i]}")
    print(f"Spacecraft Mass: {spacecraft_masses[i]}")
    print(f"Launch Date: {launch_dates[i]}")
    print(f"Scientific Instrument: {scientific_instruments[i]}\n")
