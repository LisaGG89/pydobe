from pydobe.core import PydobeBaseObject, PydobeBaseCollection, format_to_extend
from pydobe.adobe_objects import File
from pydobe.after_effects.data import *
from pydobe.after_effects.ae_utils import *


# BASE OBJECTS


class Application(PydobeBaseObject):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)

    # PROPERTIES

    """ This is the current active project. """

    @property
    def project(self) -> object:
        kwargs = self._eval_on_this_object("project")
        return Project(**kwargs) if kwargs else None

    # FUNCTIONS

    def new_project(self, save: bool = None) -> object:
        """Create a new empty project."""
        if save is None:
            pass
        elif save:
            self.project.close(save=True)
        else:
            self.project.close(save=False)
        kwargs = self._eval_on_this_object("newProject()")
        return Project(**kwargs) if kwargs else None

    def open(self, path: str = None, save: bool = None) -> object:
        """A new Project object for the specified project, or null if the user cancels the Open dialog box."""
        if save is None:
            pass
        elif save:
            self.project.close(save=True)
        else:
            self.project.close(save=False)
        if path:
            file = File(**eval_script_returning_object(f'File("{path}")'))
            extend_file_object = format_to_extend(file)
            kwargs = self._eval_on_this_object(f"open({extend_file_object})")
        else:
            kwargs = self._eval_on_this_object(f"open()")
        return Project(**kwargs) if kwargs else None


class Project(PydobeBaseObject):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)

    # PROPERTIES

    """The item that is currently active and is to be acted upon, 
    or a null if no item is currently selected or if multiple items are selected."""

    @property
    def active_item(self) -> object:
        item = None
        kwargs = self._eval_on_this_object("activeItem")
        if not kwargs:
            raise TypeError("'active_item' requires precisely one item to be selected")
        type_name = self._eval_on_this_object("activeItem.typeName")
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
        return self._eval_on_this_object("dirty")

    """Identifies the file object containing the project"""

    @property
    def file(self) -> object:
        kwargs = self._eval_on_this_object("file")
        return File(**kwargs) if kwargs else None

    """All of the items in the project"""

    @property
    def items(self) -> object:
        kwargs = self._eval_on_this_object("items")
        return ItemCollection(**kwargs) if kwargs else None

    """The number of items within the project"""

    @property
    def num_items(self) -> int:
        return self._eval_on_this_object("numItems")

    """The root folder containing the contents of the project
    Items inside internal folders will not be shown"""

    @property
    def root_folder(self) -> object:
        kwargs = self._eval_on_this_object("rootFolder")
        return FolderItem(**kwargs) if kwargs else None

    # CUSTOM PROPERTIES

    """All of the composition items within the project"""

    @property
    def compositions(self) -> list:
        composition_items = []
        for item in self.items:
            if item.type_name == "Composition":
                composition_items.append(item)
        return composition_items

    """All of the footage items within the project"""

    @property
    def footages(self) -> list:
        footage_items = []
        for item in self.items:
            if item.type_name == "Footage":
                footage_items.append(item)
        return footage_items

    """All of the folder items within the project"""

    @property
    def folders(self) -> list:
        folder_items = []
        for item in self.items:
            if item.type_name == "Folder":
                folder_items.append(item)
        return folder_items

    # FUNCTIONS

    def close(self, save: bool = None) -> bool:
        """This will close the current project with an option to save changes or not"""
        if save is None:
            return self._eval_on_this_object(
                "close(CloseOptions.PROMPT_TO_SAVE_CHANGES)"
            )
        elif save:
            return self._eval_on_this_object("close(CloseOptions.SAVE_CHANGES)")
        else:
            return self._eval_on_this_object("close(CloseOptions.DO_NOT_SAVE_CHANGES)")

    def import_file(self, path: str, sequence: bool = False, force_alphabetical: bool = False):
        """This will import a file"""
        import_options = ImportOptions(**eval_script_returning_object('new ImportOptions()'))
        file = File(**eval_script_returning_object(f'File("{path}")'))
        import_options.file = file
        import_options.sequence = sequence
        import_options.force_alphabetical = force_alphabetical
        extend_import_options = format_to_extend(import_options)
        kwargs = self._eval_on_this_object(f'importFile({extend_import_options})')
        return FootageItem(**kwargs)

    def save(self, path: str = None) -> bool:
        """This will save the current scene"""
        if path:
            file = File(**eval_script_returning_object(f'File("{path}")'))
            extend_file_object = format_to_extend(file)
            return self._eval_on_this_object(f"save({extend_file_object})")
        else:
            return self._eval_on_this_object("save()")

    # CUSTOM FUNCTIONS

    def item_by_name(self, name: str) -> object:
        """Get an item by its name from within this project"""
        for item in self.items:
            if item.name == name:
                return item
        raise LookupError("There is no item by this name in your project")


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
        return self._eval_on_this_object("comment")

    @comment.setter
    def comment(self, value: str):
        self._eval_on_this_object(f'comment = "{value}"')

    """A unique and persistent identification number used internally to identify an item between sessions"""

    @property
    def id(self) -> int:
        return self._eval_on_this_object("id")

    """The colour of the label assigned to the item, expressed as an integer between 1-16. 0 = none"""

    @property
    def label(self) -> int:
        return self._eval_on_this_object("label")

    @label.setter
    def label(self, value: int or str):
        if type(value) == int:
            int_value = value
        else:
            int_value = label_dictionary[value]
        self._eval_on_this_object(f"label = {int_value};")

    """The name of the item as displayed in the Project panel"""

    @property
    def name(self) -> str:
        return self._eval_on_this_object("name")

    @name.setter
    def name(self, value: str):
        self._eval_on_this_object(f'name = "{value}"')

    """The folder object that the item is parented to"""

    @property
    def parent_folder(self) -> object:
        kwargs = self._eval_on_this_object("parentFolder")
        return FolderItem(**kwargs) if kwargs else None

    @parent_folder.setter
    def parent_folder(self, value: object):
        if value.type_name == "Folder":
            extend_value = format_to_extend(value)
            self._eval_on_this_object(f"parentFolder = {extend_value}")
        else:
            raise TypeError("Unable to set 'parent_folder', type must be 'Folder'")

    """Whether the item is selected or not, multiple items can be selected at the same time"""

    @property
    def selected(self) -> bool:
        return self._eval_on_this_object("selected")

    @selected.setter
    def selected(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_this_object(f'selected = "{extend_value}"')

    """User readable name for Item type"""

    @property
    def type_name(self) -> str:
        return self._eval_on_this_object("typeName")

    # FUNCTIONS

    def remove(self):
        """Deletes this item from the project and the Project panel.
        If the item is a FolderItem, all the items contained in the folder are also removed from the project
        """
        self._eval_on_this_object("remove()")


class AVItem(Item):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)


