from __future__ import annotations
from typing import List
from pydobe.core import PydobeBaseObject, PydobeBaseCollection, format_to_extend
from pydobe.adobe_objects import File
from pydobe.utils import hex_to_rgb
from pydobe.after_effects.data import *
from pydobe.after_effects.ae_utils import *


# BASE OBJECTS


class Application(PydobeBaseObject):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """ This is the current active project. """

    @property
    def project(self) -> Project:
        kwargs = self._eval_on_object("project")
        return Project(**kwargs) if kwargs else None

    # FUNCTIONS

    def new_project(self, save: bool = None) -> Project:
        """Create a new empty project."""
        if save is None:
            pass
        elif save:
            self.project.close(save=True)
        else:
            self.project.close(save=False)
        kwargs = self._eval_on_object("newProject()")
        return Project(**kwargs) if kwargs else None

    def open(self, path: str = None, save: bool = None) -> Project:
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
            kwargs = self._eval_on_object(f"open({extend_file_object})")
        else:
            kwargs = self._eval_on_object(f"open()")
        return Project(**kwargs) if kwargs else None


class Project(PydobeBaseObject):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """The item that is currently active and is to be acted upon, 
    or a null if no item is currently selected or if multiple items are selected."""

    @property
    def active_item(self) -> Item:
        item = None
        kwargs = self._eval_on_object("activeItem")
        if not kwargs:
            raise TypeError("'active_item' requires precisely one item to be selected")
        type_name = self._eval_on_object("activeItem.typeName")
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
        return self._eval_on_object("dirty")

    """Identifies the file object containing the project"""

    @property
    def file(self) -> File:
        kwargs = self._eval_on_object("file")
        return File(**kwargs) if kwargs else None

    """All of the items in the project"""

    @property
    def items(self) -> ItemCollection:
        kwargs = self._eval_on_object("items")
        return ItemCollection(**kwargs) if kwargs else None

    """The number of items within the project"""

    @property
    def num_items(self) -> int:
        return self._eval_on_object("numItems")

    """The root folder containing the contents of the project
    Items inside internal folders will not be shown"""

    @property
    def root_folder(self) -> FolderItem:
        kwargs = self._eval_on_object("rootFolder")
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
            return self._eval_on_object(
                "close(CloseOptions.PROMPT_TO_SAVE_CHANGES)"
            )
        elif save:
            return self._eval_on_object("close(CloseOptions.SAVE_CHANGES)")
        else:
            return self._eval_on_object("close(CloseOptions.DO_NOT_SAVE_CHANGES)")

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
        kwargs = self._eval_on_object(f"importFile({extend_import_options})")
        return FootageItem(**kwargs) if kwargs else None

    def save(self, path: str = None) -> bool:
        """This will save the current scene"""
        if path:
            file = File(**eval_script_returning_object(f'File("{path}")'))
            extend_file_object = format_to_extend(file)
            return self._eval_on_object(f"save({extend_file_object})")
        else:
            return self._eval_on_object("save()")

    def save_with_dialog(self) -> bool:
        """This will prompt the user to save with a dialog box"""
        return self._eval_on_object('saveWithDialog()')

    # CUSTOM FUNCTIONS

    def item_by_name(self, name: str) -> Item:
        """Get an item by its name from within this project"""
        for item in self.items:
            if item.name == name:
                return item
        raise LookupError("There is no item by this name in your project")

    def save_incremental(self):
        """Save inc"""
        self._execute_command("app.executeCommand(3088)")


# ITEMS


class Item(PydobeBaseObject):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    def __str__(self):
        return self.name

    # PROPERTIES

    """A string that holds a comment, the comment is for the user’s purpose only"""

    @property
    def comment(self) -> str:
        return self._eval_on_object("comment")

    @comment.setter
    def comment(self, value: str):
        self._eval_on_object(f'comment = "{value}"')

    """A unique and persistent identification number used for the dynamic link"""

    @property
    def dynamic_link_guide(self):
        return self._eval_on_object("dynamicLinkGUID")

    """An array of guide objects, containing orientationType, positionType, and position attributes."""

    @property
    def guides(self):
        return self._eval_on_object('guides')

    """A unique and persistent identification number used internally to identify an item between sessions"""

    @property
    def id(self) -> int:
        return self._eval_on_object("id")

    """The colour of the label assigned to the item, expressed as an integer between 1-16. 0 = none"""

    @property
    def label(self) -> int:
        return self._eval_on_object("label")

    @label.setter
    def label(self, value: int or str):
        if type(value) == int:
            if value not in range(17):
                raise ValueError("Cannot set label, value must be between 0 and 16")
            int_value = value
        else:
            if not label_dictionary.get(value.title()):
                raise ValueError("Cannot set label, value is not an available label colour")
            int_value = label_dictionary[value.title()]
        self._eval_on_object(f"label = {int_value};")

    """The name of the item as displayed in the Project panel"""

    @property
    def name(self) -> str:
        return self._eval_on_object("name")

    @name.setter
    def name(self, value: str):
        self._eval_on_object(f'name = "{value}"')

    """The folder object that the item is parented to"""

    @property
    def parent_folder(self) -> FolderItem:
        kwargs = self._eval_on_object("parentFolder")
        return FolderItem(**kwargs) if kwargs else None

    @parent_folder.setter
    def parent_folder(self, value: FolderItem):
        if value.type_name == "Folder":
            extend_value = format_to_extend(value)
            self._eval_on_object(f"parentFolder = {extend_value}")
        else:
            raise TypeError("Unable to set 'parent_folder', type must be 'Folder'")

    """Whether the item is selected or not, multiple items can be selected at the same time"""

    @property
    def selected(self) -> bool:
        return self._eval_on_object("selected")

    @selected.setter
    def selected(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f'selected = {extend_value}')

    """User readable name for Item type"""

    @property
    def type_name(self) -> str:
        return self._eval_on_object("typeName")

    # FUNCTIONS

    def add_guide(self, orientation: int, position: int):
        """Creates a new guide and adds it to the guides object of the Item."""
        self._eval_on_object(f'addGuide({orientation},{position})')

    def duplicate(self):
        """Duplicates the Item"""
        self._execute_command("app.executeCommand(2080)")

    def remove(self):
        """Deletes this item from the project and the Project panel.
        If the item is a FolderItem, all the items contained in the folder are also removed from the project
        """
        self._eval_on_object("remove()")

    def remove_guide(self, index: int):
        """Removes an existing guide. Choose the guide based on its index"""
        if index not in range(len(self.guides)):
            raise ValueError("The index provided is outside of the range of guides")
        self._eval_on_object(f'removeGuide({index})')

    def set_guide(self, position: int, index: int):
        """Modifies the position of an existing guide"""
        if index not in range(len(self.guides)):
            raise ValueError("The index provided is outside of the range of guides")
        self._eval_on_object(f'setGuide({position}, {index})')


