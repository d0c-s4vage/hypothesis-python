from hypothesis.utils.dynamicvariables import DynamicVariable
from hypothesis.internal.conjecture.data import Status
from hypothesis.internal.conjecture.engine import ExitReason
import math


collector = DynamicVariable(None)


class Statistics(object):
    def __init__(self, engine):
        self.passing_examples = len(
            engine.status_runtimes.get(Status.VALID, ()))
        self.invalid_examples = len(
            engine.status_runtimes.get(Status.INVALID, []) + 
            engine.status_runtimes.get(Status.OVERRUN, [])
        )
        self.failing_examples = len(engine.status_runtimes.get(
            Status.INTERESTING, ()))

        runtimes = sorted(
            engine.status_runtimes.get(Status.VALID, []) +
            engine.status_runtimes.get(Status.INVALID, []) +
            engine.status_runtimes.get(Status.INTERESTING, [])
        )

        n = max(0, len(runtimes) - 1)
        lower = int(runtimes[int(math.floor(n * 0.05))] * 1000)
        upper = int(runtimes[int(math.ceil(n * 0.95))] * 1000)
        if upper == 0:
            self.runtimes = "< 1ms"
        elif lower == upper:
            self.runtimes = "~ %dms" % (lower,)
        else:
            self.runtimes = "%d-%d ms" % (lower, upper)

        if engine.exit_reason != ExitReason.finished:
            self.exit_reason = (
                'settings.%s=%r' % (
                    engine.exit_reason.name,
                    getattr(engine.settings, engine.exit_reason.name)
                )
            )
        else:
            self.exit_reason = "nothing left to do"



def note_engine_for_statistics(engine):
    callback = collector.value
    if callback is not None:
        callback(Statistics(engine))
