import logging

import numpy as np

from kozmo_core.user_model import KozmoComponent, client_class_names


class UserObjectClassAttr(KozmoComponent):
    def __init__(self, metrics_ok=True, ret_nparray=False, ret_meta=False):
        self.class_names = ["a", "b"]


class UserObjectClassMethod(KozmoComponent):
    def class_names(self):
        return ["x", "y"]


def test_class_names_attr(caplog):
    caplog.set_level(logging.INFO)
    user_object = UserObjectClassAttr()
    predictions = np.array([[1, 2], [3, 4]])
    names = client_class_names(user_object, predictions)
    assert names == ["a", "b"]
    assert (
        "class_names attribute is deprecated. Please define a class_names method"
        in caplog.text
    )


def test_class_names_method(caplog):
    caplog.set_level(logging.INFO)
    user_object = UserObjectClassMethod()
    predictions = np.array([[1, 2], [3, 4]])
    names = client_class_names(user_object, predictions)
    assert names == ["x", "y"]
    assert (
        not "class_names attribute is deprecated. Please define a class_names method"
        in caplog.text
    )


def test_no_class_names_on_kozmo_component(caplog):
    caplog.set_level(logging.INFO)
    user_object = KozmoComponent()
    predictions = np.array([[1, 2], [3, 4]])
    names = client_class_names(user_object, predictions)
    assert names == ["t:0", "t:1"]


def test_no_class_names(caplog):
    caplog.set_level(logging.INFO)

    class X:
        pass

    user_object = X()
    predictions = np.array([[1, 2], [3, 4]])
    names = client_class_names(user_object, predictions)
