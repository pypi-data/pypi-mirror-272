from ..api_and_utils import np, deepcopy, sp, ParamsBase, OptionType, RegularGridInterpolator


class TwoAssetFDSnowball(ParamsBase):

    def __init__(self, param, Ns=None):
        super().__init__(param)

        self.Smin1 = 0 * min(self.param.spot_price1, self.param.entrance_price1)
        self.Smax1 = 3 * max(self.param.spot_price1, self.param.entrance_price1)
        self.Smin2 = 0 * min(self.param.spot_price2, self.param.entrance_price2)
        self.Smax2 = 3 * max(self.param.spot_price2, self.param.entrance_price2)

        self._T0 = round(self.param.current_date, 4)
        self._TT = round(self.param.expiry_date, 4)
        self._Ns1 = 200 if Ns is None else int(Ns)
        self._Ns2 = 200 if Ns is None else int(Ns)
        self._Nt = int(round(self._TT - int(self._T0), 4))

        self._Tau = round(self._T0 - int(self._T0), 4)
        self._T_KO = np.array([round(obs.obs_index - int(self._T0), 4) for obs in self.param.knock_out_obs_date])
        self._T_KI = np.array([round(obs.obs_index - int(self._T0), 4) for obs in self.param.knock_in_obs_date])
        self._Rbt_KO = np.array([obs.coupon_rate for obs in self.param.knock_out_obs_date])

        self.__grid = 'KIgrid' if self.param.is_knock_in else 'NKIgrid'
        self.__round = 8

        self.__present_value_solved = False
        self.__greeks_solved = False

    def _set_direction_(self):
        self._is_call = {OptionType.STANDARD: True, OptionType.REVERSE: False}[self.param.option_type]
        self._omega = 1 if self._is_call else -1

    def _set_spot_vector_(self):
        self.ds1 = (self.Smax1 - self.Smin1) / max(1, self._Ns1)
        self.ds2 = (self.Smax2 - self.Smin2) / max(1, self._Ns2)
        self.S1vec = np.linspace(self.Smin1, self.Smax1, self._Ns1 + 1)
        self.S2vec = np.linspace(self.Smin2, self.Smax2, self._Ns2 + 1)

    def _set_term_vector_(self):
        self.dt = round(self._TT - int(self._T0), 4) / max(1, self._Nt)
        self.Tvec = np.linspace(0, round(self._TT - int(self._T0), 4), self._Nt + 1)

    def _set_value_grid_(self):
        self.KIgrid = np.zeros(shape=(self._Ns2 + 1, self._Ns1 + 1))
        self.NKIgrid = np.zeros(shape=(self._Ns2 + 1, self._Ns1 + 1))
        self.T1KIgrid = None
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
        N = (self._Ns1 - 1) * (self._Ns2 - 1)
        j1mat, j2mat = np.meshgrid(self.S1vec / self.ds1, self.S2vec / self.ds2)

        A = 0.25 * self.param.correlation * self.param.volatility1 * self.param.volatility2 * (j1mat * j2mat)
        B = 0.5 * self.param.volatility1 ** 2 * j1mat ** 2
        C = 0.5 * (self.param.riskfree_rate - self.param.dividend1) * j1mat
        D = 0.5 * self.param.volatility2 ** 2 * j2mat ** 2
        E = 0.5 * (self.param.riskfree_rate - self.param.dividend2) * j2mat

        self._LL = A
        self._LC = B - C
        self._LU = -A
        self._CL = D - E
        self._CC = -2 * B - 2 * D - self.param.riskfree_rate
        self._CU = D + E
        self._UL = -A
        self._UC = B + C
        self._UU = A

        a = np.reshape(A[1:-1, 1:-1], (N,), order='F')
        b = np.reshape(B[1:-1, 1:-1], (N,), order='F')
        c = np.reshape(C[1:-1, 1:-1], (N,), order='F')
        d = np.reshape(D[1:-1, 1:-1], (N,), order='F')
        e = np.reshape(E[1:-1, 1:-1], (N,), order='F')

        self._ll = a
        self._lc = b - c
        self._lu = -a
        self._cl = d - e
        self._cc = -2 * b - 2 * d - self.param.riskfree_rate
        self._cu = d + e
        self._ul = -a
        self._uc = b + c
        self._uu = a

    def _set_matrix_(self):
        m1, m2 = self._Ns1 - 1, self._Ns2 - 1
        self._A = sp.diags([self._ll[m2 + 1:], self._lc[m2:], self._lu[m2 - 1:],
                            self._cl[1:], self._cc, self._cu[:-1],
                            self._ul[:-m2 + 1], self._uc[:-m2], self._uu[:-m2 - 1]],
                           [-m2 - 1, -m2, -m2 + 1, -1, 0, 1, m2 - 1, m2, m2 + 1], format='lil')

        mij = np.arange(m1)
        i, j = np.meshgrid(mij, mij)
        self._A[i * m2, (j + 1) * m2 - 1] = 0
        self._A[(i + 1) * m2 - 1, j * m2] = 0

        self._M = sp.eye(m1 * m2) - self.dt / self.param.year_base * self._A

    def _update_boundary_(self, grid):
        y = np.zeros((self._Ns2 + 1, self._Ns1 + 1))
        m1, m2 = self._Ns1 - 1, self._Ns2 - 1

        for c in np.arange(1, m1 + 1):
            for r in np.arange(1, m2 + 1):
                if c == 1:
                    y[r, c] = self._LL[r, c] * grid[r - 1, c - 1] + self._LC[r, c] * grid[r, c - 1] + self._LU[r, c] * grid[r + 1, c - 1]

                    if r == 1:
                        y[r, c] = y[r, c] + self._CL[r, c] * grid[r - 1, c] + self._UL[r, c] * grid[r - 1, c + 1]
                    elif r == m2:
                        y[r, c] = y[r, c] + self._CU[r, c] * grid[r + 1, c] + self._UU[r, c] * grid[r + 1, c + 1]

                elif c == m1:
                    y[r, c] = self._UL[r, c] * grid[r - 1, c + 1] + self._UC[r, c] * grid[r, c + 1] + self._UU[r, c] * grid[r + 1, c + 1]

                    if r == 1:
                        y[r, c] = y[r, c] + self._LL[r, c] * grid[r - 1, c - 1] + self._CL[r, c] * grid[r - 1, c]
                    elif r == m2:
                        y[r, c] = y[r, c] + self._LU[r, c] * grid[r + 1, c - 1] + self._CU[r, c] * grid[r + 1, c]
                else:
                    if r == 1:
                        y[r, c] = self._LL[r, c] * grid[r - 1, c - 1] + self._CL[r, c] * grid[r - 1, c] + self._UL[r, c] * grid[r - 1, c + 1]
                    elif r == m2:
                        y[r, c] = self._LU[r, c] * grid[r + 1, c - 1] + self._CU[r, c] * grid[r + 1, c] + self._UU[r, c] * grid[r + 1, c + 1]

        return np.reshape(y[1:-1, 1:-1], (m1 * m2, 1), order='F')

    def _solve_intraday_(self, idx, KIcube, NKIcube):
        return KIcube, NKIcube

    def _solve_(self):
        pass

    def _set_grid_delta1_(self, grid: str):
        grid = getattr(self, grid)
        grid_delta = np.zeros(shape=(grid.shape[0], grid.shape[1]))
        grid_delta[:, 1: -1] = (grid[:, 2:] - grid[:, :-2]) / (2 * self.ds1)
        grid_delta[:, 0] = (grid[:, 1] - grid[:, 0]) / self.ds1
        grid_delta[:, -1] = (grid[:, -1] - grid[:, -2]) / self.ds1
        return grid_delta

    def _set_grid_delta2_(self, grid: str):
        grid = getattr(self, grid)
        grid_delta = np.zeros(shape=(grid.shape[0], grid.shape[1]))
        grid_delta[1: -1, :] = (grid[2:, :] - grid[:-2, :]) / (2 * self.ds2)
        grid_delta[0, :] = (grid[1, :] - grid[0, :]) / self.ds2
        grid_delta[-1, :] = (grid[-1, :] - grid[-2, :]) / self.ds2
        return grid_delta

    def _set_grid_gamma1_(self, grid: str):
        grid = getattr(self, grid)
        grid_gamma = np.zeros(shape=(grid.shape[0], grid.shape[1]))
        grid_gamma[:, 1: -1] = (grid[:, 2:] - grid[:, :-2]) / (2 * self.ds1)
        grid_gamma[:, 0] = (grid[:, 1] - grid[:, 0]) / self.ds1
        grid_gamma[:, -1] = (grid[:, -1] - grid[:, -2]) / self.ds1
        return grid_gamma

    def _set_grid_gamma2_(self, grid: str):
        grid = getattr(self, grid)
        grid_gamma = np.zeros(shape=(grid.shape[0], grid.shape[1]))
        grid_gamma[1: -1, :] = (grid[2:, :] - grid[:-2, :]) / (2 * self.ds2)
        grid_gamma[0, :] = (grid[1, :] - grid[0, :]) / self.ds2
        grid_gamma[-1, :] = (grid[-1, :] - grid[-2, :]) / self.ds2
        return grid_gamma

    def _set_grid_theta_(self, grid: str):
        T0grid = getattr(self, grid)
        T1grid = getattr(self, f'T1{grid}')
        return T1grid - T0grid

    def _set_grid_vega1_(self, grid: str, dv: float = 0.01):
        pricer_up = deepcopy(self)
        pricer_up.param.volatility1 = self.param.volatility1 + dv
        pricer_up.price()
        return getattr(pricer_up, grid) - getattr(self, grid)

    def _set_grid_vega2_(self, grid: str, dv: float = 0.01):
        pricer_up = deepcopy(self)
        pricer_up.param.volatility2 = self.param.volatility2 + dv
        pricer_up.price()
        return getattr(pricer_up, grid) - getattr(self, grid)

    def _set_grid_rho_(self, grid: str, dr: float = 0.0001):
        pricer_up = deepcopy(self)
        pricer_up.param.riskfree_rate = self.param.riskfree_rate + dr
        pricer_up.price()
        return getattr(pricer_up, grid) - getattr(self, grid)

    def _set_grid_dpvdcorr_(self, grid: str, dcorr: float = 0.01):
        pricer_up = deepcopy(self)
        pricer_up.param.correlation = self.param.correlation + dcorr
        pricer_up.price()
        return getattr(pricer_up, grid) - getattr(self, grid)

    def _set_grid_greeks_(self, grid, include_vega, include_rho, include_dpvdcorr):
        setattr(self, f'{grid}_delta1', self._set_grid_delta1_(grid))
        setattr(self, f'{grid}_delta2', self._set_grid_delta2_(grid))
        setattr(self, f'T1{grid}_delta1', self._set_grid_delta1_(f'T1{grid}'))
        setattr(self, f'T1{grid}_delta2', self._set_grid_delta2_(f'T1{grid}'))
        setattr(self, f'{grid}_gamma1', self._set_grid_gamma1_(f'{grid}_delta1'))
        setattr(self, f'{grid}_gamma2', self._set_grid_gamma2_(f'{grid}_delta2'))
        setattr(self, f'{grid}_theta', self._set_grid_theta_(grid))

        if include_vega:
            setattr(self, f'{grid}_vega1', self._set_grid_vega1_(grid))
            setattr(self, f'{grid}_vega2', self._set_grid_vega2_(grid))
        if include_rho:
            setattr(self, f'{grid}_rho', self._set_grid_rho_(grid))
        if include_dpvdcorr:
            setattr(self, f'{grid}_dpvdcorr', self._set_grid_dpvdcorr_(grid))

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

    def greeks(self, include_vega=True, include_rho=False, include_dpvdcorr=False):
        self._check_present_value_solved_()
        self._set_grid_greeks_(grid=self.__grid, include_vega=include_vega, include_rho=include_rho, include_dpvdcorr=include_dpvdcorr)
        self.__greeks_solved = True

    def present_value(self, S1=None, S2=None):
        self._check_present_value_solved_()
        S1 = self.param.spot_price1 if S1 is None else S1
        S2 = self.param.spot_price2 if S2 is None else S2
        grid = getattr(self, self.__grid)
        interp_array = np.array([S2, S1]).T
        return RegularGridInterpolator((self.S2vec, self.S1vec), grid,  method="linear")(interp_array).round(self.__round)

    def delta(self, leg, S1=None, S2=None):
        self._check_greeks_solved_()
        S1 = self.param.spot_price1 if S1 is None else S1
        S2 = self.param.spot_price2 if S2 is None else S2
        grid = getattr(self, f'{self.__grid}_delta{leg}')
        interp_array = np.array([S2, S1]).T
        return RegularGridInterpolator((self.S2vec, self.S1vec), grid,  method="linear")(interp_array).round(self.__round)

    def gamma(self, leg, S1=None, S2=None):
        self._check_greeks_solved_()
        S1 = self.param.spot_price1 if S1 is None else S1
        S2 = self.param.spot_price2 if S2 is None else S2
        grid = getattr(self, f'{self.__grid}_gamma{leg}')
        interp_array = np.array([S2, S1]).T
        return RegularGridInterpolator((self.S2vec, self.S1vec), grid,  method="linear")(interp_array).round(self.__round)

    def theta(self, S1=None, S2=None):
        self._check_greeks_solved_()
        S1 = self.param.spot_price1 if S1 is None else S1
        S2 = self.param.spot_price2 if S2 is None else S2
        grid = getattr(self, f'{self.__grid}_theta')
        interp_array = np.array([S2, S1]).T
        return RegularGridInterpolator((self.S2vec, self.S1vec), grid,  method="linear")(interp_array).round(self.__round)

    def vega(self, leg, S1=None, S2=None):
        self._check_greeks_solved_()
        S1 = self.param.spot_price1 if S1 is None else S1
        S2 = self.param.spot_price2 if S2 is None else S2
        grid = getattr(self, f'{self.__grid}_vega{leg}')
        interp_array = np.array([S2, S1]).T
        return RegularGridInterpolator((self.S2vec, self.S1vec), grid,  method="linear")(interp_array).round(self.__round)

    def rho(self, S1=None, S2=None):
        self._check_greeks_solved_()
        S1 = self.param.spot_price1 if S1 is None else S1
        S2 = self.param.spot_price2 if S2 is None else S2
        grid = getattr(self, f'{self.__grid}_rho')
        interp_array = np.array([S2, S1]).T
        return RegularGridInterpolator((self.S2vec, self.S1vec), grid,  method="linear")(interp_array).round(self.__round)

    def dpvdcorr(self, S1=None, S2=None):
        self._check_greeks_solved_()
        S1 = self.param.spot_price1 if S1 is None else S1
        S2 = self.param.spot_price2 if S2 is None else S2
        grid = getattr(self, f'{self.__grid}_dpvdcorr')
        interp_array = np.array([S2, S1]).T
        return RegularGridInterpolator((self.S2vec, self.S1vec), grid,  method="linear")(interp_array).round(self.__round)
