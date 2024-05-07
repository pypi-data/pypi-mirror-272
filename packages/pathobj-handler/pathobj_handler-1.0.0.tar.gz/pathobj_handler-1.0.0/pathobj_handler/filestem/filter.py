from typing import List, Union, Optional, Callable

from pathlib import Path

from datetime import datetime
import re
from dateutil import parser

from ..base import ProcessorBase


class FilterByCustomFunction(ProcessorBase):

    def __init__(
            self,
            filter_method: Callable[[str], bool],
    ):
        """
        :param filter_method: Callable[[str], bool]
        フィルタリングで使用するCallableな関数を渡す。
        この関数は、引数として与えた文字列が、ピックアップの対象である場合である場合にTrueを返すように設計しておく。
        """

        self._is_target: Callable[[str], bool] = filter_method

    def process_handling(
            self,
            file: Union[str, Path],
    ) -> Optional[Path]:
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

        is_target = self._is_target(stem)

        return p_file if is_target else None


''' ---------- Examples of concrete filters --------------- '''


class FilterWithDateRange(FilterByCustomFunction):
    def __init__(
            self,
            re_time: str,
            dt_from: datetime,
            dt_to: datetime,
    ):
        """
        '20240410T150525_DDDDDD111111_AAA.txt'の'20240410T150525'の部分を正規表現で取り出して日付判定する
        :param re_time:
            e.g. r'/d+T/d+'
        :param dt_from:
            e.g. datetime(2024, 4, 5)
        :param dt_to:
            e.g. datetime(2024, 4, 15)
        """

        def is_target(stem: str) -> bool:
            m = re.search(re_time, stem)
            if m is None:
                return False
            dt_stem = parser.parse(m.group())
            if dt_from <= dt_stem <= dt_to:
                return True
            return False

        super().__init__(is_target)


class FilterWithRegExp(FilterByCustomFunction):
    def __init__(
            self,
            re_list: List[str],
    ):
        """

        :param re_list:
            正規表現の文字列（単純一致であれば該当文字列）をList[str]で与える
            [ 'hoge', 'fuga' ] とした場合、file_handlingに引数として与えた
            ファイルオブジェクトのファイル名（stem）に'hoge'が'fuga'が含まれていれば、ピックアップする対象となる。
        """

        def is_target(stem: str) -> bool:
            # boot_list = [t in stem for t in reg_exp_list]  # 単純一致
            boot_list = [re.search(t, stem) for t in re_list]  # 正規表現の一致（単純一致含む）
            return any(boot_list)

        super().__init__(is_target)

