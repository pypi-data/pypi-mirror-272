from ..multi_asset_option_base import *


class TwoAssetBasket(MultiAssetOptionBase):
    """
    价差期权（双标的）
    要求首个资产权重为正数
    归一化处理，首个资产权重置为1。Gauss-Hermitte近似求解积分。
    条件概率下的BS期权定价公式。
    """

    def __calculate_present_value__(self):
        rst = 0
        cp = {OptionType.CALL: 1, OptionType.PUT: -1}[self.param.option_type]
        time_to_expiry = (self.param.expiry_date - self.param.current_date) / self.param.year_base

        if time_to_expiry <= 0 or (self.param.volatility1 == 0 and self.param.volatility2 == 0):
            sT = self.param.weight1 * self.param.spot_price1 + self.param.weight2 * self.param.spot_price2
            rst = max(cp * (sT - self.param.strike_price), 0)
        else:
            vol1_sq = self.param.volatility1 * self.param.volatility1
            vol2_sq = self.param.volatility2 * self.param.volatility2
            t_adj_vol1 = self.param.volatility1 * np.sqrt(time_to_expiry)
            t_adj_vol2 = self.param.volatility2 * np.sqrt(time_to_expiry)
            corr_sq = self.param.correlation * self.param.correlation

            deg = int(6 * math.ceil(((max(self.param.volatility2, self.param.volatility1) / self.param.volatility1) + 1) / np.sqrt(1 - corr_sq)))
            Abscissa, Weight = GuassQuadAbscissaWeight(deg)     # hermgauss(deg), GuassQuadAbscissaWeight(deg)

            s1T = self.param.spot_price1 * np.exp(t_adj_vol1 * np.sqrt(2) * Abscissa * self.param.correlation - corr_sq * vol1_sq * time_to_expiry / 2)
            s2T = self.param.spot_price2 * np.exp(t_adj_vol2 * np.sqrt(2) * Abscissa - vol2_sq * time_to_expiry / 2)

            strike_price = self.param.strike_price / self.param.weight1 - s2T * self.param.weight2 / self.param.weight1
            volatility = self.param.volatility1 * np.sqrt(1 - corr_sq)

            IntegralValue = BlackModelVector(cp, s1T, np.maximum(strike_price, 0), time_to_expiry, self.param.riskfree_rate, volatility) @ Weight
            rst = np.exp(-self.param.riskfree_rate * time_to_expiry) * self.param.weight1 * IntegralValue / np.sqrt(np.pi)

        return rst
