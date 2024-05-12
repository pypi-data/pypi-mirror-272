# Third-party
from PySide2 import QtWidgets
from PySide2.QtWidgets import QStyleFactory
from PySide2.QtGui import QPalette, QColor

# Internal
try:
    from fxgui import style
except ModuleNotFoundError:
    import style


###### CODE ####################################################################


class VFXApplication(QtWidgets.QApplication):
    def __init__(self):
        super().__init__()

        style.set_application_palette(self)
        style.set_application_style(self)
