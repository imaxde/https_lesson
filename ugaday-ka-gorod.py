import sys
import requests
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import QByteArray
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit
from random import choice
from search import object_position


CITIES = ["Москва", "Телеграф-Крик", "Кызылорда", "Поптун", "Джиэргалесайхан"]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.current = CITIES[0]
        self.initUI()
        self.nextCity()

    def getImage(self, ll, spn):
        server_address = "https://static-maps.yandex.ru/v1?"
        params = {
            "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
            "ll": ll,
            "spn": spn,
            "style": "tags.any:admin|stylers.visibility:off",
            "format": "json"}
        response = requests.get(server_address, params=params)
        return QImage().fromData(QByteArray(response.content))

    def initUI(self):
        self.setGeometry(100, 100, 600, 500)
        self.setWindowTitle("Отображение карты")
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.field = QLineEdit(self)
        self.field.move(240, 470)
        self.field.textEdited.connect(self.checkAnswer)

    def nextCity(self):
        self.current = choice(CITIES)
        location = object_position(self.current)
        img = self.getImage(",".join(location[:2]), ",".join(location[2:]))
        self.image.setPixmap(QPixmap(img))
        self.field.clear()

    def checkAnswer(self):
        if self.field.text() == self.current:
            self.field.setReadOnly(True)
            self.nextCity()
            self.field.setReadOnly(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())

