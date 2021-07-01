#Required Libraries
import json
import hcl2
import re

#set the input and output paths
terraform_variable_file = 'filepath/terraform.tf'
output_file = 'output/filepath/filename.json'

#The list that holds the JSON
output_json = []

#Method that stores result in a JSON file
def write_template(template,output_file):
    with open(output_file, 'w') as json_file:
        json.dump(template, json_file,indent=4)
    print("\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\tTemplate stored in file",
          output_file, 
          "\n\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
#Calculations on defining the properties
def allowed_values(v):
    for l in v['validation'][0]['condition']:
        l =re.sub("[\$\{\}=\" ]", "", l)
        l = re.sub("var.", "", l)
    return l
def visiblity(v):
    list_possiblity  =  ['Hide','Hidden']
    try:

        if (list_possiblity[0].lower() in v['description'][0].lower() or 
            list_possiblity[1].lower() in v['description'][0].lower()
            ):
            return True
        else:
            return False
    except:
            return False

def edit(v):
    list_possiblity  =  ['Read Only']
    try:
        if (list_possiblity[0].lower() in v['description'][0].lower()):
            return True
        else:
            return False
    except:
        return False
def check_fields(k,v):

    try:
        if(v['default']!=[] and v['validation']!=[]):
            
            
            l = allowed_values(v)
                
            output_json.append({'name':k,
                            "type":re.sub("[\$\{\}]", "", v['type'][0]),
                            "allowedvalues":re.sub(k, "", l).split("||"),
                            "default":v['default'][0],
                            'Hide':visiblity(v),
                            'Edit':edit(v)
                            })
                
    except:
        
        try:
            if (v['default']!=[]):
                output_json.append({'name':k,
                            "type":re.sub("[\$\{\}]", "", v['type'][0]),
                            "default":v['default'][0],
                            'Hide':visiblity(v),
                            'Edit':edit(v)
                            })
        except:
            try:
                
                if (v['validation']!=[]):
                    l = allowed_values(v)
                    
                    output_json.append({'name':k,
                            "type":re.sub("[\$\{\}]", "", v['type'][0]),
                            "allowedvalues":re.sub(k, "", l).split("||"),
                            'Hide':visiblity(v),
                            'Edit':edit(v)
                            })
            except:
                
                output_json.append({'name':k,
                            "type":re.sub("[\$\{\}]", "", v['type'][0]),
                            'Hide':visiblity(v),
                            'Edit':edit(v)
                            })

def conversion():
    with open(terraform_variable_file, 'r') as file:
        dict = hcl2.load(file)
    for i in dict['variable']:
        for k,v in i.items():
            check_fields(k, v)

    write_template(output_json, output_file)
#Code begins here
if __name__ == "__main__":
    conversion()
    #Output_JSON list is cleared after successfull creation of JSON file as it is a global variable
    output_json.clear()
    

