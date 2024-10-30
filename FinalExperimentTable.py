from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests

# Define the extract_experiment_info function
def extract_experiment_info(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML contentm
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing experiment information
    table = soup.find('table', class_='alternate')

    # If table is not found, return empty lists
    if table is None:
        print(f"Table not found in the HTML content. Skipping URL: {url}")
        return [], [], [], [], []

    # Initialize lists to store experiment data
    experiment_names = []
    spacecraft_names = []
    principal_investigators = []
    experiment_links = []
    spacecraft_links = []

    # Extract experiment information from the table
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cols = row.find_all('td')
        if len(cols) >= 3:  # Ensure there are at least three columns
            experiment_name = cols[0].a.text.strip()
            spacecraft_name = cols[1].a.text.strip()
            principal_investigator = cols[2].text.strip()
            experiment_link = "https://nssdc.gsfc.nasa.gov" + cols[0].a['href']
            spacecraft_link = "https://nssdc.gsfc.nasa.gov" + cols[1].a['href']
            experiment_names.append(experiment_name)
            spacecraft_names.append(spacecraft_name)
            principal_investigators.append(principal_investigator)
            experiment_links.append(experiment_link)
            spacecraft_links.append(spacecraft_link)

    # Return the extracted experiment information
    return experiment_names, spacecraft_names, principal_investigators, experiment_links, spacecraft_links

# Initialize the WebDriver (replace 'chromedriver' with the path to your WebDriver executable)
driver = webdriver.Chrome()

# Load the webpage
driver.get("https://nssdc.gsfc.nasa.gov/nmc/SpacecraftQuery.jsp")

# Execute JavaScript to submit the form with "Planetary Science" selected
js_script = '''
document.querySelector("#name").value = "";
document.querySelector("#query_discipline").value = "PSNO";
document.forms["query"].submit();
'''
driver.execute_script(js_script)

# Wait for some time for the webpage to load
driver.implicitly_wait(5)  # Adjust the delay as needed

# Get the page source after form submission
page_source = driver.page_source

# Parse the HTML content
soup = BeautifulSoup(page_source, 'html.parser')

# Find the table containing spacecraft information
table = soup.find('table', class_='alternate')

# If table is not found, print a message and exit
if table is None:
    print("Table containing spacecraft information not found.")
    driver.quit()
    exit()

# Extract all links from the table
links = table.find_all('a')

# Iterate over the links
for link in links:
    href = link.get('href')

    # Construct the absolute URL for the spacecraft link
    spacecraft_absolute_url = "https://nssdc.gsfc.nasa.gov/nmc/" + href

    # Visit the spacecraft link
    spacecraft_response = requests.get(spacecraft_absolute_url)

    # If request to spacecraft link fails, skip to the next link
    if spacecraft_response.status_code != 200:
        print(f"Failed to visit spacecraft link: {spacecraft_absolute_url}. Skipping.")
        continue

    # Construct the URL for the second link (Experiment)
    # Extract the spacecraft ID from the href
    spacecraft_id = href.split("=")[-1]

    # Construct the absolute URL for the Experiment link
    experiment_absolute_url = f"https://nssdc.gsfc.nasa.gov/nmc/spacecraft/displayExperiment.action?spacecraftId={spacecraft_id}"

    # Visit the Experiment link and extract information
    experiment_names, spacecraft_names, principal_investigators, _, _ = extract_experiment_info(experiment_absolute_url)

    # Print the extracted experiment information
    for i in range(len(experiment_names)):
        print(f"Experiment Name: {experiment_names[i]}")
        print(f"Spacecraft Name: {spacecraft_names[i]}")
        print(f"Principal Investigator(s): {principal_investigators[i]}")
        print(f"Experiment Link: {experiment_absolute_url}")
        print(f"Spacecraft Link: {spacecraft_absolute_url}")
        print()

# Close the WebDriver
driver.quit()