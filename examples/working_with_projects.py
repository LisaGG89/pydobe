import pydobe

app = pydobe.objects.app

# Open a Project
project_path = "path/to/my/project.aep"
app.open(project_path)

# Get path of current project
current_project = app.project.file
print(current_project)

# # Save a Project
app.project.save()

# Save a Project to a new path
new_path = "path/to/my/new/project.aep"
app.project.save(new_path)

# Make some changes to your project

# Check if scene has been modified
print(app.project.dirty)

# # Close a Project
app.project.close()  # This will display a user prompt
# app.project.close(save=True)  # This will save before opening a new project
# app.project.close(save=False)  # This will not save before opening a new project


# Create a new Project
app.new_project()  # This will display a user prompt
# app.new_project(save=True)  # This will save before opening a new project
# app.new_project(save=False)  # This will not save before opening a new project
