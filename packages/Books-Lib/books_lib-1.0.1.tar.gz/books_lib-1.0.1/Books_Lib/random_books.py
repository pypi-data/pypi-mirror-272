import pkg_resources
import pandas as pd

class SelectBooks:
    FILE_PATH = pkg_resources.resource_filename(__name__,'books.csv')

    def __init__(self):
        self._file = pd.read_csv(SelectBooks.FILE_PATH)
        self._title = None
        self._author = None
        self._genre = None
        self._height = None
        self._publisher = None

    def gen_books(self):
        self._books = self._file.sample()
        self._title = self._books["Title"].values[0]
        self._author = self._books["Author"].values[0]
        self._genre = self._books["Genre"].values[0]
        self._height = self._books["Height"].values[0]
        self._publisher = self._books["Publisher"].values[0]


    def getAuthor(_autor):
        file = "books.csv"
        dat = pd.read_csv(file)
        bus = dat[dat["Author"] == _autor]
        if bus.size == 0:
            return "No se encontro el autor"
        else:
            return bus

    def getTitle(_title):
        file = "books.csv"
        dat = pd.read_csv(file)
        bus = dat[dat["Title"] == _title]
        if bus.size == 0:
            return "No se encontro el titulo "
        else:
            return bus

