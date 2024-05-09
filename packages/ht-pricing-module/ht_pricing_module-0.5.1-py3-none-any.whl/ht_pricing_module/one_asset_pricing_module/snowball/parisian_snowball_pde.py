from ..one_asset_option_base import interpolate, np, spilu, sp, OneAssetFDParisianSnowball


class ParisianSnowballPde(OneAssetFDParisianSnowball):

    def _set_other_vector_(self):
        self._IntVec = self.param.margin_rate * (np.exp(self.param.riskfree_rate * self.Tauvec / self.param.year_base) - 1)
        self._EnhVec = np.maximum(self._omega * self.param.participation_rate * ((self.Svec - self.param.knock_out_barrier_price) / self.param.entrance_price), 0)
        self._S_KO = self._omega * (self.Svec - self.param.knock_out_barrier_price) >= 0
        self._S_KI = self._omega * (self.Svec - self.param.knock_in_barrier_price) <= 0

    def _set_terminal_condition_(self):
        S_NKI_NKO = ~(self._S_KO | self._S_KI)

        self.KIgrid2nd[self._S_KO, -1] = (self.param.bonus_rate - self._IntVec[-1] + self._EnhVec[self._S_KO]) * self.param.notional
        self.KIgrid2nd[self._S_KI, -1] = (np.maximum((self.param.floor_rate - 1), np.minimum(self._omega * (self.Svec[self._S_KI] - self.param.knock_in_strike_price) / self.param.entrance_price, 0)) - self._IntVec[-1]) * self.param.notional
        self.KIgrid2nd[S_NKI_NKO, -1] = (np.maximum((self.param.floor_rate - 1), np.minimum(self._omega * (self.Svec[S_NKI_NKO] - self.param.knock_in_strike_price) / self.param.entrance_price, 0)) - self._IntVec[-1]) * self.param.notional

        self.KIgrid1st[self._S_KO, -1] = self.KIgrid2nd[self._S_KO, -1].copy()
        self.KIgrid1st[self._S_KI, -1] = self.KIgrid2nd[self._S_KI, -1].copy()
        self.KIgrid1st[S_NKI_NKO, -1] = (self.param.bonus_rate - self._IntVec[-1]) * self.param.notional

        self.NKIgrid[self._S_KO, -1] = self.KIgrid1st[self._S_KO, -1]
        self.NKIgrid[self._S_KI, -1] = (self.param.bonus_rate - self._IntVec[-1]) * self.param.notional
        self.NKIgrid[S_NKI_NKO, -1] = (self.param.bonus_rate - self._IntVec[-1]) * self.param.notional

    def _set_boundary_condition_(self):
        DFr = np.exp(-self.param.riskfree_rate * (self.Tvec[-1] - self.Tvec) / self.param.year_base)

        if self._is_call:
            self.KIgrid2nd[0, :] = (np.maximum((self.param.floor_rate - 1), np.minimum(self._omega * (self.Svec[0] - self.param.knock_in_strike_price) / self.param.entrance_price, 0)) - self._IntVec) * self.param.notional * DFr
            if not np.isscalar(self._Rbt_KO) and len(self._Rbt_KO) > 1:
                f1 = interpolate(x=self._T_KO, y=self._Rbt_KO, kind='next', bounds_error=False, fill_value=(self._Rbt_KO[0], self._Rbt_KO[-1]))
                f2 = interpolate(x=self._T_KO, y=self._T_KO, kind='next', bounds_error=False, fill_value=(self._T_KO[0], self._T_KO[-1]))
                self.KIgrid2nd[-1, :] = (f1(self.Tvec) - self._IntVec + self._EnhVec[-1]) * self.param.notional * np.exp(-self.param.riskfree_rate * (f2(self.Tvec) - self.Tvec) / self.param.year_base)
            else:
                self.KIgrid2nd[-1, :] = (self._Rbt_KO - self._IntVec + self._EnhVec[-1]) * self.param.notional * DFr
        else:
            self.KIgrid2nd[-1, :] = (np.maximum((self.param.floor_rate - 1), np.minimum(self._omega * (self.Svec[-1] - self.param.knock_in_strike_price) / self.param.entrance_price, 0)) - self._IntVec) * self.param.notional * DFr
            if not np.isscalar(self._Rbt_KO) and len(self._Rbt_KO) > 1:
                f1 = interpolate(x=self._T_KO, y=self._Rbt_KO, kind='next', bounds_error=False, fill_value=(self._Rbt_KO[0], self._Rbt_KO[-1]))
                f2 = interpolate(x=self._T_KO, y=self._T_KO, kind='next', bounds_error=False, fill_value=(self._T_KO[0], self._T_KO[-1]))
                self.KIgrid2nd[0, :] = (f1(self.Tvec) - self._IntVec + self._EnhVec[0]) * self.param.notional * np.exp(-self.param.riskfree_rate * (f2(self.Tvec) - self.Tvec) / self.param.year_base)
            else:
                self.KIgrid2nd[0, :] = (self._Rbt_KO - self._IntVec + self._EnhVec[0]) * self.param.notional * DFr

        self.KIgrid1st[0, :] = self.KIgrid2nd[0, :].copy()
        self.KIgrid1st[-1, :] = self.KIgrid2nd[-1, :].copy()

        self.NKIgrid[0, :] = self.KIgrid1st[0, :].copy()
        self.NKIgrid[-1, :] = self.KIgrid1st[-1, :].copy()

        KI_idx = np.searchsorted(self.Tvec, self._T_KI)
        if self._is_call:
            self.NKIgrid[0, KI_idx[-2] + 1:] = DFr[KI_idx[-2] + 1:] * (self.param.bonus_rate - self._IntVec[-1]) * self.param.notional
        else:
            self.NKIgrid[-1, KI_idx[-2] + 1:] = DFr[KI_idx[-2] + 1:] * (self.param.bonus_rate - self._IntVec[-1]) * self.param.notional

    def _solve_(self):
        iluM = spilu(sp.csc_matrix(self._M2), drop_tol=1e-10, fill_factor=100)

        KO_idx = np.searchsorted(self.Tvec, self._T_KO)
        KI_idx = np.searchsorted(self.Tvec, self._T_KI)

        for j in list(reversed(np.arange(self._Nt))):

            if j + 1 in KO_idx:
                self.KIgrid2nd[self._S_KO, j + 1] = (self._Rbt_KO[np.where(KO_idx == j + 1)] - self._IntVec[j + 1] + self._EnhVec[self._S_KO]) * self.param.notional
                self.KIgrid1st[self._S_KO, j + 1] = self.KIgrid2nd[self._S_KO, j + 1].copy()
                self.NKIgrid[self._S_KO, j + 1] = self.KIgrid1st[self._S_KO, j + 1].copy()

            U = self.KIgrid2nd[1: -1, j + 1].copy()
            U[0] += self._l[0] * self.dt / self.param.year_base * self.KIgrid2nd[0, j]
            U[-1] += self._u[-1] * self.dt / self.param.year_base * self.KIgrid2nd[-1, j]
            self.KIgrid2nd[1: -1, j] = iluM.solve(U)

            if j + 1 in KI_idx:
                if j + 1 in KI_idx[:-1]:
                    self.NKIgrid[self._S_KI, j + 1] = self.KIgrid1st[self._S_KI, j + 1].copy()
                self.KIgrid1st[self._S_KI, j + 1] = self.KIgrid2nd[self._S_KI, j + 1].copy()

            U = self.KIgrid1st[1: -1, j + 1].copy()
            U[0] += self._l[0] * self.dt / self.param.year_base * self.KIgrid1st[0, j]
            U[-1] += self._u[-1] * self.dt / self.param.year_base * self.KIgrid1st[-1, j]
            self.KIgrid1st[1: -1, j] = iluM.solve(U)

            U = self.NKIgrid[1: -1, j + 1].copy()
            U[0] += self._l[0] * self.dt / self.param.year_base * self.NKIgrid[0, j]
            U[-1] += self._u[-1] * self.dt / self.param.year_base * self.NKIgrid[-1, j]
            self.NKIgrid[1: -1, j] = iluM.solve(U)

        if self._Nt > 1:
            self.T1KIgrid1st, self.T1KIgrid2nd, self.T1NKIgrid = self.KIgrid1st[:, 1:].copy(), self.KIgrid2nd[:, 1:].copy(), self.NKIgrid[:, 1:].copy()
        else:
            self.T1KIgrid1st, self.T1KIgrid2nd, self.T1NKIgrid = self.KIgrid1st[:, self._Nt:].copy(), self.KIgrid2nd[:, self._Nt:].copy(), self.NKIgrid[:, self._Nt:].copy()
