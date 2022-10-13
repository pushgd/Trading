export interface strategy {
    index: number;
    name: string;
    inUse: boolean;
    parameters: parameter[]
}

export interface parameter {
    index: number;
    name: string;
    type: string;
    value: any;
}

export interface symbolInfo {
    index: number;
    name: string;
    tradingSymbol: string;
    exchangeCode: string;
    currentPrice: number;

}

export interface trade {
    'status': number;
    'entryPrice': number;
    'entryTime': string;
    'exitPrice': number;
    'exitTime': string;
    'buyTriggerCall': number;
    'buyTriggerPut': number;
    'stopLoss': number;
    'takeProfit': number;
    'ID': number;
    'strategyName': string;
    'gain': number;
    "startDate": string;
    "buyDate": string;
    "exitDate": string

}