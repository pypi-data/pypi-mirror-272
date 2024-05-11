from __future__ import annotations

from typing import Annotated, Any, Dict, Generic, List, TypeVar

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    ImportString,
)

T = TypeVar("T")


class PluginModel(BaseModel, Generic[T]):
    model_config = ConfigDict(
        arbitrary_types_allowed=True, extra="forbid", frozen=True
    )

    obj: ImportString | Any = Field(
        description="Plugin's object.",
        examples=["builtins.len", "sklearn.preprocessing.StandardScaler"],
    )
    init: bool = Field(
        description="Whether to call the obj with args and kwargs.",
        default=True,
    )
    args: List[ImportPlugin | Any] = Field(
        default_factory=list,
        description="Arguments passed to the object along with kwargs if"
        " init=True. Arguments representing a ImportPlugin are resolved to the"
        " plugin's value.",
        examples=[
            [5, True],
            [1, 2, 3],
            [{"obj": "builtins.len", "args": [1, 2, 3]}],
        ],
    )
    kwargs: Dict[str, ImportPlugin | Any] = Field(  # type: ignore
        default_factory=dict,
        description="keyword arguments passed to the object along with args if"
        " init=True. keyword arguments representing a ImportPlugin are"
        " resolved to the plugin's value.",
        examples=[
            {
                "param1": "val1",
                "param2": {"obj": "builtins.len", "args": [1, 2, 3]},
            }
        ],
    )

    def generate(self) -> T:
        """
        Generate the desired plugin.

        Returns:
            If `init` is set to False, `obj` is returned. Otherwise, the
            result of `obj(*args, **kwargs)` is returned.
        """
        if self.init:
            return self.obj(*self.args, **self.kwargs)
        return self.obj


def generate_plugin(plugin_dict: Dict):
    return PluginModel.model_validate(plugin_dict).generate()


ImportPlugin = Annotated[T, BeforeValidator(generate_plugin)]
