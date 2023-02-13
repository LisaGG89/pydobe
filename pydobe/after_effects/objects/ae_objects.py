from pydobe.core import PydobeBaseObject, PydobeBaseCollection, format_to_extend
from pydobe.adobe_objects import File
from pydobe.utils import format_colour
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

    def import_file(
            self, path: str, sequence: bool = False, force_alphabetical: bool = False
    ):
        """This will import a file"""
        import_options = ImportOptions(
            **eval_script_returning_object("new ImportOptions()")
        )
        file = File(**eval_script_returning_object(f'File("{path}")'))
        import_options.file = file
        import_options.sequence = sequence
        import_options.force_alphabetical = force_alphabetical
        extend_import_options = format_to_extend(import_options)
        kwargs = self._eval_on_this_object(f"importFile({extend_import_options})")
        return FootageItem(**kwargs) if kwargs else None

    def save(self, path: str = None) -> bool:
        """This will save the current scene"""
        if path:
            file = File(**eval_script_returning_object(f'File("{path}")'))
            extend_file_object = format_to_extend(file)
            return self._eval_on_this_object(f"save({extend_file_object})")
        else:
            return self._eval_on_this_object("save()")

    def save_with_dialog(self) -> bool:
        """This will prompt the user to save with a dialog box"""
        return self._eval_on_this_object('saveWithDialog()')

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

    # PROPERTIES

    """All of the layers in the composition"""

    @property
    def layers(self):
        kwargs = self._eval_on_this_object('layers')
        return LayerCollection(**kwargs) if kwargs else None


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

    # FUNCTIONS

    def item(self, sub_index: int) -> object:
        """Returns the top-level item in this folder at the specified index position."""
        item = None
        sub_index += 1
        kwargs = self._eval_on_this_object(f"item({sub_index})")
        type_name = self._eval_on_this_object(f"item({sub_index}).typeName")
        if type_name == "Composition":
            item = CompositionItem(**kwargs)
        if type_name == "Footage":
            item = FootageItem(**kwargs)
        elif type_name == "Folder":
            item = FolderItem(**kwargs)
        return item


class FootageItem(AVItem):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)

    # PROPERTIES

    """The footage source, an object that contains all of the settings related to that footage item, 
    including those that are normally accessed through the Interpret Footage dialog box"""

    @property
    def main_source(self) -> object:
        item = None
        kwargs = self._eval_on_this_object("mainSource")
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
        kwargs = self._eval_on_this_object("file")
        return File(**kwargs) if kwargs else None

    # FUNCTIONS

    def open_in_viewer(self):
        """Opens the comp in a panel, moves it to the front and gives it focus"""
        kwargs = self._eval_on_this_object("openInViewer()")
        return Viewer(**kwargs) if kwargs else None

    def replace(self, path: str):
        """Changes the source of this Footage Item to the specified file"""
        file = File(**eval_script_returning_object(f'File("{path}")'))
        extend_file_object = format_to_extend(file)
        self._eval_on_this_object(f"replace({extend_file_object})")

    def replace_with_placeholder(
            self,
            name: str,
            width: int,
            height: int,
            frame_rate: float,
            duration: float,
            duration_as_frames=True,
    ):
        """Changes the source of this FootageItem to the specified placeholder"""
        if duration_as_frames:
            duration = current_format_to_time(duration, frame_rate)
        self._eval_on_this_object(
            f'replaceWithPlaceholder("{name}", {width}, {height}, {frame_rate}, {duration})'
        )

    def replace_with_sequence(self, path: str, force_alphabetical: bool = False):
        """Changes the source of this Footage Item to the specified image sequence."""
        file = File(**eval_script_returning_object(f'File("{path}")'))
        extend_file_object = format_to_extend(file)
        force_alphabetical = format_to_extend(force_alphabetical)
        self._eval_on_this_object(
            f"replaceWithSequence({extend_file_object}, {force_alphabetical})"
        )

    def replace_with_solid(
            self, colour: list, name: str, width: int, height: int, pixel_aspect: float
    ):
        """Changes the source of this FootageItem to the specified solid"""
        self._eval_on_this_object(
            f'replaceWithSolid({colour},"{name}", {width}, {height}, {pixel_aspect})'
        )


# SOURCES


