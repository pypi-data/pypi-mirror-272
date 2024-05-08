from emsa.sensitivity.sensitivity_model_base import SensitivityModelBase


class VaccinatedModel(SensitivityModelBase):
    def __init__(self, sim_object):
        """
        Initializes the VaccinatedModel class.

        This method initializes the VaccinatedModel class by calling the parent class (EpidemicModelBase)
        constructor, and instantiating the matrix generator used in solving the model.

        Args:
            sim_object (SimulationVaccinated): Simulation object

        """
        super().__init__(sim_object=sim_object)

    def get_solution(self, y0, t_eval, **kwargs):
        lhs_table = kwargs["lhs_table"]
        self.V_1 = self._get_V_1_from_lhs(lhs_table=lhs_table)
        odefun = self.get_vaccinated_ode(curr_batch_size=lhs_table.shape[0])
        return self.get_sol_from_ode(y0, t_eval, odefun)

    def _get_V_1_from_lhs(self, lhs_table):
        daily_vacc = (lhs_table * self.ps['total_vaccines'] / self.ps["T"]).to(self.device)
        lhs_dict = {"daily_vac": daily_vacc}
        return self.get_matrix_from_lhs(lhs_dict=lhs_dict, matrix_name="V_1")
