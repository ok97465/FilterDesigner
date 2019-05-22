# -*- coding: utf-8 -*-
#
# Licensed under the terms of the MIT License

"""."""

# Third party imports
from numpy import ndarray
from qtpy.QtGui import QIntValidator, QDoubleValidator
from qtpy.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                            QRadioButton, QButtonGroup)

# Local import
from scipy.signal import firls, remez

from filterdesigner.filterbase import (FilterBase, TYPE_LPF, TYPE_BPF,
                                       TYPE_BSF, TYPE_HPF)


class EquiRipple(FilterBase):
    """."""
    def __init__(self, ui_parent):
        self.ui_parent = ui_parent
        self.name = 'Equiripple'

        # ui_order
        self.order_layout: QVBoxLayout = None
        self.order_line: QLineEdit = None

        # ui_options
        self.options_layout: QVBoxLayout = None
        self.density_line: QLineEdit = None

        # ui_frequency
        self.fre_layout: QVBoxLayout = None
        self.fs_label: QLabel = None
        self.fs_line: QLineEdit = None
        self.fre1_label: QLabel = None
        self.fre1_line: QLineEdit = None
        self.fre2_label: QLabel = None
        self.fre2_line: QLineEdit = None
        self.fre3_label: QLabel = None
        self.fre3_line: QLineEdit = None
        self.fre4_label: QLabel = None
        self.fre4_line: QLineEdit = None

        # ui_magnitude
        self.mag_layout: QVBoxLayout = None
        self.mag_label: QLabel = None
        self.weight1_label: QLabel = None
        self.weight1_line: QLineEdit = None
        self.weight2_label: QLabel = None
        self.weight2_line: QLineEdit = None
        self.weight3_label: QLabel = None
        self.weight3_line: QLineEdit = None

    def generate_ui_order(self):
        self.order_line = QLineEdit('129', self.ui_parent)
        self.order_line.setValidator(QIntValidator(1, 8192))

        self.order_layout = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Specify order", self.ui_parent))
        hbox.addWidget(self.order_line)
        self.order_layout.addLayout(hbox)

    def generate_ui_options(self):
        self.options_layout = QHBoxLayout()
        label = QLabel("Density Factor")
        self.density_line = QLineEdit("16", self.ui_parent)
        self.density_line.setValidator(QIntValidator(1, 1000))
        self.options_layout.addWidget(label)
        self.options_layout.addWidget(self.density_line)

    def generate_ui_frequency(self):
        self.fre_layout = QVBoxLayout()

        hbox = QHBoxLayout()
        self.fs_label = QLabel("fs", self.ui_parent)
        self.fs_line = QLineEdit("1000", self.ui_parent)
        self.fs_line.setValidator(QDoubleValidator(1, 99999999, 10))
        hbox.addWidget(self.fs_label)
        hbox.addWidget(self.fs_line)
        self.fre_layout.addLayout(hbox)

        hbox = QHBoxLayout()
        self.fre1_label = QLabel("Fpass", self.ui_parent)
        self.fre1_line = QLineEdit('100', self.ui_parent)
        self.fre1_line.setValidator(QDoubleValidator(1, 99999999, 10))
        hbox.addWidget(self.fre1_label)
        hbox.addWidget(self.fre1_line)
        self.fre_layout.addLayout(hbox)

        hbox = QHBoxLayout()
        self.fre2_label = QLabel("Fstop")
        self.fre2_line = QLineEdit('200', self.ui_parent)
        self.fre2_line.setValidator(QDoubleValidator(1, 99999999, 10))
        hbox.addWidget(self.fre2_label)
        hbox.addWidget(self.fre2_line)
        self.fre_layout.addLayout(hbox)

        hbox = QHBoxLayout()
        self.fre3_label = QLabel("Fstop")
        self.fre3_line = QLineEdit('300', self.ui_parent)
        self.fre3_line.setValidator(QDoubleValidator(1, 99999999, 10))
        hbox.addWidget(self.fre3_label)
        hbox.addWidget(self.fre3_line)
        self.fre_layout.addLayout(hbox)

        hbox = QHBoxLayout()
        self.fre4_label = QLabel("Fstop")
        self.fre4_line = QLineEdit('400', self.ui_parent)
        self.fre4_line.setValidator(QDoubleValidator(1, 99999999, 10))
        hbox.addWidget(self.fre4_label)
        hbox.addWidget(self.fre4_line)
        self.fre_layout.addLayout(hbox)

        self.set_size_policy_when_hidden(self.fre1_label, True)
        self.set_size_policy_when_hidden(self.fre1_line, True)

        self.set_size_policy_when_hidden(self.fre2_label, True)
        self.set_size_policy_when_hidden(self.fre2_line, True)

        self.set_size_policy_when_hidden(self.fre3_label, True)
        self.set_size_policy_when_hidden(self.fre3_line, True)

        self.set_size_policy_when_hidden(self.fre4_label, True)
        self.set_size_policy_when_hidden(self.fre4_line, True)

    def generate_ui_magnitude(self):
        self.mag_layout = QVBoxLayout()

        self.mag_label = QLabel(
            "Enter a weight value for each band below")
        self.mag_label.setMaximumHeight(50)
        self.mag_label.setWordWrap(True)
        self.mag_layout.addWidget(self.mag_label)

        hbox = QHBoxLayout()
        self.weight1_label = QLabel("Wpass")
        self.weight1_line = QLineEdit()
        self.weight1_line.setValidator(QDoubleValidator(1, 9999, 10))
        self.weight1_line.setText('1')
        hbox.addWidget(self.weight1_label)
        hbox.addWidget(self.weight1_line)
        self.mag_layout.addLayout(hbox)

        hbox = QHBoxLayout()
        self.weight2_label = QLabel("Wstop")
        self.weight2_line = QLineEdit()
        self.weight2_line.setValidator(QDoubleValidator(1, 9999, 10))
        self.weight2_line.setText('80')
        hbox.addWidget(self.weight2_label)
        hbox.addWidget(self.weight2_line)
        self.mag_layout.addLayout(hbox)

        hbox = QHBoxLayout()
        self.weight3_label = QLabel("Wstop")
        self.weight3_line = QLineEdit()
        self.weight3_line.setValidator(QDoubleValidator(1, 9999, 10))
        self.weight3_line.setText('80')
        hbox.addWidget(self.weight3_label)
        hbox.addWidget(self.weight3_line)
        self.mag_layout.addLayout(hbox)

        self.set_size_policy_when_hidden(self.weight1_label, True)
        self.set_size_policy_when_hidden(self.weight1_line, True)

        self.set_size_policy_when_hidden(self.weight2_label, True)
        self.set_size_policy_when_hidden(self.weight2_line, True)

        self.set_size_policy_when_hidden(self.weight3_label, True)
        self.set_size_policy_when_hidden(self.weight3_line, True)

    def get_ui_order(self, filter_type):
        self.generate_ui_order()
        return self.order_layout

    def get_ui_options(self, filter_type):
        self.generate_ui_options()
        return self.options_layout

    def get_ui_frequency(self, filter_type):
        self.generate_ui_frequency()
        return self.fre_layout

    def get_ui_magnitude(self, filter_type):
        self.generate_ui_magnitude()
        return self.mag_layout

    def set_ui_options(self, filter_type):
        if filter_type == TYPE_LPF:
            self.fre1_label.setVisible(True)
            self.fre2_label.setVisible(True)
            self.fre3_label.setVisible(False)
            self.fre4_label.setVisible(False)

            self.fre1_line.setVisible(True)
            self.fre2_line.setVisible(True)
            self.fre3_line.setVisible(False)
            self.fre4_line.setVisible(False)

            self.fre1_label.setText("Fpass")
            self.fre2_label.setText("Fstop")

            self.weight1_label.setVisible(True)
            self.weight2_label.setVisible(True)
            self.weight3_label.setVisible(False)

            self.weight1_line.setVisible(True)
            self.weight2_line.setVisible(True)
            self.weight3_line.setVisible(False)

            self.weight1_label.setText("Wpass")
            self.weight2_label.setText("Wstop")

        elif filter_type == TYPE_HPF:
            self.fre1_label.setVisible(True)
            self.fre2_label.setVisible(True)
            self.fre3_label.setVisible(False)
            self.fre4_label.setVisible(False)

            self.fre1_line.setVisible(True)
            self.fre2_line.setVisible(True)
            self.fre3_line.setVisible(False)
            self.fre4_line.setVisible(False)

            self.fre1_label.setText("Fstop")
            self.fre2_label.setText("Fpass")

            self.weight1_label.setVisible(True)
            self.weight2_label.setVisible(True)
            self.weight3_label.setVisible(False)

            self.weight1_line.setVisible(True)
            self.weight2_line.setVisible(True)
            self.weight3_line.setVisible(False)

            self.weight1_label.setText("Wstop")
            self.weight2_label.setText("Wpass")

        elif filter_type == TYPE_BPF:
            self.fre1_label.setVisible(True)
            self.fre2_label.setVisible(True)
            self.fre3_label.setVisible(True)
            self.fre4_label.setVisible(True)

            self.fre1_line.setVisible(True)
            self.fre2_line.setVisible(True)
            self.fre3_line.setVisible(True)
            self.fre4_line.setVisible(True)

            self.fre1_label.setText("Fstop1")
            self.fre2_label.setText("Fpass1")
            self.fre3_label.setText("Fpass2")
            self.fre4_label.setText("Fstop2")

            self.weight1_label.setVisible(True)
            self.weight2_label.setVisible(True)
            self.weight3_label.setVisible(True)

            self.weight1_line.setVisible(True)
            self.weight2_line.setVisible(True)
            self.weight3_line.setVisible(True)

            self.weight1_label.setText("Wstop1")
            self.weight2_label.setText("Wpass1")
            self.weight3_label.setText("Wstop2")

        elif filter_type == TYPE_BSF:
            self.fre1_label.setVisible(True)
            self.fre2_label.setVisible(True)
            self.fre3_label.setVisible(True)
            self.fre4_label.setVisible(True)

            self.fre1_line.setVisible(True)
            self.fre2_line.setVisible(True)
            self.fre3_line.setVisible(True)
            self.fre4_line.setVisible(True)

            self.fre1_label.setText("Fpass1")
            self.fre2_label.setText("Fstop1")
            self.fre3_label.setText("Fstop2")
            self.fre4_label.setText("Fpass2")

            self.weight1_label.setVisible(True)
            self.weight2_label.setVisible(True)
            self.weight3_label.setVisible(True)

            self.weight1_line.setVisible(True)
            self.weight2_line.setVisible(True)
            self.weight3_line.setVisible(True)

            self.weight1_label.setText("Wpass1")
            self.weight2_label.setText("Wstop1")
            self.weight3_label.setText("Wpass2")

    def calc_filter(self, filter_type):
        """

        Parameters
        ----------
        filter_type: int
            [TYPE_LPF, TYPE_BPF, TYPE_BSF, TYPE_HPF]

        Returns
        -------
        (ndarray, float)
            taps, sampling frequency

        """
        n_tap = int(self.order_line.text())

        fs = float(self.fs_line.text())
        f1 = float(self.fre1_line.text())
        f2 = float(self.fre2_line.text())
        f3 = float(self.fre3_line.text())
        f4 = float(self.fre4_line.text())
        density = int(self.density_line.text())

        w1 = float(self.weight1_line.text())
        w2 = float(self.weight2_line.text())
        w3 = float(self.weight3_line.text())

        if filter_type == TYPE_LPF:
            taps = remez(n_tap, [0, f1, f2, fs / 2], [1, 0], [w1, w2],
                         grid_density=density, fs=fs)
        elif filter_type == TYPE_HPF:
            taps = remez(n_tap, [0, f1, f2, fs / 2], [0, 1], [w1, w2],
                         grid_density=density, fs=fs)
        elif filter_type == TYPE_BPF:
            taps = remez(n_tap, [0, f1, f2, f3, f4, fs / 2], [0, 1, 0],
                         [w1, w2, w3],
                         grid_density=density, fs=fs)
        else:
            taps = remez(n_tap, [0, f1, f2, f3, f4, fs / 2], [1, 0, 1],
                         [w1, w2, w3],
                         grid_density=density, fs=fs)

        return taps, fs