class AVItem(Item):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    """Duration of the item in seconds"""

    @property
    def duration(self) -> float:
        return self._eval_on_object('duration')

    @duration.setter
    def duration(self, value: float):
        self._eval_on_object(f'duration = {value}')

    """When true the item is a placeholder"""

    @property
    def footage_missing(self) -> float:
        return self._eval_on_object('footageMissing')

    """Returns the length of a frame for this AVItem, in seconds."""

    @property
    def frame_duration(self) -> float:
        return self._eval_on_object('frameDuration')

    @frame_duration.setter
    def frame_duration(self, value: float):
        self._eval_on_object(f'frameDuration = {value}')

    """The fps of the item, when set the frame duration is automatically set"""

    @property
    def frame_rate(self) -> float:
        return self._eval_on_object('frameRate')

    @frame_rate.setter
    def frame_rate(self, value: float):
        self._eval_on_object(f'frameRate = {value}')

    """Returns True if the item has an audio component"""

    @property
    def has_audio(self) -> bool:
        return self._eval_on_object('hasAudio')

    """Returns True if the item has an video component"""

    @property
    def has_video(self) -> bool:
        return self._eval_on_object('hasVideo')

    """The height of the item in pixels"""

    @property
    def height(self) -> int:
        return self._eval_on_object('height')

    @height.setter
    def height(self, value: int):
        self._eval_on_object(f'height = {value}')

    """Test whether the AVItem can be used as an alternate source when calling Property.set_alternate_source()."""

    @property
    def is_media_replacement_compatible(self) -> bool:
        return self._eval_on_object('isMediaReplacementCompatible')

    """The pixel aspect ratio of the item"""

    @property
    def pixel_aspect(self) -> float:
        return self._eval_on_object('pixelAspect')

    @pixel_aspect.setter
    def pixel_aspect(self, value: float):
        self._eval_on_object(f'pixelAspect = {value}')

    """The Footage Source being used as a proxy"""

    @property
    def proxy_source(self) -> FileSource:
        kwargs = self._eval_on_object('proxySource')
        return FileSource(**kwargs) if kwargs else None

    """The current time of the item when it is being previewed"""

    @property
    def time(self) -> float:
        return self._eval_on_object('time')

    @time.setter
    def time(self, value: float):
        self._eval_on_object(f'time = "{value}"')

    """A list of compositions that use this item"""

    @property
    def used_in(self) -> list:
        comp_list = []
        kwargs_list = self._eval_on_object('usedIn')
        for kwargs in kwargs_list:
            comp = CompositionItem(**kwargs)
            comp_list.append(comp)
        return comp_list

    """The width of the item in pixels"""

    @property
    def use_proxy(self) -> bool:
        return self._eval_on_object('useProxy')

    @use_proxy.setter
    def use_proxy(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f'useProxy = "{extend_value}"')

    """The width of the item in pixels"""

    @property
    def width(self) -> int:
        return self._eval_on_object('width')

    @width.setter
    def width(self, value: int):
        self._eval_on_object(f'width = {value}')

    # CUSTOM PROPERTIES

    @property
    def time_in_current_format(self) -> float:
        return time_to_current_format(self.time, self.frame_rate)

    @time_in_current_format.setter
    def time_in_current_format(self, value: float):
        value = current_format_to_time(value, self.frame_rate)
        self._eval_on_object(f'time = "{value}"')

    @property
    def duration_in_current_format(self) -> float:
        return time_to_current_format(self.duration, self.frame_rate)

    @duration_in_current_format.setter
    def duration_in_current_format(self, value: float):
        value = current_format_to_time(value, self.frame_rate)
        self._eval_on_object(f'duration = "{value}"')

    # FUNCTIONS

    def set_proxy(self, file_path: str):
        """Sets a file as the proxy of this AVItem."""
        file = File(**eval_script_returning_object(f'File("{file_path}")'))
        extend_file_object = format_to_extend(file)
        self._eval_on_object(f'setProxy({extend_file_object})')

    def set_proxy_to_none(self):
        """Removes the proxy from this AVItem"""
        self._eval_on_object('setProxyToNone()')

    def set_proxy_with_place_holder(self, name: str, width: int, height: int, frame_rate: int, duration: float):
        """Creates a PlaceholderSource object with specified values, sets this as the value of the proxySource
        attribute """
        self._eval_on_object(f'setProxyWithPlaceholder("{name}", {width}, {height}, {frame_rate}, {duration})')

    def set_proxy_with_sequence(self, file_path: str, force_alphabetical: bool = False):
        """Sets a sequence of files as the proxy of this AVItem"""
        file = File(**eval_script_returning_object(f'File("{file_path}")'))
        extend_file_object = format_to_extend(file)
        extend_force_alphabetical = format_to_extend(force_alphabetical)
        self._eval_on_object(f'setProxyWithSequence({extend_file_object}, {extend_force_alphabetical})')

    def set_proxy_with_solid(self, colour: list, name: str, width: int, height: int, pixel_aspect: float):
        """Creates a SolidSource object with specified values, sets this as the value of the proxySource attribute"""
        self._eval_on_object(f'setProxyWithSolid({colour}, "{name}", {width}, {height}, {pixel_aspect})')


