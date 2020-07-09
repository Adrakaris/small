import json
import os
import crafting as c

# we gonna generate some data


def main():
    print("""JSON GENERATOR MENU
    Pick JSON to generate:
    [1] Recipe
    [2] Loot Table
    [E] Exit""")
    choice = input("Choice> ")
    while choice not in ["1", "2", "E", "e"]:
        choice = input("Invalid choice! Choice> ")
        
    choice = choice.lower()
    # run the choice cases
    cases = {"e": exit, "1": recipes, "2": loot_tables}
    file, name = cases[choice]()
    name = name.split(':')
    
    # write to file
    c = input("Push to file? y/n > ")
    if c.lower() == "y":
        with open(f"output/{name[1]}.json", "w+") as w:
            json.dump(file, w, ensure_ascii=False, indent=4)
        clr()
        print("write ok!")
    else:
        clr()
        print("File ignored.")
    main()


def clr():
    os.system("cls")
    
    
def recipes():
    output = {}
    
    # get type
    craft = "-1"
    craft_relationships = {
        1: "minecraft:crafting_shaped",
        2: "minecraft:crafting_shapeless",
        3: "minecraft:smelting",
        4: "minecraft:blasting",
        5: "minecraft:campfire_cooking",
        6: "minecraft:smoking",
        7: "minecraft:stonecutting",
        8: "minecraft:smithing"
    }
    print("Crafting type:")
    for i in craft_relationships:
        print(f"    {i}: {craft_relationships[i]}")
        
    while int(craft) not in craft_relationships.keys():
        craft = input("Enter type > ")
    craft = int(craft)
    output["type"] = craft_relationships[craft]  # add type to output
    
    # cases are different based on the type
    if craft == 1:  # shaped crafting
        return c.crafting_table(output)
    elif craft == 2:  # shapeless crafting
        return c.crafting_shapeless(output)
    elif craft in [3, 4, 5, 6]:  # any of the cooking things
        return c.smelting(output)
    elif craft == 7:
        return c.stonecutter(output)
    elif craft == 8:
        return c.smithing(output)

    
def loot_tables():
    print("Loot tables")
    raise NotImplementedError

if __name__ == "__main__":
    main()
