from ..types import WonderSchedulerType


class WonderSchedulerConfig:

    def __init__(
        self,
        scheduler_type:  WonderSchedulerType | str = WonderSchedulerType.DPM_SOLVER_MULTISTEP,
        **kwargs
    ):
        self.scheduler_type = scheduler_type if type(
            scheduler_type) == WonderSchedulerType else WonderSchedulerType(scheduler_type)

        self.kwargs = kwargs