class CompositionItem(AVItem):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """The front most camera layer that is enabled"""

    @property
    def active_camera(self) -> CameraLayer:
        kwargs = self._eval_on_object('activeCamera')
        return CameraLayer(**kwargs)

    """The background Colour of the composition"""

    @property
    def bg_colour(self):
        return self._eval_on_object('bgColor')

    @bg_colour.setter
    def bg_colour(self, value: list or str):
        if type(value) == str:
            colour = hex_to_rgb(value)
        self._eval_on_object(f'bgColor = {colour}')

    """The time set as the beginning of the composition in frames"""

    @property
    def display_start_frame(self) -> int:
        return self._eval_on_object('displayStartFrame')

    @display_start_frame.setter
    def display_start_frame(self, value: int):
        self._eval_on_object(f'displayStartFrame = {value}')

    """The time set as the beginning of the composition in seconds"""

    @property
    def display_start_time(self) -> float:
        return self._eval_on_object('displayStartTime')

    @display_start_time.setter
    def display_start_time(self, value: float):
        self._eval_on_object(f'displayStartTime = {value}')

    """When true, Draft 3D mode is enabled for the Composition panel."""

    @property
    def draft_3d(self) -> bool:
        return self._eval_on_object('draft3d')

    @draft_3d.setter
    def draft_3d(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f'draft3d = {extend_value}')

    """When true, indicates that the composition uses drop-frame timecode."""

    @property
    def drop_frame(self) -> bool:
        return self._eval_on_object('dropFrame')

    @drop_frame.setter
    def drop_frame(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f'dropFrame = {extend_value}')

    """When true, frame blending is enabled for this Composition."""

    @property
    def frame_blending(self) -> bool:
        return self._eval_on_object('frameBlending')

    @frame_blending.setter
    def frame_blending(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f'frameBlending = {extend_value}')

    """The duration of a frame, in seconds. This is the inverse of the frameRate value"""

    @property
    def frame_duration(self) -> float:
        return self._eval_on_object('frameDuration')

    @frame_duration.setter
    def frame_duration(self, value: float):
        self._eval_on_object(f'frameDuration = {value}')

    """When true, only layers with shy set to false are shown in the Timeline panel"""

    @property
    def hide_shy_layers(self) -> bool:
        return self._eval_on_object('hideShyLayers')

    @hide_shy_layers.setter
    def hide_shy_layers(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f'hideShyLayers = {extend_value}')

    """All of the layers in the composition"""

    @property
    def layers(self) -> LayerCollection:
        kwargs = self._eval_on_object('layers')
        return LayerCollection(**kwargs) if kwargs else None

    """A PropertyGroup object that contains all a composition’s markers."""

    @property
    def marker_property(self) -> PropertyGroup:
        kwargs = self._eval_on_object('markerProperty')
        return PropertyGroup(**kwargs) if kwargs else None

    """When true, only layers with shy set to false are shown in the Timeline panel"""

    @property
    def motion_blur(self) -> bool:
        return self._eval_on_object('motionBlur')

    @motion_blur.setter
    def motion_blur(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f'motionBlur = {extend_value}')

    """The maximum number of motion blur samples of 2D layer motion."""

    @property
    def motion_blur_adaptive_sample_limit(self) -> int:
        return self._eval_on_object('motionBlurAdaptiveSampleLimit')

    @motion_blur_adaptive_sample_limit.setter
    def motion_blur_adaptive_sample_limit(self, value: int):
        if value not in range(16, 257):
            raise ValueError("Cannot set motion blur adaptive sample limit, value must be between 16 and 256")
        self._eval_on_object(f'motionBlurAdaptiveSampleLimit = {value}')

    """The minimum number of motion blur samples per frame for Classic 3D layers, shape layers, and certain effects"""

    @property
    def motion_blur_samples_per_frame(self) -> int:
        return self._eval_on_object('motionBlurSamplesPerFrame')

    @motion_blur_samples_per_frame.setter
    def motion_blur_samples_per_frame(self, value: int):
        if value not in range(2, 65):
            raise ValueError("Cannot set motion blur adaptive sample limit, value must be between 2 and 64")
        self._eval_on_object(f'motionBlurSamplesPerFrame = {value}')

    """The number of properties in the Essential Graphics panel for the composition"""

    @property
    def motion_graphics_template_controller_count(self) -> int:
        return self._eval_on_object('motionGraphicsTemplateControllerCount')

    """Name property in the Essential Graphics panel for the composition"""

    @property
    def motion_graphics_template_name(self) -> str:
        return self._eval_on_object('motionGraphicsTemplateName')

    @motion_graphics_template_name.setter
    def motion_graphics_template_name(self, value: str):
        self._eval_on_object(f'motionGraphicsTemplateName = "{value}"')

    """The number of Layers in the Composition"""

    @property
    def num_layers(self) -> int:
        return self._eval_on_object('numLayers')

    """When true, the frame rate of nested compositions is preserved in the current composition."""

    @property
    def preserve_nested_frame_rate(self) -> bool:
        return self._eval_on_object('preserveNestedFrameRate')

    @preserve_nested_frame_rate.setter
    def preserve_nested_frame_rate(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f'preserveNestedFrameRate = {extend_value}')

    """When true, the resolution of nested compositions is preserved in the current composition."""

    @property
    def preserve_nested_resolution(self) -> bool:
        return self._eval_on_object('preserveNestedResolution')

    @preserve_nested_resolution.setter
    def preserve_nested_resolution(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f'preserveNestedResolution = {extend_value}')

    """The current rendering plug-in module to be used to render this composition"""

    @property
    def renderer(self) -> str:
        return self._eval_on_object('renderer')

    @renderer.setter
    def renderer(self, value: str):
        if value not in self.renderers:
            raise ValueError(f"{value} is not a valid renderer")
        extend_value = format_to_extend(value)
        self._eval_on_object(f'renderer = {extend_value}')

    """The available rendering plugin modules"""

    @property
    def renderers(self) -> list:
        return self._eval_on_object('renderers')

    """The x and y downsample resolution factors for rendering the composition."""

    @property
    def resolution_factor(self) -> List[int]:
        return self._eval_on_object('resolutionFactor')

    @resolution_factor.setter
    def resolution_factor(self, value: List[int]):
        self._eval_on_object(f'resolutionFactor = {value}')

    """All of the selected layers in this composition."""

    @property
    def selected_layers(self) -> list:
        layer_list = []
        kwargs_list = self._eval_on_object('selectedLayers')
        for kwargs in kwargs_list:
            object_type = kwargs["object_type"]
            layer = None
            if object_type == "AVLayer":
                layer = AVLayer(**kwargs)
            elif object_type == "CameraLayer":
                layer = CameraLayer(**kwargs)
            elif object_type == "LightLayer":
                layer = LightLayer(**kwargs)
            elif object_type == "ShapeLayer":
                layer = ShapeLayer(**kwargs)
            elif object_type == "TextLayer":
                layer = TextLayer(**kwargs)
            layer_list.append(layer)
        return layer_list

    """All of the selected properties in this composition."""

    @property
    def selected_properties(self):
        properties_list = []
        kwargs_list = self._eval_on_object('selectedProperties')
        for kwargs in kwargs_list:
            object_type = kwargs["object_type"]
            if object_type == "PropertyGroup" or object_type == "MaskPropertyGroup":
                property_ = PropertyGroup(**kwargs)
            else:
                property_ = Property(**kwargs)
            properties_list.append(property_)
        return properties_list

    """The shutter angle setting for the composition."""

    @property
    def shutter_angle(self) -> int:
        return self._eval_on_object('shutterAngle')

    @shutter_angle.setter
    def shutter_angle(self, value: int):
        if value not in range(721):
            raise ValueError("Cannot set shutter angle, value must be between 0 and 720")
        self._eval_on_object(f'shutterAngle = {value}')

    """The shutter phase setting for the composition."""

    @property
    def shutter_phase(self) -> int:
        return self._eval_on_object('shutterPhase')

    @shutter_phase.setter
    def shutter_phase(self, value: int):
        if value not in range(-360, 361):
            raise ValueError("Cannot set shutter phase, value must be between -360 and 360")
        self._eval_on_object(f'shutterPhase = {value}')

    """The duration of the work area in seconds"""

    @property
    def work_area_duration(self) -> float:
        return self._eval_on_object('workAreaDuration')

    @work_area_duration.setter
    def work_area_duration(self, value: float):
        self._eval_on_object(f'workAreaDuration = {value}')

    """The time when the Composition work area begins, in seconds."""

    @property
    def work_area_start(self) -> float:
        return self._eval_on_object('workAreaStart')

    @work_area_start.setter
    def work_area_start(self, value: float):
        self._eval_on_object(f'workAreaStart = {value}')

    # CUSTOM PROPERTIES

    @property
    def work_area_duration_in_current_format(self) -> str:
        duration = self._eval_on_object('workAreaDuration')
        formatted_duration = time_to_current_format(duration, self.frame_rate)
        return formatted_duration

    @work_area_duration_in_current_format.setter
    def work_area_duration_in_current_format(self, value: str or int):
        value = current_format_to_time(value, self.frame_rate)
        self._eval_on_object(f'workAreaDuration = {value}')

    @property
    def work_area_start_in_current_format(self) -> str:
        duration = self._eval_on_object('workAreaStart')
        formatted_duration = time_to_current_format(duration, self.frame_rate)
        return formatted_duration

    @work_area_start_in_current_format.setter
    def work_area_start_in_current_format(self, value: str or int):
        value = current_format_to_time(value, self.frame_rate)
        self._eval_on_object(f'workAreaStart = {value}')

    # FUNCTIONS

    def export_as_motion_graphics_template(self, overwrite: bool = True, path: str = None) -> bool:
        """Exports the composition as a Motion Graphics template."""
        extend_overwrite = format_to_extend(overwrite)
        if path:
            return self._eval_on_object(f'exportAsMotionGraphicsTemplate({extend_overwrite},"{path}")')
        else:
            return self._eval_on_object(f'exportAsMotionGraphicsTemplate({extend_overwrite})')

    def get_motion_graphics_template_controller_name(self, index: int) -> str:
        """Gets the name of a single property in the Essential Graphics panel."""
        index += 1
        return self._eval_on_object(f'getMotionGraphicsTemplateControllerName({index})')

    def set_get_motion_graphics_controller_name(self, index: int, name: str) -> str:
        """Sets the name of a single property in the Essential Graphics panel."""
        index += 1
        return self._eval_on_object(f'getMotionGraphicsTemplateControllerName({index}, "{name}")')

    def layer(self, layer, relative_index=None):
        """Returns a Layer object, which can be specified by name, an index position in this layer,
        or an index position relative to another layer. """
        if relative_index:
            layer = format_to_extend(layer)
            kwargs = self._eval_on_object(f'layer({layer}, {relative_index})')
            if not kwargs.get("pydobe_id"):
                raise ValueError("The value for the relative index is out of range")
        else:
            if type(layer) == str:
                kwargs = self._eval_on_object(f'layer("{layer}")')
            else:
                layer += 1
                kwargs = self._eval_on_object(f'layer({layer})')
        object_type = kwargs["object_type"]
        if object_type == "AVLayer":
            layer = AVLayer(**kwargs)
        elif object_type == "CameraLayer":
            layer = CameraLayer(**kwargs)
        elif object_type == "LightLayer":
            layer = LightLayer(**kwargs)
        elif object_type == "ShapeLayer":
            layer = ShapeLayer(**kwargs)
        elif object_type == "TextLayer":
            layer = TextLayer(**kwargs)
        return layer

    def open_in_essential_graphics(self):
        """Opens the composition in the Essential Graphics panel."""
        self._eval_on_object("openInEssentialGraphics()")

    def open_in_viewer(self):
        """Opens the comp in a panel, moves it to the front and gives it focus"""
        kwargs = self._eval_on_object("openInViewer()")
        return Viewer(**kwargs) if kwargs else None


