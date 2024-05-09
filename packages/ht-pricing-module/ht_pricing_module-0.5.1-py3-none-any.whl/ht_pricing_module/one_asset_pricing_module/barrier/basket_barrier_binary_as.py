from ..one_asset_option_base import *
from ..binary.basket_binary_as import BasketBinary


class BasketBarrierBinary(OneAssetOptionBase):

    def __calculate_present_value__(self) -> float:

        def __bachelier_binary__(f, k, x, r, v, t, cp, h=None):
            d = (f - (k if h is None else h)) / (v * math.sqrt(t))
            return x * math.exp(-1 * r * t) * norm.cdf(cp * d)

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
                    return self.param.payoff if cp * (self.param.spot_price - self.param.strike_price) >= 0 else 0
                else:
                    return 0
            elif self.param.knock_type == KnockType.OUT:
                if u_knock_flag or d_knock_flag:
                    """敲出"""
                    return 0
                else:
                    return self.param.payoff if cp * (self.param.spot_price - self.param.strike_price) >= 0 else 0
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
                    param['payoff'] = self.param.payoff
                    param['year_base'] = self.param.year_base
                    pricer = BasketBinary(param)
                    return pricer.present_value()
            elif self.param.knock_type == KnockType.OUT:
                if u_knock_flag or d_knock_flag:
                    """敲出"""
                    return 0

            A = __bachelier_binary__(self.param.spot_price, self.param.strike_price, self.param.payoff, self.param.riskfree_rate, self.param.volatility, time_to_expiry, cp)
            B = __bachelier_binary__(self.param.spot_price, self.param.strike_price, self.param.payoff, self.param.riskfree_rate, self.param.volatility, time_to_expiry, cp, self.param.barrier_price)
            C = __bachelier_binary__(2 * self.param.barrier_price - self.param.spot_price, self.param.strike_price, self.param.payoff, self.param.riskfree_rate, self.param.volatility, time_to_expiry, cp)
            D = __bachelier_binary__(2 * self.param.barrier_price - self.param.spot_price, self.param.strike_price, self.param.payoff, self.param.riskfree_rate, self.param.volatility, time_to_expiry, cp, self.param.barrier_price)

            cp = {OptionType.CALL: 'c', OptionType.PUT: 'p'}[self.param.option_type]
            du = {BarrierType.DOWN: 'd', BarrierType.UP: 'u'}[self.param.barrier_type]
            io = {KnockType.IN: 'i', KnockType.OUT: 'o'}[self.param.knock_type]

            rst = {'cdi': C if self.param.strike_price >= self.param.barrier_price else A - B + D,
                   'cui': A if self.param.strike_price >= self.param.barrier_price else B + C - D,
                   'pdi': B + C - D if self.param.strike_price >= self.param.barrier_price else A,
                   'pui': A - B + D if self.param.strike_price >= self.param.barrier_price else C,
                   'cdo': A - C if self.param.strike_price >= self.param.barrier_price else B - D,
                   'cuo': 0 if self.param.strike_price >= self.param.barrier_price else A - B - C + D,
                   'pdo': A - B - C + D if self.param.strike_price >= self.param.barrier_price else 0,
                   'puo': B - D if self.param.strike_price >= self.param.barrier_price else A - C}[f'{cp}{du}{io}']
            return rst
