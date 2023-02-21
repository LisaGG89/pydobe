import pydobe

project = pydobe.objects.app.project

# Create a new composition

my_comp = project.item_by_name("My Comp")
footage_folder = project.item_by_name("My Footage")

# Check the settings of the composition

print(my_comp.width)
print(my_comp.height)
print(my_comp.duration)
print(my_comp.bg_colour)

# Adjust the settings of the composition

my_comp.width = 1920
my_comp.height = 1080
my_comp.duration = 50
my_comp.bg_colour = [0.1, 0.7, 0.8]

# Create a new layer within your composition using your footage
for footage in footage_folder.items:
    my_comp.layers.add(footage)

# Check which compositions your footage is used in
for footage in footage_folder.items:
    print(footage.used_in)

# Check number of layers in the composition
print(my_comp.num_layers)

# Set the work area duration in your comp

my_comp.work_area_start = 0
my_comp.work_area_duration = 2

# Hide the shy layers in your composition

my_comp.hide_shy_layers = True

# Check if motion Blur is turned on
print(my_comp.motion_blur)
