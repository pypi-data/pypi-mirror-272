from __future__ import annotations

from typing import IO, Any, Optional

from click import ClickException, echo

File_Data = dict[str, tuple[Optional[str], Any, Optional[str]]]
Metadata = dict[str, Any]


class KaasCliException(ClickException):
    def show(self, file: IO[Any] | None = None) -> None:
        echo(f'{self.message}', file=file)
