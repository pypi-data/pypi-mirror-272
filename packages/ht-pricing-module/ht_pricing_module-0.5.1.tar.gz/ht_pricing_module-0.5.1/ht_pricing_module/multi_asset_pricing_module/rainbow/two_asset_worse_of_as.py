from ..multi_asset_option_base import *


class TwoAssetWorseOf(MultiAssetOptionBase):

    def __calculate_present_value__(self):
        def __params__(s1, s2, k, r, q1, q2, v1, v2, rho, T):
            b1 = r - q1
            b2 = r - q2

            cov = math.sqrt(v1 * v1 + v2 * v2 - 2 * rho * v1 * v2)
            rho1 = (v1 - rho * v2) / cov
            rho2 = (v2 - rho * v1) / cov

            tv1 = v1 * math.sqrt(T)
            tv2 = v2 * math.sqrt(T)
            tcov = cov * math.sqrt(T)

            y1 = (math.log(s1 / k) + (b1 + v1 * v1 / 2) * T) / tv1
            y2 = (math.log(s2 / k) + (b2 + v2 * v2 / 2) * T) / tv2
            d = (math.log(s1 / s2) + (b1 - b2 + cov * cov / 2) * T) / tcov

            return b1, b2, y1, y2, tv1, tv2, tcov, rho1, rho2, rho, d

        def __call_min__(s1, s2, k, r, q1, q2, v1, v2, rho, T):
            b1, b2, y1, y2, tv1, tv2, tcov, rho1, rho2, rho, d = __params__(s1, s2, k, r, q1, q2, v1, v2, rho, T)

            p1 = s1 * math.exp((b1 - r) * T) * mvn2d(y1, -d, -rho1)
            p2 = s2 * math.exp((b2 - r) * T) * mvn2d(y2, d - tcov, -rho2)
            p3 = k * math.exp(-r * T) * mvn2d(y1 - tv1, y2 - tv2, rho)

            return p1 + p2 - p3

        def __put_min__(s1, s2, k, r, q1, q2, v1, v2, rho, T):
            b1, b2, y1, y2, tv1, tv2, tcov, rho1, rho2, rho, d = __params__(s1, s2, k, r, q1, q2, v1, v2, rho, T)

            p1 = s1 * math.exp((b1 - r) * T) * mvn2d(-y1, -d, rho1)
            p2 = s2 * math.exp((b2 - r) * T) * mvn2d(-y2, d - tcov, rho2)
            p3 = k * math.exp(-r * T) * (1 - mvn2d(y1 - tv1, y2 - tv2, rho))

            return p3 - p1 - p2

        time_to_expiry = (self.param.expiry_date - self.param.current_date) / self.param.year_base

        func = {OptionType.CALL: __call_min__, OptionType.PUT: __put_min__}[self.param.option_type]
        rst = func(self.param.spot_price1, self.param.spot_price2, self.param.strike_price, self.param.riskfree_rate, self.param.dividend1,
                   self.param.dividend2, self.param.volatility1, self.param.volatility2, self.param.correlation, time_to_expiry)
        return rst
