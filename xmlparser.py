import xml.etree.ElementTree as ET

# Parse XML intro ElementTree
tree = ET.parse('P2778.xml')
root = tree.getroot()

print(root.tag)