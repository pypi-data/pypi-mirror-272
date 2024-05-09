from ..one_asset_option_base import *


def __mc_snowball_small__(notional, spot_price, knock_out_barrier_price, option_type, riskfree_rate,
                          dividend, volatility, residual_intraday, expiry_date, year_base, knock_out_obs):

    phi = {OptionType.STANDARD: 1, OptionType.REVERSE: -1}[option_type]

    if expiry_date <= 0:
        ko_coupon_rate = knock_out_obs['coupon_rate'][np.where(knock_out_obs['obs_index'] == expiry_date)][0]
        ko_swap = knock_out_obs['swap_rate'][np.where(knock_out_obs['obs_index'] == expiry_date)][0]
        ko_flag = phi * (spot_price - knock_out_barrier_price) >= 0
        ko_flag = False if len(ko_flag) == 0 else ko_flag[0]
        if ko_flag:
            # 敲出损益
            rst = notional * (ko_coupon_rate + ko_swap)
        else:
            # 未敲入未敲出
            rst = 0
        return rst

    intraday = round(math.ceil(residual_intraday) - residual_intraday, 4)
    price = spot_price * McPathGenerator.generate(riskfree_rate=riskfree_rate, dividend=dividend, volatility=volatility,
                                                  intraday=intraday, expiry_date=expiry_date, year_base=year_base, random_seed=0)
    M = len(price)

    ko_obs_idx = np.where(knock_out_obs['obs_index'] >= 0) if intraday == 0 else np.where(knock_out_obs['obs_index'] > 0)
    ko_coupon = knock_out_obs['coupon_rate'][ko_obs_idx]
    ko_swap = knock_out_obs['swap_rate'][ko_obs_idx]
    ko_obs_idx = knock_out_obs['obs_index'][ko_obs_idx].astype(int)

    t_arr = np.hstack([0, np.arange(1, expiry_date + 1, 1) - intraday])
    assert round(expiry_date - intraday, 4) == round(t_arr[-1], 4)

    ko_mat_flag = np.zeros((M, 1), dtype=bool) if len(ko_obs_idx) == 0 else phi * (price[:, ko_obs_idx] - knock_out_barrier_price) >= 0
    ko_idx = ko_mat_flag.argmax(axis=1)

    # 敲出
    discount_factor = 1 / np.exp(riskfree_rate * t_arr[ko_obs_idx][ko_idx] / year_base)
    ko_arr_flag = np.max(ko_mat_flag, axis=1)
    ko_payoff = ko_arr_flag * discount_factor * notional * (ko_coupon[ko_idx] + ko_swap[ko_idx])

    # 未敲出
    no_ko_payoff = np.logical_not(ko_arr_flag) * 0

    rst = np.round(np.mean(ko_payoff + no_ko_payoff), 8)
    return rst


class SnowballSmallMc(OneAssetOptionBase):

    def __calculate_present_value__(self) -> float:
        residual_intraday = round(math.ceil(self.param.current_date) - self.param.current_date, 4)
        current_date_index = math.floor(self.param.current_date)
        return __mc_snowball_small__(
            notional=self.param.notional,
            spot_price=self.param.spot_price,
            knock_out_barrier_price=self.param.knock_out_barrier_price,
            option_type=self.param.option_type,
            riskfree_rate=self.param.riskfree_rate,
            dividend=self.param.dividend,
            volatility=self.param.volatility,
            residual_intraday=residual_intraday,
            expiry_date=self.param.expiry_date - current_date_index,
            year_base=self.param.year_base,
            knock_out_obs={'obs_index': np.array([obs.obs_index - current_date_index for obs in self.param.knock_out_obs_date]),
                           'coupon_rate': np.array([obs.coupon_rate for obs in self.param.knock_out_obs_date]),
                           'swap_rate': np.array([obs.swap_rate for obs in self.param.knock_out_obs_date])}
        )
