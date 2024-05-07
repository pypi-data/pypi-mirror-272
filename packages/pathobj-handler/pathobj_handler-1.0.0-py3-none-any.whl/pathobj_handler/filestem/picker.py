import pathlib
from typing import Generator, Iterator, List, Dict, Tuple, Union, Optional, overload, Type, Any

from pathlib import Path

from ..base import ProcessorBase, GenerateBase


class PickFilesBySuffix(GenerateBase):

    def __init__(
            self,
            file_suffix: Union[str, List[str]],
            recursive: bool = False
    ):
        """
        This class picks up files with a specified extension in the source directory.

        Parameters
        ----------
        file_suffix : Specify the suffix of the files to search.
        recursive : Whether to search recursively or not.
        """

        assert file_suffix, "Need to specify the file extension. It is currently empty."
        self._recursive = recursive

        self._file_suffix_list = []
        if isinstance(file_suffix, str):
            self._file_suffix_list.append(file_suffix)
        if isinstance(file_suffix, list):
            self._file_suffix_list = file_suffix

    def generate_handling(
            self,
            src_dir: Union[str, Path],
    ) -> Generator[pathlib.Path, None, None]:
        """

        :param src_dir:
        The source directory as a starting pont for search.
        :return:
        """

        if isinstance(src_dir, type(None)):
            p_src_dir = Path.cwd()
        elif isinstance(src_dir, str):
            p_src_dir = Path(src_dir)
        elif isinstance(src_dir, Path):
            p_src_dir = src_dir
        else:
            raise TypeError(f"Type '{type(src_dir)}' is not assignable to type '{type(pathlib.Path)}'.")

        if not p_src_dir.is_dir():
            raise ValueError(f"Need to specify a directory path. {p_src_dir} is not a directory.")

        globs = []

        for suffix in self._file_suffix_list:
            wild_card = "*" + suffix
            if self._recursive:  # for recursive search
                wild_card = "**/" + wild_card
            globs.append(p_src_dir.glob(wild_card))

        def all_gen(gen_list: list[Generator[Any, None, None]]) -> Generator[Any, None, None]:
            for g in gen_list:
                yield from g

        return all_gen(globs)

