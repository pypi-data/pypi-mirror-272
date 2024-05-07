import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def execute_preset(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    filepath: typing.Union[str, typing.Any] = "",
    menu_idname: typing.Union[str, typing.Any] = "",
):
    """Load a preset

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param filepath: filepath
    :type filepath: typing.Union[str, typing.Any]
    :param menu_idname: Menu ID Name, ID name of the menu this was called from
    :type menu_idname: typing.Union[str, typing.Any]
    """

    ...

def python_file_run(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    filepath: typing.Union[str, typing.Any] = "",
):
    """Run Python file

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param filepath: Path
    :type filepath: typing.Union[str, typing.Any]
    """

    ...

def reload(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Reload scripts

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...
