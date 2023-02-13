import pydobe

project = pydobe.objects.app.project

# Check how many items are in the project
print(project.num_items)

# Get the names of all the items in the project
for item in project.items:
    print(item.name)
    # check which items are selected
    if item.selected:
        print(f"{item.name} is selected")

# Get the active item
my_item = project.active_item  # This attribute requires precisely 1 item to be selected

# Find out what type of item it is
print(my_item.type_name)

# Find the parent folder of the item
print(my_item.parent_folder)

# Get all compositions
for comp in project.compositions:
    print(comp.name)

# Get item by name
footage_folder = project.item_by_name("My Footage")

# Remove items from the scene:
for child in footage_folder.items:
    child.remove()