class CompositionItem(AVItem):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)


class FolderItem(Item):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)

    # PROPERTIES

    """All of the items in the folder"""

    @property
    def items(self) -> object:
        kwargs = self._eval_on_this_object("items")
        return ItemCollection(**kwargs) if kwargs else None

    """The number of items within the folder"""

    @property
    def num_items(self) -> int:
        return self._eval_on_this_object("numItems")

    # CUSTOM PROPERTIES

    """The composition items found in the folder"""

    @property
    def compositions(self) -> list:
        composition_items = []
        for item in self.items:
            if item.type_name == "Composition":
                composition_items.append(item)
        return composition_items

    """The footage items found in the folder"""

    @property
    def footages(self) -> list:
        footage_items = []
        for item in self.items:
            if item.type_name == "Footage":
                footage_items.append(item)
        return footage_items

    """The folder items found in the folder"""

    @property
    def folders(self) -> list:
        folder_items = []
        for item in self.items:
            if item.type_name == "Folder":
                folder_items.append(item)
        return folder_items


class FootageItem(AVItem):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)

    # PROPERTIES

    """The footage source, an object that contains all of the settings related to that footage item, 
    including those that are normally accessed through the Interpret Footage dialog box"""

    @property
    def main_source(self) -> object:
        item = None
        kwargs = self._eval_on_this_object('mainSource')
        object_type = kwargs["object_type"]
        if object_type == "FileSource":
            item = FileSource(**kwargs)
        elif object_type == "SolidSource":
            item = SolidSource(**kwargs)
        elif object_type == "PlaceholderSource":
            item = PlaceHolderSource(**kwargs)
        return item

    """The file object associated with this footage"""

    @property
    def file(self) -> object:
        kwargs = self._eval_on_this_object('file')
        return File(**kwargs) if kwargs else None

    # FUNCTIONS

    def open_in_viewer(self):
        """Opens the comp in a panel, moves it to the front and gives it focus"""
        kwargs = self._eval_on_this_object('openInViewer()')
        return Viewer(**kwargs)

    def replace(self, path: str):
        """Changes the source of this Footage Item to the specified file"""
        file = File(**eval_script_returning_object(f'File("{path}")'))
        extend_file_object = format_to_extend(file)
        self._eval_on_this_object(f'replace({extend_file_object})')

    def replace_with_placeholder(self, name: str, width: int, height: int, frame_rate: float, duration: float,
                                 duration_as_frames=True):
        """Changes the source of this FootageItem to the specified placeholder"""
        if duration_as_frames:
            duration = current_format_to_time(duration, frame_rate)
        self._eval_on_this_object(f'replaceWithPlaceholder("{name}", {width}, {height}, {frame_rate}, {duration})')


    def replace_with_sequence(self, path: str, force_alphabetical: bool = False):
        """Changes the source of this Footage Item to the specified image sequence."""
        file = File(**eval_script_returning_object(f'File("{path}")'))
        extend_file_object = format_to_extend(file)
        force_alphabetical = format_to_extend(force_alphabetical)
        self._eval_on_this_object(f'replaceWithSequence({extend_file_object}, {force_alphabetical})')

    def replace_with_solid(self, colour: list, name: str, width: int, height: int, pixel_aspect: float):
        """Changes the source of this FootageItem to the specified solid"""
        self._eval_on_this_object(f'replaceWithSolid({colour},"{name}", {width}, {height}, {pixel_aspect})')