class FolderItem(Item):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """All of the items in the folder"""

    @property
    def items(self) -> ItemCollection:
        kwargs = self._eval_on_object("items")
        return ItemCollection(**kwargs) if kwargs else None

    """The number of items within the folder"""

    @property
    def num_items(self) -> int:
        return self._eval_on_object("numItems")

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

    def item(self, sub_index: int) -> Item:
        """Returns the top-level item in this folder at the specified index position."""
        item = None
        sub_index += 1
        kwargs = self._eval_on_object(f"item({sub_index})")
        type_name = self._eval_on_object(f"item({sub_index}).typeName")
        if type_name == "Composition":
            item = CompositionItem(**kwargs)
        if type_name == "Footage":
            item = FootageItem(**kwargs)
        elif type_name == "Folder":
            item = FolderItem(**kwargs)
        return item


class FootageItem(AVItem):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """The footage source, an object that contains all of the settings related to that footage item, 
    including those that are normally accessed through the Interpret Footage dialog box"""

    @property
    def main_source(self) -> FootageSource:
        item = None
        kwargs = self._eval_on_object("mainSource")
        object_type = kwargs["object_type"]
        if object_type == "FileSource":
            item = FileSource(**kwargs)
        elif object_type == "SolidSource":
            item = SolidSource(**kwargs)
        elif object_type == "PlaceholderSource":
            item = PlaceholderSource(**kwargs)
        return item

    """The file object associated with this footage"""

    @property
    def file(self) -> File:
        kwargs = self._eval_on_object("file")
        return File(**kwargs) if kwargs else None

    # OVERRIDES

    @AVItem.duration.setter
    def duration(self, value: float):
        raise AttributeError(f"Can not change duration of {self.name} as it is not a Comp Item")

    @AVItem.frame_duration.setter
    def frame_duration(self, value: float):
        raise AttributeError(
            f"Can not set frame duration on a footage Item. Instead set the conform frame"
            f" rate on the main source or proxy source of the item")

    @AVItem.frame_rate.setter
    def frame_rate(self, value: float):
        raise AttributeError("Can not set frame rate on a footage item. Instead set the conform frame rate")

    @AVItem.height.setter
    def height(self, value: int):
        if self.main_source.object_type == "SolidSource":
            self._eval_on_object(f'height = {value}')
        else:
            raise AttributeError("Attribute 'height' cannot be set, as the item is neither a comp, nor a solid")

    @AVItem.width.setter
    def width(self, value: int):
        if self.main_source.object_type == "SolidSource":
            self._eval_on_object(f'width = {value}')
        else:
            raise AttributeError("Attribute 'width' cannot be set, as the item is neither a comp, nor a solid")

    # FUNCTIONS

    def replace(self, path: str):
        """Changes the source of this Footage Item to the specified file"""
        file = File(**eval_script_returning_object(f'File("{path}")'))
        extend_file_object = format_to_extend(file)
        self._eval_on_object(f"replace({extend_file_object})")

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
        self._eval_on_object(
            f'replaceWithPlaceholder("{name}", {width}, {height}, {frame_rate}, {duration})'
        )

    def replace_with_sequence(self, path: str, force_alphabetical: bool = False):
        """Changes the source of this Footage Item to the specified image sequence."""
        file = File(**eval_script_returning_object(f'File("{path}")'))
        extend_file_object = format_to_extend(file)
        force_alphabetical = format_to_extend(force_alphabetical)
        self._eval_on_object(
            f"replaceWithSequence({extend_file_object}, {force_alphabetical})"
        )

    def replace_with_solid(
            self, colour: list, name: str, width: int, height: int, pixel_aspect: float
    ):
        """Changes the source of this FootageItem to the specified solid"""
        self._eval_on_object(
            f'replaceWithSolid({colour},"{name}", {width}, {height}, {pixel_aspect})'
        )


