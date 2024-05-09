from ..multi_asset_option_base import *


class ThreeAssetBestOf(MultiAssetOptionBase):

    def __calculate_present_value__(self):

        def __dij__(si, sj, bi, bj, vij, T):
            return (math.log(si / sj) + (bi - bj + vij * vij / 2) * T) / vij / math.sqrt(T)

        def __d1__(s, k, b, v, T):
            return (math.log(s / k) + (b + v * v / 2) * T) / v / math.sqrt(T)

        def __d2__(s, k, b, v, T):
            return (math.log(s / k) + (b - v * v / 2) * T) / v / math.sqrt(T)

        def __rho_iij__(vi, vj, vij, rhoij):
            return (vi - rhoij * vj) / vij

        def __rho_ijk__(vi, vj, vk, vij, vik, rhoij, rhoik, rhojk):
            return (vi * vi - rhoij * vi * vj - rhoik * vi * vk + rhojk * vj * vk) / vij / vik

        def __cov_ij__(vi, vj, rhoij):
            return math.sqrt(vi * vi - 2 * rhoij * vi * vj + vj * vj)

        def __params__(s1, s2, s3, k, r, q1, q2, q3, v1, v2, v3, rho12, rho13, rho23, T):
            b1 = r - q1
            b2 = r - q2
            b3 = r - q3

            con12 = __cov_ij__(v1, v2, rho12)
            con13 = __cov_ij__(v1, v3, rho13)
            con23 = __cov_ij__(v2, v3, rho23)

            rho112 = __rho_iij__(v1, v2, con12, rho12)
            rho113 = __rho_iij__(v1, v3, con13, rho13)
            rho123 = __rho_ijk__(v1, v2, v3, con12, con13, rho12, rho13, rho23)

            rho212 = __rho_iij__(v2, v1, con12, rho12)
            rho213 = __rho_ijk__(v2, v1, v3, con12, con23, rho12, rho23, rho13)
            rho223 = __rho_iij__(v2, v3, con23, rho23)

            rho312 = __rho_ijk__(v3, v1, v2, con13, con23, rho13, rho23, rho12)
            rho313 = __rho_iij__(v3, v1, con13, rho13)
            rho323 = __rho_iij__(v3, v2, con23, rho23)

            d1k = __d1__(s1, k, b1, v1, T)
            d2k = __d1__(s2, k, b2, v2, T)
            d3k = __d1__(s3, k, b3, v3, T)
            dk1 = __d2__(s1, k, b1, v1, T)

            d12 = __dij__(s1, s2, b1, b2, con12, T)
            d21 = __dij__(s2, s1, b2, b1, con12, T)
            d31 = __dij__(s3, s1, b3, b1, con13, T)
            dk2 = __d2__(s2, k, b2, v2, T)

            d13 = __dij__(s1, s3, b1, b3, con13, T)
            d23 = __dij__(s2, s3, b2, b3, con23, T)
            d32 = __dij__(s3, s2, b3, b2, con23, T)
            dk3 = __d2__(s3, k, b3, v3, T)

            return b1, b2, b3, d1k, d2k, d3k, dk1, dk2, dk3, d12, d13, d21, d23, d31, d32, rho112, rho113, rho123, rho212, rho223, rho213, rho313, rho323, rho312

        def __call_max__(s1, s2, s3, k, r, q1, q2, q3, v1, v2, v3, rho12, rho13, rho23, T):
            b1, b2, b3, d1k, d2k, d3k, dk1, dk2, dk3, d12, d13, d21, d23, d31, d32, rho112, rho113, rho123, rho212, rho223, rho213, rho313, rho323, rho312 = __params__(s1, s2, s3, k, r, q1, q2, q3, v1, v2, v3, rho12, rho13, rho23, T)

            p1 = s1 * math.exp((b1 - r) * T) * mvn3d(d1k, d12, d13, rho112, rho113, rho123)
            p2 = s2 * math.exp((b2 - r) * T) * mvn3d(d2k, d21, d23, rho212, rho223, rho213)
            p3 = s3 * math.exp((b3 - r) * T) * mvn3d(d3k, d31, d32, rho313, rho323, rho312)
            p4 = k * math.exp(-r * T) * (1 - mvn3d(-dk1, -dk2, -dk3, rho12, rho13, rho23))

            return p1 + p2 + p3 - p4

        def __put_max__(s1, s2, s3, k, r, q1, q2, q3, v1, v2, v3, rho12, rho13, rho23, T):
            b1, b2, b3, d1k, d2k, d3k, dk1, dk2, dk3, d12, d13, d21, d23, d31, d32, rho112, rho113, rho123, rho212, rho223, rho213, rho313, rho323, rho312 = __params__(s1, s2, s3, k, r, q1, q2, q3, v1, v2, v3, rho12, rho13, rho23, T)

            p1 = s1 * math.exp((b1 - r) * T) * mvn3d(-d1k, d12, d13, -rho112, -rho113, rho123)
            p2 = s2 * math.exp((b2 - r) * T) * mvn3d(-d2k, d21, d23, -rho212, -rho223, rho213)
            p3 = s3 * math.exp((b3 - r) * T) * mvn3d(-d3k, d31, d32, -rho313, -rho323, rho312)
            p4 = k * math.exp(-r * T) * mvn3d(-dk1, -dk2, -dk3, rho12, rho13, rho23)

            return p4 - p1 - p2 - p3

        time_to_expiry = (self.param.expiry_date - self.param.current_date) / self.param.year_base

        func = {OptionType.CALL: __call_max__, OptionType.PUT: __put_max__}[self.param.option_type]
        rst = func(self.param.spot_price1, self.param.spot_price2, self.param.spot_price3, self.param.strike_price, self.param.riskfree_rate,
                   self.param.dividend1, self.param.dividend2, self.param.dividend3, self.param.volatility1, self.param.volatility2,
                   self.param.volatility3, self.param.correlation12, self.param.correlation23, self.param.correlation23, time_to_expiry)

        return rst
