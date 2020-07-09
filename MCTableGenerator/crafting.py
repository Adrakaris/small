import json
import os


def clr():
    os.system("cls")


def crafting_table(output):
    clr()
    print("CRAFTING - SHAPED")
    output["pattern"] = []
    output["key"] = {}
    output["result"] = {}
    
    # get pattern
    pattern = get_pattern()
    output["pattern"] = [i for i in pattern]
    print()
    
    # key logic
    keys = []
    for line in output["pattern"]:
        for char in line:
            if char not in keys and char != " ":
                keys.append(char)
    
    print(f'Key Characters: {keys}')
    print("Enter key as (type).(item)")
    print("Example: item.minecraft:diamond")
    for k in keys:
        ktype, kitem = its(f"    Key {k} > ")
        output["key"][ktype] = kitem
    
    # result
    print("Crafting result")
    rtype, ritem = its("    (type).(item) > ")
    rcount = input("    Count > ")
    output["result"][rtype] = ritem
    output["result"]["count"] = int(rcount)
    print()

    print("Result:")
    print(json.dumps(output, indent=4))
    print()
    return output, ritem


def crafting_shapeless(output):
    clr()
    print("CRAFTING - SHAPELESS")
    output["ingredients"] = []
    output["result"] = {}
    
    print("Enter ingredient as (type).(item), or xxx to exit")
    print("Example: item.minecraft:diamond")
    # get ingredients
    while True:
        ins = input("    Ingredient > ")
        if ins == "xxx":
            break
        itype, iitem = ins.split(".")
        output["ingredients"].append({itype: iitem})
    
    print()
    # result
    print("Crafting result")
    rtype, ritem = its("    (type).(item) > ")
    rcount = input("    Count > ")
    output["result"][rtype] = ritem
    output["result"]["count"] = int(rcount)
    print()

    print("Result:")
    print(json.dumps(output, indent=4))
    print()
    return output, ritem
    

def smelting(output):
    clr()
    print("ANY SMELTING")
    output["ingredient"] = {}
    output["result"] = ""
    output["experience"] = 0  # def 0.1
    output["cookingtime"] = 0  # def 200 furnace

    print("Enter items as (type).(item)")
    print("Example: item.minecraft:diamond\n")
    
    # get ingredient
    print("Ingredient:")
    itype, iitem = its("    (type).(item) > ")
    output["ingredient"][itype] = iitem
    print()
    
    # get result
    print("Result (DO NOT enter type):")
    ritem = input("    (item) > ")
    output["result"] = ritem
    print()
    
    # get times and stuff
    print("Other values (leave blank for default)")
    try:
        exp = float(input("    Experience (default 0.1) > "))
    except ValueError:
        exp = 0.1
    try:
        cooktime = int(input("    Cooking Time (furnace::default 200) > "))
    except ValueError:
        cooktime = 200
    output["experience"] = exp
    output["cookingtime"] = cooktime
    print()

    print("Result:")
    print(json.dumps(output, indent=4))
    print()
    return output, ritem


def stonecutter(output):
    clr()
    output["ingredient"] = {}
    output["result"] = ""
    output["count"] = 0

    print("Enter items as (type).(item)")
    print("Example: item.minecraft:diamond\n")

    # get ingredient
    print("Ingredient:")
    itype, iitem = its("    (type).(item) > ")
    output["ingredient"][itype] = iitem
    print()

    # get result
    print("Result (DO NOT enter type):")
    ritem = input("    (item) > ")
    output["result"] = ritem
    rcount = int(input("    count > "))
    output["count"] = rcount
    print()

    print("Result:")
    print(json.dumps(output, indent=4))
    print()
    return output, ritem


def smithing(output):
    clr()
    output["base"] = {}
    output["addition"] = {}
    output["result"] = {}
    print("Enter items as (type).(item)")
    print("Example: item.minecraft:diamond\n")

    # get base
    print("Base:")
    btype, bitem = its("    (type).(item) > ")
    output["base"][btype] = bitem
    print()
    
    # get addition
    print("Addition:")
    atype, aitem = its("    (type).(item) > ")
    output["addition"][atype] = aitem
    print()

    # get result
    print("Result:")
    rtype, ritem = its("    (type).(item) > ")
    output["result"][rtype] = ritem
    print()

    print("Result:")
    print(json.dumps(output, indent=4))
    print()
    return output, ritem


def get_pattern():
    n_lines = int(input("How many lines > "))
    n_list = []
    lr = 0
    for i in range(n_lines):
        r = input(f"Line {i} > ")
        if len(r) > lr:
            lr = len(r)
        n_list.append(r)
    for i in range(len(n_list)):
        while len(n_list[i]) < lr:
            n_list[i] += " "
    
    print()
    print(f"Lines: {n_list}")
    satisfied = input("Satisfied? Y/N > ")
    if satisfied.lower() == "y":
        return n_list
    else:
        return get_pattern()
    
    
def its(prompt):
    i = input(prompt)
    itype, iitem = i.split(".")
    return itype, iitem
