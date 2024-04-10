import glob
import os

xml_files = glob.glob("*.xml")

# Loop through each XML file and run the functions on it
for i, xml_file in enumerate(xml_files):
    # Extract the number from the filename and store it in a variable
    filename = os.path.splitext(os.path.basename(xml_file))[0]
    # Extract the numeric part from the filename
    numero_rpi = ''.join(filter(str.isdigit, filename))

    if numero_rpi: 
        numero_rpi = int(numero_rpi)
        print(f"Processing {xml_file}... for {numero_rpi}!")

        print(f"Done processing {xml_file}.")
    else:
        print(f"Skipping {xml_file}, no numeric part found in the filename!")