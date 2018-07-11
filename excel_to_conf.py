import pandas
import json
from lxml import etree

pandas.set_option('display.height', 1000)
pandas.set_option('display.max_rows', 6)
pandas.set_option('display.max_columns', 5)
pandas.set_option('display.width', 1000)

conf_dataframe = pandas.read_excel("output.xlsx", sheet_name=None)


##Let create tree out of the conf dataframe

complex_elements = conf_dataframe.keys()

element_dict = {}
variables_dict = {}

process_list = ["root"]

for item in process_list:

    item_dict = {0:{"PARENT": "", "DATA": {"element": item}}}

    for n, row in conf_dataframe[item].iterrows():

        if row["Element"] in complex_elements:
            process_list.append(row["Element"])
            #item_dict[n] = {"PARENT": 0, "DATA": {"element": row["Element"], "text": row["Element"]}}

        else:

            item_dict[n+1] = {"PARENT": "0", "DATA": {"element": row["Element"], "text": "{" + row["Element"] + "}", "attributes": {"usage": row["Usage"], "type": row["Type"], "description": row["Description"]}}}
            variables_dict[row["Element"]] = row["Type"]
            if row["Element"] == row["Type"]:
                print("Warning - complex element missing in conf -> {}".format(row["Type"]))

        element_dict[item] = item_dict


conf_files = {"internal_conf": element_dict,
              "default_variables": variables_dict}

for key in conf_files:
    with open("{}.json".format(key), "w") as file:
        json.dump(conf_files[key], file, indent=4)





##Old code to ceoorect the inital excel conf file
##conf_dataframe = pandas.read_excel("EN.xlsx",header = None, sheet_name=None)

##modified_dataframe = {}

##for key in conf_dataframe.keys():

##    conf_dataframe[key].rename(columns={0: 'Element', 5: 'Usage', 7: "Type", 3: "Description"}, inplace=True)


#print(conf_dataframe["INVOICELINE"][["Element", "Usage", "Type", "Description"]]) #3

##    dataframe = conf_dataframe[key][["Element", "Usage", "Type", "Description"]].copy(deep=True)

##    for i, row in dataframe.iterrows():
##        dataframe.iloc[i, 3] = row["Description"].split(" Description ")[1]

##    modified_dataframe[key] = dataframe


##writer = pandas.ExcelWriter('output.xlsx')
##for key in modified_dataframe.keys():
##    modified_dataframe[key].to_excel(writer,key)

##writer.save()