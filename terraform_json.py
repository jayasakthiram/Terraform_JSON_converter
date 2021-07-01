import json
import hcl2
import re

terraform_variable_file = 'filepath/terraform.tf'
output_file = 'output/filepath/filename.json'
output_json = []

def write_template(template,output_file):
    with open(output_file, 'w') as json_file:
        json.dump(template, json_file,indent=4)
    print("\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\tTemplate stored in file",
          output_file, 
          "\n\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
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
if __name__ == "__main__":
    conversion()
    output_json.clear()

