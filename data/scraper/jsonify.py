import re
import json

# Read the document
with open("document.txt", "r") as file:
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
                    "section": current_section,
                    "title": section_title,
                    "paragraphs": paragraphs
                })
                paragraphs = []
            current_section = int(section_match.group(1))
            section_title = section_match.group(2)
        else:
            # Check if there are any paragraphs in the list
            if paragraphs:
                # If there are, concatenate the line with the last paragraph
                paragraphs[-1] += " " + line
            else:
                # If not, append the line as a new paragraph
                paragraphs.append(line)


    # Add the last section
    sections.append({
        "section": current_section,
        "title": section_title,
        "paragraphs": paragraphs
    })

    return sections

# Extract sections and paragraphs
sections = extract_sections_and_paragraphs(document_text)

# Convert to JSON
json_data = json.dumps(sections, indent=4)

# Write JSON data to file
with open("document.json", "w") as json_file:
    json_file.write(json_data)
