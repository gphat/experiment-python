from nose import tools as t
from experiment import Experiment
import time

def slow_ok():
    time.sleep(3)
    return "OK"

def medium_ok():
    time.sleep(2)
    return "medium OK"

def fast_ok():
    time.sleep(1)
    return "OK"

class TestExperiment(object):

    def test_simple_experiment(self):
        result = Experiment(control=medium_ok, experiment=fast_ok).result()
        t.assert_true(result == "medium OK")

    def test_matching_experiment(self):
        result = Experiment(control=slow_ok, experiment=fast_ok).get_future().result()
        t.assert_true(result.matches())

        t.assert_true(result.get_control_result().result() == "OK")
        t.assert_true(result.get_experiment_result().result() == "OK")
