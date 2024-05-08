import torch

from emsa.sensitivity.sensitivity_model_base import SensitivityModelBase
from emsa.sensitivity.target_calc.sol_based.target_calc_base import TargetCalcBase


class FinalSizeCalculator(TargetCalcBase):
    def __init__(self, model: SensitivityModelBase):
        super().__init__(model)

    def metric(self, sol, comp: str):
        return sol[:, -1, self.model.idx(f"{comp}_0")].sum(axis=1)

    def stopping_condition(self, **kwargs):
        last_val = kwargs["solutions"][:, -1, :]  # solutions.shape = (len(indices), t_limit, n_comp)
        inf_sum = torch.zeros(last_val.shape[0], device=self.model.device)
        for state, data in self.model.state_data.items():
            if data.get("type") in ["infected"]:
                inf_sum += self.model.aggregate_by_age(solution=last_val, comp=state)
        finished = inf_sum < 1
        return finished, last_val
