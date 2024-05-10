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

from typing import Any
from jinja2 import Environment, PackageLoader, select_autoescape

from datasurface.md import Datastore
from datasurface.md import Dataset
from datasurface.md import DDLTable
from datasurface.md.Schema import DDLColumn, DEFAULT_nullable, DEFAULT_primaryKey


def getDatasets(store: Datastore) -> list[Any]:
    datasets: list[Any] = []
    for dataset in store.datasets.values():
        if (dataset):
            datasets.append(dataset)
    return datasets


def getColumns(dataset: Dataset) -> list[DDLColumn]:
    columns: list[DDLColumn] = []
    if (dataset.originalSchema and isinstance(dataset.originalSchema, DDLTable)):
        table: DDLTable = dataset.originalSchema
        for column in table.columns.values():
            if (column):
                columns.append(column)
    return columns


def convertColumnAttributesToString(column: DDLColumn) -> str:
    rc: str = ""
    if (column.nullable != DEFAULT_nullable):
        rc += f", {column.nullable}"
    if (column.classification is not None):
        rc += f", {column.classification}"
    if (column.primaryKey != DEFAULT_primaryKey):
        rc += f", {column.primaryKey}"
    return rc


def generate_code(store: Datastore) -> str:
    env = Environment(
        loader=PackageLoader('datasurface.codegen', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('datastore.jinja2', None)

    data: dict[str, Any] = {}
    data["datastore"] = store
    data["getDatasets"] = getDatasets
    data["getColumns"] = getColumns
    data["convertColumnAttributesToString"] = convertColumnAttributesToString
    code: str = template.render(data)
    return code
