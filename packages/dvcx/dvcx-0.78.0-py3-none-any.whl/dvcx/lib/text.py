import inspect
from typing import Any, Optional

from dvcx.lib.feature import (
    Feature,
)
from dvcx.lib.feature_types import ColumnFeature, FeatureTypes, overwrite_value_function


def convert_text(
    clm: ColumnFeature,
    tokenizer=None,
    tokenizer_kwargs: Optional[dict[str, Any]] = None,
    open_clip_model=None,
):
    if open_clip_model:
        method_name = "encode_text"
        if not (
            hasattr(open_clip_model, method_name)
            and inspect.ismethod(getattr(open_clip_model, method_name))
        ):
            raise ValueError(
                f"TextColumn error: 'model' doesn't support '{method_name}()'"
            )

    text = clm._get_column_value()
    if not tokenizer:
        return text

    res = tokenizer([text], **tokenizer_kwargs)
    from transformers.tokenization_utils_base import PreTrainedTokenizerBase

    tokens = (
        res.input_ids[0] if isinstance(tokenizer, PreTrainedTokenizerBase) else res[0]
    )
    if not open_clip_model:
        return tokens

    return open_clip_model.encode_text(tokens)


def TextColumn(  # noqa
    name: str,
    typ=Any,
    default=None,
    tokenizer=None,
    tokenizer_kwargs=None,
    open_clip_model=None,
) -> type[Feature]:
    return overwrite_value_function(
        FeatureTypes.column_class(name, typ, default),
        func=convert_text,
        tokenizer=tokenizer,
        tokenizer_kwargs=tokenizer_kwargs,
        open_clip_model=open_clip_model,
    )
