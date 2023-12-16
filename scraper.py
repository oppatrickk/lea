import requests
import json
from bs4 import BeautifulSoup

def scrape_philippine_constitution(url, output_file="philippine_constitution.json"):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
        # Send a GET request to the website with headers
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the elements containing the articles and sections
            articles_and_sections = soup.find_all(['h2', 'p'])

            # Initialize variables to store current article and section
            current_article = None
            current_section = None

            # Initialize a dictionary to store the constitution data
            constitution_data = {"title": "1987 Constitution of the Republic of the Philippines", "articles": []}

            # Iterate through each element
            for element in articles_and_sections:
                text = element.get_text().strip()

                # Check for the presence of "ARTICLE" in the text
                if "ARTICLE" in text:
                    # Extract the article number and title
                    article_number, _, article_title = text.partition(" ")
                    article_number = article_number.replace("ARTICLE", "").strip()

                    # Start a new article
                    current_article = {"article_no": article_number, "article_title": article_title, "sections": []}
                    constitution_data["articles"].append(current_article)
                    current_section = None
                elif current_article and "SECTION" in text:
                    # Start a new section within the current article
                    current_section = {"section_no": text, "content": ""}
                    current_article["sections"].append(current_section)
                elif current_section is not None:
                    # Add content to the current section
                    current_section["content"] += text + "\n"

            # Convert the constitution_data dictionary to JSON format
            constitution_json = json.dumps(constitution_data, indent=2, ensure_ascii=False)

            # Save the JSON data to a file
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(constitution_json)

            print(f"JSON data saved to {output_file}")
            return constitution_json
        else:
            print(f"Failed to retrieve content. Status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# URL of the Philippine Constitution page
constitution_url = "https://www.officialgazette.gov.ph/constitutions/1987-constitution/"

# Scrape text, remove HTML tags, and save as JSON file
scrape_philippine_constitution(constitution_url, output_file="philippine_constitution.json")
