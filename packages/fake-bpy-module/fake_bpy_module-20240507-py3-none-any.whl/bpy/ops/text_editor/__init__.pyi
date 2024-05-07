import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def preset_add(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    name: typing.Union[str, typing.Any] = "",
    remove_name: typing.Optional[typing.Union[bool, typing.Any]] = False,
    remove_active: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Add or remove a Text Editor Preset

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param name: Name, Name of the preset, used to make the path name
    :type name: typing.Union[str, typing.Any]
    :param remove_name: remove_name
    :type remove_name: typing.Optional[typing.Union[bool, typing.Any]]
    :param remove_active: remove_active
    :type remove_active: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...
