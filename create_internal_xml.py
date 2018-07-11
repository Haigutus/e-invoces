import json
from lxml import etree
from pprint import pprint

def create_XML_from_conf(conf_dic):
    """Create XML file from dictionary conf input"""
    end_key       = len(conf_dic)-1
    current_key   = 0

    xml_elements_dic = {}

    while current_key <= end_key:

        element_name = conf_dic[str(current_key)]["DATA"]["element"]

        #print (element_name) #DEBUG

        #Create Element
        #CHECK if root element
        if (current_key == 0):
            element = etree.Element(element_name)

        else:
            parent_name  = xml_elements_dic[conf_dic[str(current_key)]["PARENT"]]

            #print (element_name, parent_name) #DEBUG

            element = etree.SubElement(parent_name, element_name)

            #Set Element attributes

        if "attributes" in conf_dic[str(current_key)]["DATA"]:

            for attrib_key in conf_dic[str(current_key)]["DATA"]["attributes"]:

                element.attrib[attrib_key] = conf_dic[str(current_key)]["DATA"]["attributes"][attrib_key]

        #Set Element text value

        element.text = conf_dic[str(current_key)]["DATA"].get("text", "")

        #Add current Element to element list

        xml_elements_dic[str(current_key)] = element

        #Move to next element
        current_key+=1

    xml_file = etree.tostring(xml_elements_dic["0"], pretty_print=True)
    return xml_file.decode('UTF-8')
    #return xml_elements_dic["0"]

def append_XML_object(root, message_template_dictionary, variables_dictionary):
    parser = etree.XMLParser(remove_blank_text=True)

    if root == "create_root":

        root = etree.XML(create_XML_from_conf(message_template_dictionary).format(**variables_dictionary), parser = parser)
        return root

    else:
        root.append(etree.XML(create_XML_from_conf(message_template_dictionary).format(**variables_dictionary), parser = parser))


def remove_root(text_xml):
    without_root = text_xml[text_xml.find('>')+1:text_xml.rfind('<')]
    return without_root

def load_json(file_path_or_fileobject):

    if type(file_path_or_fileobject) == str:
        with open(file_path_or_fileobject) as file:
            loaded_json = json.load(file)
    else:
        loaded_json = json.load(file_path_or_fileobject)

    return loaded_json


internal_message_conf   = load_json("internal_conf.json")
variables_conf          = load_json("default_variables.json")

root        = append_XML_object("create_root", internal_message_conf["root"],variables_conf)

INVOICENOTE = append_XML_object("create_root", internal_message_conf["INVOICENOTE"],variables_conf)

root.append(INVOICENOTE)


with open("test.xml", "w") as file:

    xml_string = etree.tostring(root, pretty_print=True)
    file.write(xml_string.decode('utf-8'))