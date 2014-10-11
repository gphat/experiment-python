from nose import tools as t
from experiment import Experiment
import time

def slow_ok():
    time.sleep(3)
    return "OK"

def fast_ok():
    time.sleep(1)
    return "OK"

class TestExperiment(object):

    def test_matching_experiment(self):
        result = Experiment(control=slow_ok, experiment=fast_ok).result()
        # exp = yield result
        t.assert_true(result.did_match())
