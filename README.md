Experiment is a Python module inspired by GitHub's [dat-science](https://github.com/github/dat-science).

It uses a Python's [futures](https://pypi.python.org/pypi/futures).

# Overview

Experiment takes two Futures and executes both using a ThreadPoolExecutor. The
`Experiment` object itself is a future that will be completed when the control
finishes. The `result` of this Future is the output of the control Future! This
way you get your results as quickly as the control finishes.

You can also call `get_future` on the `Experiment` to get a Future that covers
the completion of the the control *and* the experiment!

# Usage

```python
from experiment import Experiment

def old_func():
  # Do things the old way

def new_func():
  # Do things the new way

# Conduct an experiment where control is your old
# code path and experiment is the new!
exp = Experiment(
    control = old_func,
    experiment = new_func
)

# The returned experiment is a Future. You can get the result,
# which will be the result of the control!

# Send this back!
control = exp.result()

# You can also get a future that covers *both* the control and
# the experiment to verify that they match.

total_result = exp.get_future().result()
if(total_result.matches()):
  print "Yay!"
else:
  # Here's the control's result (it's a Future!)
  print total_result.get_control_result().result()
  # And the experiment, also a Future!
  print total_result.get_experiment_result().result()
```
