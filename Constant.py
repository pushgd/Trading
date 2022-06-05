# tick date
from ast import Constant


DATE = 0
OPEN = 1
HIGH = 2
LOW = 3
CLOSE = 4
BODY = 5
LENGTH = 6
TYPE = 7
STATUS = 8
DOJI_RATIO = 0.25
MEAN_RATIO = 0.05

# candle type
BULL = 'Bull'
BEAR = 'Bear'

# pattern Name
DOJI = "Doji"
HARAMI = "HARAMI"   # updward bullish engulfing 2nd bull
ENGULFING = "ENGULFING"  # updward bullish engulfing 2nd bull
DARK_CLOUD = "DARK CLOUD"  # downward
PIERCING = "PIERCING"  # upward
INVERTED_PIERCING = "INVERTED PIERCING"  # upward
EVENING_STAR = "EVENING STAR"  # downward
MORNING_STAR = "MORNING STAR"  # upward


STRATEGY_MA_CROSSOVER_UP = "MACrossoverup"

# indicator parameters
MOVING_AVERAGE_SHORT_WINDOW = 20
MOVING_AVERAGE_MEDIUM_WINDOW = 50
MOVING_AVERAGE_LONG_WINDOW = 200
EXPONENTIAL_AVERAGE_WINDOW = 20

RSI_WINDOW = 14


# trade parameters
RISK_REWARD_RATIO = 2
STRATEGY_CHECK_DELAY = 5
CANDLE_CRATION_TIME = 5*60  # in sec

KEY_DATE = 'date'
KEY_HIGH = 'high'
KEY_LOW = 'low'
KEY_OPEN = 'open'
KEY_CLOSE = 'close'
KEY_LOSS = 'loss'
KEY_GAIN = 'gain'
KEY_BODY_LENGTH = 'bodyLength'
KEY_LENGTH = 'length'
KEY_TYPE = 'type'
KEY_MEAN = 'mean'
KEY_BODY_MEAN = 'bodyMean'
KEY_AVERAGE_LOSS = 'lossAverage'
KEY_AVERAGE_GAIN = 'gainAverage'

# indicators key
KEY_VOLUME = 'volume'
KEY_RSI = 'RSI'
KEY_RS = 'RS'
KEY_MOVING_AVERAGE_SHORT_OPEN = 'movingAverageShortOpen'
KEY_MOVING_AVERAGE_SHORT_CLOSE = 'movingAverageShortClose'
KEY_MOVING_AVERAGE_SHORT_HIGH = 'movingAverageShortHigh'
KEY_MOVING_AVERAGE_SHORT_LOW = 'movingAverageShortLow'

KEY_MOVING_AVERAGE_MEDUIM_OPEN = 'movingAverageMediumOpen'
KEY_MOVING_AVERAGE_MEDUIM_CLOSE = 'movingAverageMediumClose'
KEY_MOVING_AVERAGE_MEDUIM_HIGH = 'movingAverageMediumHigh'
KEY_MOVING_AVERAGE_MEDUIM_LOW = 'movingAverageMediumLow'

KEY_MOVING_AVERAGE_LONG_OPEN = 'movingAverageLongOpen'
KEY_MOVING_AVERAGE_LONG_CLOSE = 'movingAverageLongClose'
KEY_MOVING_AVERAGE_LONG_HIGH = 'movingAverageLongHigh'
KEY_MOVING_AVERAGE_LONG_LOW = 'movingAverageLongLow'

KEY_EXPONENTIAL_AVERAGE_OPEN = 'expAverageOpen'
KEY_EXPONENTIAL_AVERAGE_CLOSE = 'expAverageClose'
KEY_EXPONENTIAL_AVERAGE_HIGH = 'expAverageHigh'
KEY_EXPONENTIAL_AVERAGE_LOW = 'expAverageLow'


KEY_CUMMULATIVE_VOLUME = 'cumulativeVolume'
KEY_CUMMULATIVE_PV = 'cumulativePV'
KEY_CUMMULATIVE_VWAP = 'VWAP'


KEY_PATTERN = 'pattern'
KEY_STRATEGY = 'Strategy'

TRADE_NOT_STARTED = 1
TRADE_ENTRY = 2
TRADE_COMPLETED = 3