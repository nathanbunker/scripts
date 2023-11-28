import xml.etree.ElementTree as ET

def parse_field(segment_name, field_element, field_position):
    name = field_element.get('Name')
    data_type = field_element.get('Datatype')
    max_occurrence = field_element.get('max')
    usage = field_element.get('Usage')
    return f"{segment_name}-{field_position} {name}: is a {data_type} data type, with usage {usage} that can be sent {max_occurrence} times."

def parse_segment(segment_name, segment_element):
    fields = segment_element.findall('Field')
    field_descriptions = [parse_field(segment_name, f, i) for i, f in enumerate(fields)]
    return field_descriptions

def main():
    tree = ET.parse('VXU-Z22-Profile.xml')  # Replace with your XML file path
    root = tree.getroot()
    segments = root.findall('.//Segment')

    for i, segment in enumerate(segments):
        segment_name = segment.get('Name')
        description = segment.get('Description')

        print(f"The {segment_name} {description} segment contains these fields:")
        descriptions = parse_segment(segment_name, segment)
        for desc in descriptions:
            print(f"  {desc}")

if __name__ == "__main__":
    main()
# Replace 'your_file.xml' with the path to your XML file. This script will read the file, go through each segment, and print the narrative for each field. Adjust as needed.





