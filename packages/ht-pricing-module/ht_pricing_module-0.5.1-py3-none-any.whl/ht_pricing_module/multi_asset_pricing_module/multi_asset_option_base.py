from ..monte_carlo_engine import *
from ..api_and_utils import *
from ..finite_difference_engine import *


@lru_cache(maxsize=1024)
def mvn2d(a, b, rho):
    return multivariate_normal(mean=np.array([0, 0]), cov=np.array([[1, rho], [rho, 1]])).cdf(np.array([a, b]))


@lru_cache(maxsize=1024)
def mvn3d(a, b, c, rho12, rho13, rho23):
    return multivariate_normal_frozen(mean=np.array([0, 0, 0]), cov=np.array([[1, rho12, rho13], [rho12, 1, rho23], [rho13, rho23, 1]]), abseps=1e-8, releps=1e-8).cdf(np.array([a, b, c]))


@lru_cache(maxsize=1024)
def GuassQuadAbscissaWeight(n):
    a = np.sqrt((np.array(range(n - 1)) + 1) / 2)
    L, V = np.linalg.eig(np.diag(a, 1) + np.diag(a, -1))

    V = V[:, np.argsort(L)].T
    L = np.sort(L)

    w = np.sqrt(np.pi) * V[:, 0] * V[:, 0]
    return L, w


def BlackModelVector(cp, f, k, T, r, v):
    d1 = (np.log(f / k) + v * v / 2 * T) / (v * np.sqrt(T))
    return cp * np.exp(-r * T) * (f * norm.cdf(cp * d1) - k * norm.cdf(cp * (d1 - v * np.sqrt(T))))


def BlackScholesModelVector(cp, s, k, T, r, q, v):
    d1 = (np.log(s / k) + (r - q + v * v / 2) * T) / (v * np.sqrt(T))
    return cp * (s * np.exp(-q * T) * norm.cdf(cp * d1) - k * np.exp(-r * T) * norm.cdf(cp * (d1 - v * np.sqrt(T))))


