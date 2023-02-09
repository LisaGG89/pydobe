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

# Add some footage
# Not implemented yet

# Create a composition
my_comp = project.items.add_comp("My New Comp", 1920, 1080, 1, 100, 25)
# duration is set using frames, to set duration using seconds:
# my_comp = project.items.add_comp("My New Comp", 1920, 1080, 1, 4, 25, duration_as_frames=False)
