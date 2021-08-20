import pandas as pd
import xml.etree.ElementTree as Xet
import os
import glob

# path of the folder that is to be converted
annotate_path = os.path.join(os.getcwd(), 'Annotations')

def xml_to_csv(annotate_path):

    xml_list = [] #Used to store the info parsed from xml file

    # Iterating through directories (if any)
    for directory in os.listdir(annotate_path):   
        # Iterating through XML files
        for xml_doc in glob.glob(annotate_path+f'/{directory}'+'/*.xml'):
            # parsing the xml file and storing it in root
            xmlparse  = Xet.parse(xml_doc)
            root = xmlparse .getroot()
            # Iterating throught all the object in the xml file
            for member in root.findall('object'):
                # Parsing the required infos form the xml file
                value=(root.find('filename').text,      #To find Filename
                       int(root.find('size')[0].text),      #To find height
                       int(root.find('size')[1].text),      #To find height
                       member[0].text,      #To find Name 
                       int(member[4][0].text),      #To find xmin
                       int(member[4][1].text),      #To find ymin
                       int(member[4][2].text),      #To find xmax
                       int(member[4][3].text)       #To find ymax
                      )

                xml_list.append(value)

    column_info = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax'] #column names for dataframe
    xml_dataframe = pd.DataFrame(xml_list, columns=column_info)
    return xml_dataframe

df = xml_to_csv(annotate_path)

def saving_the_file():
    print('Converting....')
    df.to_csv('test.csv')
    print('Successfully converted')

saving_the_file()
