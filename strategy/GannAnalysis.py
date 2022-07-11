import strategy.Strategy

s = strategy.Strategy.StrategyBaseClass()
print(s)


class GannAnalysis(strategy.technicalStrategy.StrategyBaseClass):
    def __init__(self):
        print("Creating Gann Strategy")
