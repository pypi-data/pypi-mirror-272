from typing import Optional, TYPE_CHECKING

from PySide6.QtWidgets import (
    QGroupBox, QButtonGroup
)

from modernqt.src.core import Loader

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget


class GroupBox(QGroupBox):
    def __init__(
            self,
            title: Optional[str] = None,
            *,
            stylesheet: Optional[str] = None,
            parent: Optional["QWidget"] = None
    ) -> None:
        super().__init__(parent)

        self.setObjectName("group-box")
        if stylesheet is not None:
            self.setStyleSheet(
                Loader.load_file("modernqt/widgets/basic/styles/group_box.css") + "\n" 
                + stylesheet.replace("GroupBox", "QGroupBox#group-box")
            )
        else:
            self.setStyleSheet(Loader.load_file("modernqt/widgets/basic/styles/group_box.css"))

        if title is not None: self.setTitle(title)
