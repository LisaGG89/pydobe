import pydobe

# Retrieve project object
print(pydobe.objects.app.project)

# With after effects open you should receive a project object
# With after effects closed you should receive a Connection Error