class FootageSource(PydobeBaseObject):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id)
        self.object_type = object_type

    # PROPERTIES

    @property
    def type_name(self):
        return self.object_type

    """Defines how the alpha information in the footage is interpreted."""

    @property
    def alpha_mode(self) -> int:
        return self._eval_on_this_object("alphaMode")

    @alpha_mode.setter
    def alpha_mode(self, value: str or int):
        if type(value) == str:
            value = alpha_dictionary[value]
        self._eval_on_this_object(f"alphaMode = {value}")

    """A frame rate to use instead of the native frame rate value."""

    @property
    def conform_frame_rate(self) -> float:
        return self._eval_on_this_object("conformFrameRate")

    @conform_frame_rate.setter
    def conform_frame_rate(self, value: float):
        self._eval_on_this_object(f'conformFrameRate = "{value}"')

    """The effective frame rate as displayed and rendered in compositions by After Effects."""

    @property
    def display_frame_rate(self) -> float:
        return self._eval_on_this_object("displayFrameRate")

    """How the fields are to be separated in non-still footage."""

    # todo can add dict to make setting easier

    @property
    def field_separation_type(self) -> int:
        return self._eval_on_this_object("fieldSeparationType")

    @field_separation_type.setter
    def field_separation_type(self, value: int):
        self._eval_on_this_object(f"fieldSeparationType = {value}")

    """When true, the footage has an alpha component."""

    @property
    def has_alpha(self) -> bool:
        return self._eval_on_this_object("hasAlpha")

    """When true, After Effects performs high-quality field separation."""

    @property
    def high_quality_field_separation(self) -> bool:
        return self._eval_on_this_object("highQualityFieldSeparation")

    @high_quality_field_separation.setter
    def high_quality_field_separation(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_this_object(f"highQualityFieldSeparation = {extend_value}")

    """When true, the footage has an alpha component."""

    @property
    def invert_alpha(self) -> bool:
        return self._eval_on_this_object("invertAlpha")

    @invert_alpha.setter
    def invert_alpha(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_this_object(f"invertAlpha = {extend_value}")

    """When true the footage is still; when false, it has a time-based component."""

    @property
    def is_still(self) -> bool:
        return self._eval_on_this_object("isStill")

    """The number of times that the footage is to be played consecutively when used in a composition."""

    @property
    def loop(self) -> int:
        return self._eval_on_this_object("loop")

    @loop.setter
    def loop(self, value: int):
        self._eval_on_this_object(f"loop = {value}")

    """The native frame rate of the footage."""

    @property
    def native_frame_rate(self) -> float:
        return self._eval_on_this_object("nativeFrameRate")

    """The color to be premultiplied."""

    @property
    def premul_colour(self) -> int:
        return self._eval_on_this_object("premulColor")

    @premul_colour.setter
    def premul_colour(self, value: list or str):
        colour = format_colour(value)
        self._eval_on_this_object(f"premulColor = {colour}")

    """How the pulldowns are to be removed when field separation is used"""

    # todo can add dict to make setting easier

    @property
    def remove_pulldown(self) -> int:
        return self._eval_on_this_object("removePulldown")

    @remove_pulldown.setter
    def remove_pulldown(self, value: int):
        self._eval_on_this_object(f"removePulldown = {value}")

    # FUNCTIONS

    def guess_alpha_mode(self):
        """Sets alphaMode, premulColor, and invertAlpha to the best estimates for this footage source"""
        self._eval_on_this_object("guessAlphaMode()")

    def guess_pulldown(self, advance_24p=False):
        """Sets fieldSeparationType and removePulldown to the best estimates for this footage source."""
        if advance_24p:
            self._eval_on_this_object(f"guessPulldown(PulldownMethod.ADVANCE_24P)")
        else:
            self._eval_on_this_object(f"guessPulldown(PulldownMethod.PULLDOWN_3_2)")


class FileSource(FootageSource):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """The file"""

    @property
    def file(self):
        kwargs = self._eval_on_this_object("file")
        return File(**kwargs) if kwargs else None

    """The path and filename of footage that is missing from this asset."""

    @property
    def missing_footage_path(self):
        return self._eval_on_this_object("missingFootagePath")

    # FUNCTIONS

    def reload(self):
        """Reloads the asset from the file."""
        return self._eval_on_this_object("reload()")


class SolidSource(FootageSource):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """The color of the solid"""

    @property
    def colour(self) -> float:
        return self._eval_on_this_object("color")

    @colour.setter
    def colour(self, value: list or str):
        colour = format_colour(value)
        self._eval_on_this_object(f"color = {colour}")


class PlaceHolderSource(FootageSource):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)


# PROPERTIES

class PropertyBase(PydobeBaseObject):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)

    # PROPERTIES

    """True if the layer, property, or effect is active
        Will return False if other layers are solo, or if time is not between layers in and out point"""

    @property
    def active(self) -> bool:
        return self._eval_on_this_object('active')

    """True if you can set the enabled attribute value"""

    @property
    def can_set_enabled(self) -> bool:
        return self._eval_on_this_object('canSetEnabled')

    """True if the layer, property, or effect is enabled"""

    @property
    def enabled(self) -> bool:
        return self._eval_on_this_object('enabled')

    @enabled.setter
    def enabled(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_this_object(f'enabled = {extend_value}')

    """When true, this property is an effect property group"""

    @property
    def is_effect(self) -> bool:
        return self._eval_on_this_object('isEffect')

    """When true, this property is a mask property group"""

    @property
    def is_mask(self) -> bool:
        return self._eval_on_this_object('isMask')

    """When true, this property has been changed since it's creation"""

    @property
    def is_modified(self) -> bool:
        return self._eval_on_this_object('isModified')

    """A special name for the property used to build unique naming paths.
    Every property has a unique match-name identifier."""

    @property
    def match_name(self) -> bool:
        return self._eval_on_this_object('matchName')

    """The name of a layer, or the display name of a property"""

    @property
    def name(self) -> str:
        return self._eval_on_this_object('name')

    @name.setter
    def name(self, value: str):
        self._eval_on_this_object(f'name = "{value}"')

    """The property group that is the parent of this property. Null if this is a layer"""

    @property
    def parent_property(self) -> object:
        return self._eval_on_this_object('parentProperty')

    """When true, the property is selected"""

    @property
    def selected(self) -> bool:
        return self._eval_on_this_object('selected')

    @selected.setter
    def selected(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_this_object(f'selected = {extend_value}')


class Property(PropertyBase):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)


class PropertyGroup(PropertyBase):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)