# SOURCES


class FootageSource(PydobeBaseObject):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """Defines how the alpha information in the footage is interpreted."""

    @property
    def alpha_mode(self) -> int:
        return self._eval_on_object("alphaMode")

    @alpha_mode.setter
    def alpha_mode(self, value: str or int):
        if type(value) == str:
            value = alpha_dictionary[value]
        self._eval_on_object(f"alphaMode = {value}")

    """A frame rate to use instead of the native frame rate value."""

    @property
    def conform_frame_rate(self) -> float:
        return self._eval_on_object("conformFrameRate")

    @conform_frame_rate.setter
    def conform_frame_rate(self, value: float):
        self._eval_on_object(f'conformFrameRate = "{value}"')

    """The effective frame rate as displayed and rendered in compositions by After Effects."""

    @property
    def display_frame_rate(self) -> float:
        return self._eval_on_object("displayFrameRate")

    """How the fields are to be separated in non-still footage."""

    @property
    def field_separation_type(self) -> int:
        return self._eval_on_object("fieldSeparationType")

    @field_separation_type.setter
    def field_separation_type(self, value: int or str):
        if type(value) == str:
            value = field_separation_dictionary[value.title()]
        self._eval_on_object(f"fieldSeparationType = {value}")

    """When true, the footage has an alpha component."""

    @property
    def has_alpha(self) -> bool:
        return self._eval_on_object("hasAlpha")

    """When true, After Effects performs high-quality field separation."""

    @property
    def high_quality_field_separation(self) -> bool:
        return self._eval_on_object("highQualityFieldSeparation")

    @high_quality_field_separation.setter
    def high_quality_field_separation(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"highQualityFieldSeparation = {extend_value}")

    """When true, the footage has an alpha component."""

    @property
    def invert_alpha(self) -> bool:
        return self._eval_on_object("invertAlpha")

    @invert_alpha.setter
    def invert_alpha(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"invertAlpha = {extend_value}")

    """When true the footage is still; when false, it has a time-based component."""

    @property
    def is_still(self) -> bool:
        return self._eval_on_object("isStill")

    """The number of times that the footage is to be played consecutively when used in a composition."""

    @property
    def loop(self) -> int:
        return self._eval_on_object("loop")

    @loop.setter
    def loop(self, value: int):
        self._eval_on_object(f"loop = {value}")

    """The native frame rate of the footage."""

    @property
    def native_frame_rate(self) -> float:
        return self._eval_on_object("nativeFrameRate")

    """The color to be premultiplied."""

    @property
    def premul_colour(self) -> int:
        return self._eval_on_object("premulColor")

    @premul_colour.setter
    def premul_colour(self, value: list or str):
        if type(value) == str:
            colour = hex_to_rgb(value)
        self._eval_on_object(f"premulColor = {colour}")

    """How the pulldowns are to be removed when field separation is used"""

    @property
    def remove_pulldown(self) -> int:
        return self._eval_on_object("removePulldown")

    @remove_pulldown.setter
    def remove_pulldown(self, value: int or str):
        if type(value) == str:
            value = pulldown_dictionary[value.upper()]
        self._eval_on_object(f"removePulldown = {value}")

    # FUNCTIONS

    def guess_alpha_mode(self):
        """Sets alphaMode, premulColor, and invertAlpha to the best estimates for this footage source"""
        self._eval_on_object("guessAlphaMode()")

    def guess_pulldown(self, advance_24p=False):
        """Sets fieldSeparationType and removePulldown to the best estimates for this footage source."""
        if advance_24p:
            self._eval_on_object(f"guessPulldown(PulldownMethod.ADVANCE_24P)")
        else:
            self._eval_on_object(f"guessPulldown(PulldownMethod.PULLDOWN_3_2)")


