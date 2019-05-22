# -*- coding: utf-8 -*-
#
# Licensed under the terms of the MIT License

"""."""

# Third Party Libraries Imports
import pytest

# Local imports
from filterdesigner.main import QDesignerMainWindow
from filterdesigner.lpf import LeastSquareLPF

# @pytest.fixture
def test_mainwindow_init(qtbot):
    mainwindow = QDesignerMainWindow()
    qtbot.addWidget(mainwindow)

    assert mainwindow


# def test_name():
#     l = LeastSquareLPF()
#     assert l.name == 'LeastSquare'
