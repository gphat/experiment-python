import time
from concurrent.futures import Future, ThreadPoolExecutor

class ExperimentResult(object):
    def __init__(self, control_result, control_completion, experiment_result, experiment_completion):
        self.control_result = control_result
        self.control_completion = control_completion
        self.experiment_result = experiment_result
        self.experiment_completion = experiment_completion

    def get_control_result(self):
        return self.control_result

    def get_experiment_result(self):
        return self.experiment_result

    def matches(self):
        if(self.experiment_result.exception() != None and self.control_result.exception() != None):
            # Compare the exceptions
            # http://stackoverflow.com/questions/15844131/comparing-exception-objects-in-python
            exp_ex = self.experiment_result.exception()
            con_ex = self.control_result.exception()
            if type(exp_ex) is type(con_ex) and exp_ex.args == con_ex.args:
                return True
            else:
                return False

        elif(self.experiment_result.exception() != None and self.control_result.exception() == None):
            # Only the experiment threw an exception
            return False
        elif(self.experiment_result.exception() == None and self.control_result.exception() != None):
            # Only the control threw an exception
            return False
        elif(self.experiment_result.result() != self.control_result.result()):
            # Results do not match!
            return False
        else:
            return True

class Experiment(Future):
    """
    Initialize an Experiment object.
    """

    def __init__(self, control, experiment):
        super(Experiment, self).__init__()
        self.control_result = None
        self.control_seen = None

        self.experiment_result = None
        self.experiment_seen = None

        self.total_future = Future()

        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(control).add_done_callback(self.store_control)
            executor.submit(experiment).add_done_callback(self.store_experiment)

    def store_control(self, future):
        self.control_seen = time.time()
        self.control_result = future
        # When the control is completed, we'll complete "this" future.
        self.set_result(future.result())
        self.check_results()

    def store_experiment(self, future):
        self.experiment_seen = time.time()
        self.experiment_result = future
        self.check_results()

    def get_future(self):
        return self.total_future

    def check_results(self):
        # XXX How do we ensure no race condition here?
        if self.experiment_seen != None and self.control_seen != None:
            # Always return the control's result as the result
            # of our future.
            self.total_future.set_result(ExperimentResult(
                self.control_result,
                self.control_seen,
                self.experiment_result,
                self.experiment_seen
            ))
        else:
            # Nothing to do, as we're not done with everything yet
            pass