class FileSource(FootageSource):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """The file"""

    @property
    def file(self) -> File:
        kwargs = self._eval_on_object("file")
        return File(**kwargs) if kwargs else None

    """The path and filename of footage that is missing from this asset."""

    @property
    def missing_footage_path(self) -> str:
        return self._eval_on_object("missingFootagePath")

    # FUNCTIONS

    def reload(self):
        """Reloads the asset from the file."""
        self._eval_on_object("reload()")


class SolidSource(FootageSource):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """The color of the solid"""

    @property
    def colour(self) -> float:
        return self._eval_on_object("color")

    @colour.setter
    def colour(self, value: list or str):
        if type(value) == str:
            colour = hex_to_rgb(value)
        self._eval_on_object(f"color = {colour}")


class PlaceholderSource(FootageSource):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)


# PROPERTIES

class PropertyBase(PydobeBaseObject):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """True if the layer, property, or effect is active
        Will return False if other layers are solo, or if time is not between layers in and out point"""

    @property
    def active(self) -> bool:
        return self._eval_on_object('active')

    """True if you can set the enabled attribute value"""

    @property
    def can_set_enabled(self) -> bool:
        return self._eval_on_object('canSetEnabled')

    """True if the layer, property, or effect is enabled"""

    @property
    def enabled(self) -> bool:
        return self._eval_on_object('enabled')

    @enabled.setter
    def enabled(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f'enabled = {extend_value}')

    """When true, this property is an effect property group"""

    @property
    def is_effect(self) -> bool:
        return self._eval_on_object('isEffect')

    """When true, this property is a mask property group"""

    @property
    def is_mask(self) -> bool:
        return self._eval_on_object('isMask')

    """When true, this property has been changed since it's creation"""

    @property
    def is_modified(self) -> bool:
        return self._eval_on_object('isModified')

    """A special name for the property used to build unique naming paths.
    Every property has a unique match-name identifier."""

    @property
    def match_name(self) -> bool:
        return self._eval_on_object('matchName')

    """The name of a layer, or the display name of a property"""

    @property
    def name(self) -> str:
        return self._eval_on_object('name')

    @name.setter
    def name(self, value: str):
        self._eval_on_object(f'name = "{value}"')

    """The property group that is the parent of this property. Null if this is a layer"""

    @property
    def parent_property(self) -> PropertyGroup:
        kwargs = self._eval_on_object('parentProperty')
        return PropertyGroup(**kwargs) if kwargs else None

    """When true, the property is selected"""

    @property
    def selected(self) -> bool:
        return self._eval_on_object('selected')

    @selected.setter
    def selected(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f'selected = {extend_value}')


