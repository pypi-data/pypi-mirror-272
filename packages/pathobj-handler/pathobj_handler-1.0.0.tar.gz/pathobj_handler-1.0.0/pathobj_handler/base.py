from typing import Dict, Generator, Iterator, List, Union, Optional, overload, Type, Any
from abc import ABCMeta, abstractmethod


class ProcessorBase(metaclass=ABCMeta):
    """
    input_data に何らか処理を行うジェネレータの抽象基底クラス。

    self.process_handling(Any)->Any

    サブクラスにおいて、@abstractmethodであるprocess_handling()をオーバーライドして利用してください。
    """

    def __call__(
            self,
            input_data: Union[Any, List[Any], Iterator[Any]],
    ) -> Generator[Any, None, None]:
        return self.process(input_data)

    @abstractmethod
    def process_handling(
            self,
            path: Any,
    ) -> Any:
        raise NotImplementedError

    def __process_iter(
            self,
            paths: Iterator[Any],
    ) -> Generator[Any, None, None]:
        for p in paths:
            out_p = self.process_handling(p)
            if not out_p:
                continue
            yield out_p

    @overload
    def process(self, input_data: Any) -> Generator[Any, None, None]:
        pass

    @overload
    def process(self, input_data: List[Any]) -> Generator[Any, None, None]:
        pass

    @overload
    def process(self, input_data: Iterator[Any]) -> Generator[Any, None, None]:
        pass

    def process(
            self,
            input_data: Union[Any, List[Any], Iterator[Any]],
    ) -> Generator[Any, None, None]:
        if isinstance(input_data, list):
            yield from self.__process_iter(iter(input_data))
        elif isinstance(input_data, Iterator):
            yield from self.__process_iter(input_data)
        elif input_data:
            yield from self.__process_iter(iter([input_data]))


class GenerateBase(metaclass=ABCMeta):
    """
    input_data からさらにgeneratorを生成する（たとえばTextを分割し、複数のTextを生成）するジェネレータの抽象基底クラス。

    self.generate_handling(Any) -> Generator[Any, None, None]

    サブクラスにおいて、@abstractmethodであるsplit_handling()をオーバーライドして利用してください。
    """

    def __call__(
            self,
            input_data: Union[Any, List[Any], Iterator[Any]],
    ) -> Generator[Any, None, None]:
        return self.generate(input_data)

    @abstractmethod
    def generate_handling(
            self,
            path: Any,
    ) -> Generator[Any, None, None]:
        raise NotImplementedError

    def __generate_iter(
            self,
            paths: Iterator[Any],
    ) -> Generator[Any, None, None]:
        for p in paths:
            # print(text)
            return self.generate_handling(p)

    @overload
    def generate(self, input_data: Any) -> Generator[Any, None, None]:
        pass

    @overload
    def generate(self, input_data: List[Any]) -> Generator[Any, None, None]:
        pass

    @overload
    def generate(self, input_data: Iterator[Any]) -> Generator[Any, None, None]:
        pass

    def generate(
            self,
            input_data: Union[Any, List[Any], Iterator[Any]],
    ) -> Generator[Any, None, None]:
        if isinstance(input_data, list):
            yield from self.__generate_iter(iter(input_data))
        elif isinstance(input_data, Iterator):
            yield from self.__generate_iter(input_data)
        elif input_data:
            yield from self.__generate_iter(iter([input_data]))
