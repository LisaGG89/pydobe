import pydobe

project = pydobe.objects.app.project

# Create some folders
# Add a comment and set a label colour
footage_folder = project.items.add_folder("Footage")
footage_folder.comment = "This is where we keep our footage"
footage_folder.label = "Fuchsia"

comps_folder = project.items.add_folder("Compositions")
comps_folder.comment = "This is where we keep our comps"
comps_folder.label = "Blue"

# Create a composition
my_comp = project.items.add_comp("My New Comp", 1920, 1080, 1, 100, 25)
my_comp.parent_folder = comps_folder
# duration is set using frames, to set duration using seconds
# ("My New Comp", 1920, 1080, 1, 4, 25, duration_as_frames=False)

# Add some footage
list_of_paths = ["path/to/my/file_01_v001_0000.png", "path/to/my/file_02_v001_0000.png", "path/to/my/file_03_v001_0000.png"]

for path in list_of_paths:
    footage = project.import_file(path)
    # Set the frame rate
    footage.main_source.conform_frame_rate = 24
    # Set the parent
    footage.parent_folder = footage_folder

# Replace the footage with a new version
list_of_replacement_paths = ["path/to/my/file_01_v002_0000.png", "path/to/my/file_02_v002_0000.png", "path/to/my/file_03_v002_0000.png"]

for footage in footage_folder.items:
    for new_path in list_of_replacement_paths:
        file_name = new_path.split("/")[-1]
        unique_file = file_name.rsplit("_", 2)[0]
        unique_footage = footage.name.rsplit("_", 2)[0]
        print(unique_footage)
        print(unique_file)
        if unique_file == unique_footage:
            footage.replace(new_path)
