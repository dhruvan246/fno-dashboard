# NSE F&O ticker list (as of April 2026, best-effort).
# Yahoo Finance suffix .NS

FNO_TICKERS = [
    # ---- Nifty 50 / mega caps ----
    "RELIANCE", "TCS", "HDFCBANK", "BHARTIARTL", "ICICIBANK", "INFY", "SBIN",
    "LICI", "HINDUNILVR", "ITC", "LT", "HCLTECH", "BAJFINANCE", "MARUTI",
    "SUNPHARMA", "KOTAKBANK", "AXISBANK", "M&M", "NTPC", "ULTRACEMCO",
    "TITAN", "ASIANPAINT", "BAJAJFINSV", "ONGC", "ADANIENT", "WIPRO",
    "POWERGRID", "JSWSTEEL", "TATAMOTORS", "ADANIPORTS", "COALINDIA",
    "NESTLEIND", "BAJAJ-AUTO", "TATASTEEL", "GRASIM", "TRENT", "HINDALCO",
    "BEL", "TECHM", "DRREDDY", "INDUSINDBK", "EICHERMOT", "CIPLA",
    "BPCL", "BRITANNIA", "DIVISLAB", "APOLLOHOSP", "HEROMOTOCO",
    "SBILIFE", "HDFCLIFE", "SHRIRAMFIN", "TATACONSUM",

    # ---- Banking / NBFC / Insurance ----
    "BANKBARODA", "PNB", "CANBK", "IDFCFIRSTB", "FEDERALBNK", "AUBANK",
    "BANDHANBNK", "RBLBANK", "INDIANB", "CHOLAFIN", "BAJAJHLDNG",
    "MUTHOOTFIN", "MANAPPURAM", "PEL", "LICHSGFIN", "PFC", "RECLTD",
    "IRFC", "SBICARD", "ICICIPRULI", "ICICIGI", "MAXHEALTH", "MFSL",
    "POLICYBZR", "PAYTM", "ANGELONE", "MOTILALOFS", "NAM-INDIA",
    "HDFCAMC", "CDSL", "BSE", "MCX", "IEX", "JIOFIN",

    # ---- IT / Tech ----
    "LTIM", "PERSISTENT", "COFORGE", "MPHASIS", "OFSS", "TATATECH",
    "KPITTECH", "TATAELXSI", "INTELLECT",

    # ---- Auto / Auto ancillary ----
    "TVSMOTOR", "ASHOKLEY", "BHARATFORG", "MOTHERSON",
    "BOSCHLTD", "BALKRISIND", "MRF", "APOLLOTYRE", "EXIDEIND", "ESCORTS",
    "TIINDIA", "SONACOMS", "UNOMINDA", "HYUNDAI",

    # ---- Capital goods / Defence / Engineering ----
    "SIEMENS", "ABB", "BHEL", "CUMMINSIND", "HAL", "BDL", "MAZDOCK",
    "COCHINSHIP", "GRSE", "SOLARINDS", "POLYCAB", "HAVELLS", "VOLTAS",
    "DIXON", "AMBER", "KAYNES", "CGPOWER", "THERMAX", "PIIND",

    # ---- Metals / Mining ----
    "VEDL", "JSWENERGY", "SAIL", "NMDC", "JINDALSTEL", "HINDCOPPER",
    "NATIONALUM", "JSL", "APLAPOLLO", "RATNAMANI",

    # ---- Oil & Gas / Energy ----
    "IOC", "GAIL", "HINDPETRO", "PETRONET", "GUJGASLTD", "IGL",
    "MGL", "OIL", "ATGL", "ADANIGREEN", "ADANIENSOL", "ADANIPOWER",
    "TATAPOWER", "TORNTPOWER", "NHPC", "SJVN",

    # ---- Cement ----
    "ACC", "AMBUJACEM", "DALBHARAT", "JKCEMENT", "RAMCOCEM", "SHREECEM",
    "INDIACEM",

    # ---- Pharma / Healthcare ----
    "LUPIN", "AUROPHARMA", "TORNTPHARM", "ZYDUSLIFE", "ALKEM",
    "BIOCON", "GLENMARK", "GRANULES", "IPCALAB", "LAURUSLABS",
    "ABBOTINDIA", "PFIZER", "GLAXO", "MANKIND", "FORTIS", "SYNGENE",

    # ---- FMCG / Consumer ----
    "GODREJCP", "DABUR", "MARICO", "COLPAL", "UBL", "VBL",
    "HATSUN", "JUBLFOOD", "DEVYANI", "SAPPHIRE",
    "WESTLIFE", "PGHH", "GILLETTE", "EMAMILTD", "RADICO",
    "PATANJALI", "VINATIORGA",

    # ---- Retail / Discretionary ----
    "DMART", "PAGEIND", "ABFRL", "VMART", "VISHAL",
    "JUBLPHARMA", "RELAXO", "BATAINDIA", "METROBRAND",

    # ---- Telecom / Media ----
    "IDEA", "INDUSTOWER", "ZEEL", "SUNTV", "NETWORK18", "PVRINOX",

    # ---- Real estate / Infra ----
    "DLF", "GODREJPROP", "OBEROIRLTY", "PRESTIGE", "LODHA", "PHOENIXLTD",
    "BRIGADE", "IRB", "GMRAIRPORT", "NCC", "KNRCON", "RVNL",
    "IRCON", "RAILTEL", "TITAGARH", "JWL",

    # ---- Chemicals / Specialty ----
    "UPL", "SRF", "AARTIIND", "DEEPAKNTR", "NAVINFLUOR", "TATACHEM",
    "ATUL", "CHAMBLFERT", "COROMANDEL", "GNFC", "PIDILITIND", "LINDEINDIA",
    "BAYERCROP", "SUMICHEM",

    # ---- Misc / Diversified ----
    "GODREJIND", "ABCAPITAL", "BERGEPAINT", "KANSAINER",
    "INDIGO", "CONCOR", "DELHIVERY",
    "POLYMED", "HONAUT", "ASTRAL", "SUPREMEIND", "FINOLEXIND",
    "NAUKRI", "ZOMATO", "NYKAA",
    "MCDOWELL-N", "BIKAJI", "DOMS",
]

# Dedupe while preserving order
seen = set()
FNO_TICKERS = [t for t in FNO_TICKERS if not (t in seen or seen.add(t))]

if __name__ == "__main__":
    print(f"Total tickers: {len(FNO_TICKERS)}")
