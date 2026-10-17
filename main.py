"""Minimal Windows floating button that captures the primary screen to Clipboard."""
from __future__ import annotations

import sys

from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QColor, QGuiApplication, QPainter, QPen, QBrush
from PySide6.QtWidgets import QApplication, QWidget, QMenu, QMessageBox


class ScreenshotDot(QWidget):
    SIZE = 44

    def __init__(self) -> None:
        super().__init__()
        self._capturing = False
        self._capture_ok = False

        self.setWindowTitle("Screen Dot")
        self.setToolTip("Бір рет бас — скриншот Clipboard-қа көшіріледі. Қою үшін Ctrl+V.")
        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setFixedSize(self.SIZE, self.SIZE)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        screen = QGuiApplication.primaryScreen()
        if screen is not None:
            area = screen.availableGeometry()
            self.move(area.right() - self.width() - 24, area.bottom() - self.height() - 52)

    def paintEvent(self, _event) -> None:  # noqa: N802 - Qt override
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        rect = QRectF(2, 2, self.width() - 4, self.height() - 4)
        fill = QColor(20, 115, 55, 250) if self._capture_ok else QColor(15, 15, 15, 248)
        painter.setPen(QPen(QColor(255, 255, 255, 225), 2))
        painter.setBrush(QBrush(fill))
        painter.drawEllipse(rect)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802 - Qt override
        if event.button() == Qt.MouseButton.LeftButton:
            self.capture_screen()
        else:
            super().mouseReleaseEvent(event)

    def contextMenuEvent(self, event) -> None:  # noqa: N802 - Qt override
        menu = QMenu(self)
        exit_action = menu.addAction("Жабу / Exit")
        chosen = menu.exec(event.globalPos())
        if chosen == exit_action:
            QApplication.quit()

    def capture_screen(self) -> None:
        if self._capturing:
            return
        self._capturing = True
        self._capture_ok = False
        self.hide()  # Keep the floating button out of the screenshot.
        # Let Windows repaint the area behind the hidden button.
        QTimer.singleShot(180, self._capture_hidden_screen)

    def _capture_hidden_screen(self) -> None:
        try:
            app = QApplication.instance()
            screen = QGuiApplication.primaryScreen()
            if app is None or screen is None:
                raise RuntimeError("Экран табылмады.")

            app.processEvents()
            pixmap = screen.grabWindow(0)
            if pixmap.isNull():
                raise RuntimeError("Скриншот түсіру сәтсіз аяқталды.")

            # Copy the screenshot image directly into the Windows Clipboard.
            QGuiApplication.clipboard().setImage(pixmap.toImage())
            self._capture_ok = True
            QTimer.singleShot(450, self._clear_success_state)
        except Exception as exc:
            QMessageBox.warning(
                self,
                "Screen Dot",
                "Скриншот түсіру мүмкін болмады.\n\n"
                f"Қате: {exc}\n\n"
                "Бағдарламаны қайта ашып көр.",
            )
        finally:
            self.show()
            self.raise_()
            self.activateWindow()
            self.update()
            self._capturing = False

    def _clear_success_state(self) -> None:
        self._capture_ok = False
        self.update()


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Screen Dot")
    app.setQuitOnLastWindowClosed(False)

    dot = ScreenshotDot()
    dot.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