# SOURCES

class FootageSource(PydobeBaseObject):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id)
        self.object_type = object_type

    # PROPERTIES

    @property
    def type_name(self):
        return self.object_type


class FileSource(FootageSource):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)


class SolidSource(FootageSource):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)


class PlaceHolderSource(FootageSource):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)


# COLLECTIONS

class ItemCollection(PydobeBaseCollection):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id, "length")

    def __getitem__(self, index: int):
        item = None
        index = index + 1
        kwargs = super(ItemCollection, self).__getitem__(index)
        type_name = self._eval_on_this_object(extend_property="typeName", index=index)
        if type_name == "Composition":
            item = CompositionItem(**kwargs)
        if type_name == "Footage":
            item = FootageItem(**kwargs)
        elif type_name == "Folder":
            item = FolderItem(**kwargs)
        return item

    # FUNCTIONS

    def add_comp(
        self,
        name: str,
        width: int,
        height: int,
        aspect_ratio: float,
        duration: float,
        frame_rate: float,
        duration_as_frames=True,
    ) -> object:
        """Add a new Composition to the project"""
        if duration_as_frames:
            duration = current_format_to_time(duration, frame_rate)
        kwargs = self._eval_on_this_object(
            f'addComp("{name}", {width}, {height}, {aspect_ratio}, {duration}, {frame_rate})'
        )
        return CompositionItem(**kwargs)

    def add_folder(self, name: str) -> object:
        """Add a new Folder to the project"""
        kwargs = self._eval_on_this_object(f'addFolder("{name}")')
        return FolderItem(**kwargs)


# MISC

class ImportOptions(PydobeBaseObject):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)

    """The file object to be imported"""

    @property
    def file(self) -> object:
        kwargs = self._eval_on_this_object('file')
        return File(**kwargs) if kwargs else None

    @file.setter
    def file(self, value: object):
        extend_object = format_to_extend(value)
        self._eval_on_this_object(f"file = {extend_object}")

    """Creates sequence from available files in alphateical order with no gaps"""

    @property
    def force_alphabetical(self) -> bool:
        return self._eval_on_this_object('forceAlphabetical')

    @force_alphabetical.setter
    def force_alphabetical(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_this_object(f"forceAlphabetical = {extend_value}")

    """Import as sequence"""

    @property
    def sequence(self) -> bool:
        return self._eval_on_this_object('sequence')

    @sequence.setter
    def sequence(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_this_object(f"sequence = {extend_value}")


class Viewer(PydobeBaseObject):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)
