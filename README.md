Experiment is a Python module inspired by GitHub's [dat-science](https://github.com/github/dat-science).

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
# which is an ExperimentResult

# Send this back!
control = exp.result.control_result

# Verify they match
if(exp.result.matches):
  print "Yay!"
```