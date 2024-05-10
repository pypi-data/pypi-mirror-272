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

from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import OperationalError
from datasurface.md import Datastore
from datasurface.md.SqlAlchemyUtils import convertSQLAlchemyTableSetToDatastore
from datasurface.codegen import generate_code

"""This test assumes a local postgres database with the northwind database loaded in the postgres database."""


def get_metadata():
    engine = None
    metadata = MetaData()
    try:
        engine = create_engine('postgresql://postgres:apjc3742@localhost:5432/postgres')
        connection = engine.connect()
        connection.commit()
        metadata.reflect(bind=engine)
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return metadata


# Disabled except when running locally, needs a postgres database
# with the northwind database loaded
def xtest_get_metadata():
    """This test assumes a local postgres database with the northwind database loaded in the postgres database."""
    metadata = get_metadata()
    store: Datastore = convertSQLAlchemyTableSetToDatastore("Test_Store", list(metadata.tables.values()))
    for dataset in store.datasets.values():
        if (dataset):
            print("Dataset: {}".format(dataset.name))
    assert store.name == "Test_Store"
    code: str = generate_code(store)
    print(code)
    assert len(metadata.tables) > 0
