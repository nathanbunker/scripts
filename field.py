import xml.etree.ElementTree as ET

def parse_xml_and_generate_mapping(file_path):
    # Define the usage description mapping
    usage_description = {
        "R": "required",
        "RE": "required, but may be empty",
        "O": "optional",
        "X": "not supported"
    }

    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Initialize a dictionary for the mappings
    mappings = {}

    segments = root.find("Segments");

    # Iterate over each segment in the XML
    for segment in segments.findall('Segment'):
        segment_name = segment.attrib['Name']
        segment_description = segment.attrib['Description']
        field_number = 1

        # Iterate over each field in the segment
        for field in segment.findall('Field'):
            field_name = field.attrib['Name']
            field_usage = field.attrib['Usage']
            usage_desc = usage_description.get(field_usage, "")

            # Generate the mapping key and value
            key = f"{segment_name}-{field_number}"
            value = f"{key} {field_name} field is {usage_desc} for {segment_description} ({segment_name}) segment. "

            # Add the mapping to the dictionary
            mappings[key] = value
            field_number += 1

    return mappings

# Example usage
file_path = 'VXU-Z22-Profile.xml'
mapping = parse_xml_and_generate_mapping(file_path)

# Print the mapping
for key, value in mapping.items():
    print(f"'{key}' => '{value}'")
