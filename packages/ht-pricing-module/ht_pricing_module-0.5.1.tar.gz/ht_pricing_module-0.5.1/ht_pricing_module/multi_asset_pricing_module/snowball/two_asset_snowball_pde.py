from ..multi_asset_option_base import TwoAssetFDSnowball, interpolate, np, spilu, sp, tqdm


class TwoAssetSnowballPde(TwoAssetFDSnowball):
    
    def _set_other_vector_(self):
        self._S1Rtn = self._omega * (self.S1vec - self.param.entrance_price1) / self.param.entrance_price1
        self._S2Rtn = self._omega * (self.S2vec - self.param.entrance_price2) / self.param.entrance_price2
        self._S1Rtn, self._S2Rtn = np.meshgrid(self._S1Rtn, self._S2Rtn)
        S1_d_S2_u = self._S1Rtn - self._S2Rtn <= 0
        self._Min_S1Rtn_S2Rtn = np.minimum(self._S1Rtn * S1_d_S2_u + self._S2Rtn * np.logical_not(S1_d_S2_u), 0)

        self._S1_KO = self._omega * (self.S1vec - self.param.knock_out_barrier_price1) >= 0
        self._S2_KO = self._omega * (self.S2vec - self.param.knock_out_barrier_price2) >= 0
        self._S1_KI = self._omega * (self.S1vec - self.param.knock_in_barrier_price1) <= 0
        self._S2_KI = self._omega * (self.S2vec - self.param.knock_in_barrier_price2) <= 0

    def _set_terminal_condition_(self):
        self._S_KO = np.logical_and(*np.meshgrid(self._S1_KO, self._S2_KO))
        self._S_KI = np.logical_or(*np.meshgrid(self._S1_KI, self._S2_KI))
        self._S_NKI_NKO = np.logical_not(np.logical_or(self._S_KO, self._S_KI))

        self.KIgrid[self._S_KO] = self.param.bonus_rate * self.param.notional
        self.KIgrid[self._S_KI] = self._Min_S1Rtn_S2Rtn[self._S_KI] * self.param.notional
        self.KIgrid[self._S_NKI_NKO] = self._Min_S1Rtn_S2Rtn[self._S_NKI_NKO] * self.param.notional

        self.NKIgrid[self._S_KO] = self.KIgrid[self._S_KO]
        self.NKIgrid[self._S_KI] = self.KIgrid[self._S_KI]
        self.NKIgrid[self._S_NKI_NKO] = self.param.bonus_rate * self.param.notional

    def _set_boundary_condition_(self):
        DFr = np.exp(-self.param.riskfree_rate * (self.Tvec[-1] - self.Tvec) / self.param.year_base)

        if self._is_call:
            self._BC_1d_2 = np.outer(DFr, self._Min_S1Rtn_S2Rtn[:, 0]) * self.param.notional
            self._BC_1_2d = np.outer(DFr, self._Min_S1Rtn_S2Rtn[0, :]) * self.param.notional
            self._BC_1u_2 = np.outer(DFr, self._Min_S1Rtn_S2Rtn[:, -1]) * self.param.notional
            self._BC_1_2u = np.outer(DFr, self._Min_S1Rtn_S2Rtn[-1, :]) * self.param.notional

            if not np.isscalar(self._Rbt_KO) and len(self._Rbt_KO) > 1:
                f1 = interpolate(x=self._T_KO, y=self._Rbt_KO, kind='next', bounds_error=False, fill_value=(self._Rbt_KO[0], self._Rbt_KO[-1]))
                f2 = interpolate(x=self._T_KO, y=self._T_KO, kind='next', bounds_error=False, fill_value=(self._T_KO[0], self._T_KO[-1]))
                DFRbt = f1(self.Tvec) * np.exp(-self.param.riskfree_rate * (f2(self.Tvec) - self.Tvec) / self.param.year_base) * self.param.notional
                self._BC_1u_2[:, self._S2_KO] = DFRbt.reshape(self._Nt + 1, -1)
                self._BC_1_2u[:, self._S1_KO] = DFRbt.reshape(self._Nt + 1, -1)
            else:
                self._BC_1u_2[:, self._S2_KO] = (self._Rbt_KO * self.param.notional * DFr).reshape(self._Nt + 1, -1)
                self._BC_1_2u[:, self._S1_KO] = (self._Rbt_KO * self.param.notional * DFr).reshape(self._Nt + 1, -1)
        else:
            self._BC_1d_2 = np.outer(DFr, self._Min_S1Rtn_S2Rtn[:, 0]) * self.param.notional
            self._BC_1_2d = np.outer(DFr, self._Min_S1Rtn_S2Rtn[0, :]) * self.param.notional
            self._BC_1u_2 = np.outer(DFr, self._Min_S1Rtn_S2Rtn[:, -1]) * self.param.notional
            self._BC_1_2u = np.outer(DFr, self._Min_S1Rtn_S2Rtn[-1, :]) * self.param.notional

            if not np.isscalar(self._Rbt_KO) and len(self._Rbt_KO) > 1:
                f1 = interpolate(x=self._T_KO, y=self._Rbt_KO, kind='next', bounds_error=False, fill_value=(self._Rbt_KO[0], self._Rbt_KO[-1]))
                f2 = interpolate(x=self._T_KO, y=self._T_KO, kind='next', bounds_error=False, fill_value=(self._T_KO[0], self._T_KO[-1]))
                DFRbt = f1(self.Tvec) * np.exp(-self.param.riskfree_rate * (f2(self.Tvec) - self.Tvec) / self.param.year_base) * self.param.notional
                self._BC_1d_2[:, self._S2_KO] = DFRbt.reshape(self._Nt + 1, -1)
                self._BC_1_2d[:, self._S1_KO] = DFRbt.reshape(self._Nt + 1, -1)
            else:
                self._BC_1d_2[:, self._S2_KO] = (self._Rbt_KO * self.param.notional * DFr).reshape(self._Nt + 1, -1)
                self._BC_1_2d[:, self._S1_KO] = (self._Rbt_KO * self.param.notional * DFr).reshape(self._Nt + 1, -1)

    def _solve_intraday_(self, idx, KIcube, NKIcube):
        if self._Tau > 0 and self._Nt > 0:
            dt = round(1 - self._Tau, 4)
            m1, m2 = self._Ns1 - 1, self._Ns2 - 1
            M = sp.eye(m1 * m2) - dt / self.param.year_base * self._A
            iluA = spilu(M, drop_tol=1e-10, fill_factor=100)

            KIgrid = KIcube[idx + 1].copy()
            KIgrid[:, 0], KIgrid[:, -1] = self._BC_1d_2[idx, :], self._BC_1u_2[idx, :]
            KIgrid[0, :], KIgrid[-1, :] = self._BC_1_2d[idx, :], self._BC_1_2u[idx, :]
            U = np.reshape(KIgrid[1:-1, 1:-1], (m1 * m2, 1), order='F') + dt / self.param.year_base * self._update_boundary_(KIgrid)
            KIgrid[1:-1, 1:-1] = np.reshape(iluA.solve(U), (m2, m1), order='F')

            NKIgrid = NKIcube[idx + 1].copy()
            NKIgrid[:, 0], NKIgrid[:, -1] = self._BC_1d_2[idx, :], self._BC_1u_2[idx, :]
            NKIgrid[0, :], NKIgrid[-1, :] = self._BC_1_2d[idx, :], self._BC_1_2u[idx, :]
            U = np.reshape(NKIgrid[1:-1, 1:-1], (m1 * m2, 1), order='F') + dt / self.param.year_base * self._update_boundary_(NKIgrid)
            NKIgrid[1:-1, 1:-1] = np.reshape(iluA.solve(U), (m2, m1), order='F')

            NKIcube[idx] = NKIgrid
        return KIcube, NKIcube

    def _solve_(self):
        m1, m2 = self._Ns1 - 1, self._Ns2 - 1
        iluA = spilu(self._M, drop_tol=1e-10, fill_factor=100)

        KO_idx = np.searchsorted(self.Tvec, self._T_KO)
        KI_idx = np.searchsorted(self.Tvec, self._T_KI)

        self.KIcube, self.NKIcube = [self.KIgrid.copy()], [self.NKIgrid.copy()]
        for j in tqdm(list(reversed(np.arange(self._Nt))), leave=False):

            if j + 1 in KO_idx:
                self.KIgrid[self._S_KO] = (self._Rbt_KO[np.where(KO_idx == j + 1)]) * self.param.notional
                self.NKIgrid[self._S_KO] = self.KIgrid[self._S_KO]

            self.KIgrid[:, 0], self.KIgrid[:, -1] = self._BC_1d_2[j, :], self._BC_1u_2[j, :]
            self.KIgrid[0, :], self.KIgrid[-1, :] = self._BC_1_2d[j, :], self._BC_1_2u[j, :]
            U = np.reshape(self.KIgrid[1:-1, 1:-1], (m1 * m2, 1), order='F') + self.dt / self.param.year_base * self._update_boundary_(self.KIgrid)
            self.KIgrid[1:-1, 1:-1] = np.reshape(iluA.solve(U), (m2, m1), order='F')

            if j + 1 in KI_idx:
                self.NKIgrid[self._S_KI] = self.KIgrid[self._S_KI]

            self.NKIgrid[:, 0], self.NKIgrid[:, -1] = self._BC_1d_2[j, :], self._BC_1u_2[j, :]
            self.NKIgrid[0, :], self.NKIgrid[-1, :] = self._BC_1_2d[j, :], self._BC_1_2u[j, :]
            U = np.reshape(self.NKIgrid[1:-1, 1:-1], (m1 * m2, 1), order='F') + self.dt / self.param.year_base * self._update_boundary_(self.NKIgrid)
            self.NKIgrid[1:-1, 1:-1] = np.reshape(iluA.solve(U), (m2, m1), order='F')

            self.KIcube.append(self.KIgrid.copy())
            self.NKIcube.append(self.NKIgrid.copy())

        self.KIcube, self.NKIcube = np.array(self.KIcube[::-1]), np.array(self.NKIcube[::-1])
        self.KIcube, self.NKIcube = self._solve_intraday_(idx=0, KIcube=self.KIcube, NKIcube=self.NKIcube)
        self.KIgrid, self.NKIgrid = self.KIcube[0], self.NKIcube[0]

        if self._Nt > 1:
            TempKIcube, TempNKIcube = self._solve_intraday_(idx=0, KIcube=self.KIcube[1:], NKIcube=self.NKIcube[1:])
        else:
            TempKIcube, TempNKIcube = self.KIcube[self._Nt:], self.NKIcube[self._Nt:]
        self.T1KIgrid, self.T1NKIgrid = TempKIcube[0], TempNKIcube[0]