# LAYERS


class Layer(PropertyGroup):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)

    # PROPERTIES
    @property
    def type_name(self):
        return self.match_name.split(" ", 1)[-1]

    """When true, the layer is locked"""

    @property
    def locked(self) -> bool:
        return self._eval_on_this_object("locked")

    @locked.setter
    def locked(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_this_object(f"locked = {extend_value}")

    """If the layer is shy, it will be hidden when hide shy layers is toggled"""

    @property
    def shy(self) -> bool:
        return self._eval_on_this_object("shy")

    @shy.setter
    def shy(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_this_object(f"shy = {extend_value}")

    """When true, the layer is soloed"""

    @property
    def solo(self) -> bool:
        return self._eval_on_this_object("shy")

    @solo.setter
    def solo(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_this_object(f"solo = {extend_value}")

    # FUNCTION

    def remove(self):
        """Remove a layer from a composition"""
        return self._eval_on_this_object("remove()")


class AVLayer(Layer):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)


class CameraLayer(Layer):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)


class LightLayer(Layer):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)


class ShapeLayer(AVLayer):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)


class TextLayer(AVLayer):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)


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
        return CompositionItem(**kwargs) if kwargs else None

    def add_folder(self, name: str) -> object:
        """Add a new Folder to the project"""
        kwargs = self._eval_on_this_object(f'addFolder("{name}")')
        return FolderItem(**kwargs) if kwargs else None


