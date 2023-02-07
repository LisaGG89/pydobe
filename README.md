# Pydobe

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg?style=flat-square)](https://www.python.org/)
[![License](http://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-black.svg?style=flat-square)](https://github.com/psf/black)
[![SemVer](https://img.shields.io/badge/semver-2.0.0-blueviolet?style=flat-square)](https://semver.org/)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/LisaGG89/pydobe/main?style=flat-square)

A Python wrapper allowing developers to communicate with adobe applications

This package is based upon Pymiere - created by Quentin Masingarbe (https://github.com/qmasingarbe/pymiere)

# Installation

Windows: 

``
pip install pydobe
``

# Use cases and examples

Snippets and examples for potential uses within After Effects

### Working with projects

```
app = pydobe.objects.app

# Open a Project
project_path = "path/to/my/project.aep"
app.open(project_path)

# Get path of current project
current_project = app.project.file
print(current_project)

# Save a Project
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

```


# Thanks

Thank you to Quentin Masingarbe for his Pymiere repository, as well as sharing his knowledge with me.

Thank you to Corentin Charron for constant mentoring.

# License

This project is licensed under the MIT License. See the LICENSE file for details. Copy it, steal it, modify it, share it!
# Contact

For support, questions, or interest, please contact me at lisa.gg89@gmail.com