# -*- coding: utf-8 -*-
"""Run Filter Designer."""

# Standard library imports
import sys

# Third party imports
from jupyterthemes import jtplot

from qdarkstyle import load_stylesheet_from_environment
from qtpy.QtWidgets import (QMainWindow, QApplication, QStackedWidget)

# Local import
from filterdesigner.config import UserConfig as CONF
from filterdesigner.filterdesign.filterwidget import FilterDesignWidget


class QDesignerMainWindow(QMainWindow):
    """Main Window of Filter Designer."""
    def __init__(self, parent=None):
        super(QDesignerMainWindow, self).__init__(parent)

        if CONF.dark_theme:
            jtplot.style('onedork', fscale=0.8)
        else:
            jtplot.style('grade3', fscale=0.8)
        self.stacked_widget = QStackedWidget(self)

        # Widget Add
        self.stacked_widget.addWidget(FilterDesignWidget(self))

        self.setCentralWidget(self.stacked_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QDesignerMainWindow()

    # setup stylesheet
    if CONF.dark_theme:
        app.setStyleSheet(load_stylesheet_from_environment())

    # run
    window.show()
    sys.exit(app.exec_())
