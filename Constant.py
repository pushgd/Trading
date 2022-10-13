# tick date
import logging
import datetime

EXPIRY_DATES =[
    datetime.date(2022,1,29),
    datetime.date(2022,1,29),
    datetime.date(2022,2,15),
    datetime.date(2022,3,29),
    datetime.date(2022,4,29),
    datetime.date(2022,5,29),
    datetime.date(2022,6,29),
    datetime.date(2022,7,29),
    datetime.date(2022,8,29),
    datetime.date(2022,9,29),
    datetime.date(2022,10,27),
    datetime.date(2022,11,24),
    datetime.date(2022,12,29)
]

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



PARAMETER_TICK_DATA = 'tickData'
PARAMETER_Quantity = 'Quantity'

STRATEGY_MA_CROSSOVER_UP = "MACrossoverup"
STRATEGY_PARAMETER_MA_CROSSOVER_UP = [
    {"name": PARAMETER_Quantity,
    "type":"number"}]
STRATEGY_GANN_ANALYSIS = "GannAnalysis"
STRATEGY_PARAMETER_GANN_ANALYSIS = [
    {"name": "Quantity",
    "type":"number"}]



# indicator parameters
MOVING_AVERAGE_SHORT_WINDOW = 21
MOVING_AVERAGE_MEDIUM_WINDOW = 51
MOVING_AVERAGE_LONG_WINDOW = 200
EXPONENTIAL_AVERAGE_WINDOW = 20

RSI_WINDOW = 9


# trade parameters
RISK_REWARD_RATIO = 2
STRATEGY_CHECK_DELAY = 5
CANDLE_CRATION_TIME = 3*60  # in sec

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

KEY_TICK_DATA = 'tickData'

TRADE_LOOKING_FOR_ENTRY = 0
TRADE_NOT_STARTED = 1
TRADE_ENTERED = 2
TRADE_COMPLETED = 3
TRADE_FORCE_EXIT = 4
TRADE_TIMED_OUT = 5
TRADE_LOOKING_FOR_EXIT = 6

TRADE_TYPE_PUT = "PE"
TRADE_TYPE_CALL = "CE"

TRADE_TIMEOUT_TIME = 100 * 60 * 60

KEY_GANN_REFERENCE = 'GANN_REFERENCE'

KEY_CURRENT_PRICE = 'CURRENT_PRICE'
KEY_SYMBOL = 'CURRENT_SYMBOL'


LOCAL_CANDLE_FREQUENCY = 999999999999999

EVENT_CANDLE_CREATED = 0
EVENT_TRADE_COMPLETED = 1
EVENT_TRADE_TIMEOUT = 2

EXIT_TIME = datetime.datetime.now().replace(hour=14,minute=45)
START_TIME = datetime.time(hour=9, minute=30)

LOGGING_LEVEL_VERBOSE = 1
LOGGING_LEVEL_NEW_DATA_RECEIVED = 2
LOGGING_LEVEL_ACTION = 3

LOGGER = logging.getLogger("AlgoTrade")


def verbose(msg, *args, **kwargs):
    if LOGGER.isEnabledFor(LOGGING_LEVEL_VERBOSE):
        LOGGER.log(LOGGING_LEVEL_VERBOSE, msg)


def dataReceived(msg, *args, **kwargs):
    if LOGGER.isEnabledFor(LOGGING_LEVEL_NEW_DATA_RECEIVED):
        LOGGER.log(LOGGING_LEVEL_NEW_DATA_RECEIVED, msg)


def action(msg, *args, **kwargs):
    if LOGGER.isEnabledFor(LOGGING_LEVEL_ACTION):
        LOGGER.log(LOGGING_LEVEL_ACTION, msg)


logging.addLevelName(LOGGING_LEVEL_VERBOSE, "VERBOSE")
LOGGER.verbose = verbose


logging.addLevelName(LOGGING_LEVEL_NEW_DATA_RECEIVED, "DATA_RECEIVED")
LOGGER.dataReceived = dataReceived

logging.addLevelName(LOGGING_LEVEL_ACTION, "ACTION")
LOGGER.action = action


f = logging.Formatter(fmt='%(asctime)s,%(levelname)s,%(message)s')
fileName = "logs/Log"+str(datetime.datetime.now().day)+str(
    datetime.datetime.now().month)+str(datetime.datetime.now().year)+".csv"

fh = logging.FileHandler(fileName)
fh.setLevel(LOGGING_LEVEL_VERBOSE)
fh.setFormatter(f)
LOGGER.addHandler(fh)
LOGGER.setLevel(LOGGING_LEVEL_VERBOSE)

