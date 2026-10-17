"""Minimal Windows floating button that captures the primary screen to Clipboard."""
from __future__ import annotations

import sys

from PySide6.QtCore import Qt, QTimer, QRectF, QPoint
from PySide6.QtGui import QColor, QGuiApplication, QPainter, QPen, QBrush
from PySide6.QtWidgets import QApplication, QWidget, QMenu, QMessageBox


class ScreenshotDot(QWidget):
    SIZE = 28

    def __init__(self) -> None:
        super().__init__()
        self._capturing = False
        self._capture_ok = False
        self._press_global_pos: QPoint | None = None
        self._window_start_pos: QPoint | None = None
        self._was_dragged = False

        self.setWindowTitle("Screen Dot")
        self.setToolTip(
            "Сол жақ шерту: скриншот түсіру | "
            "Басып тұрып сүйреу: орнын ауыстыру | Оң жақ шерту: шығу"
        )
        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        self.setFixedSize(self.SIZE, self.SIZE)
        self.setCursor(Qt.CursorShape.SizeAllCursor)

        screen = QGuiApplication.primaryScreen()
        if screen is not None:
            area = screen.availableGeometry()
            self.move(area.right() - self.width() - 24, area.bottom() - self.height() - 52)

    def paintEvent(self, _event) -> None:  # noqa: N802 - Qt override
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        rect = QRectF(1.5, 1.5, self.width() - 3, self.height() - 3)
        fill = QColor(20, 115, 55, 250) if self._capture_ok else QColor(15, 15, 15, 248)
        painter.setPen(QPen(QColor(255, 255, 255, 220), 1))
        painter.setBrush(QBrush(fill))
        painter.drawEllipse(rect)

    def mousePressEvent(self, event) -> None:  # noqa: N802 - Qt override
        if event.button() == Qt.MouseButton.LeftButton:
            self._press_global_pos = event.globalPosition().toPoint()
            self._window_start_pos = self.pos()
            self._was_dragged = False
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:  # noqa: N802 - Qt override
        if (
            self._press_global_pos is not None
            and self._window_start_pos is not None
            and event.buttons() & Qt.MouseButton.LeftButton
        ):
            current_pos = event.globalPosition().toPoint()
            delta = current_pos - self._press_global_pos
            if delta.manhattanLength() >= 3:
                self._was_dragged = True
            if self._was_dragged:
                self.move(self._window_start_pos + delta)
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802 - Qt override
        if event.button() == Qt.MouseButton.LeftButton:
            was_dragged = self._was_dragged
            self._press_global_pos = None
            self._window_start_pos = None
            self._was_dragged = False
            if not was_dragged:
                self.capture_screen()
            event.accept()
            return
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
