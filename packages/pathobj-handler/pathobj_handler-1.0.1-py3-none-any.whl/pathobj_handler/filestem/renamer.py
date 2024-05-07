from typing import Union, Callable

from pathlib import Path

from ..base import ProcessorBase


class RenameFilesByCustomFunction(ProcessorBase):

    def __init__(
            self,
            rename_method: Callable[[str], str],
    ):
        """
        :param rename_method:
        """
        self._rename = rename_method

    def process_handling(
            self,
            file: Union[str, Path],
    ) -> Path:
        """
        :param file:
        :return:
        """
        if isinstance(file, str):
            p_file = Path(file)
        elif isinstance(file, Path):
            p_file = file
        else:
            raise TypeError(f"Type '{type(file)}' is not assignable to type '{type(Path)}'.")

        if not p_file.is_file():
            raise ValueError(f"Need to specify a file path. {p_file} is not a file.")

        stem = p_file.stem
        suffix = p_file.suffix
        new_stem = self._rename(stem)
        new_path = p_file.with_name(new_stem + suffix)
        p_r_file = p_file.rename(new_path)
        return p_r_file


''' ---------- Examples of concrete renamers --------------- '''


class RenamerWithReplaceStr(RenameFilesByCustomFunction):
    def __init__(
            self,
            old: str,
            new: str,
    ):
        """
        与えられたファイルオブジェクトのstemに含まれる文字列のうち、oldで指定された文字列を全てnewに置き換える

        :param old:
            置換するターゲットとなる文字列
        :param new:
            置き換える文字列
        """

        def replace_stem(src_stem: str) -> str:
            return src_stem.replace(old, new)

        super().__init__(replace_stem)
