from ..one_asset_option_base import *
from ..binary.binary_as import Binary
from ..vanilla.vanilla_as import Vanilla


class SharkfinYield(OneAssetOptionBase):

    def __calculate_present_value__(self):
        time_to_expiry = (self.param.expiry_date - self.param.entrance_date) / self.param.year_base
        participation_rate = (self.param.max_yield_annual - self.param.min_yield_annual) * time_to_expiry / abs((self.param.strike_price - self.param.barrier_price) / self.param.entrance_price)

        param = Params()
        param['option_type'] = self.param.option_type
        param['exercise_type'] = self.param.exercise_type
        param['spot_price'] = self.param.spot_price / self.param.entrance_price
        param['strike_price'] = self.param.strike_price / self.param.entrance_price
        param['expiry_date'] = self.param.expiry_date
        param['current_date'] = self.param.current_date
        param['volatility'] = self.param.volatility
        param['riskfree_rate'] = self.param.riskfree_rate
        param['dividend'] = self.param.dividend
        param['year_base'] = self.param.year_base
        vanilla1 = Vanilla(param)

        param = Params()
        param['option_type'] = self.param.option_type
        param['exercise_type'] = self.param.exercise_type
        param['spot_price'] = self.param.spot_price / self.param.entrance_price
        param['strike_price'] = self.param.barrier_price / self.param.entrance_price
        param['expiry_date'] = self.param.expiry_date
        param['current_date'] = self.param.current_date
        param['volatility'] = self.param.volatility
        param['riskfree_rate'] = self.param.riskfree_rate
        param['dividend'] = self.param.dividend
        param['year_base'] = self.param.year_base
        vanilla2 = Vanilla(param)

        param = Params()
        param['option_type'] = self.param.option_type
        param['exercise_type'] = self.param.exercise_type
        param['spot_price'] = self.param.spot_price / self.param.entrance_price
        param['strike_price'] = self.param.barrier_price / self.param.entrance_price
        param['expiry_date'] = self.param.expiry_date
        param['current_date'] = self.param.current_date
        param['volatility'] = self.param.volatility
        param['riskfree_rate'] = self.param.riskfree_rate
        param['dividend'] = self.param.dividend
        param['payoff'] = self.param.rebate_annual * time_to_expiry
        param['year_base'] = self.param.year_base
        binary3 = Binary(param)

        return self.param.notional * (participation_rate * (vanilla1.present_value() - vanilla2.present_value()) - binary3.present_value() + self.param.min_yield_annual * time_to_expiry)


