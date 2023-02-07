from pydobe.core import PydobeBaseObject, PydobeBaseCollection, format_to_extend, eval_script_returning_object
from pydobe.after_effects.data import *


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

    """The item that is currently active and is to be acted upon, 
    or a null if no item is currently selected or if multiple items are selected."""

    @property
    def active_item(self) -> object:
        item = None
        kwargs = self._eval_on_this_object('activeItem')
        type_name = self._eval_on_this_object('activeItem.typeName')
        if type_name == "Composition":
            item = CompositionItem(**kwargs)
        elif type_name == "Footage":
            item = FootageItem(**kwargs)
        elif type_name == "Folder":
            item = FolderItem(**kwargs)
        return item

    """Returns True if file has been modified since last save. False if it has not"""

    @property
    def dirty(self) -> bool:
        return self._eval_on_this_object('dirty')

    """Identifies the file object containing the project"""

    @property
    def file(self) -> object:
        kwargs = self._eval_on_this_object('file')
        return File(**kwargs) if kwargs else None

    """All of the items in the project"""

    @property
    def items(self):
        kwargs = self._eval_on_this_object('items')
        return ItemCollection(**kwargs) if kwargs else None

    """The number of items within the project"""

    @property
    def num_items(self):
        return self._eval_on_this_object('numItems')

    """The root folder containing the contents of the project
    Items inside internal folders will not be shown"""

    @property
    def root_folder(self):
        kwargs = self._eval_on_this_object('rootFolder')
        return FolderItem(**kwargs) if kwargs else None

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

    # PROPERTIES

    """A string that holds a comment, the comment is for the user’s purpose only"""

    @property
    def comment(self) -> str:
        return self._eval_on_this_object('comment')

    @comment.setter
    def comment(self, value: str):
        self._eval_on_this_object(f'comment = "{value}"')

    """A unique and persistent identification number used internally to identify an item between sessions"""

    @property
    def id(self) -> int:
        return self._eval_on_this_object('id')

    """The colour of the label assigned to the item, expressed as an integer between 1-16. 0 = none"""

    @property
    def label(self) -> int:
        return self._eval_on_this_object('label')

    @label.setter
    def label(self, value: int or str):
        if type(value).__name__ == 'int':
            int_value = value
        else:
            int_value = label_dictionary[value]
        self._eval_on_this_object(f"label = {int_value};")

    """The name of the item as displayed in the Project panel"""

    @property
    def name(self) -> str:
        return self._eval_on_this_object('name')

    @name.setter
    def name(self, value: str):
        self._eval_on_this_object(f'name = "{value}"')

    """The folder object that the item is parented to"""

    @property
    def parent_folder(self) -> object:
        kwargs = self._eval_on_this_object('parentFolder')
        return FolderItem(**kwargs) if kwargs else None

    @parent_folder.setter
    def parent_folder(self, value: object):
        if value.type_name == "Folder":
            extend_value = format_to_extend(value)
            self._eval_on_this_object(f'parentFolder = {extend_value}')
        else:
            raise TypeError("Unable to set 'parent_folder', type must be 'Folder'")

    """Whether the item is selected or not, multiple items can be selected at the same time"""

    @property
    def selected(self) -> bool:
        return self._eval_on_this_object('selected')

    @selected.setter
    def selected(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_this_object(f'selected = "{extend_value}"')

    """User readable name for Item type"""

    @property
    def type_name(self) -> str:
        return self.eval_on_this_object('typeName')

    # FUNCTIONS

    def remove(self):
        """Deletes this item from the project and the Project panel.
        If the item is a FolderItem, all the items contained in the folder are also removed from the project"""
        return self.eval_on_this_object("remove()")



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


# COLLECTIONS

class ItemCollection(PydobeBaseCollection):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id, "length")


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