class LeastSquare(FilterBase):
    """."""

    def __init__(self, ui_parent):
        self.ui_parent = ui_parent
        self.name = 'Least-squares'

        # ui_order
        self.order_layout: QVBoxLayout = None
        self.order_line: QLineEdit = None

        # ui_options
        self.options_layout: QVBoxLayout = None
        self.density_line: QLineEdit = None

        # ui_frequency
        self.fre_layout: QVBoxLayout = None
        self.fs_label: QLabel = None
        self.fs_line: QLineEdit = None
        self.fre1_label: QLabel = None
        self.fre1_line: QLineEdit = None
        self.fre2_label: QLabel = None
        self.fre2_line: QLineEdit = None
        self.fre3_label: QLabel = None
        self.fre3_line: QLineEdit = None
        self.fre4_label: QLabel = None
        self.fre4_line: QLineEdit = None

        # ui_magnitude
        self.mag_layout: QVBoxLayout = None
        self.mag_label: QLabel = None
        self.weight1_label: QLabel = None
        self.weight1_line: QLineEdit = None
        self.weight2_label: QLabel = None
        self.weight2_line: QLineEdit = None
        self.weight3_label: QLabel = None
        self.weight3_line: QLineEdit = None

    def generate_ui_order(self):
        self.order_line = QLineEdit()
        self.order_line.setValidator(QIntValidator(1, 9999999))
        self.order_line.setText('129')

        self.order_layout = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Specify order"))
        hbox.addWidget(self.order_line)
        self.order_layout.addLayout(hbox)

    def generate_ui_options(self):
        self.options_layout = QHBoxLayout()
        label = QLabel(
            "There are no optional parameters for this design method")
        label.setWordWrap(True)
        self.options_layout.addWidget(label)

    def generate_ui_frequency(self):
        self.fre_layout = QVBoxLayout()

        hbox = QHBoxLayout()
        self.fs_label = QLabel("fs")
        self.fs_line = QLineEdit()
        self.fs_line.setValidator(QDoubleValidator(1, 99999999, 10))
        self.fs_line.setText('1000')
        hbox.addWidget(self.fs_label)
        hbox.addWidget(self.fs_line)
        self.fre_layout.addLayout(hbox)

        hbox = QHBoxLayout()
        self.fre1_label = QLabel("Fpass")
        self.fre1_line = QLineEdit()
        self.fre1_line.setValidator(QDoubleValidator(1, 99999999, 10))
        self.fre1_line.setText('100')
        hbox.addWidget(self.fre1_label)
        hbox.addWidget(self.fre1_line)
        self.fre_layout.addLayout(hbox)

        hbox = QHBoxLayout()
        self.fre2_label = QLabel("Fstop")
        self.fre2_line = QLineEdit()
        self.fre2_line.setValidator(QDoubleValidator(1, 99999999, 10))
        self.fre2_line.setText('200')
        hbox.addWidget(self.fre2_label)
        hbox.addWidget(self.fre2_line)
        self.fre_layout.addLayout(hbox)

        hbox = QHBoxLayout()
        self.fre3_label = QLabel("Fstop")
        self.fre3_line = QLineEdit()
        self.fre3_line.setValidator(QDoubleValidator(1, 99999999, 10))
        self.fre3_line.setText('300')
        hbox.addWidget(self.fre3_label)
        hbox.addWidget(self.fre3_line)
        self.fre_layout.addLayout(hbox)

        hbox = QHBoxLayout()
        self.fre4_label = QLabel("Fstop")
        self.fre4_line = QLineEdit()
        self.fre4_line.setValidator(QDoubleValidator(1, 99999999, 10))
        self.fre4_line.setText('400')
        hbox.addWidget(self.fre4_label)
        hbox.addWidget(self.fre4_line)
        self.fre_layout.addLayout(hbox)

        self.set_size_policy_when_hidden(self.fre1_label, True)
        self.set_size_policy_when_hidden(self.fre1_line, True)

        self.set_size_policy_when_hidden(self.fre2_label, True)
        self.set_size_policy_when_hidden(self.fre2_line, True)

        self.set_size_policy_when_hidden(self.fre3_label, True)
        self.set_size_policy_when_hidden(self.fre3_line, True)

        self.set_size_policy_when_hidden(self.fre4_label, True)
        self.set_size_policy_when_hidden(self.fre4_line, True)

    def generate_ui_magnitude(self):
        self.mag_layout = QVBoxLayout()

        self.mag_label = QLabel(
            "Enter a weight value for each band below")
        self.mag_label.setWordWrap(True)
        self.mag_label.setMaximumHeight(50)
        self.mag_layout.addWidget(self.mag_label)

        hbox = QHBoxLayout()
        self.weight1_label = QLabel("Wpass")
        self.weight1_line = QLineEdit()
        self.weight1_line.setValidator(QDoubleValidator(1, 9999, 10))
        self.weight1_line.setText('1')
        hbox.addWidget(self.weight1_label)
        hbox.addWidget(self.weight1_line)
        self.mag_layout.addLayout(hbox)

        hbox = QHBoxLayout()
        self.weight2_label = QLabel("Wstop")
        self.weight2_line = QLineEdit()
        self.weight2_line.setValidator(QDoubleValidator(1, 9999, 10))
        self.weight2_line.setText('80')
        hbox.addWidget(self.weight2_label)
        hbox.addWidget(self.weight2_line)
        self.mag_layout.addLayout(hbox)

        hbox = QHBoxLayout()
        self.weight3_label = QLabel("Wstop")
        self.weight3_line = QLineEdit()
        self.weight3_line.setValidator(QDoubleValidator(1, 9999, 10))
        self.weight3_line.setText('80')
        hbox.addWidget(self.weight3_label)
        hbox.addWidget(self.weight3_line)
        self.mag_layout.addLayout(hbox)

        self.set_size_policy_when_hidden(self.weight1_label, True)
        self.set_size_policy_when_hidden(self.weight1_line, True)

        self.set_size_policy_when_hidden(self.weight2_label, True)
        self.set_size_policy_when_hidden(self.weight2_line, True)

        self.set_size_policy_when_hidden(self.weight3_label, True)
        self.set_size_policy_when_hidden(self.weight3_line, True)

    def get_ui_order(self, filter_type):
        self.generate_ui_order()
        return self.order_layout

    def get_ui_options(self, filter_type):
        self.generate_ui_options()
        return self.options_layout

    def get_ui_frequency(self, filter_type):
        self.generate_ui_frequency()
        return self.fre_layout

    def get_ui_magnitude(self, filter_type):
        self.generate_ui_magnitude()
        return self.mag_layout

    def set_ui_options(self, filter_type):
        if filter_type == TYPE_LPF:
            self.fre1_label.setVisible(True)
            self.fre2_label.setVisible(True)
            self.fre3_label.setVisible(False)
            self.fre4_label.setVisible(False)

            self.fre1_line.setVisible(True)
            self.fre2_line.setVisible(True)
            self.fre3_line.setVisible(False)
            self.fre4_line.setVisible(False)

            self.fre1_label.setText("Fpass")
            self.fre2_label.setText("Fstop")

            self.weight1_label.setVisible(True)
            self.weight2_label.setVisible(True)
            self.weight3_label.setVisible(False)

            self.weight1_line.setVisible(True)
            self.weight2_line.setVisible(True)
            self.weight3_line.setVisible(False)

            self.weight1_label.setText("Wpass")
            self.weight2_label.setText("Wstop")

        elif filter_type == TYPE_HPF:
            self.fre1_label.setVisible(True)
            self.fre2_label.setVisible(True)
            self.fre3_label.setVisible(False)
            self.fre4_label.setVisible(False)

            self.fre1_line.setVisible(True)
            self.fre2_line.setVisible(True)
            self.fre3_line.setVisible(False)
            self.fre4_line.setVisible(False)

            self.fre1_label.setText("Fstop")
            self.fre2_label.setText("Fpass")

            self.weight1_label.setVisible(True)
            self.weight2_label.setVisible(True)
            self.weight3_label.setVisible(False)

            self.weight1_line.setVisible(True)
            self.weight2_line.setVisible(True)
            self.weight3_line.setVisible(False)

            self.weight1_label.setText("Wstop")
            self.weight2_label.setText("Wpass")

        elif filter_type == TYPE_BPF:
            self.fre1_label.setVisible(True)
            self.fre2_label.setVisible(True)
            self.fre3_label.setVisible(True)
            self.fre4_label.setVisible(True)

            self.fre1_line.setVisible(True)
            self.fre2_line.setVisible(True)
            self.fre3_line.setVisible(True)
            self.fre4_line.setVisible(True)

            self.fre1_label.setText("Fstop1")
            self.fre2_label.setText("Fpass1")
            self.fre3_label.setText("Fpass2")
            self.fre4_label.setText("Fstop2")

            self.weight1_label.setVisible(True)
            self.weight2_label.setVisible(True)
            self.weight3_label.setVisible(True)

            self.weight1_line.setVisible(True)
            self.weight2_line.setVisible(True)
            self.weight3_line.setVisible(True)

            self.weight1_label.setText("Wstop1")
            self.weight2_label.setText("Wpass1")
            self.weight3_label.setText("Wstop2")

        elif filter_type == TYPE_BSF:
            self.fre1_label.setVisible(True)
            self.fre2_label.setVisible(True)
            self.fre3_label.setVisible(True)
            self.fre4_label.setVisible(True)

            self.fre1_line.setVisible(True)
            self.fre2_line.setVisible(True)
            self.fre3_line.setVisible(True)
            self.fre4_line.setVisible(True)

            self.fre1_label.setText("Fpass1")
            self.fre2_label.setText("Fstop1")
            self.fre3_label.setText("Fstop2")
            self.fre4_label.setText("Fpass2")

            self.weight1_label.setVisible(True)
            self.weight2_label.setVisible(True)
            self.weight3_label.setVisible(True)

            self.weight1_line.setVisible(True)
            self.weight2_line.setVisible(True)
            self.weight3_line.setVisible(True)

            self.weight1_label.setText("Wpass1")
            self.weight2_label.setText("Wstop1")
            self.weight3_label.setText("Wpass2")

    def calc_filter(self, filter_type):
        """

        Parameters
        ----------
        filter_type: int
            [TYPE_LPF, TYPE_BPF, TYPE_BSF, TYPE_HPF]

        Returns
        -------
        (ndarray, float)
            taps, sampling frequency

        """
        n_tap = int(self.order_line.text())

        fs = float(self.fs_line.text())
        f1 = float(self.fre1_line.text())
        f2 = float(self.fre2_line.text())
        f3 = float(self.fre3_line.text())
        f4 = float(self.fre4_line.text())

        w1 = float(self.weight1_line.text())
        w2 = float(self.weight2_line.text())
        w3 = float(self.weight3_line.text())

        if filter_type == TYPE_LPF:
            taps = firls(n_tap, [0, f1, f2, fs / 2], [1, 1, 0, 0],
                         [w1, w2], fs=fs)
        elif filter_type == TYPE_HPF:
            taps = firls(n_tap, [0, f1, f2, fs / 2], [0, 0, 1, 1],
                         [w1, w2], fs=fs)
        elif filter_type == TYPE_BPF:
            taps = firls(n_tap, [0, f1, f2, f3, f4, fs / 2],
                         [0, 0, 1, 1, 0, 0],
                         [w1, w2, w3], fs=fs)
        else:
            taps = firls(n_tap, [0, f1, f2, f3, f4, fs / 2],
                         [1, 1, 0, 0, 1, 1],
                         [w1, w2, w3], fs=fs)

        return taps, fs
