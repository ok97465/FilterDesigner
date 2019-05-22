# -*- coding: utf-8 -*-
#
# Licensed under the terms of the MIT License

"""."""

# Standard library imports
from abc import ABCMeta, abstractmethod

TYPE_LPF = 0
TYPE_HPF = 1
TYPE_BPF = 2
TYPE_BSF = 3
METHOD_IIR = 0
METHOD_FIR = 0


class FilterBase(metaclass=ABCMeta):

    @abstractmethod
    def get_ui_order(self, filter_type):
        pass

    @abstractmethod
    def get_ui_options(self, filter_type):
        pass

    @abstractmethod
    def get_ui_frequency(self, filter_type):
        pass

    @abstractmethod
    def get_ui_magnitude(self, filter_type):
        pass

    @abstractmethod
    def calc_filter(self, filter_type):
        pass

    @staticmethod
    def set_size_policy_when_hidden(widget, is_retain):
        policy = widget.sizePolicy()
        policy.setRetainSizeWhenHidden(is_retain)
        widget.setSizePolicy(policy)
