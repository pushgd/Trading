import Common
import Constant
from strategy.GannAnalysis import GannAnalysis


def init():
    Common.strategyDict[Constant.STRATEGY_GANN_ANALYSIS] = GannAnalysis()
    Common.strategyDict[Constant.STRATEGY_GANN_ANALYSIS].update()


class StrategyBaseClass:
    def update(self):
        print("Update base class")