class Property(PropertyBase):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)


class PropertyGroup(PropertyBase):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)


# LAYERS


class Layer(PropertyGroup):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """The composition that contains this Layer"""

    @property
    def containing_comp(self) -> CompositionItem:
        kwargs = self._eval_on_object("containingComp")
        return CompositionItem(**kwargs) if kwargs else None

    """When true, the layer is locked"""

    @property
    def locked(self) -> bool:
        return self._eval_on_object("locked")

    @locked.setter
    def locked(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"locked = {extend_value}")

    """If the layer is shy, it will be hidden when hide shy layers is toggled"""

    @property
    def shy(self) -> bool:
        return self._eval_on_object("shy")

    @shy.setter
    def shy(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"shy = {extend_value}")

    """When true, the layer is soloed"""

    @property
    def solo(self) -> bool:
        return self._eval_on_object("shy")

    @solo.setter
    def solo(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"solo = {extend_value}")

    # FUNCTION

    def remove(self):
        """Remove a layer from a composition"""
        self._eval_on_object("remove()")


class AVLayer(Layer):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)


class CameraLayer(Layer):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)


class LightLayer(Layer):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)


class ShapeLayer(AVLayer):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)


class TextLayer(AVLayer):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)


# COLLECTIONS


class ItemCollection(PydobeBaseCollection):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type, "length")

    def __getitem__(self, index: int):
        item = None
        index = index + 1
        kwargs = super(ItemCollection, self).__getitem__(index)
        type_name = self._eval_on_object(extend_property="typeName", index=index)
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
    ) -> CompositionItem:
        """Add a new Composition to the project"""
        if duration_as_frames:
            duration = current_format_to_time(duration, frame_rate)
        kwargs = self._eval_on_object(
            f'addComp("{name}", {width}, {height}, {aspect_ratio}, {duration}, {frame_rate})'
        )
        return CompositionItem(**kwargs) if kwargs else None

    def add_folder(self, name: str) -> FolderItem:
        """Add a new Folder to the project"""
        kwargs = self._eval_on_object(f'addFolder("{name}")')
        return FolderItem(**kwargs) if kwargs else None


