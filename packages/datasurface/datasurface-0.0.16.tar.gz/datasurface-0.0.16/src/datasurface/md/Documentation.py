"""
Copyright (C) 2024 William Newport

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Optional

from datasurface.md.Lint import ValidationTree


class Documentation(ABC):
    def __init__(self, description: str, tags: Optional[OrderedDict[str, str]] = None) -> None:
        self.description: str = description
        self.tags: Optional[OrderedDict[str, str]] = tags

    def __eq__(self, other: object):
        if (not isinstance(other, Documentation)):
            return False
        return self.description == other.description and self.tags == other.tags

    def __str__(self) -> str:
        return "Documentation()"

    @abstractmethod
    def lint(self, tree: ValidationTree):
        pass


class Documentable:
    def __init__(self, documentation: Optional[Documentation]) -> None:
        self.documentation: Optional[Documentation] = documentation

    def __eq__(self, __value: object):
        if (not isinstance(__value, Documentable)):
            return False
        return self.documentation == __value.documentation

    def __str__(self) -> str:
        return f"Documentable({self.documentation})"


class PlainTextDocumentation(Documentation):
    def __init__(self, description: str, tags: Optional[OrderedDict[str, str]] = None) -> None:
        super().__init__(description, tags)

    def __eq__(self, other: object):
        if (not isinstance(other, PlainTextDocumentation)):
            return False
        return super().__eq__(other)

    def lint(self, tree: ValidationTree):
        pass


class MarkdownDocumentation(Documentation):
    def __init__(self, description: str, markdown: str, tags: Optional[OrderedDict[str, str]] = None) -> None:
        super().__init__(description, tags)
        self.markdown: str = markdown

    def __eq__(self, other: object):
        if (not isinstance(other, MarkdownDocumentation)):
            return False
        return super().__eq__(other) and self.markdown == other.markdown

    def lint(self, tree: ValidationTree):
        pass
