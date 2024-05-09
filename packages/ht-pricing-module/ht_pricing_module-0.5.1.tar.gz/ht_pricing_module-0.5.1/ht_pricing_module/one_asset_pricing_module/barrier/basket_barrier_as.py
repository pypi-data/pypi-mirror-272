from ..one_asset_option_base import *
from ..basket.basket_vanilla_as import BasketVanilla


class BasketBarrier(OneAssetOptionBase):
    def __calculate_present_value__(self) -> float:

        def __bachelier__(f, k, r, v, t, cp, h=None):
            d = (f - (k if h is None else h)) / (v * math.sqrt(t))
            return math.exp(-1 * r * t) * (v * math.sqrt(t) / math.sqrt(2 * math.pi) * math.exp(-1 * pow(d, 2) / 2) + cp * (f - k) * norm.cdf(cp * d))

        cp = {OptionType.CALL: 1, OptionType.PUT: -1}[self.param.option_type]
        du = {BarrierType.DOWN: 1, BarrierType.UP: -1}[self.param.barrier_type]
        time_to_expiry = (self.param.expiry_date - self.param.current_date) / self.param.year_base

        u_knock_flag = self.param.barrier_type == BarrierType.UP and self.param.spot_price >= self.param.barrier_price
        d_knock_flag = self.param.barrier_type == BarrierType.DOWN and self.param.spot_price <= self.param.barrier_price

        if time_to_expiry <= 0:
            """已到期"""
            if self.param.knock_type == KnockType.IN:
                if self.param.is_knock_in or u_knock_flag or d_knock_flag:
                    """敲入"""
                    return max(cp * (self.param.spot_price - self.param.strike_price), 0)
                else:
                    return self.param.rebate
            elif self.param.knock_type == KnockType.OUT:
                if u_knock_flag or d_knock_flag:
                    """敲出"""
                    return self.param.rebate
                else:
                    return max(cp * (self.param.spot_price - self.param.strike_price), 0)
        else:
            """存续"""
            if self.param.knock_type == KnockType.IN:
                if self.param.is_knock_in or u_knock_flag or d_knock_flag:
                    """敲入"""

                    param = Params()
                    param['option_type'] = self.param.option_type
                    param['exercise_type'] = self.param.exercise_type
                    param['spot_price'] = self.param.spot_price
                    param['strike_price'] = self.param.strike_price
                    param['expiry_date'] = self.param.expiry_date
                    param['current_date'] = self.param.current_date
                    param['volatility'] = self.param.volatility
                    param['riskfree_rate'] = self.param.riskfree_rate
                    param['year_base'] = self.param.year_base
                    pricer = BasketVanilla(param)
                    return pricer.present_value()
            elif self.param.knock_type == KnockType.OUT:
                if u_knock_flag or d_knock_flag:
                    """敲出"""
                    return self.param.rebate

        A = __bachelier__(self.param.spot_price, self.param.strike_price, self.param.riskfree_rate, self.param.volatility, time_to_expiry, cp)
        B = __bachelier__(self.param.spot_price, self.param.strike_price, self.param.riskfree_rate, self.param.volatility, time_to_expiry, cp, self.param.barrier_price)
        C = __bachelier__(2 * self.param.barrier_price - self.param.spot_price, self.param.strike_price, self.param.riskfree_rate, self.param.volatility, time_to_expiry, cp)
        D = __bachelier__(2 * self.param.barrier_price - self.param.spot_price, self.param.strike_price, self.param.riskfree_rate, self.param.volatility, time_to_expiry, cp, self.param.barrier_price)

        E = self.param.rebate * 2 * norm.cdf(du * (self.param.barrier_price - self.param.spot_price) / self.param.volatility / math.sqrt(time_to_expiry))
        F = math.exp(-1 * self.param.riskfree_rate * time_to_expiry) * (self.param.rebate - E)

        cp = {OptionType.CALL: 'c', OptionType.PUT: 'p'}[self.param.option_type]
        du = {BarrierType.DOWN: 'd', BarrierType.UP: 'u'}[self.param.barrier_type]
        io = {KnockType.IN: 'i', KnockType.OUT: 'o'}[self.param.knock_type]

        rst = {'cdi': C + F if self.param.strike_price >= self.param.barrier_price else A - B + D + F,
               'cui': A + F if self.param.strike_price >= self.param.barrier_price else B + C - D + F,
               'pdi': B + C - D + F if self.param.strike_price >= self.param.barrier_price else A + F,
               'pui': A - B + D + F if self.param.strike_price >= self.param.barrier_price else C + F,
               'cdo': A - C + E if self.param.strike_price >= self.param.barrier_price else B - D + E,
               'cuo': E if self.param.strike_price >= self.param.barrier_price else A - B - C + D + E,
               'pdo': A - B - C + D + E if self.param.strike_price >= self.param.barrier_price else E,
               'puo': B - D + E if self.param.strike_price >= self.param.barrier_price else A - C + E}[f'{cp}{du}{io}']
        return rst
