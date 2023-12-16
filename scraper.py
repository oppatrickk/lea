import os
import requests
from bs4 import BeautifulSoup

def scrape_philippine_constitution(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
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
                text = paragraph.get_text().strip()
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

# URL of the Philippine Constitution page
constitution_url = "https://lawphil.net/consti/cons1987.html"

# Scrape text and save as text file with the website title as the filename
scrape_philippine_constitution(constitution_url)
