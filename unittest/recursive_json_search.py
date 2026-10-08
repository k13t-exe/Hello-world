from test_data import *
from policy import *

def check_RBAC(key,role):
    avl_roles = ["admin", "operator", "viewer"]
    if role not in avl_roles: # Only available roles
        return False
    return key not in POLICY or role in POLICY[key] # Show non-sensitive fields & check permission
    
def show_fields(value,role):
    if isinstance(value, dict): # Case 1: value is dict
        res = {}
        for k, v in value.items():
            if check_RBAC(k,role):
                res[k] = show_fields(v,role)
        return res
    elif isinstance(value, list): # Case 2: value is list
        res = []
        for item in value:
            res.append(show_fields(item,role))
        return res
    else:
        return value # Case 3: normal value

def json_search(key,input_object,role=None):
    ret_val=[]
        
    if isinstance(input_object, dict): # Iterate dictionary
        for k, v in input_object.items(): # searching key in the dict
            if not check_RBAC(key,role):
                continue
            if k == key:
                temp={k:show_fields(v,role)}
                ret_val.append(temp)
            if isinstance(v, dict): # the value is another dict so repeat
                ret_val.extend(json_search(key,v,role))
            elif isinstance(v, list): # it's a list
                for item in v:
                    if not isinstance(item, (str,int)): # if dict or list repeat
                        ret_val.extend(json_search(key,item,role))
    else: # Iterate a list because some APIs return JSON object in a list
        for val in input_object:
            if not isinstance(val, (str,int)):
                ret_val.extend(json_search(key,val,role))
    return ret_val

#print(json_search("issueSummary",data,"hacker"))
#print(json_search("connectedDevice",data,"viewer"))
#print(json_search("apiKey",data,"admin"))
#print(json_search("managementIpAddress",data,"operator"))
#print(json_search("managementIpAddress",data,"viewer"))
#print(json_search("connectedDevice",data,"admin"))

