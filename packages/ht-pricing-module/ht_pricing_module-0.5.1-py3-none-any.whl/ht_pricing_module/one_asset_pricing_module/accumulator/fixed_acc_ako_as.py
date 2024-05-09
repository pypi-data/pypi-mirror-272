from ..one_asset_option_base import *
from ..barrier.discrete_barrier_as import DiscreteBarrier
from ..barrier.discrete_barrier_binary_as import DiscreteBarrierBinary


class FixedAccAko(OneAssetOptionBase):

    def __calculate_present_value__(self) -> float:
        rst = 0

        option_type1 = {OptionType.ACCUMULATOR: OptionType.PUT, OptionType.DECUMULATOR: OptionType.CALL}[self.param.option_type]
        option_type2 = {OptionType.ACCUMULATOR: OptionType.CALL, OptionType.DECUMULATOR: OptionType.PUT}[self.param.option_type]
        barrier_type = {OptionType.ACCUMULATOR: BarrierType.UP, OptionType.DECUMULATOR: BarrierType.DOWN}[self.param.option_type]

        for obs in self.param.obs_date:
            param = Params()
            param['option_type'] = option_type1
            param['exercise_type'] = self.param.exercise_type
            param['spot_price'] = obs.obs_price if self.param.current_date > obs.obs_index else self.param.spot_price
            param['strike_price'] = self.param.strike_price
            param['barrier_price'] = self.param.barrier_price
            param['riskfree_rate'] = self.param.riskfree_rate
            param['dividend'] = self.param.dividend
            param['volatility'] = self.param.volatility
            param['expiry_date'] = obs.obs_index
            param['current_date'] = self.param.current_date
            param['year_base'] = self.param.year_base
            param['barrier_type'] = barrier_type
            param['knock_type'] = KnockType.OUT
            param['is_knock_in'] = 0
            param['rebate'] = 0
            param['obs_freq'] = self.param.obs_freq
            barrier1 = DiscreteBarrier(param)

            param = Params()
            param['option_type'] = option_type2
            param['exercise_type'] = self.param.exercise_type
            param['spot_price'] = obs.obs_price if self.param.current_date > obs.obs_index else self.param.spot_price
            param['strike_price'] = self.param.strike_price
            param['barrier_price'] = self.param.barrier_price
            param['riskfree_rate'] = self.param.riskfree_rate
            param['dividend'] = self.param.dividend
            param['volatility'] = self.param.volatility
            param['expiry_date'] = obs.obs_index
            param['current_date'] = self.param.current_date
            param['year_base'] = self.param.year_base
            param['barrier_type'] = barrier_type
            param['knock_type'] = KnockType.OUT
            param['is_knock_in'] = 0
            param['payoff'] = self.param.payoff
            param['obs_freq'] = self.param.obs_freq
            binary2 = DiscreteBarrierBinary(param)
            rst = rst + (-self.param.leverage * barrier1.present_value() + binary2.present_value())
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

        cp = {OptionType.ACCUMULATOR: 1, OptionType.DECUMULATOR: -1}[self.param.option_type]
        if hasattr(self.param, 'current_date') and hasattr(self.param, 'spot_price'):
            current_up = self.param.current_date + time_step
            pricer_up = deepcopy(self)
            pricer_up.param.current_date = current_up
            for obs in pricer_up.param.obs_date:
                if self.param.current_date <= obs.obs_index < pricer_up.param.current_date:
                    obs.obs_price = pricer_up.param.spot_price

            if cp * (self.param.spot_price - self.param.barrier_price) >= 0:
                return 0 - self.delta(step=price_step)
            else:
                return pricer_up.delta(step=price_step) - self.delta(step=price_step)

        return 0.0
