from .one_asset_fd_generator import interpolate
from ..api_and_utils import np, deepcopy, sp, ParamsBase, OptionType


class OneAssetFDParisianSnowball(ParamsBase):

    def __init__(self, param, Ns=None):
        super().__init__(param)

        self.Smin = 0 * min(self.param.spot_price, self.param.entrance_price)
        self.Smax = 3 * max(self.param.spot_price, self.param.entrance_price)

        self._T0 = round(self.param.current_date, 4)
        self._TT = round(self.param.expiry_date, 4)
        self._Ns = pow(10, 3) if Ns is None else int(Ns)
        self._Nt = int(round(self._TT - int(self._T0), 4))

        self._Tau = round(self._T0 - int(self._T0), 4)
        self._T_KO = np.array([round(obs.obs_index - int(self._T0), 4) for obs in self.param.knock_out_obs_date])
        self._T_KI = np.array([round(obs.obs_index - int(self._T0), 4) for obs in self.param.knock_in_obs_date])
        self._Rbt_KO = np.array([obs.coupon_rate for obs in self.param.knock_out_obs_date])

        self.__grid = 'KIgrid2nd' if self.param.is_knock_in or self.param.knock_in_times >= 2 else 'KIgrid1st' if self.param.knock_in_times == 1 else 'NKIgrid'
        self.__round = 8

        self.__present_value_solved = False
        self.__greeks_solved = False

    def _set_direction_(self):
        self._is_call = {OptionType.STANDARD: True, OptionType.REVERSE: False}[self.param.option_type]
        self._omega = 1 if self._is_call else -1

    def _set_spot_vector_(self):
        self.ds = (self.Smax - self.Smin) / max(1, self._Ns)
        self.Svec = np.linspace(self.Smin, self.Smax, self._Ns + 1)

    def _set_term_vector_(self):
        self.dt = round(self._TT - int(self._T0), 4) / max(1, self._Nt)
        self.Tvec = np.linspace(0, round(self._TT - int(self._T0), 4), self._Nt + 1)
        self.Tauvec = self.Tvec.copy()
        self.Tauvec[1:] = self.Tauvec[1:] - self._Tau

    def _set_value_grid_(self):
        self.KIgrid1st = np.zeros(shape=(self._Ns + 1, self._Nt + 1))
        self.KIgrid2nd = np.zeros(shape=(self._Ns + 1, self._Nt + 1))
        self.NKIgrid = np.zeros(shape=(self._Ns + 1, self._Nt + 1))

        self.T1KIgrid1st = None
        self.T1KIgrid2nd = None
        self.T1NKIgrid = None

    def _set_other_vector_(self):
        pass

    def _set_initial_vector_grid_(self):
        self._set_direction_()
        self._set_spot_vector_()
        self._set_term_vector_()
        self._set_value_grid_()
        self._set_other_vector_()

    def _set_terminal_condition_(self):
        pass

    def _set_boundary_condition_(self):
        pass

    def _set_coefficient_(self):
        drift = (self.param.riskfree_rate - self.param.dividend) * self.Svec[1: -1] / self.ds
        diffusion_square = (self.param.volatility * self.Svec[1: -1] / self.ds) ** 2

        self._l = 0.5 * (diffusion_square - drift)
        self._c = -diffusion_square - self.param.riskfree_rate
        self._u = 0.5 * (diffusion_square + drift)

    def _set_matrix_(self):
        self._A = sp.diags([self._l[1:], self._c, self._u[:-1]], [-1, 0, 1], format='csc')
        self._M1 = sp.eye(self._Ns - 1)
        self._M2 = self._M1 - self.dt / self.param.year_base * self._A

    def _solve_(self):
        pass

    def _set_grid_delta_(self, grid: str):
        grid = getattr(self, grid)
        grid_delta = np.zeros(shape=(grid.shape[0], grid.shape[1]))
        grid_delta[1: -1] = (grid[2:] - grid[:-2]) / (2 * self.ds)
        grid_delta[0] = (grid[1] - grid[0]) / self.ds
        grid_delta[-1] = (grid[-1] - grid[-2]) / self.ds
        grid_delta[:, -1] = 0
        return grid_delta

    def _set_grid_gamma_(self, grid: str):
        grid = getattr(self, grid)
        grid_gamma = np.zeros(shape=(grid.shape[0], grid.shape[1]))
        grid_gamma[1: -1] = (grid[2:] - grid[:-2]) / (2 * self.ds)
        grid_gamma[0] = (grid[1] - grid[0]) / self.ds
        grid_gamma[-1] = (grid[-1] - grid[-2]) / self.ds
        return grid_gamma

    def _set_grid_theta_(self, grid: str):
        T0grid = getattr(self, grid)
        T1grid = getattr(self, f'T1{grid}')
        return T1grid - T0grid[:, :max(1, self._Nt)]

    def _set_grid_vega_(self, grid: str, dv: float = 0.01):
        pricer_up = deepcopy(self)
        pricer_up.param.volatility = self.param.volatility + dv
        pricer_up.price()
        return getattr(pricer_up, grid) - getattr(self, grid)

    def _set_grid_phi_(self, grid: str, dq: float = 0.001):
        pricer_up = deepcopy(self)
        pricer_up.param.dividend = self.param.dividend + dq
        pricer_up.price()
        return getattr(pricer_up, grid) - getattr(self, grid)

    def _set_grid_rho_(self, grid: str, dr: float = 0.0001):
        pricer_up = deepcopy(self)
        pricer_up.param.riskfree_rate = self.param.riskfree_rate + dr
        pricer_up.price()
        return getattr(pricer_up, grid) - getattr(self, grid)

    def _set_grid_ddeltadt_(self, grid: str):
        T0grid = getattr(self, grid)
        T1grid = getattr(self, f'T1{grid}')
        return T1grid - T0grid[:, :max(1, self._Nt)]

    def _set_grid_greeks_(self, grid, include_vega, include_phi, include_rho):
        setattr(self, f'{grid}_delta', self._set_grid_delta_(grid))
        setattr(self, f'T1{grid}_delta', self._set_grid_delta_(f'T1{grid}'))
        setattr(self, f'{grid}_gamma', self._set_grid_gamma_(f'{grid}_delta'))
        setattr(self, f'{grid}_theta', self._set_grid_theta_(grid))
        setattr(self, f'{grid}_ddeltadt', self._set_grid_ddeltadt_(f'{grid}_delta'))

        if include_vega:
            setattr(self, f'{grid}_vega', self._set_grid_vega_(grid))
        if include_phi:
            setattr(self, f'{grid}_phi', self._set_grid_phi_(grid))
        if include_rho:
            setattr(self, f'{grid}_rho', self._set_grid_rho_(grid))

    def _check_present_value_solved_(self):
        if not self.__present_value_solved:
            self.price()

    def _check_greeks_solved_(self):
        self._check_present_value_solved_()
        if not self.__greeks_solved:
            self.greeks()

    def price(self):
        self._set_initial_vector_grid_()
        self._set_terminal_condition_()
        self._set_boundary_condition_()
        self._set_coefficient_()
        self._set_matrix_()
        self._solve_()
        self.__present_value_solved = True

    def greeks(self, include_vega=True, include_phi=False, include_rho=False):
        self._check_present_value_solved_()
        self._set_grid_greeks_(grid=self.__grid, include_vega=include_vega, include_phi=include_phi, include_rho=include_rho)
        self.__greeks_solved = True

    def present_value(self, S=None):
        self._check_present_value_solved_()
        S = self.param.spot_price if S is None else S
        grid = getattr(self, self.__grid)
        return interpolate(x=self.Svec, y=grid[:, 0])(S).round(self.__round)

    def delta(self, S=None):
        self._check_greeks_solved_()
        S = self.param.spot_price if S is None else S
        grid = getattr(self, f'{self.__grid}_delta')
        return interpolate(x=self.Svec, y=grid[:, 0])(S).round(self.__round)

    def gamma(self, S=None):
        self._check_greeks_solved_()
        S = self.param.spot_price if S is None else S
        grid = getattr(self, f'{self.__grid}_gamma')
        return interpolate(x=self.Svec, y=grid[:, 0])(S).round(self.__round)

    def theta(self, S=None):
        self._check_greeks_solved_()
        S = self.param.spot_price if S is None else S
        grid = getattr(self, f'{self.__grid}_theta')
        return interpolate(x=self.Svec, y=grid[:, 0])(S).round(self.__round)

    def vega(self, S=None):
        self._check_greeks_solved_()
        S = self.param.spot_price if S is None else S
        grid = getattr(self, f'{self.__grid}_vega')
        return interpolate(x=self.Svec, y=grid[:, 0])(S).round(self.__round)

    def phi(self, S=None):
        self._check_greeks_solved_()
        S = self.param.spot_price if S is None else S
        grid = getattr(self, f'{self.__grid}_phi')
        return interpolate(x=self.Svec, y=grid[:, 0])(S).round(self.__round)

    def rho(self, S=None):
        self._check_greeks_solved_()
        S = self.param.spot_price if S is None else S
        grid = getattr(self, f'{self.__grid}_rho')
        return interpolate(x=self.Svec, y=grid[:, 0])(S).round(self.__round)

    def ddeltadt(self, S=None):
        self._check_greeks_solved_()
        S = self.param.spot_price if S is None else S
        grid = getattr(self, f'{self.__grid}_ddeltadt')
        return interpolate(x=self.Svec, y=grid[:, 0])(S).round(self.__round)
