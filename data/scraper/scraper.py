import os
import requests
from bs4 import BeautifulSoup
import random

def scrape_philippine_constitution(url):
    try:
         # Select a random user agent from the list
        user_agents_ = [
            'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
        ]
        headers = {'User-Agent': random.choice(user_agents_)}

        # Send a GET request to the website with headers
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the title of the website
            website_title = soup.title.string.strip()

            # Define the data folder and create it if it doesn't exist
            data_folder = "data"
            if not os.path.exists(data_folder):
                os.makedirs(data_folder)

            # Define the republic_acts subfolder and create it if it doesn't exist
            republic_acts_folder = os.path.join(data_folder, "republic_acts")
            if not os.path.exists(republic_acts_folder):
                os.makedirs(republic_acts_folder)

            # Define subfolders for txt and html within republic_acts
            txt_folder = os.path.join(republic_acts_folder, "txt")
            html_folder = os.path.join(republic_acts_folder, "html")

            # Create subfolders if they don't exist
            if not os.path.exists(txt_folder):
                os.makedirs(txt_folder)
            if not os.path.exists(html_folder):
                os.makedirs(html_folder)

            # Save the raw HTML to a file within the html subfolder
            html_output_file = os.path.join(html_folder, f"{website_title}_raw.html")
            with open(html_output_file, 'w', encoding='utf-8') as html_file:
                html_file.write(str(soup))

            print(f"Raw HTML data saved to {html_output_file}")

            # Initialize a list to store the constitution text
            constitution_text = []

            # Find all paragraphs within the body
            paragraphs = soup.find('body').find_all('p')

            # Iterate through each paragraph
            for paragraph in paragraphs:
                text = paragraph.get_text().strip() + "\n"
                constitution_text.append(text)

            # Use the website title as the filename for the text file within the txt subfolder
            text_output_file = os.path.join(txt_folder, f"{website_title}.txt")
            with open(text_output_file, 'w', encoding='utf-8') as text_file:
                text_file.write('\n'.join(constitution_text))

            print(f"Text data saved to {text_output_file}")
            return '\n'.join(constitution_text)
        else:
            print(f"Failed to retrieve content. Status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
pass
# URL of the Philippine Constitution page
constitution_url = ["https://lawphil.net/consti/cons1987.html",
                    "https://lawphil.net/executive/execord/eo1987/eo_209_1987.html",
                    "https://lawphil.net/executive/execord/eo1987/eo_227_1987.html",
                    # "https://lawphil.net/statutes/repacts/ra1949/ra_386_1949.html",
                    "https://lawphil.net/statutes/presdecs/pd1974/pd_442_1974.html",
                    "https://lawphil.net/statutes/presdecs/pd1974/pd_603_1974.html",
                    "https://lawphil.net/statutes/acts/act_3815_1930.html",
                    "https://lawphil.net/statutes/repacts/ra2009/ra_9710_2009.html",
                    "https://lawphil.net/statutes/repacts/ra1989/ra_6725_1989.html",
                    "https://lawphil.net/statutes/repacts/ra1990/ra_6955_1990.html",
                    "https://lawphil.net/statutes/repacts/ra2016/ra_10906_2016.html",
                    "https://lawphil.net/statutes/repacts/ra1992/ra_7610_1992.html",
                    "https://lawphil.net/statutes/repacts/ra2003/ra_9231_2003.html",
                    "https://lawphil.net/statutes/repacts/ra2006/ra_9344_2006.html",
                    "https://lawphil.net/statutes/repacts/ra2009/ra_9775_2009.html",
                    # "https://lawphil.net/statutes/repacts/ra2022/ra_11930_2022.html",
                    # "https://lawphil.net/statutes/repacts/ra2021/ra_11596_2021.html",
                    "https://lawphil.net/statutes/repacts/ra2004/ra_9262_2004.html",
                    "https://lawphil.net/statutes/repacts/ra2013/ra_10398_2013.html",
                    "https://lawphil.net/statutes/repacts/ra2019/ra_11313_2019.html",
                    "https://lawphil.net/statutes/repacts/ra1997/ra_8353_1997.html",
                    "https://lawphil.net/statutes/repacts/ra1998/ra_8505_1998.html",
                    "https://lawphil.net/statutes/repacts/ra2000/ra_8972_2000.html",
                    "https://lawphil.net/statutes/repacts/ra2022/ra_11861_2022.html",
                    "https://lawphil.net/statutes/repacts/ra2003/ra_9208_2003.html",
                    "https://lawphil.net/statutes/repacts/ra1997/ra_8369_1997.html",
                    "https://lawphil.net/statutes/repacts/ra2012/ra_10354_2012.html",
                    "https://lawphil.net/statutes/repacts/ra2010/ra_9995_2010.html"
]

for url in constitution_url:
    try:
        print(f"Scraping {url}")
        scraped_text = scrape_philippine_constitution(url)
        if scraped_text:
            print(f"Text data saved to {os.path.join('data', 'republic_acts', f'{os.path.basename(url)}.txt')}")
        else:
            print(f"Failed to scrape text data from {url}")
    except Exception as e:
        print(f"An error occurred while scraping {url}: {str(e)}")

# You don't need to call the function again after the loop
