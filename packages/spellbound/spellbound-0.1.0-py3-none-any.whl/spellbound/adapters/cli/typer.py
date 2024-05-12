import asyncio
import inspect
from inspect import Parameter

import typer
from pydantic.fields import Undefined as PydanticUndefined
from typing_extensions import Annotated


def pydantic_field_to_parameter(field):
    """
    Given a Pydantic field, create a Parameter annotated with Typer CLI setting.

    Args:
        field (Field): Pydantic field

    Returns:
        Parameter: Parameter
    """
    field_info = field.field_info
    description = field_info.description
    has_default = field_info.default != PydanticUndefined
    typer_setting = typer.Option(help=description)

    return Parameter(
        field.name,
        Parameter.POSITIONAL_OR_KEYWORD,
        annotation=Annotated[field.annotation, typer_setting],
        default=field.default if has_default else Parameter.empty,
    )


def pydantic_model_to_parameters(model):
    """
    Given a Pydantic model class,
    create a list of Parameters annotated with Typer CLI settings.

    Args:
        model (class): Pydantic model class

    Returns:
        List[Parameter]: list of Parameters
    """
    return [pydantic_field_to_parameter(field) for field in model.__fields__.values()]


def override_function_signature(func, name, parameters):
    """
    Override the signature of a function.
    This mutates the signature of the input `func`, and returns it.
    but it does not mutate the function body.

    Args:
        func (function): function to override
        name (str): new function name
        parameters (List[Parameter]): new function parameters

    Returns:
        function: original function `func` with overridden signature
    """
    sig = inspect.signature(func)
    func.__name__ = name
    func.__signature__ = sig.replace(parameters=parameters)
    return func


def as_typer_command_func(func, command_name, command_params):
    """
    Annotate a function with Typer CLI settings based on the given Pydantic model.

    Args:
        func (function): function to annotate
        command_name (str): Typer command name
        command_params (class): Pydantic model class

    Returns:
        function: original function `func` with Typer CLI settings
    """
    parameters = pydantic_model_to_parameters(command_params)

    # required parameters must come before optional parameters
    required = [p for p in parameters if p.default == Parameter.empty]
    optional = [p for p in parameters if p.default != Parameter.empty]

    return override_function_signature(
        func, command_name, parameters=required + optional
    )


def convert_spell_to_command(caster, name):
    """
    Convert a spell to a function that can be used as Typer CLI command.

    Args:
        caster (SpellCaster): Caster
        name (str): spell name

    Returns:
        function: function that can be used as Typer CLI command
    """

    spell_class = caster.find(name)

    def f(**kwargs):
        result = asyncio.run(caster.cast(name, **kwargs))

        raise typer.Exit(1 if result.is_error() else 0)

    func = as_typer_command_func(f, name, spell_class.InputParams)
    func.__doc__ = spell_class.description
    return func


def register_spells_as_commands(cli, caster):
    """
    Register all spells from the caster as CLI commands.

    Args:
        cli (Typer): Typer CLI app
        caster (SpellCaster): Caster
    """

    for group, spells in caster.list_by_group().items():
        for name, _ in spells:
            fn = convert_spell_to_command(caster, name)
            if group:
                cli.command(rich_help_panel=f"Commands - {group}")(fn)
            else:
                cli.command()(fn)
