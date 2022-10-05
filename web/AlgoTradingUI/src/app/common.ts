export interface strategy {
    index: number;
    name: string;
    inUse: boolean;
}

export interface parameter {
    pos: number;
    name: string;
    type: string;
    value: any;
}