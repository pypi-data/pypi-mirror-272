import numpy as np
import torch

from emsa.sensitivity.target_calc.sol_based.final_size_calc import FinalSizeCalculator
from emsa.sensitivity.target_calc.sol_based.peak_calc import PeakCalculator
from emsa.sensitivity.target_calc.r0calculator import R0Calculator


class OutputGenerator:
    def __init__(self, sim_object, variable_params):
        self.batch_size = sim_object.batch_size
        self.sim_object = sim_object
        self.variable_params = variable_params

    def get_output(self, lhs_table: np.ndarray) -> dict:
        lhs = torch.from_numpy(lhs_table).float().to(self.sim_object.device)
        results = {}
        for target in self.sim_object.target_vars:
            if target == "r0":
                r0calc = R0Calculator(self.sim_object)
                results[target] = r0calc.get_output(lhs_table=lhs)
            else:
                results[target] = self.calculate_target(lhs_table=lhs, target_var=target)
        return results

    def calculate_target(self, lhs_table: torch.Tensor, target_var: str) -> torch.Tensor:
        if target_var.split('_')[1] == "sup":
            target_calculator = FinalSizeCalculator(model=self.sim_object.model)
        else:
            target_calculator = PeakCalculator(model=self.sim_object.model)
        return target_calculator.get_output(lhs_table=lhs_table,
                                            batch_size=self.batch_size,
                                            target_var=target_var)
