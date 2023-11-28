import xml.etree.ElementTree as ET


def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root

def generate_mapping(root):
    mappings = {}
    usage_map = {'R': 'required', 'RE': 'required, when information is available', 'O': 'optional'}
    for message in root.findall('.//Message'):
        msg_type = message.get('Type')
        msg_identifier = message.get('Identifier')
        msg_name = message.get('Name')

        def process_segment(segment, group_info1=None, group_info2=None):
            ref = segment.get('Ref')
            usage = segment.get('Usage')
            seg_name = ref[:3]

            usage_desc = usage_map.get(usage, usage)

            description = f"The {seg_name} segment is {usage_desc} ({usage})"
            if group_info2:
                description += f" within the {group_info1} segment group, which is within the {group_info2} segment group"
            elif group_info1:
                description += f" within the {group_info1} segment group"

            description += f" for the {msg_name} ({msg_type}) {msg_identifier} message."
            return seg_name, description

        for segment in message.findall('./Segment'):
            seg_name, description = process_segment(segment)
            mappings[seg_name] = description
            print(f"--> Segment: {seg_name}")

        for group in message.findall('./Group'):
            group_id = group.get('ID').split('.')[1]  # Remove 'VXU_V04' prefix
            group_usage = group.get('Usage')
            group_usage_desc = usage_map.get(group_usage, group_usage)
            print(f"--> Group: {group_id}")

            for segment in group.findall('./Segment'):
                seg_name, description = process_segment(segment, f"{group_usage_desc} ({group_usage}) {group_id}")
                mappings[seg_name] = description
                print(f"-->   Segment: {seg_name}")

                for sg in group.findall('./Group'):
                    sg_id = sg.get('ID').split('.')[1]  # Remove 'VXU_V04' prefix
                    sg_usage = sg.get('Usage')
                    sg_usage_desc = usage_map.get(sg_usage, sg_usage)
                    print(f"-->      Group: {sg_usage_desc} ({sg_usage}) {sg_id}")

                    for s in sg.findall('./Segment'):
                        s_name, description = process_segment(s, f"{group_usage_desc} ({group_usage}) {group_id}", f"{sg_usage_desc} ({sg_usage}) {sg_id}")
                        print(f"-->        Segment: {s.get('Ref')}")
                        mappings[s_name] = description

    return mappings

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
field_mapping = parse_xml_and_generate_mapping(file_path)

root = parse_xml('VXu-Z22-Profile.xml')
segment_mappings = generate_mapping(root)

# Print the mapping
for key, value in field_mapping.items():
    segment_name = key.split('-')[0];
    print(f"'{key}' => '{value} {segment_mappings[segment_name]}'")
