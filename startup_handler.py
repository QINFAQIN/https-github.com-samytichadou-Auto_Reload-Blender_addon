import bpy
import os

from bpy.app.handlers import persistent

from . import functions
from .global_variables import handler_statement
from .addon_prefs import get_addon_preferences
from .update_module import check_addon_version
from .properties import create_preview_texture


@persistent
def reload_startup(scene):

    wm = bpy.data.window_managers['WinMan']
    props = wm.autoreload_properties
    prefs = get_addon_preferences()

    # check for addon new version
    if prefs.update_check_launch:
        check_addon_version(wm)

    # check for image editor executable
    if os.path.isfile(prefs.image_executable):
        props.autoreload_is_editor_executable = True

    # images
    functions.check_images_startup()
    create_preview_texture()
    props.autoreload_active_image_index = 0

    # libraries
    functions.check_libraries_startup()

    # launch timer on startup
    if prefs.startup_launch:
        props.autoreload_is_timer = True

    print(handler_statement)


### REGISTER ---

def register():
    bpy.app.handlers.load_post.append(reload_startup)

def unregister():
    bpy.app.handlers.load_post.remove(reload_startup)