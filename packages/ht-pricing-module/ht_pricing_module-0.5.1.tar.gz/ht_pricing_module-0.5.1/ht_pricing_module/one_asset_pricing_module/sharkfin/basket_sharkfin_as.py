from ..one_asset_option_base import *
from ..binary.basket_binary_as import BasketBinary
from ..basket.basket_vanilla_as import BasketVanilla


class BasketSharkfin(OneAssetOptionBase):
        
    def __calculate_present_value__(self):
        if self.param.strike_price == self.param.barrier_price:
            return 0

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
        basket_vanilla1 = BasketVanilla(param)

        cp = {OptionType.CALL: 1, OptionType.PUT: -1}[self.param.option_type]
        gt = 1 if (self.param.strike_price - self.param.barrier_price) > 0 else -1
        if cp * gt > 0:
            return 0

        param = Params()
        param['option_type'] = self.param.option_type
        param['exercise_type'] = self.param.exercise_type
        param['spot_price'] = self.param.spot_price
        param['strike_price'] = self.param.barrier_price
        param['expiry_date'] = self.param.expiry_date
        param['current_date'] = self.param.current_date
        param['volatility'] = self.param.volatility
        param['riskfree_rate'] = self.param.riskfree_rate
        param['year_base'] = self.param.year_base
        basket_vanilla2 = BasketVanilla(param)

        param = Params()
        param['option_type'] = self.param.option_type
        param['exercise_type'] = self.param.exercise_type
        param['spot_price'] = self.param.spot_price
        param['strike_price'] = self.param.barrier_price
        param['expiry_date'] = self.param.expiry_date
        param['current_date'] = self.param.current_date
        param['volatility'] = self.param.volatility
        param['riskfree_rate'] = self.param.riskfree_rate
        param['payoff'] = abs(self.param.strike_price - self.param.barrier_price)
        param['year_base'] = self.param.year_base
        basket_binary3 = BasketBinary(param)

        return basket_vanilla1.present_value() - basket_vanilla2.present_value() - basket_binary3.present_value()
