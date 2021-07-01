# Terraform to JSON converter
<p>This script & demo is useful for converting Terraform .tf file to a JSON document. Moreover this script targets the variables defined in terraform file and converts them into JSON documents.

---
### Note
1. Python script uses **python-hcl2** package 
2. Script is provided with features like to mark variables as Hidden or Read-only. This property will be set if those respective keywords mentioned in the variable description.
~~~
    variable "subnet_name" { 
    type = string 
    default = "internal"
    description = "Hide - Subnet Name" 
    }
~~~
> This Terraform code will be converted into JSON along with the hidden property set to true.
~~~
    variable "subscription_id" { 
    type = string 
    description = "Read only - subscription id" 
    }
~~~

> This Terraform code will be converted into JSON along with the Edit property set to false [Read-only]. By **default** set to **true**.

3. Each JSON document will have 5 properties set in result
    <br> For example:-
~~~
{
    "Name": "subnet_name",
    "Type": "string",
    "Default": "internal",
    "Hide": "True",
    "Edit": "True" 
}
~~~  
---
## Workflow Diagram
![Design View](https://github.com/mynameisjai/Terraform_JSON_converter/blob/main/media/Terraform_json.PNG?raw=true)
---
### Prerequisite
- Define the paths of the following in the py script:-
    - Input Terraform script
    - Output Json file
- Install python package **python-hcl2**
---
- Author : Jayasakthiram N <br>
- Input File: terraform_to_json.py <br>
- Date Modified: 02nd July 2021 
---
