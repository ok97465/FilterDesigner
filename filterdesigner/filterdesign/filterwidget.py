# -*- coding: utf-8 -*-
#
# Licensed under the terms of the MIT License

"""."""

# Standard library imports
import warnings
import sip

# Third party imports
from numpy import ndarray, zeros
from matplotlib.pyplot import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from qtpy.QtCore import Slot
from qtpy.QtWidgets import (QVBoxLayout, QHBoxLayout, QWidget, QGroupBox,
                            QLabel, QRadioButton, QPushButton, QComboBox,
                            QButtonGroup, QMessageBox)

# Local import
from filterdesigner.filterbase import (TYPE_LPF, TYPE_HPF, TYPE_BPF, TYPE_BSF,
                                       METHOD_IIR, METHOD_FIR)
from filterdesigner.filterdesign.fir import EquiRipple, LeastSquare
from filterdesigner.helper.signal import magnitude_of_frequency_response


class FilterDesignWidget(QWidget):
    """UI for FilterDesign Window."""

    def __init__(self, parent=None):
        super(FilterDesignWidget, self).__init__(parent)

        self.fir_list = [EquiRipple(self), LeastSquare(self)]
        self.iir_list = []

        # filter result
        self.taps: ndarray = zeros(1)
        self.fs: float = 0

        # Figure
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.init_plot()

        # Units
        unit_layout = QHBoxLayout()
        unit_layout.addWidget(QLabel("Units", self))
        self.freq_unit_combo = QComboBox(self)
        self.freq_unit_combo.addItems(['Hz', 'Khz', 'Mhz', 'Ghz'])
        unit_layout.addWidget(self.freq_unit_combo)

        # Radio Button for Filter Type
        self.type_radio_group = QButtonGroup(self)
        self.type_radio_group.buttonClicked.connect(self.select_filter_type)
        self.radio_lpf = QRadioButton("LowPass", self)
        self.radio_hpf = QRadioButton("HighPass", self)
        self.radio_bpf = QRadioButton("BandPass", self)
        self.radio_bsf = QRadioButton("BandStop", self)
        self.type_radio_group.addButton(self.radio_lpf, TYPE_LPF)
        self.type_radio_group.addButton(self.radio_hpf, TYPE_HPF)
        self.type_radio_group.addButton(self.radio_bpf, TYPE_BPF)
        self.type_radio_group.addButton(self.radio_bsf, TYPE_BSF)

        # Radio Button and combo for Design Method
        self.method_radio_group = QButtonGroup(self)
        self.radio_iir = QRadioButton("IIR", self)
        self.radio_fir = QRadioButton("FIR", self)
        self.method_radio_group.addButton(self.radio_iir, METHOD_IIR)
        self.method_radio_group.addButton(self.radio_fir, METHOD_FIR)
        self.combo_iir = QComboBox()
        self.combo_fir = QComboBox()

        self.radio_iir.setDisabled(True)
        self.combo_iir.setVisible(False)

        # Push Button for Filter Design
        self.push_design = QPushButton("Filter Design", self)
        self.push_design.clicked.connect(self.push_filter_design)

        # GroupBox
        self.group_order = QGroupBox(self)
        layout = QVBoxLayout()
        # layout.setContentsMargins(0, 0, 0, 0)
        self.group_order.setLayout(layout)
        self.group_order.setTitle("Filter Order")

        self.group_options = QGroupBox(self)
        layout = QVBoxLayout()
        # layout.setContentsMargins(0, 0, 0, 0)
        self.group_options.setLayout(layout)
        self.group_options.setTitle("Options")

        self.group_fre_spec = QGroupBox(self)
        layout = QVBoxLayout()
        # layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(unit_layout)
        self.group_fre_spec.setLayout(layout)
        self.group_fre_spec.setTitle("Frequency Specification")

        self.group_mag_spec = QGroupBox(self)
        layout = QVBoxLayout()
        # layout.setContentsMargins(0, 0, 0, 0)
        self.group_mag_spec.setLayout(layout)
        self.group_mag_spec.setTitle("Magnitude Specification")

        # Set Layout
        base_layout = QVBoxLayout(self)
        upper_hbox = QHBoxLayout()
        bottom_hbox = QHBoxLayout()

        base_layout.addLayout(upper_hbox)
        base_layout.addLayout(bottom_hbox)
        base_layout.addWidget(self.push_design)

        upper_hbox.addWidget(self.group_description())
        upper_hbox.addWidget(self.group_figure())

        bottom_hbox.addWidget(self.group_bottom())

        self.setLayout(base_layout)

        # Add Filter to Combobox
        for fir in self.fir_list:
            self.combo_fir.addItem(fir.name)

        self.combo_fir.currentIndexChanged.connect(self.change_ui)
        self.change_ui()

    def select_filter_type(self):
        filter_instance = self.get_filter()

        filter_type = self.type_radio_group.checkedId()
        filter_instance.set_ui_options(filter_type)

    def init_plot(self):
        self.ax.clear()
        self.fig.tight_layout()

    def group_description(self):
        """Generate GroupBox for Description."""
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("Structure"))

        group = QGroupBox(self)
        group.setLayout(vbox)
        group.setTitle("Current Filter Information")
        group.setMaximumWidth(400)

        return group

    def group_figure(self):
        """Generate GroupBox for figure."""
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)

        group = QGroupBox(self)
        group.setLayout(vbox)
        group.setTitle("Filter Specifications")

        return group

    def group_bottom(self):
        """Generate GroupBox for Bottom."""
        hbox = QHBoxLayout()

        vbox_type_method = QVBoxLayout()
        vbox_type_method.addWidget(self.group_filter_type())
        vbox_type_method.addWidget(self.group_design_method())

        vbox_order_option = QVBoxLayout()
        vbox_order_option.addWidget(self.group_order)
        vbox_order_option.addWidget(self.group_options)

        hbox.addLayout(vbox_type_method)
        hbox.addLayout(vbox_order_option)
        hbox.addWidget(self.group_fre_spec)
        hbox.addWidget(self.group_mag_spec)

        group = QGroupBox(self)
        group.setLayout(hbox)

        self.group_order.setFixedWidth(190)
        self.group_options.setFixedWidth(190)
        self.group_fre_spec.setFixedWidth(190)
        self.group_mag_spec.setFixedWidth(190)
        group.setFixedSize(800, 300)

        return group

    def group_filter_type(self):
        """Generate GroupBox for filter type."""
        vbox = QVBoxLayout()

        vbox.addWidget(self.radio_lpf)
        vbox.addWidget(self.radio_hpf)
        vbox.addWidget(self.radio_bpf)
        vbox.addWidget(self.radio_bsf)

        self.radio_lpf.setChecked(True)

        group = QGroupBox(self)
        group.setLayout(vbox)
        group.setTitle("Filter Type")

        return group

    def group_design_method(self):
        """Generate GroupBox for design method."""
        vbox = QVBoxLayout()

        hbox_iir = QHBoxLayout()
        hbox_fir = QHBoxLayout()

        hbox_iir.addWidget(self.radio_iir)
        hbox_iir.addWidget(self.combo_iir)

        hbox_fir.addWidget(self.radio_fir)
        hbox_fir.addWidget(self.combo_fir)

        vbox.addLayout(hbox_iir)
        vbox.addLayout(hbox_fir)

        self.radio_fir.setChecked(True)

        group = QGroupBox(self)
        group.setLayout(vbox)
        group.setTitle("Design Method")

        return group

    @Slot()
    def push_filter_design(self):
        """Design filter tap and plot filter."""

        filter_instance = self.get_filter()

        filter_type = self.type_radio_group.checkedId()

        self.ax.clear()
        try:
            self.taps, self.fs = filter_instance.calc_filter(filter_type)
            self.plot_filter()
        except ValueError as e:
            self.taps = zeros(1)
            self.fs = 0
            QMessageBox.warning(self, "Error", str(e))

        self.fig.tight_layout()
        self.fig.canvas.draw()

    def plot_filter(self):
        if (isinstance(self.taps, ndarray) is not True) or \
           (len(self.taps) < 2):
            return

        mag_fre_db, fre = magnitude_of_frequency_response(
            self.taps, self.fs, 1024)

        unit = self.freq_unit_combo.itemText(
            self.freq_unit_combo.currentIndex())
        self.ax.plot(fre, mag_fre_db)
        self.ax.set_ylabel("Magnitude [dB]")
        self.ax.set_xlabel(f"Frequency [{unit}]")
        self.ax.set_xlim([0, self.fs / 2])

    def resizeEvent(self, event):
        """Override resizeEvent of Qt."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            self.fig.tight_layout()
        super(FilterDesignWidget, self).resizeEvent(event)

    def delete_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.delete_layout(item.layout())
            sip.delete(layout)

    def get_filter(self):
        if self.method_radio_group.checkedId() == METHOD_FIR:
            filter_instance = self.fir_list[self.combo_fir.currentIndex()]
        else:
            filter_instance = self.iir_list[self.combo_iir.currentIndex()]

        return filter_instance

    def change_ui(self):
        filter_instance = self.get_filter()

        filter_type = self.type_radio_group.checkedId()

        self.delete_layout(self.group_order.layout().itemAt(0))
        self.delete_layout(self.group_options.layout().itemAt(0))
        self.delete_layout(self.group_fre_spec.layout().itemAt(1))
        self.delete_layout(self.group_mag_spec.layout().itemAt(0))

        self.group_order.layout().addLayout(
            filter_instance.get_ui_order(filter_type))
        self.group_options.layout().addLayout(
            filter_instance.get_ui_options(filter_type))
        self.group_fre_spec.layout().addLayout(
            filter_instance.get_ui_frequency(filter_type))
        self.group_mag_spec.layout().addLayout(
            filter_instance.get_ui_magnitude(filter_type))

        filter_instance.set_ui_options(filter_type)
