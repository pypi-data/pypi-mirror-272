from .one_asset_pricing_module import *
from .multi_asset_pricing_module import *
from .api_and_utils import *


class SimplePricerEngine:

    @classmethod
    def vanilla(
            cls,
            option_type:                int,
            spot_price:                 Union[int, float],
            strike_price:               Union[int, float],
            expiry_date:                Union[int, float],
            current_date:               Union[int, float],
            volatility:                 Union[int, float],
            riskfree_rate:              Union[int, float],
            dividend:                   Union[int, float],
            year_base:                  int,
            exercise_type:              int = ExerciseType.EUROPEAN,
            pricing_method:             int = PricingMethod.AS
    ):
        """

        :param option_type: 期权类型OptionType属性
        :param exercise_type: 行权类型ExerciseType属性
        :param pricing_method: 模型方法PricingMethod属性
        :param spot_price:  标的价格
        :param strike_price: 行权价格
        :param expiry_date: 到期日
        :param current_date: 当前日
        :param volatility: 波动率
        :param riskfree_rate: 无风险利率
        :param dividend: 分红率
        :param year_base: 年化天数
        :return: BSM香草期权定价引擎
        """

        param = {
            'option_type': option_type,
            'exercise_type': exercise_type,
            'spot_price': spot_price,
            'strike_price': strike_price,
            'expiry_date': expiry_date,
            'current_date': current_date,
            'volatility': volatility,
            'riskfree_rate': riskfree_rate,
            'dividend': dividend,
            'year_base': year_base
        }

        # Vanilla
        if pricing_method == PricingMethod.AS:
            return Vanilla(param)

    @classmethod
    def quotient(
            cls,
            option_type:                int,
            spot_price1:                Union[int, float],
            spot_price2:                Union[int, float],
            strike_price:               Union[int, float],
            expiry_date:                Union[int, float],
            current_date:               Union[int, float],
            volatility1:                Union[int, float],
            volatility2:                Union[int, float],
            correlation:                Union[int, float],
            riskfree_rate:              Union[int, float],
            dividend1:                  Union[int, float],
            dividend2:                  Union[int, float],
            year_base:                  int,
            exercise_type:              int = ExerciseType.EUROPEAN,
            pricing_method:             int = PricingMethod.AS
    ):
        """

        :param option_type: 期权类型OptionType属性
        :param exercise_type: 行权类型ExerciseType属性
        :param pricing_method: 模型方法PricingMethod属性
        :param spot_price1:  标的价格1
        :param spot_price2:  标的价格2
        :param strike_price: 行权价格
        :param expiry_date: 到期日
        :param current_date: 当前日
        :param volatility1: 波动率1
        :param volatility2: 波动率2
        :param correlation: 相关性
        :param riskfree_rate: 无风险利率
        :param dividend1: 分红率1
        :param dividend2: 分红率2
        :param year_base: 年化天数
        :return: BSM香草期权定价引擎
        """

        param = {
            'option_type': option_type,
            'exercise_type': exercise_type,
            'spot_price1': spot_price1,
            'spot_price2': spot_price2,
            'strike_price': strike_price,
            'expiry_date': expiry_date,
            'current_date': current_date,
            'volatility1': volatility1,
            'volatility2': volatility2,
            'correlation': correlation,
            'riskfree_rate': riskfree_rate,
            'dividend1': dividend1,
            'dividend2': dividend2,
            'year_base': year_base
        }

        # TwoAssetQuotient
        if pricing_method == PricingMethod.AS:
            return TwoAssetQuotient(param)

    @classmethod
    def sharkfin(
            cls,
            option_type:                int,
            spot_price:                 Union[int, float],
            strike_price:               Union[int, float],
            barrier_price:              Union[int, float],
            expiry_date:                Union[int, float],
            current_date:               Union[int, float],
            volatility:                 Union[int, float],
            riskfree_rate:              Union[int, float],
            dividend:                   Union[int, float],
            year_base:                  int,
            exercise_type:              int = ExerciseType.EUROPEAN,
            pricing_method:             int = PricingMethod.AS
    ):
        """

        :param option_type: 期权类型OptionType属性
        :param exercise_type: 行权类型ExerciseType属性
        :param pricing_method: 模型方法PricingMethod属性
        :param spot_price:  标的价格
        :param strike_price: 行权价格
        :param barrier_price: 障碍价
        :param expiry_date: 到期日
        :param current_date: 当前日
        :param volatility: 波动率
        :param riskfree_rate: 无风险利率
        :param dividend: 分红率
        :param year_base: 年化天数
        :return: 鲨鱼鳍定价引擎
        """

        param = {
            'option_type': option_type,
            'exercise_type': exercise_type,
            'spot_price': spot_price,
            'strike_price': strike_price,
            'barrier_price': barrier_price,
            'expiry_date': expiry_date,
            'current_date': current_date,
            'volatility': volatility,
            'riskfree_rate': riskfree_rate,
            'dividend': dividend,
            'year_base': year_base
        }

        # Sharkfin
        if pricing_method == PricingMethod.AS:
            return Sharkfin(param)

    @classmethod
    def ratio_spread(
            cls,
            option_type:                int,
            spot_price:                 Union[int, float],
            strike_price:               Union[int, float],
            leverage:                   Union[int, float],
            expiry_date:                Union[int, float],
            current_date:               Union[int, float],
            volatility:                 Union[int, float],
            riskfree_rate:              Union[int, float],
            dividend:                   Union[int, float],
            year_base:                  int,
            exercise_type:              int = ExerciseType.EUROPEAN,
            pricing_method:             int = PricingMethod.AS
    ):
        """

        :param option_type: 期权类型OptionType属性
        :param exercise_type: 行权类型ExerciseType属性
        :param pricing_method: 模型方法PricingMethod属性
        :param spot_price:  标的价格
        :param strike_price: 行权价格
        :param leverage: OTM杠杆
        :param expiry_date: 到期日
        :param current_date: 当前日
        :param volatility: 波动率
        :param riskfree_rate: 无风险利率
        :param dividend: 分红率
        :param year_base: 年化天数
        :return: 价差比率期权定价引擎
        """

        param = {
            'option_type': option_type,
            'exercise_type': exercise_type,
            'spot_price': spot_price,
            'strike_price': strike_price,
            'expiry_date': expiry_date,
            'current_date': current_date,
            'volatility': volatility,
            'riskfree_rate': riskfree_rate,
            'dividend': dividend,
            'year_base': year_base,
            'leverage': leverage
        }

        # Ratio Spread
        if pricing_method == PricingMethod.AS:
            return RatioSpread(param)

    @classmethod
    def barrier(
            cls,
            option_type:                int,
            barrier_type:               int,
            knock_type:                 int,
            spot_price:                 Union[int, float],
            strike_price:               Union[int, float],
            expiry_date:                Union[int, float],
            current_date:               Union[int, float],
            volatility:                 Union[int, float],
            riskfree_rate:              Union[int, float],
            dividend:                   Union[int, float],
            year_base:                  int,
            barrier_price:              Union[int, float],
            rebate:                     Union[int, float],
            is_knock_in:                Union[int] = 0,
            obs_date:                   Union[dict, list, DataFrame] = None,
            obs_freq:                   Union[float, int] = 1,
            exercise_type:              int = ExerciseType.EUROPEAN,
            pricing_method:             int = PricingMethod.AS,
            obs_type:                   int = ObsType.DISCRETE
    ):
        """

        :param obs_type: 观察类型ObsType属性
        :param option_type: 期权类型OptionType属性
        :param exercise_type: 行权类型ExerciseType属性
        :param barrier_type: 障碍类BarrierType属性
        :param knock_type: 障碍敲击类型KnockType属性
        :param pricing_method: 模型方法PricingMethod属性
        :param spot_price:  标的价格
        :param strike_price: 行权价格
        :param expiry_date: 到期日
        :param current_date: 当前日
        :param volatility: 波动率
        :param riskfree_rate: 无风险利率
        :param dividend: 分红率
        :param year_base: 年化天数
        :param barrier_price: 障碍价格
        :param rebate: 回扣
        :param obs_freq: 离散障碍解析解观测频率
        :param obs_date: 离散障碍MC观测日，dict， Dataframe类型
               或RepeatedStruct返回结果: [Params(), ...], Params().obs_index离散观测日
        :param is_knock_in: 1为已敲入0为未敲入
        :return: 障碍期权定价引擎
        """

        assert is_knock_in in [0, 1], "param: is_knock_in should be either 0 or 1"

        param = {
            'option_type': option_type,
            'exercise_type': exercise_type,
            'spot_price': spot_price,
            'strike_price': strike_price,
            'expiry_date': expiry_date,
            'current_date': current_date,
            'volatility': volatility,
            'riskfree_rate': riskfree_rate,
            'dividend': dividend,
            'year_base': year_base,
            'barrier_price': barrier_price,
            'barrier_type': barrier_type,
            'knock_type': knock_type,
            'rebate': rebate,
            'is_knock_in': is_knock_in
        }

        # Barrier
        if obs_type == ObsType.CONTINUOUS and pricing_method == PricingMethod.AS:
            return Barrier(param)

        # DiscreteBarrier
        elif obs_type == ObsType.DISCRETE and pricing_method == PricingMethod.AS:
            param['obs_freq'] = obs_freq
            return DiscreteBarrier(param)

        # DiscreteBarrierMc
        elif obs_type == ObsType.DISCRETE and pricing_method == PricingMethod.MC:

            if obs_date is None:
                obs_date = np.hstack([np.arange(math.floor(current_date) + obs_freq, expiry_date, obs_freq), expiry_date])
                obs_date = {'obs_index': obs_date}

            param['obs_date'] = Params.RepeatedStruct(obs_date)
            return DiscreteBarrierMc(param)

    @classmethod
    def barrier_binary(
            cls,
            option_type:                int,
            barrier_type:               int,
            knock_type:                 int,
            spot_price:                 Union[int, float],
            strike_price:               Union[int, float],
            expiry_date:                Union[int, float],
            current_date:               Union[int, float],
            volatility:                 Union[int, float],
            riskfree_rate:              Union[int, float],
            dividend:                   Union[int, float],
            year_base:                  int,
            barrier_price:              Union[int, float],
            payoff:                     Union[int, float],
            is_knock_in:                Union[int] = 0,
            obs_freq:                   Union[float, int] = 1,
            exercise_type:              int = ExerciseType.EUROPEAN,
            pricing_method:             int = PricingMethod.AS,
            obs_type:                   int = ObsType.DISCRETE
    ):
        """

        :param obs_type: 观察类型ObsType属性
        :param option_type: 期权类型OptionType属性
        :param exercise_type: 行权类型ExerciseType属性
        :param barrier_type: 障碍类BarrierType属性
        :param knock_type: 障碍敲击类型KnockType属性
        :param pricing_method: 模型方法PricingMethod属性
        :param spot_price:  标的价格
        :param strike_price: 行权价格
        :param expiry_date: 到期日
        :param current_date: 当前日
        :param volatility: 波动率
        :param riskfree_rate: 无风险利率
        :param dividend: 分红率
        :param year_base: 年化天数
        :param barrier_price: 障碍价格
        :param payoff: 回扣
        :param obs_freq: 离散障碍解析解观测频率
        :param is_knock_in: 1为已敲入0为未敲入
        :return: 二元障碍期权定价引擎
        """

        assert is_knock_in in [0, 1], "param: is_knock_in should be either 0 or 1"

        param = {
            'option_type': option_type,
            'exercise_type': exercise_type,
            'spot_price': spot_price,
            'strike_price': strike_price,
            'expiry_date': expiry_date,
            'current_date': current_date,
            'volatility': volatility,
            'riskfree_rate': riskfree_rate,
            'dividend': dividend,
            'year_base': year_base,
            'barrier_price': barrier_price,
            'barrier_type': barrier_type,
            'knock_type': knock_type,
            'payoff': payoff,
            'is_knock_in': is_knock_in
        }

        # BarrierBinary
        if obs_type == ObsType.CONTINUOUS and pricing_method == PricingMethod.AS:
            return BarrierBinary(param)

        # DiscreteBarrierBinary
        elif obs_type == ObsType.DISCRETE and pricing_method == PricingMethod.AS:
            param['obs_freq'] = obs_freq
            return DiscreteBarrierBinary(param)

    @classmethod
    def asian(
            cls,
            option_type:                int,
            spot_price:                 Union[int, float],
            strike_price:               Union[int, float],
            expiry_date:                Union[int, float],
            current_date:               Union[int, float],
            volatility:                 Union[int, float],
            riskfree_rate:              Union[int, float],
            dividend:                   Union[int, float],
            year_base:                  int,
            obs_start_date:             Union[int, float],
            running_avg:                Union[int, float],
            obs_date:                   Union[dict, list, DataFrame] = None,
            exercise_type:              int = ExerciseType.EUROPEAN,
            pricing_method:             int = PricingMethod.AS,
            obs_type:                   int = ObsType.DISCRETE
    ):
        """

        :param option_type: 期权类型OptionType属性
        :param exercise_type: 行权类型ExerciseType属性
        :param pricing_method: 模型方法PricingMethod属性
        :param obs_type: 观察类型ObsType属性
        :param spot_price:  标的价格
        :param strike_price: 行权价格
        :param expiry_date: 到期日
        :param current_date: 当前日
        :param volatility: 波动率
        :param riskfree_rate: 无风险利率
        :param dividend: 分红率
        :param year_base: 年化天数
        :param running_avg: 已实现平均价格
        :param obs_start_date: 价格平均观测期开始日期
        :param obs_date: 离散亚式MC观测日，dict， Dataframe类型
               或RepeatedStruct返回结果: [Params(), ...], Params().obs_index离散观测日，Params().obs_price为已实现价格日
        :return: 亚式期权定价引擎
        """

        param = {
            'option_type': option_type,
            'exercise_type': exercise_type,
            'spot_price': spot_price,
            'strike_price': strike_price,
            'expiry_date': expiry_date,
            'current_date': current_date,
            'volatility': volatility,
            'riskfree_rate': riskfree_rate,
            'dividend': dividend,
            'year_base': year_base,
            'obs_start_date': obs_start_date,
            'running_avg': running_avg
        }

        # Asian
        if obs_type == ObsType.CONTINUOUS and pricing_method == PricingMethod.AS:
            return Asian(param)

        # DiscreteAsianMc
        elif obs_type == ObsType.DISCRETE and pricing_method == PricingMethod.MC:
            assert obs_date is not None, "obs_date & obs_price are required for DiscreteAsianMc"
            param['obs_date'] = Params.RepeatedStruct(obs_date)
            return DiscreteAsianMc(param)
        # DiscreteAsianHhm
        elif obs_type == ObsType.DISCRETE and pricing_method == PricingMethod.AS:
            return DiscreteAsianHhm(param)

    @classmethod
    def basket_vanilla(
            cls,
            option_type:                int,
            spot_price:                 Union[int, float],
            strike_price:               Union[int, float],
            expiry_date:                Union[int, float],
            current_date:               Union[int, float],
            volatility:                 Union[int, float],
            riskfree_rate:              Union[int, float],
            dividend:                   Union[int, float],
            year_base:                  int,
            exercise_type:              int = ExerciseType.EUROPEAN,
            pricing_method:             int = PricingMethod.AS
    ):
        """

        :param option_type: 期权类型OptionType属性
        :param exercise_type: 行权类型ExerciseType属性
        :param pricing_method: 模型方法PricingMethod属性
        :param spot_price:  标的价格
        :param strike_price: 行权价格
        :param expiry_date: 到期日
        :param current_date: 当前日
        :param volatility: 波动率
        :param riskfree_rate: 无风险利率
        :param dividend: 分红率
        :param year_base: 年化天数
        :return: 篮子期权定价引擎
        """

        param = {
            'option_type': option_type,
            'exercise_type': exercise_type,
            'spot_price': spot_price,
            'strike_price': strike_price,
            'expiry_date': expiry_date,
            'current_date': current_date,
            'volatility': volatility,
            'riskfree_rate': riskfree_rate,
            'dividend': dividend,
            'year_base': year_base
        }

        # BasketVanilla
        if pricing_method == PricingMethod.AS:
            return BasketVanilla(param)

    @classmethod
    def basket_barrier(
            cls,
            option_type:                int,
            barrier_type:               int,
            knock_type:                 int,
            spot_price:                 Union[int, float],
            strike_price:               Union[int, float],
            expiry_date:                Union[int, float],
            current_date:               Union[int, float],
            volatility:                 Union[int, float],
            riskfree_rate:              Union[int, float],
            dividend:                   Union[int, float],
            year_base:                  int,
            barrier_price:              Union[int, float],
            rebate:                     Union[int, float],
            is_knock_in:                Union[int] = 0,
            obs_freq:                   Union[float, int] = 1,
            exercise_type:              int = ExerciseType.EUROPEAN,
            pricing_method:             int = PricingMethod.AS,
            obs_type:                   int = ObsType.DISCRETE
    ):
        """

        :param obs_type: 观察类型ObsType属性
        :param option_type: 期权类型OptionType属性
        :param exercise_type: 行权类型ExerciseType属性
        :param barrier_type: 障碍类BarrierType属性
        :param knock_type: 障碍敲击类型KnockType属性
        :param pricing_method: 模型方法PricingMethod属性
        :param spot_price:  标的价格
        :param strike_price: 行权价格
        :param expiry_date: 到期日
        :param current_date: 当前日
        :param volatility: 波动率
        :param riskfree_rate: 无风险利率
        :param dividend: 分红率
        :param year_base: 年化天数
        :param barrier_price: 障碍价格
        :param rebate: 回扣
        :param obs_freq: 离散障碍解析解观测频率
        :param is_knock_in: 1为已敲入0为未敲入
        :return: 价差障碍期权定价引擎
        """

        assert is_knock_in in [0, 1], "param: is_knock_in should be either 0 or 1"

        param = {
            'option_type': option_type,
            'exercise_type': exercise_type,
            'spot_price': spot_price,
            'strike_price': strike_price,
            'expiry_date': expiry_date,
            'current_date': current_date,
            'volatility': volatility,
            'riskfree_rate': riskfree_rate,
            'dividend': dividend,
            'year_base': year_base,
            'barrier_price': barrier_price,
            'barrier_type': barrier_type,
            'knock_type': knock_type,
            'rebate': rebate,
            'is_knock_in': is_knock_in
        }

        # BasketBarrier
        if obs_type == ObsType.CONTINUOUS and pricing_method == PricingMethod.AS:
            return BasketBarrier(param)

        # DiscreteBasketBarrier
        elif obs_type == ObsType.DISCRETE and pricing_method == PricingMethod.AS:
            param['obs_freq'] = obs_freq
            return BasketDiscreteBarrier(param)

    @classmethod
    def binary(
            cls,
            option_type:                int,
            spot_price:                 Union[int, float],
            strike_price:               Union[int, float],
            expiry_date:                Union[int, float],
            current_date:               Union[int, float],
            volatility:                 Union[int, float],
            riskfree_rate:              Union[int, float],
            dividend:                   Union[int, float],
            payoff:                     Union[int, float],
            year_base:                  int,
            obs_type:                   int = ObsType.CONTINUOUS,
            exercise_type:              int = ExerciseType.EUROPEAN,
            pricing_method:             int = PricingMethod.AS,
            obs_date:                   Union[dict, list, DataFrame] = None,
            obs_freq:                   Union[float, int] = 1,
    ):
        """

        :param option_type: 期权类型OptionType属性
        :param exercise_type: 行权类型ExerciseType属性
        :param pricing_method: 模型方法PricingMethod属性
        :param obs_type: 观察类型ObsType属性
        :param spot_price:  标的价格
        :param strike_price: 行权价格
        :param expiry_date: 到期日
        :param current_date: 当前日
        :param volatility: 波动率
        :param riskfree_rate: 无风险利率
        :param dividend: 分红率
        :param year_base: 年化天数
        :param payoff: 到期赔付
        :param obs_date: 离散亚式MC观测日，dict， Dataframe类型
               或RepeatedStruct返回结果: [Params(), ...], Params().obs_index离散观测日，Params().obs_price为已实现价格日
        :param obs_freq 默认等于1
        :return: 二元期权定价引擎
        """

        param = {
            'option_type': option_type,
            'exercise_type': exercise_type,
            'spot_price': spot_price,
            'strike_price': strike_price,
            'expiry_date': expiry_date,
            'current_date': current_date,
            'volatility': volatility,
            'riskfree_rate': riskfree_rate,
            'dividend': dividend,
            'payoff': payoff,
            'year_base': year_base
        }

        # Binary
        if obs_type == ObsType.CONTINUOUS and pricing_method == PricingMethod.AS:
            return Binary(param)
        elif obs_type == ObsType.DISCRETE and pricing_method == PricingMethod.MC:

            if obs_date is None:
                obs_date = np.hstack([np.arange(math.floor(current_date) + obs_freq, expiry_date, obs_freq), expiry_date])
                obs_date = {'obs_index': obs_date}

            param['obs_date'] = Params.RepeatedStruct(obs_date)
            return DiscreteBinaryMc(param)

    @classmethod
    def snowball(
            cls,
            notional:                   Union[int, float],
            spot_price:                 Union[int, float],
            knock_in_barrier_price:     Union[int, float],
            knock_out_barrier_price:    Union[int, float],
            current_date:               Union[int, float],
            expiry_date:                Union[int, float],
            volatility:                 Union[int, float],
            riskfree_rate:              Union[int, float],
            dividend:                   Union[int, float],
            bonus_rate:                 Union[int, float],
            year_base:                  int,
            knock_in_obs_date:          Union[dict, list, DataFrame],
            knock_out_obs_date:         Union[dict, list, DataFrame],
            floor_rate:                 Union[int, float] = 0,
            margin_rate:                Union[int, float] = 0,
            participation_rate:         Union[int, float] = 0,
            is_discount:                Union[int] = 0,
            is_knock_in:                Union[int] = 0,
            option_type:                int = OptionType.STANDARD,
            pricing_method:             int = PricingMethod.PDE,
            entrance_price:             Union[int, float] = None,
            knock_in_strike_price:      Union[int, float] = None,
    ):
        """

        :param option_type: 期权类型OptionType属性, STANDARD(正向), REVERSE(反向)
        :param pricing_method: 模型方法PricingMethod属性
        :param notional: 名义本金
        :param spot_price: 标的价格
        :param entrance_price: 入场价
        :param knock_in_barrier_price: 敲出障碍
        :param knock_out_barrier_price: 敲出障碍
        :param expiry_date: 到期日
        :param current_date: 当前日
        :param volatility: 波动率
        :param riskfree_rate: 无风险利率
        :param dividend: 分红率
        :param floor_rate 保护价
        :param margin_rate 保证金率
        :param bonus_rate: 到期收益率(非年化)
        :param year_base: 年化天数
        :param knock_in_obs_date: 雪球MC敲入观测日，dict， Dataframe类型
               或RepeatedStruct返回结果: [Params(), ...], Struct(obs_index, adjust_rate)
        :param knock_out_obs_date: 雪球MC敲出观测日，dict， Dataframe类型
               或RepeatedStruct返回结果: [Params(), ...], Struct(obs_index, adjust_rate, coupon_rate)
        :param is_knock_in: 1为已敲入0为未敲入
        :param participation_rate: 增强雪球敲出参与率
        :param is_discount: 是否为折价减仓雪球
        :param knock_in_strike_price 折价建仓雪球执行价，默认值为敲入价 或 OTM雪球敲入执行价，默认值为入场价
        :return: 雪球期权定价引擎
        """

        assert is_knock_in in [0, 1], "param: is_knock_in should be either 0 or 1"
        assert is_discount in [0, 1], "param: is_discount should be either 0 or 1"
        assert option_type in [OptionType.STANDARD, OptionType.REVERSE], option_type

        param = {
            'option_type': option_type,
            'notional': notional,
            'spot_price': spot_price,
            'knock_in_barrier_price': knock_in_barrier_price,
            'knock_out_barrier_price': knock_out_barrier_price,
            'floor_rate': floor_rate,
            'margin_rate': margin_rate,
            'bonus_rate': bonus_rate,
            'is_knock_in': is_knock_in,
            'riskfree_rate': riskfree_rate,
            'dividend': dividend,
            'volatility': volatility,
            'current_date': current_date,
            'expiry_date': expiry_date,
            'year_base': year_base,
            'participation_rate': participation_rate
        }

        adjust_rate = 'adjust_rate'
        if adjust_rate not in knock_in_obs_date.keys():
            knock_in_obs_date[adjust_rate] = np.ones_like(knock_in_obs_date['obs_index'])
        if adjust_rate not in knock_out_obs_date.keys():
            knock_out_obs_date[adjust_rate] = np.ones_like(knock_out_obs_date['obs_index'])

        param['knock_in_obs_date'] = Params.RepeatedStruct(knock_in_obs_date)
        param['knock_out_obs_date'] = Params.RepeatedStruct(knock_out_obs_date)
        param['entrance_price'] = spot_price if entrance_price is None else entrance_price

        if is_discount:
            param['knock_in_strike_price'] = param['knock_in_barrier_price'] if knock_in_strike_price is None else knock_in_strike_price
            if pricing_method == PricingMethod.MC:  # SnowballDiscountMc
                return SnowballDiscountedMc(param)
            elif pricing_method == PricingMethod.PDE:   # SnowballDiscountPde
                return SnowballDiscountedPde(param)
        else:
            param['knock_in_strike_price'] = param['entrance_price'] if knock_in_strike_price is None else knock_in_strike_price
            if pricing_method == PricingMethod.MC:  # SnowballMc
                return SnowballMc(param)
            elif pricing_method == PricingMethod.PDE:   # SnowballPde
                return SnowballPde(param)

    @classmethod
    def small_snowball(
            cls,
            notional:                   Union[int, float],
            spot_price:                 Union[int, float],
            knock_out_barrier_price:    Union[int, float],
            current_date:               Union[int, float],
            expiry_date:                Union[int, float],
            volatility:                 Union[int, float],
            riskfree_rate:              Union[int, float],
            dividend:                   Union[int, float],
            year_base:                  int,
            knock_out_obs_date:         Union[dict, list, DataFrame],
            option_type:                int = OptionType.STANDARD,
            pricing_method:             int = PricingMethod.MC,
    ):
        """

        :param option_type: 期权类型OptionType属性, STANDARD(正向), REVERSE(反向)
        :param pricing_method: 模型方法PricingMethod属性
        :param notional: 名义本金
        :param spot_price: 标的价格
        :param knock_out_barrier_price: 敲出障碍
        :param expiry_date: 到期日
        :param current_date: 当前日
        :param volatility: 波动率
        :param riskfree_rate: 无风险利率
        :param dividend: 分红率
        :param year_base: 年化天数
        :param knock_out_obs_date: 雪球MC敲出观测日，dict， Dataframe类型
               或RepeatedStruct返回结果: [Params(), ...], Struct(obs_index, adjust_rate, coupon_rate)
        :return: 小雪球期权定价引擎
        """
        assert option_type in [OptionType.STANDARD, OptionType.REVERSE], option_type

        param = {
            'option_type': option_type,
            'notional': notional,
            'spot_price': spot_price,
            'knock_out_barrier_price': knock_out_barrier_price,
            'riskfree_rate': riskfree_rate,
            'dividend': dividend,
            'volatility': volatility,
            'current_date': current_date,
            'expiry_date': expiry_date,
            'year_base': year_base,
            'knock_out_obs_date': Params.RepeatedStruct(knock_out_obs_date)
        }

        if pricing_method == PricingMethod.MC:  # SnowballSmallMc
            return SnowballSmallMc(param)

    @classmethod
    def airbag(
            cls,
            spot_price:                 Union[int, float],
            strike_price:               Union[int, float],
            barrier_price:              Union[int, float],
            expiry_date:                Union[int, float],
            current_date:               Union[int, float],
            volatility:                 Union[int, float],
            riskfree_rate:              Union[int, float],
            dividend:                   Union[int, float],
            year_base:                  int,
            participation_rate:         Union[int, float],
            is_knock_in:                Union[int] = 0,
            is_capped:                  Union[int] = 0,
            cap_price:                  Union[int, float] = None,
            obs_freq:                   Union[float, int] = 1,
            option_type:                int = OptionType.STANDARD,
            exercise_type:              int = ExerciseType.EUROPEAN,
            pricing_method:             int = PricingMethod.AS,
            obs_type:                   int = ObsType.DISCRETE
    ):
        """

        :param option_type: 期权类型OptionType属性, STANDARD(正向), REVERSE(反向)
        :param obs_type: 观察类型ObsType属性
        :param exercise_type: 行权类型ExerciseType属性
        :param pricing_method: 模型方法PricingMethod属性
        :param spot_price:  标的价格
        :param strike_price: 行权价格
        :param expiry_date: 到期日
        :param current_date: 当前日
        :param volatility: 波动率
        :param riskfree_rate: 无风险利率
        :param dividend: 分红率
        :param year_base: 年化天数
        :param participation_rate 参与率
        :param barrier_price: 障碍价格
        :param obs_freq: 离散障碍解析解观测频率
        :param is_knock_in: 1为已敲入0为未敲入
        :param is_capped: 是否对收益封顶
        :param cap_price: 封顶价格
        :return: 安全气囊期权定价引擎
        """

        assert is_knock_in in [0, 1], "param: is_knock_in should be either 0 or 1"
        assert is_capped in [0, 1], "param: is_capped should be either 0 or 1"
        assert (is_capped == 1 and cap_price is not None) or not is_capped, "cap price should be given"
        assert option_type in [OptionType.STANDARD, OptionType.REVERSE], option_type

        param = {
            'option_type': option_type,
            'exercise_type': exercise_type,
            'spot_price': spot_price,
            'strike_price': strike_price,
            'expiry_date': expiry_date,
            'current_date': current_date,
            'volatility': volatility,
            'riskfree_rate': riskfree_rate,
            'dividend': dividend,
            'year_base': year_base,
            'barrier_price': barrier_price,
            'participation_rate': participation_rate,
            'is_knock_in': is_knock_in,
            'is_capped': is_capped,
            'cap_price': cap_price
        }

        # Airbag
        if obs_type == ObsType.DISCRETE and pricing_method == PricingMethod.AS:
            param['obs_freq'] = obs_freq
            return Airbag(param)

    @classmethod
    def accumulator(
            cls,
            spot_price:                 Union[int, float],
            strike_price:               Union[int, float],
            expiry_date:                Union[int, float],
            current_date:               Union[int, float],
            volatility:                 Union[int, float],
            riskfree_rate:              Union[int, float],
            dividend:                   Union[int, float],
            leverage:                   Union[int, float],
            year_base:                  int,
            accumulator_type:           int,
            barrier_price:              Union[int, float] = None,
            payoff:                     Union[int, float] = None,
            rebate:                     Union[int, float] = None,
            final_position_multiplier:  Union[int, float] = None,
            option_type:                int = OptionType.ACCUMULATOR,
            exercise_type:              int = ExerciseType.EUROPEAN,
            pricing_method:             int = PricingMethod.AS,
            obs_date:                   Union[dict, list, DataFrame] = None,
            obs_freq:                   Union[float, int] = 1,
            base_quantity:              Union[float, int] = 1,
    ):
        """

        :param accumulator_type: 累计类型AccumulatorType属性
        :param option_type: 期权类型OptionType属性, ACCUMULATOR(累计), DECUMULATOR(累沽)
        :param exercise_type: 行权类型ExerciseType属性
        :param pricing_method: 模型方法PricingMethod属性
        :param spot_price:  标的价格
        :param strike_price: 行权价格
        :param expiry_date: 到期日
        :param current_date: 当前日
        :param volatility: 波动率
        :param riskfree_rate: 无风险利率
        :param dividend: 分红率
        :param leverage: 杠杆倍数
        :param year_base: 年化天数
        :param barrier_price: LinearAcc，FixedAccBarrier, LinearAccAko, FixedAccAko, FixedAccEnhanced, LinearAccEnhanced必填参数, 障碍价格
        :param payoff: FixedAcc，FixedAccBarrier, FixedAccAko, FixedAccEnhanced, LinearAccAko, LinearAccFusing必填参数, 赔付
        :param rebate: FixedAccFusing 敲出赔付
        :param final_position_multiplier: 熔断累计到期日建仓乘数
        :param obs_date: 观测日，dict， Dataframe类型，默认每天到期一笔
               或RepeatedStruct返回结果: [Params(), ...], Params().obs_index离散观测日，Params().obs_price为已实现价格日
        :param obs_freq 默认为1，每天到期一笔
        :param base_quantity 每日观察数量
        :return: 累计期权定价引擎
        """

        assert option_type in [OptionType.ACCUMULATOR, OptionType.DECUMULATOR], option_type

        if accumulator_type in [AccumulatorType.LINEAR_ACC, AccumulatorType.FIXED_ACC_BARRIER]:
            assert (option_type == OptionType.ACCUMULATOR and strike_price <= barrier_price) or\
                   (option_type == OptionType.DECUMULATOR and strike_price >= barrier_price), "cuo: K < H, pdo: K > H"

        param = {
            'option_type': option_type,
            'exercise_type': exercise_type,
            'spot_price': spot_price,
            'strike_price': strike_price,
            'expiry_date': expiry_date,
            'current_date': current_date,
            'volatility': volatility,
            'riskfree_rate': riskfree_rate,
            'dividend': dividend,
            'leverage': leverage,
            'year_base': year_base
        }

        if obs_date is None:
            obs_date = np.hstack([np.arange(math.floor(current_date) + obs_freq, expiry_date, obs_freq), expiry_date])
            obs_date = {'obs_index': obs_date, 'obs_price': np.ones_like(obs_date) * spot_price}
        param['obs_date'] = Params.RepeatedStruct(obs_date)

        # LinearAcc
        if pricing_method == PricingMethod.AS and accumulator_type == AccumulatorType.LINEAR_ACC:
            assert barrier_price is not None, "barrier is required for LinearAcc"
            param['barrier_price'] = barrier_price
            return LinearAcc(param)

        # LinearAccEnhanced
        elif pricing_method == PricingMethod.AS and accumulator_type == AccumulatorType.LINEAR_ACC_ENHANCED:
            assert barrier_price is not None, "barrier is required for LinearAccEnhanced"
            param['barrier_price'] = barrier_price
            return LinearAccEnhanced(param)

        # LinearAccFixedEnhanced
        elif pricing_method == PricingMethod.AS and accumulator_type == AccumulatorType.LINEAR_ACC_FIXED_ENHANCED:
            assert barrier_price is not None and payoff is not None, "payoff & barrier is required for LinearAccFixedEnhanced"
            param['payoff'] = payoff
            param['barrier_price'] = barrier_price
            return LinearAccFixedEnhanced(param)

        # FixedAcc
        elif pricing_method == PricingMethod.AS and accumulator_type == AccumulatorType.FIXED_ACC:
            assert payoff is not None, "payoff is required for FixedAcc"
            param['payoff'] = payoff
            return FixedAcc(param)

        # FixedAccEnhanced
        elif pricing_method == PricingMethod.AS and accumulator_type == AccumulatorType.FIXED_ACC_ENHANCED:
            assert barrier_price is not None and payoff is not None, "payoff & barrier is required for FixedAccEnhanced"
            param['payoff'] = payoff
            param['barrier_price'] = barrier_price
            return FixedAccEnhanced(param)

        # FixedAccBarrier
        elif pricing_method == PricingMethod.AS and accumulator_type == AccumulatorType.FIXED_ACC_BARRIER:
            assert payoff is not None and barrier_price is not None, "payoff & barrier is required for FixedAccBarrier"
            param['payoff'] = payoff
            param['barrier_price'] = barrier_price
            return FixedAccBarrier(param)

        # FixedAccBarrierEnhanced
        elif pricing_method == PricingMethod.AS and accumulator_type == AccumulatorType.FIXED_ACC_BARRIER_ENHANCED:
            assert payoff is not None and barrier_price is not None, "payoff & barrier is required for FixedAccBarrierEnhanced"
            param['payoff'] = payoff
            param['barrier_price'] = barrier_price
            return FixedAccBarrierEnhanced(param)

        # FixedAccAko
        elif pricing_method == PricingMethod.AS and accumulator_type == AccumulatorType.FIXED_ACC_AKO:
            assert payoff is not None and barrier_price is not None, "payoff & barrier is required for FixedAccAko"
            param['payoff'] = payoff
            param['barrier_price'] = barrier_price
            param['obs_freq'] = obs_freq
            return FixedAccAko(param)

        # LinearAccAko
        elif pricing_method == PricingMethod.AS and accumulator_type == AccumulatorType.LINEAR_ACC_AKO:
            assert payoff is not None and barrier_price is not None, "payoff & barrier is required for LinearAccAko"
            param['payoff'] = payoff
            param['barrier_price'] = barrier_price
            param['obs_freq'] = obs_freq
            return LinearAccAko(param)

        # LinearAccFusing
        elif pricing_method == PricingMethod.AS and accumulator_type == AccumulatorType.LINEAR_ACC_FUSING:
            assert payoff is not None and barrier_price is not None, "payoff & barrier is required for LinearAccFusing"
            param['payoff'] = payoff
            param['barrier_price'] = barrier_price
            param['obs_freq'] = obs_freq
            if final_position_multiplier is None:
                final_position_multiplier = expiry_date - math.floor(current_date)
            param['final_position_multiplier'] = final_position_multiplier
            param['base_quantity'] = base_quantity
            return LinearAccFusing(param)

        # LinearAccFusingCloseSettle
        elif pricing_method == PricingMethod.AS and accumulator_type == AccumulatorType.LINEAR_ACC_FUSING_CLOSE_SETTLE:
            assert payoff is not None and barrier_price is not None, "payoff & barrier is required for LinearAccFusingCloseSettle"
            param['payoff'] = payoff
            param['barrier_price'] = barrier_price
            param['obs_freq'] = obs_freq
            if final_position_multiplier is None:
                final_position_multiplier = expiry_date - math.floor(current_date)
            param['final_position_multiplier'] = final_position_multiplier
            param['base_quantity'] = base_quantity
            return LinearAccFusingCloseSettle(param)

        # FixedAccFusing
        elif pricing_method == PricingMethod.AS and accumulator_type == AccumulatorType.FIXED_ACC_FUSING:
            assert payoff is not None and rebate is not None and barrier_price is not None, "payoff & rebate & barrier is required for FixedAccFusing"
            param['payoff'] = payoff
            param['rebate'] = rebate
            param['barrier_price'] = barrier_price
            param['obs_freq'] = obs_freq
            if final_position_multiplier is None:
                final_position_multiplier = expiry_date - math.floor(current_date)
            param['final_position_multiplier'] = final_position_multiplier
            param['base_quantity'] = base_quantity
            return FixedAccFusing(param)

        # BasketLinearAcc
        elif pricing_method == PricingMethod.AS and accumulator_type == AccumulatorType.BASKET_LINEAR_ACC:
            assert barrier_price is not None, "barrier is required for BasketLinearAcc"
            param['barrier_price'] = barrier_price
            return BasketLinearAcc(param)

        # BasketFixedAcc
        elif pricing_method == PricingMethod.AS and accumulator_type == AccumulatorType.BASKET_FIXED_ACC:
            assert payoff is not None, "payoff is required for BasketFixedAcc"
            param['payoff'] = payoff
            return BasketFixedAcc(param)

        # BasketFixedAccBarrier
        elif pricing_method == PricingMethod.AS and accumulator_type == AccumulatorType.BASKET_FIXED_ACC_BARRIER:
            assert payoff is not None and barrier_price is not None, "payoff & barrier is required for BasketFixedAccBarrier"
            param['payoff'] = payoff
            param['barrier_price'] = barrier_price
            return BasketFixedAccBarrier(param)

    @classmethod
    def enhanced_asian(
            cls,
            option_type:                int,
            spot_price:                 Union[int, float],
            strike_price:               Union[int, float],
            expiry_date:                Union[int, float],
            current_date:               Union[int, float],
            volatility:                 Union[int, float],
            riskfree_rate:              Union[int, float],
            dividend:                   Union[int, float],
            year_base:                  int,
            obs_date:                   Union[dict, list, DataFrame],
            enhanced_strike_price:      Union[int, float] = None,
            exercise_type:              int = ExerciseType.EUROPEAN,
            pricing_method:             int = PricingMethod.AS
    ):
        """

        :param option_type: 期权类型OptionType属性
        :param exercise_type: 行权类型ExerciseType属性
        :param pricing_method: 模型方法PricingMethod属性
        :param spot_price:  标的价格
        :param strike_price: 行权价格
        :param expiry_date: 到期日
        :param current_date: 当前日
        :param volatility: 波动率
        :param riskfree_rate: 无风险利率
        :param dividend: 分红率
        :param obs_date: 增强亚式观测日，dict， Dataframe类型
        :param year_base: 年化天数
        :param enhanced_strike_price: 增强价格，默认为空
        :return: 增强亚式期权定价引擎
        """

        param = {
            'option_type': option_type,
            'exercise_type': exercise_type,
            'spot_price': spot_price,
            'strike_price': strike_price,
            'expiry_date': expiry_date,
            'current_date': current_date,
            'volatility': volatility,
            'riskfree_rate': riskfree_rate,
            'dividend': dividend,
            'year_base': year_base,
            'obs_date': Params.RepeatedStruct(obs_date)
        }

        # enhanced_asian
        if enhanced_strike_price is None:
            if pricing_method == PricingMethod.AS:
                return VanillaSeries(param)
        else:
            param['enhanced_strike_price'] = enhanced_strike_price
            if pricing_method == PricingMethod.AS:
                return EnhancedAsian(param)

    @classmethod
    def enhanced_asian_spread(
            cls,
            option_type:                int,
            spot_price:                 Union[int, float],
            strike_price:               Union[int, float],
            enhanced_strike_price1:     Union[int, float],
            enhanced_strike_price2:     Union[int, float],
            expiry_date:                Union[int, float],
            current_date:               Union[int, float],
            volatility:                 Union[int, float],
            riskfree_rate:              Union[int, float],
            dividend:                   Union[int, float],
            year_base:                  int,
            obs_date:                   Union[dict, list, DataFrame],
            exercise_type:              int = ExerciseType.EUROPEAN,
            pricing_method:             int = PricingMethod.AS
    ):
        """

        :param option_type: 期权类型OptionType属性
        :param exercise_type: 行权类型ExerciseType属性
        :param pricing_method: 模型方法PricingMethod属性
        :param spot_price:  标的价格
        :param strike_price: 行权价格
        :param expiry_date: 到期日
        :param current_date: 当前日
        :param volatility: 波动率
        :param riskfree_rate: 无风险利率
        :param dividend: 分红率
        :param obs_date: 增强亚式观测日，dict， Dataframe类型
        :param year_base: 年化天数
        :param enhanced_strike_price1: 增强价格1
        :param enhanced_strike_price2: 增强价格2
        :return: 增强亚式价差期权定价引擎
        """

        param = {
            'option_type': option_type,
            'exercise_type': exercise_type,
            'spot_price': spot_price,
            'strike_price': strike_price,
            'enhanced_strike_price1': enhanced_strike_price1,
            'enhanced_strike_price2': enhanced_strike_price2,
            'expiry_date': expiry_date,
            'current_date': current_date,
            'volatility': volatility,
            'riskfree_rate': riskfree_rate,
            'dividend': dividend,
            'year_base': year_base,
            'obs_date': Params.RepeatedStruct(obs_date)
        }

        # enhanced_asian_spread
        if pricing_method == PricingMethod.AS:
            return EnhancedAsianSpread(param)

    @classmethod
    def touch(
            cls,
            option_type:                int,
            knock_type:                 int,
            spot_price:                 Union[int, float],
            barrier_price:              Union[int, float, tuple, list],
            expiry_date:                Union[int, float],
            current_date:               Union[int, float],
            volatility:                 Union[int, float],
            riskfree_rate:              Union[int, float],
            dividend:                   Union[int, float],
            rebate:                     Union[int, float],
            year_base:                  int,
            obs_freq:                   Union[float, int] = 1,
            is_knock_in:                Union[int] = 0,
            barrier_type:               int = None,
            obs_type:                   int = ObsType.DISCRETE,
            rebate_type:                Union[int] = RebateType.PAE,
            pricing_method:             int = PricingMethod.AS
    ):
        """

        :param obs_type: 观察类型ObsType属性
        :param option_type: 期权类型OptionType属性
        :param rebate: rebate
        :param barrier_type: 障碍类BarrierType属性
        :param knock_type: 障碍敲击类型KnockType属性
        :param rebate_type: 支付时间RebateType属性
        :param pricing_method: 模型方法PricingMethod属性
        :param spot_price:  标的价格
        :param barrier_price: 障碍价格, 接收int、float、tuple、list类型。e.g.单障碍参数: 100, 双障碍参数: (80, 100)
        :param expiry_date: 到期日
        :param current_date: 当前日
        :param volatility: 波动率
        :param riskfree_rate: 无风险利率
        :param dividend: 分红率
        :param year_base: 年化天数
        :param obs_freq: 离散观测天数
        :param is_knock_in: 1为已敲入0为未敲入
        :return: 触碰期权定价引擎
        """

        assert is_knock_in in [0, 1], "param: is_knock_in should be either 0 or 1"

        param = {
            'knock_type': knock_type,
            'spot_price': spot_price,
            'expiry_date': expiry_date,
            'current_date': current_date,
            'volatility': volatility,
            'riskfree_rate': riskfree_rate,
            'dividend': dividend,
            'year_base': year_base,
            'is_knock_in': is_knock_in,
            'rebate': rebate,
            'rebate_type': rebate_type
        }

        # OneTouch
        if option_type == OptionType.ONE_TOUCH:
            assert barrier_type is not None, ValueError("barrier type(up or down) is required for one touch option")
            assert isinstance(barrier_price, (int, float)), TypeError(barrier_price, type(barrier_price))

            param['barrier_type'] = barrier_type
            param['barrier_price'] = barrier_price
            # OneTouchAs
            if pricing_method == PricingMethod.AS and obs_type == ObsType.CONTINUOUS:
                return OneTouch(param)

            # DiscreteOneTouchAs
            elif pricing_method == PricingMethod.AS and obs_type == ObsType.DISCRETE:
                param['obs_freq'] = obs_freq
                return DiscreteOneTouch(param)

        # DoubleOneTouch
        elif option_type == OptionType.DOUBLE_ONE_TOUCH:
            assert isinstance(barrier_price, (tuple, list)), TypeError(barrier_price, type(barrier_price))

            param['lower_barrier_price'], param['upper_barrier_price'] = min(barrier_price), max(barrier_price)
            # DoubleOneTouchAs
            if pricing_method == PricingMethod.AS and obs_type == ObsType.CONTINUOUS:
                return DoubleOneTouch(param)
