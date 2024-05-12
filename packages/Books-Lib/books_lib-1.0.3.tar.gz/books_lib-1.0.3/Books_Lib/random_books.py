import pkg_resources
import pandas as pd

class SelectBooks:
    FILE_PATH = pkg_resources.resource_filename(__name__,'books.csv')

    def __init__(self):
        self._file = pd.read_csv(SelectBooks.FILE_PATH)


    def buscar_Author(author):
        file = "books.csv"
        datos = pd.read_csv(file)
        buscar = datos[datos["Author"] == author]
        if buscar.size == 0:
            return "No se encontro el autor"
        else:
            return buscar

    def buscar_Title(title):
        file = "books.csv"
        datos = pd.read_csv(file)
        buscar = datos[datos["Title"] == title]
        if buscar.size == 0:
            return "No se encontro el titulo "
        else:
            return buscar

