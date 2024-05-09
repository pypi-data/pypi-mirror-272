from ..one_asset_option_base import *


class BasketBinary(OneAssetOptionBase):

    def __calculate_present_value__(self):
        """欧式 cash or nothing 解析解"""
        rst = 0
        cp = {OptionType.CALL: 1, OptionType.PUT: -1}[self.param.option_type]
        time_to_expiry = (self.param.expiry_date - self.param.current_date) / self.param.year_base
        if time_to_expiry <= 0:
            rst = self.param.payoff if cp * (self.param.spot_price - self.param.strike_price) >= 0 else 0
        else:
            t_adj_vol = self.param.volatility * math.sqrt(time_to_expiry)
            d = (self.param.spot_price - self.param.strike_price) / t_adj_vol
            rst = self.param.payoff * math.exp(-1 * self.param.riskfree_rate * time_to_expiry) * norm.cdf(cp * d)
        return rst

