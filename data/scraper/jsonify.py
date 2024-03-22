import re
import json

# Read the document
with open("./data/scraper/document.txt", "r") as file:
    document_text = file.read()

# Define a function to extract sections and paragraphs
def extract_sections_and_paragraphs(text):
    sections = []
    current_section = None
    paragraphs = []

    lines = text.split('\n')
    for line in lines:
        # Check if the line represents a section
        section_match = re.match(r'^SECTION (\d+)\. (.+)$', line)
        if section_match:
            if current_section is not None:
                sections.append({
                    "Section": current_section,
                    "Section Title": section_title,
                    "Paragraphs": paragraphs
                })
                paragraphs = []
            current_section = int(section_match.group(1))
            section_title = section_match.group(2).split('.')[0]  # Split at the first period
            paragraph = '.'.join(section_match.group(2).split('.')[1:]).strip()  # Get the paragraph
            if paragraph:
                paragraphs.append(paragraph)  # Add the paragraph if it exists
        else:
            if current_section is not None:
                # Check if the line represents a paragraph
                paragraph_match = re.match(r'^([a-zA-Z])\.', line)
                if paragraph_match:
                    paragraphs.append(line)
                elif paragraphs:  # Ensure there are paragraphs before concatenating
                    paragraphs[-1] += " " + line

    # Add the last section
    if current_section is not None:
        sections.append({
            "Section": current_section,
            "Section Title": section_title,
            "Paragraphs": paragraphs
        })

    return sections

# Extract sections and paragraphs
sections = extract_sections_and_paragraphs(document_text)

# Find Republic Act details
ra_match = re.search(r'Republic Act No\. (\d+)', document_text)
ra_date_match = re.search(r'March \d{2}, \d{4}', document_text)
ra_title_match = re.search(r'AN ACT .+?$', document_text, re.MULTILINE)

# Extract Republic Act details
ra_number = ra_match.group(1) if ra_match else None
ra_date = ra_date_match.group(0) if ra_date_match else None
ra_title = ra_title_match.group(0).strip() if ra_title_match else None

# Convert to JSON
json_data = {
    "Republic Act No.": ra_number,
    "Date": ra_date,
    "Republic Act Title": ra_title,
    "Sections": sections
}

# Write JSON data to file
with open("document.json", "w") as json_file:
    json.dump(json_data, json_file, indent=4)
