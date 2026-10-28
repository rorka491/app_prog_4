from enum import StrEnum


class Airport(StrEnum):
    OVB = "OVB"
    SVO = "SVO"
    LED = "LED" 
    KZN = "KZN"
    VKO = "VKO"
    DME = "DME"
    SVX = "SVX"
    KRR = "KRR"
    ROV = "ROV"
    UFA = "UFA"
    GOJ = "GOJ"
    CEK = "CEK"
    KJA = "KJA"
    OMS = "OMS"
    IKT = "IKT"
    VVO = "VVO"
    KGD = "KGD"
    MRV = "MRV"
    ASF = "ASF"
    PEE = "PEE"
    UUS = "UUS"
    MMK = "MMK"
    ARH = "ARH"
    NAL = "NAL"
    GRV = "GRV"
    NBC = "NBC"
    ULY = "ULY"
    TJM = "TJM"
    PKC = "PKC"


class Carriers(StrEnum):
    S7 = "S7 Airlines"
    URAL = "Ural Airlines"
    AEROFLOT = "Aeroflot"
    
    


class Supplier(StrEnum):
    supplier1 = "http://localhost:8001/api/v1/flights"
    supplier2 = "http://localhost:8002/api/v1/flights"
    supplier3 = "http://localhost:8003/api/v1/flights"

