from pydobe.core import PydobeBaseObject, PydobeBaseCollection, format_to_extend, eval_script_returning_object


# BASE OBJECTS

class Application(PydobeBaseObject):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)

    # PROPERTIES

    """ This is the current active project. """

    @property
    def project(self):
        kwargs = self._eval_on_this_object('project')
        return Project(**kwargs) if kwargs else None

    # FUNCTIONS

    def new_project(self, save=None):
        """ Create a new empty project."""
        if save is None:
            pass
        elif save:
            self.project.close(save=True)
        else:
            self.project.close(save=False)
        kwargs = self._eval_on_this_object('newProject()')
        return Project(**kwargs) if kwargs else None

    def open(self, path=None):
        """A new Project object for the specified project, or null if the user cancels the Open dialog box."""
        if path:
            file = File(path, **eval_script_returning_object(f'File("{path}")'))
            extend_file_object = format_to_extend(file)
            return self._eval_on_this_object(f'open({extend_file_object})')
        else:
            return self._eval_on_this_object(f'open()')


class Project(PydobeBaseObject):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)

    # PROPERTIES

    """Returns True if file has been modified since last save. False if it has not"""

    @property
    def dirty(self) -> bool:
        return self._eval_on_this_object('dirty')

    """Identifies the file object containing the project"""

    @property
    def file(self) -> object:
        kwargs = self._eval_on_this_object('file')
        return File(**kwargs) if kwargs else None

    # FUNCTIONS

    def close(self, save=None):
        """This will close the current project with an option to save changes or not"""
        if save is None:
            return self._eval_on_this_object('close(CloseOptions.PROMPT_TO_SAVE_CHANGES)')
        elif save:
            return self._eval_on_this_object('close(CloseOptions.SAVE_CHANGES)')
        else:
            return self._eval_on_this_object('close(CloseOptions.DO_NOT_SAVE_CHANGES)')

    def save(self, path: str = None):
        """This will save the current scene"""
        if path:
            file = File(path, **eval_script_returning_object(f'File("{path}")'))
            extend_file_object = format_to_extend(file)
            return self._eval_on_this_object(f'save({extend_file_object})')
        else:
            return self._eval_on_this_object('save()')

# ITEMS

class Item(PydobeBaseObject):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)

    def __str__(self):
        return self.name

class AVItem(Item):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)

class CompositionItem(AVItem):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)

class FolderItem(Item):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)

class FootageItem(AVItem):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)

# ADOBE GENERAL OBJECTS

class File(PydobeBaseObject):
    def __init__(self, path=None, pydobe_id=None):
        super().__init__(pydobe_id)

    def __str__(self):
        return self.full_name

    # PROPERTIES

    "The full path name"

    @property
    def full_name(self):
        return self._eval_on_this_object('fullName')

    "The file name portion of the absolute URI, without the path specification."

    @property
    def name(self):
        return self._eval_on_this_object('name')

    "The path portion of the absolute URI, without the file name"

    @property
    def path(self):
        return self._eval_on_this_object('path')