class MultiAssetOptionBase(ParamsBase):

    def __init__(self, param):
        super().__init__(param)

    def __calculate_present_value__(self) -> float:
        raise NotImplementedError()

    @lru_cache(maxsize=10)
    def present_value(self) -> float:
        return self.__calculate_present_value__()

    @lru_cache(maxsize=10)
    def delta(self, leg: int, step: float = 0.001) -> float:
        spot_price = f'spot_price{leg}'
        time_to_expiry = (self.param.expiry_date - self.param.current_date) / self.param.year_base
        if time_to_expiry <= 0:
            return 0.0

        if hasattr(self.param, spot_price):
            spot_up = getattr(self.param, spot_price) * (1 + step)
            spot_down = getattr(self.param, spot_price) * (1 - step)
            pricer_up = deepcopy(self)
            setattr(pricer_up.param, spot_price, spot_up)
            pricer_down = deepcopy(self)
            setattr(pricer_down.param, spot_price, spot_down)
            return (pricer_up.present_value() - pricer_down.present_value()) / (spot_up - spot_down)
        return 0.0

    @lru_cache(maxsize=10)
    def gamma(self, leg: int, step: float = 0.001) -> float:
        spot_price = f'spot_price{leg}'
        if hasattr(self.param, spot_price):
            spot_up = getattr(self.param, spot_price) * (1 + step)
            spot_down = getattr(self.param, spot_price) * (1 - step)
            pricer_up = deepcopy(self)
            setattr(pricer_up.param, spot_price, spot_up)
            pricer_down = deepcopy(self)
            setattr(pricer_down.param, spot_price, spot_down)
            return (pricer_up.present_value() + pricer_down.present_value() - 2 * self.present_value()) / pow((spot_up - spot_down) / 2, 2) 
        return 0.0

    @lru_cache(maxsize=10)
    def cross_gamma(self, step: float = 0.001) -> float:
        if hasattr(self.param, 'expiry_date') and hasattr(self.param, 'current_date') and hasattr(self.param, 'spot_price1') and hasattr(self.param, 'spot_price2'):
            if self.param.expiry_date - self.param.current_date <= 0:
                return 0.0
            else:
                spot1_up, spot1_down = self.param.spot_price1 * (1 + step), self.param.spot_price1 * (1 - step)
                spot2_up, spot2_down = self.param.spot_price2 * (1 + step), self.param.spot_price2 * (1 - step)
                pricer_1up_2up, pricer_1down_2down, pricer_1up_2down, pricer_1down_2up = deepcopy(self), deepcopy(self), deepcopy(self), deepcopy(self)

                pricer_1up_2up.param.spot_price1, pricer_1up_2up.param.spot_price2 = spot1_up, spot2_up
                pricer_1down_2down.param.spot_price1, pricer_1down_2down.param.spot_price2 = spot1_down, spot2_down
                pricer_1up_2down.param.spot_price1, pricer_1up_2down.param.spot_price2 = spot1_up, spot2_down
                pricer_1down_2up.param.spot_price1, pricer_1down_2up.param.spot_price2 = spot1_down, spot2_up

                return (pricer_1up_2up.present_value() - pricer_1up_2down.present_value() - pricer_1down_2up.present_value() + pricer_1down_2down.present_value()) / (spot1_up - spot1_down) / (spot2_up - spot2_down)
        return 0.0

    @lru_cache(maxsize=10)
    def vega(self, leg: int, step: float = 0.01) -> float:
        volatility = f'volatility{leg}'
        if hasattr(self.param, volatility):
            vol_up = getattr(self.param, volatility) + step
            pricer_up = deepcopy(self)
            setattr(pricer_up.param, volatility, vol_up)
            return pricer_up.present_value() - self.present_value()
        return 0.0

    @lru_cache(maxsize=10)
    def theta(self, step: float = 1) -> float:
        if hasattr(self.param, 'current_date'):
            current_up = self.param.current_date + step
            pricer_up = deepcopy(self)
            pricer_up.param.current_date = current_up
            return pricer_up.present_value() - self.present_value()
        return 0.0

    @lru_cache(maxsize=10)
    def rho(self, step: float = 0.0001) -> float:
        if hasattr(self.param, 'riskfree_rate'):
            current_up = self.param.riskfree_rate + step
            pricer_up = deepcopy(self)
            pricer_up.param.riskfree_rate = current_up
            return pricer_up.present_value() - self.present_value()
        return 0.0

    @lru_cache(maxsize=10)
    def dpvdcorr(self, leg: int = None, step: float = 0.01) -> float:
        correlation = 'correlation' if leg is None else f'correlation{leg}'
        if hasattr(self.param, correlation):
            corr_up = getattr(self.param, correlation) + step
            pricer_up = deepcopy(self)
            setattr(pricer_up.param, correlation, corr_up)
            return pricer_up.present_value() - self.present_value()
        return 0.0

    @lru_cache(maxsize=10)
    def ddeltadt(self, leg: int, time_step: float = 1, price_step: float = 0.001):
        if hasattr(self.param, 'current_date'):
            current_up = self.param.current_date + time_step
            pricer_up = deepcopy(self)
            pricer_up.param.current_date = current_up
            return pricer_up.delta(leg=leg, step=price_step) - self.delta(leg=leg, step=price_step)
        return 0.0

    @lru_cache(maxsize=10)
    def ddeltadv(self, leg: int, vol_step: float = 0.01, price_step: float = 0.001):
        volatility = f'volatility{leg}'
        if hasattr(self.param, volatility):
            vol_up = getattr(self.param, volatility) + vol_step
            pricer_up = deepcopy(self)
            setattr(pricer_up.param, volatility, vol_up)
            return pricer_up.delta(leg=leg, step=price_step) - self.delta(leg=leg, step=price_step)
        return 0.0
