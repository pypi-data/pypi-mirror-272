from ..one_asset_option_base import *
from ..binary.binary_as import Binary


class BinarySeries(OneAssetOptionBase):

    def __calculate_present_value__(self) -> float:
        rst = 0
        for obs in self.param.obs_date:
            param = Params()
            param['option_type'] = self.param.option_type
            param['exercise_type'] = self.param.exercise_type
            param['spot_price'] = obs.obs_price if self.param.current_date > obs.obs_index else self.param.spot_price
            param['strike_price'] = self.param.strike_price
            param['expiry_date'] = obs.obs_index
            param['current_date'] = self.param.current_date
            param['volatility'] = self.param.volatility
            param['riskfree_rate'] = self.param.riskfree_rate
            param['dividend'] = self.param.dividend
            param['payoff'] = self.param.payoff
            param['year_base'] = self.param.year_base
            binary = Binary(param)
            rst = rst + binary.present_value() / len(self.param.obs_date)
        return rst

    @lru_cache(maxsize=10)
    def theta(self, step: float = 1) -> float:
        if hasattr(self.param, 'current_date'):
            current_up = self.param.current_date + step
            pricer_up = deepcopy(self)
            pricer_up.param.current_date = current_up
            for obs in pricer_up.param.obs_date:
                if self.param.current_date <= obs.obs_index < pricer_up.param.current_date:
                    obs.obs_price = pricer_up.param.spot_price
            return pricer_up.present_value() - self.present_value()
        return 0.0

    @lru_cache(maxsize=10)
    def ddeltadt(self, time_step: float = 1, price_step: float = 0.001):
        if hasattr(self.param, 'current_date') and hasattr(self.param, 'spot_price'):
            current_up = self.param.current_date + time_step
            pricer_up = deepcopy(self)
            pricer_up.param.current_date = current_up
            for obs in pricer_up.param.obs_date:
                if self.param.current_date <= obs.obs_index < pricer_up.param.current_date:
                    obs.obs_price = pricer_up.param.spot_price
            return pricer_up.delta(step=price_step) - self.delta(step=price_step)
        return 0.0