class LayerCollection(PydobeBaseCollection):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type, "length")

    def __getitem__(self, index: int):
        layer = None
        index = index + 1
        kwargs = super(LayerCollection, self).__getitem__(index)
        print(kwargs)
        object_type = kwargs["object_type"]
        if object_type == "AVLayer":
            layer = AVLayer(**kwargs)
        elif object_type == "CameraLayer":
            layer = CameraLayer(**kwargs)
        elif object_type == "LightLayer":
            layer = LightLayer(**kwargs)
        elif object_type == "ShapeLayer":
            layer = ShapeLayer(**kwargs)
        elif object_type == "TextLayer":
            layer = TextLayer(**kwargs)
        return layer

    def __iter__(self):
        value = iter([self.__getitem__(i) for i in range(len(self))])
        return value

    # FUNCTIONS

    def add(self, item: Item, duration: float = None) -> Layer:
        """Creates a new layer containing a specified Item"""
        layer = None
        extend_item_object = format_to_extend(item)
        if duration:
            kwargs = self._eval_on_object(f'add({extend_item_object}, {duration})')
        else:
            kwargs = self._eval_on_object(f'add({extend_item_object})')
        object_type = kwargs["object_type"]
        if object_type == "AVLayer":
            layer = AVLayer(**kwargs)
        elif object_type == "CameraLayer":
            layer = CameraLayer(**kwargs)
        elif object_type == "LightLayer":
            layer = LightLayer(**kwargs)
        elif object_type == "ShapeLayer":
            layer = ShapeLayer(**kwargs)
        elif object_type == "TextLayer":
            layer = TextLayer(**kwargs)
        return layer

    def add_box_text(self, width: int, height: int) -> TextLayer:
        """Creates a new paragraph text layer"""
        kwargs = self._eval_on_object(f'addBoxText([{width},{height}])')
        return TextLayer(**kwargs) if kwargs else None

    def add_camera(self, name: str, center_point: list) -> CameraLayer:
        """Creates a new camera layer"""
        kwargs = self._eval_on_object(f'addCamera("{name}", {center_point})')
        return CameraLayer(**kwargs) if kwargs else None

    def add_light(self, name: str, center_point: list):
        """Creates a new light layer"""
        kwargs = self._eval_on_object(f'addLight("{name}", {center_point})')
        return LightLayer(**kwargs) if kwargs else None

    def add_null(self, duration: float or str, duration_in_current_format: bool = True) -> AVLayer:
        """Creates a new Null layer"""
        if duration_in_current_format:
            frame_rate = self[0].containing_comp.frame_rate
            duration = time_to_current_format(duration, frame_rate)
        kwargs = self._eval_on_object(f'addNull({duration})')
        return AVLayer(**kwargs) if kwargs else None

    def add_shape(self) -> ShapeLayer:
        """Creates a new Shape layer"""
        kwargs = self._eval_on_object('addShape()')
        return ShapeLayer(**kwargs) if kwargs else None

    def add_solid(self, colour: list or str, name: str, width: int, height: int, pixel_aspect: float) -> LightLayer:
        """Creates a new Solid layer"""
        if type(colour) == str:
            colour = hex_to_rgb(colour)
        kwargs = self._eval_on_object(f'addSolid({colour}, "{name}", {width}, {height}, {pixel_aspect})')
        return LightLayer(**kwargs) if kwargs else None

    def add_text(self, source_text: str = "") -> TextLayer:
        """Creates a new Text layer"""
        kwargs = self._eval_on_object(f'addText("{source_text}")')
        return TextLayer(**kwargs) if kwargs else None

    def by_name(self, name: str) -> Layer:
        """Returns the first (topmost) layer found in this collection with the specified name,
        or null if no layer with the given name is found."""
        kwargs = self._eval_on_object(f'byName("{name}")')
        layer = None
        object_type = kwargs["object_type"]
        if object_type == "AVLayer":
            layer = AVLayer(**kwargs)
        elif object_type == "CameraLayer":
            layer = CameraLayer(**kwargs)
        elif object_type == "LightLayer":
            layer = LightLayer(**kwargs)
        elif object_type == "ShapeLayer":
            layer = ShapeLayer(**kwargs)
        elif object_type == "TextLayer":
            layer = TextLayer(**kwargs)
        return layer

    def precompose(self, indices: list, name: str, move_attributes: bool = True) -> CompositionItem:
        """Creates a new CompItem object and moves the specified layers into its layer collection"""
        if len(indices) != 1 and not move_attributes:
            # coco - technically this is an "AfterEffectsError" not a "ValueError" - discuss in review
            raise ValueError("Cannot set move attributes to false when precomposing with more than one layer")
        indices = [index + 1 for index in indices]
        if not move_attributes:
            extend_move_attributes = format_to_extend(move_attributes)
            kwargs = self._eval_on_object(f'precompose({indices}, "{name}", "{extend_move_attributes}")')
        else:
            kwargs = self._eval_on_object(f'precompose({indices}, "{name}")')
        return CompositionItem(**kwargs) if kwargs else None


# MISC


class ImportOptions(PydobeBaseObject):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    """The file object to be imported"""

    @property
    def file(self) -> File:
        kwargs = self._eval_on_object("file")
        return File(**kwargs) if kwargs else None

    @file.setter
    def file(self, value: File):
        extend_object = format_to_extend(value)
        self._eval_on_object(f"file = {extend_object}")

    """Creates sequence from available files in alphabetical order with no gaps"""

    @property
    def force_alphabetical(self) -> bool:
        return self._eval_on_object("forceAlphabetical")

    @force_alphabetical.setter
    def force_alphabetical(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"forceAlphabetical = {extend_value}")

    """Import as sequence"""

    @property
    def sequence(self) -> bool:
        return self._eval_on_object("sequence")

    @sequence.setter
    def sequence(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"sequence = {extend_value}")


class Viewer(PydobeBaseObject):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """When true, indicates if the viewer panel is focused."""

    @property
    def active(self) -> bool:
        return self._eval_on_object("active")

    """When true, indicates if the viewer panel is at its maximized size."""

    @property
    def maximised(self) -> bool:
        return self._eval_on_object("maximized")

    @maximised.setter
    def maximised(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"maximized = {extend_value}")

    # FUNCTIONS

    def set_active(self) -> bool:
        """Moves the viewer panel to the front and places focus on it, making it active."""
        return self._eval_on_object("setActive()")