class LayerCollection(PydobeBaseCollection):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id, "length")

    def __getitem__(self, index: int):
        item = None
        index = index + 1
        kwargs = super(LayerCollection, self).__getitem__(index)
        match_name = self._eval_on_this_object(extend_property="matchName", index=index)
        if match_name == "ADBE AV Layer":
            item = AVLayer(**kwargs)
        elif match_name == "ADBE Camera Layer":
            item = CameraLayer(**kwargs)
        elif match_name == "ADBE Light Layer":
            item = LightLayer(**kwargs)
        elif match_name == "ADBE Vector Layer":
            item = ShapeLayer(**kwargs)
        elif match_name == "ADBE Text Layer":
            item = TextLayer(**kwargs)
        return item

    def __iter__(self):
        value = iter([self.__getitem__(i) for i in range(len(self))])
        return value

    # FUNCTIONS

    def add(self, item: object, duration: float = None) -> object:
        """Creates a new layer containing a specified Item"""
        extend_item_object = format_to_extend(item)
        if duration:
            kwargs = self._eval_on_this_object(f'add({extend_item_object}, {duration})')
        else:
            kwargs = self._eval_on_this_object(f'add({extend_item_object})')
        object_type = kwargs["object_type"]
        if object_type == "AVLayer":
            item = AVLayer(**kwargs)
        elif object_type == "CameraLayer":
            item = CameraLayer(**kwargs)
        elif object_type == "LightLayer":
            item = LightLayer(**kwargs)
        elif object_type == "ShapeLayer":
            item = ShapeLayer(**kwargs)
        elif object_type == "TextLayer":
            item = TextLayer(**kwargs)
        return item

    def add_box_text(self, width: int, height: int) -> object:
        """Creates a new paragraph text layer"""
        kwargs = self._eval_on_this_object(f'addBoxText([{width},{height}])')
        return TextLayer(**kwargs) if kwargs else None

    def add_camera(self, name: str, center_point: list) -> object:
        """Creates a new camera layer"""
        kwargs = self._eval_on_this_object(f'addCamera("{name}", {center_point})')
        return CameraLayer(**kwargs) if kwargs else None

    def add_light(self, name: str, center_point: list):
        """Creates a new light layer"""
        kwargs = self._eval_on_this_object(f'addLight("{name}", {center_point})')
        return LightLayer(**kwargs) if kwargs else None

    def add_null(self, duration: float, duration_as_frames: bool = True) -> object:
        """Creates a new Null layer"""  # todo frame rate of comp? - how do I get comp from collection?
        # if duration_as_frames:
        #     duration = time_to_current_format(duration)
        kwargs = self._eval_on_this_object(f'addNull({duration})')
        return AVLayer(**kwargs) if kwargs else None

    def add_shape(self) -> object:
        """Creates a new Shape layer"""
        kwargs = self._eval_on_this_object('addShape()')
        return ShapeLayer(**kwargs) if kwargs else None

    def add_solid(self, colour: list or str, name: str, width: int, height: int, pixel_aspect: float):  # todo
        """Creates a new Solid layer"""
        colour = format_colour(colour) # todo fix this for EVERYTHING
        kwargs = self._eval_on_this_object(f'addSolid({colour}, "{name}", {width}, {height}, {pixel_aspect})')
        return LightLayer(**kwargs) if kwargs else None

    def add_text(self, source_text: str = ""):
        """Creates a new Text layer"""
        kwargs = self._eval_on_this_object(f'addText("{source_text}")')
        return TextLayer(**kwargs) if kwargs else None

    def by_name(self, name: str):
        """Returns the first (topmost) layer found in this collection with the specified name,
        or null if no layer with the given name is found."""
        kwargs = self._eval_on_this_object(f'byName("{name}")')
        return TextLayer(**kwargs) if kwargs else None

    def precompose(self, indices: list, name: str, move_attributes: bool = True) -> object:
        """Creates a new CompItem object and moves the specified layers into its layer collection"""
        if len(indices) != 1 and not move_attributes:
            #todo is this error name correct?
            raise ValueError("Cannot set move_attributes to false when precomposing with more than one layer")
        indices = [index + 1 for index in indices]
        if not move_attributes:
            extend_move_attributes = format_to_extend(move_attributes)
            kwargs = self._eval_on_this_object(f'precompose({indices}, "{name}", "{extend_move_attributes}")')
        else:
            kwargs = self._eval_on_this_object(f'precompose({indices}, "{name}")')
        return CompositionItem(**kwargs) if kwargs else None


# MISC


class ImportOptions(PydobeBaseObject):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)

    """The file object to be imported"""

    @property
    def file(self) -> object:
        kwargs = self._eval_on_this_object("file")
        return File(**kwargs) if kwargs else None

    @file.setter
    def file(self, value: object):
        extend_object = format_to_extend(value)
        self._eval_on_this_object(f"file = {extend_object}")

    """Creates sequence from available files in alphateical order with no gaps"""

    @property
    def force_alphabetical(self) -> bool:
        return self._eval_on_this_object("forceAlphabetical")

    @force_alphabetical.setter
    def force_alphabetical(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_this_object(f"forceAlphabetical = {extend_value}")

    """Import as sequence"""

    @property
    def sequence(self) -> bool:
        return self._eval_on_this_object("sequence")

    @sequence.setter
    def sequence(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_this_object(f"sequence = {extend_value}")


class Viewer(PydobeBaseObject):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)

    # PROPERTIES

    """When true, indicates if the viewer panel is focused, and thereby frontmost."""

    @property
    def active(self) -> bool:
        return self._eval_on_this_object("active")

    """When true, indicates if the viewer panel is at its maximized size."""

    @property
    def maximised(self) -> bool:
        return self._eval_on_this_object("maximized")

    @maximised.setter
    def maximised(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_this_object(f"maximized = {extend_value}")

    # FUNCTIONS

    def set_active(self) -> bool:
        """Moves the viewer panel to the front and places focus on it, making it active."""
        return self._eval_on_this_object("setActive()")
