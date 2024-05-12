import inspect
import unittest
from inspect import Parameter
from typing import List, Optional

import typer
from pydantic import BaseModel, Field
from typing_extensions import Annotated

from spellbound.adapters.cli.typer import (
    as_typer_command_func,
    override_function_signature,
    pydantic_field_to_parameter,
    pydantic_model_to_parameters,
)


class Hero(BaseModel):
    name: str
    tags: Optional[List[str]] = None
    description: str = Field(description="very fast")


class TestAdapter(unittest.TestCase):
    def assertEqualParameters(self, p1, p2):
        self.assertEqual(p1.name, p2.name)
        self.assertEqual(p1.default, p2.default)
        self.assertEqual(p1.annotation.__args__, p2.annotation.__args__)
        self.assertEqual(
            p1.annotation.__metadata__[0].help, p2.annotation.__metadata__[0].help
        )

    def test_field_no_default(self):
        p1 = pydantic_field_to_parameter(Hero.__fields__["name"])
        p2 = Parameter(
            "name",
            Parameter.POSITIONAL_OR_KEYWORD,
            annotation=Annotated[str, typer.Option()],
            default=Parameter.empty,
        )
        self.assertEqualParameters(p1, p2)

    def test_field_with_default(self):
        p1 = pydantic_field_to_parameter(Hero.__fields__["tags"])
        p2 = Parameter(
            "tags",
            Parameter.POSITIONAL_OR_KEYWORD,
            annotation=Annotated[Optional[List[str]], typer.Option()],
            default=None,
        )
        self.assertEqualParameters(p1, p2)

    def test_field_description(self):
        p1 = pydantic_field_to_parameter(Hero.__fields__["description"])
        p2 = Parameter(
            "description",
            Parameter.POSITIONAL_OR_KEYWORD,
            annotation=Annotated[str, typer.Option(help="very fast")],
            default=Parameter.empty,
        )
        self.assertEqualParameters(p1, p2)

    def test_pydantic_model_to_parameters(self):
        for p1, p2 in zip(
            pydantic_model_to_parameters(Hero),
            [
                Parameter(
                    "name",
                    Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=Annotated[str, typer.Option()],
                    default=Parameter.empty,
                ),
                Parameter(
                    "tags",
                    Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=Annotated[Optional[List[str]], typer.Option()],
                    default=None,
                ),
                Parameter(
                    "description",
                    Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=Annotated[str, typer.Option(help="very fast")],
                    default=Parameter.empty,
                ),
            ],
        ):
            self.assertEqualParameters(p1, p2)

    def test_override_function_signature(self):
        def func(*args, **kwargs):
            pass

        override_function_signature(
            func,
            "func_func",
            [
                Parameter("x", Parameter.POSITIONAL_OR_KEYWORD, annotation=str),
            ],
        )
        self.assertEqual(
            inspect.signature(func),
            inspect.Signature(
                parameters=[
                    Parameter("x", Parameter.POSITIONAL_OR_KEYWORD, annotation=str),
                ]
            ),
        )
        self.assertEqual(func.__name__, "func_func")

    def test_as_typer_command_func(self):
        def func(*args, **kwargs):
            pass

        class Params(BaseModel):
            name: str

        as_typer_command_func(
            func,
            "func_func",
            Params,
        )
        for p1, p2 in zip(
            list(inspect.signature(func).parameters.values()),
            [
                Parameter(
                    "name",
                    Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=Annotated[str, typer.Option()],
                    default=Parameter.empty,
                ),
            ],
        ):
            self.assertEqualParameters(p1, p2)
        self.assertEqual(func.__name__, "func_func")
