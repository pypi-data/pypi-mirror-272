import functools
from typing import Callable, Generator
from typing import Dict, Generator, Iterator, List, Union, Optional, overload, Type, Any


def make_pipeline(
        *funcs: Callable[..., Generator[Any, None, None]]
) -> Callable[..., Generator[Any, None, None]]:
    """ Make pipeline of generators.

    https://github.com/wwwcojp/ja_sentence_segmenter/blob/main/ja_sentence_segmenter/common/pipeline.py
    """

    def composite(
            func1: Callable[..., Generator[Any, None, None]],
            func2: Callable[..., Generator[Any, None, None]]
    ) -> Callable[..., Generator[Any, None, None]]:
        return lambda x: func2(func1(x))

    return functools.reduce(composite, funcs)


