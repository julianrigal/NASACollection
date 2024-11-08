import requests
from bs4 import BeautifulSoup

# URL of the webpage
url = "https://nssdc.gsfc.nasa.gov/nmc/spacecraft/displayExperiment.action?spacecraftId=2001-013A"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing experiment links
    table = soup.find('table', class_='alternate')

    # Find all 'td' tags within the first and second column of the table
    first_column_tds = table.select('tbody tr td:nth-of-type(1)')
    second_column_tds = table.select('tbody tr td:nth-of-type(2)')

    # Extract links and text from the first and second columns
    for td1, td2 in zip(first_column_tds, second_column_tds):
        # Find the 'a' tag within the current 'td' in the first column
        link = td1.find('a')
        if link:
            href = link.get('href')
            full_url = f"https://nssdc.gsfc.nasa.gov{href}"  # Construct the full URL

            # Send a GET request to the experiment link
            response_link = requests.get(full_url)

            # Check if the request was successful (status code 200)
            if response_link.status_code == 200:
                # Parse the HTML content of the experiment link
                soup_link = BeautifulSoup(response_link.content, 'html.parser')

                # Find all <p> tags within the experiment link
                paragraphs = soup_link.find_all('p')

                # Extract and print text within <p> tags
                for paragraph in paragraphs:
                    print(paragraph.text.strip())

                # Extract and print text from the second column
                print("Spacecraft Name:", td2.get_text(strip=True))

                print("\n")  # Add a separator between experiments
            else:
                print(f"Failed to retrieve the experiment link: {full_url}")
else:
    print("Failed to retrieve the webpage.")