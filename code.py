import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import yfinance as yf
from io import StringIO

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table", {"id": "constituents"})
df_sp500 = pd.read_html(StringIO(str(table)))[0]
df_sp500.head()

df_sp500['GICS Sector'].unique()

big_tech = df_sp500[df_sp500['Symbol'].isin(["AAPL", "GOOG", "AMZN"])]
big_tech

def extract_stock_data(symbol, start, end):
    ticker = yf.Ticker(symbol)
    df = ticker.history(start = start, end = end)
    df.reset_index(inplace=True)
    return df

tickers = ["SPY", "GOOG", "AAPL", "AMZN", "XLP", "XLU", "XLV"]

start_date = "2014-01-01"
end_date = "2025-01-01"


aapl_df = extract_stock_data("AAPL", start_date, end_date)
amzn_df = extract_stock_data("AMZN", start_date, end_date)
goog_df = extract_stock_data("GOOG", start_date, end_date)
spy_df = extract_stock_data("SPY", start_date, end_date)
xlp_df = extract_stock_data("XLP", start_date, end_date)
xlv_df = extract_stock_data("XLV", start_date, end_date)
xlu_df = extract_stock_data("XLU", start_date, end_date)

def daily_returns(df):
    df = df.copy()
    df["Daily Return"] = df["Close"].pct_change()
    return df

aapl_df = daily_returns(aapl_df)
amzn_df = daily_returns(amzn_df)
goog_df = daily_returns(goog_df)
spy_df = daily_returns(spy_df)
xlp_df = daily_returns(xlp_df)
xlv_df = daily_returns(xlv_df)
xlu_df = daily_returns(xlu_df)

def cumulative_returns(df):
    df = df.copy()
    df["Cumulative Return"] = (1 + df["Daily Return"]).cumprod()
    return df
    
aapl_df = cumulative_returns(aapl_df)
amzn_df = cumulative_returns(amzn_df)
goog_df = cumulative_returns(goog_df)
spy_df = cumulative_returns(spy_df)
xlp_df = cumulative_returns(xlp_df)
xlv_df = cumulative_returns(xlv_df)
xlu_df = cumulative_returns(xlu_df)    

aapl_df.to_csv('aapl.csv')
amzn_df.to_csv('amzn.csv')
goog_df.to_csv('goog.csv')
spy_df.to_csv('spy.csv')
xlp_df.to_csv('xlp.csv')
xlv_df.to_csv('xlv.csv')
xlu_df.to_csv('xlu.csv')


fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(16, 12))

axes[0][0].plot(spy_df["Date"], spy_df["Close"])
axes[0][0].set_title("S&P 500 Price History")
axes[0][0].set_xlabel("Year")
axes[0][0].set_ylabel("Closing Price")
axes[0][0].grid()

axes[0][1].plot(goog_df["Date"], goog_df["Close"])
axes[0][1].set_title("Google Price History")
axes[0][1].set_xlabel("Year")
axes[0][1].set_ylabel("Closing Price")
axes[0][1].grid()

axes[1][0].plot(aapl_df["Date"], aapl_df["Close"])
axes[1][0].set_title("Apple Price History")
axes[1][0].set_xlabel("Year")
axes[1][0].set_ylabel("Closing Price")
axes[1][0].grid()

axes[1][1].plot(amzn_df["Date"], amzn_df["Close"])
axes[1][1].set_title("Amazon Price History")
axes[1][1].set_xlabel("Year")
axes[1][1].set_ylabel("Closing Price")
axes[1][1].grid()

plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))

plt.plot(spy_df["Date"], spy_df["Cumulative Return"], label="SPY")
plt.plot(goog_df["Date"], goog_df["Cumulative Return"], label="GOOG")
plt.plot(aapl_df["Date"], aapl_df["Cumulative Return"], label="AAPL")
plt.plot(amzn_df["Date"], amzn_df["Cumulative Return"], label="AMZN")

plt.title("Cumulative Returns")
plt.xlabel("Year")
plt.ylabel("Cumulative Growth")
plt.legend()
plt.grid()
plt.show()


spy_2022 = spy_df[spy_df["Date"].dt.year == 2022]["Close"].tolist()
goog_2022 = goog_df[goog_df["Date"].dt.year == 2022]["Close"].tolist()
aapl_2022 = aapl_df[aapl_df["Date"].dt.year == 2022]["Close"].tolist()
amzn_2022 = amzn_df[amzn_df["Date"].dt.year == 2022]["Close"].tolist()

def annual_return_2022(prices):
    start_price = prices[0]
    end_price = prices[-1]
    return (end_price - start_price) / start_price

spy_return_2022 = annual_return_2022(spy_2022)
goog_return_2022 = annual_return_2022(goog_2022)
aapl_return_2022 = annual_return_2022(aapl_2022)
amzn_return_2022 = annual_return_2022(amzn_2022)

print("SPY 2022 return:", f"{spy_return_2022*100:.2f}%")
print("GOOG 2022 return:", f"{goog_return_2022*100:.2f}%")
print("AAPL 2022 return:", f"{aapl_return_2022*100:.2f}%")
print("AMZN 2022 return:", f"{amzn_return_2022*100:.2f}%")

def max_drawdown(prices):
    running_max = prices[0]
    max_drop_val = 0
    max_drop_pct = 0
    
    for price in prices:
        if price > running_max:
            running_max = price
            continue
        
        drop_val = running_max - price
        drop_pct = drop_val / running_max
        
        if drop_val > max_drop_val:
            max_drop_val = drop_val
            max_drop_pct = drop_pct
    
    return max_drop_val, max_drop_pct


spy_drop, spy_drop_pct = max_drop(spy_2022)
print("SPY max drop:", spy_drop)
print("SPY max drawdown:", f"{spy_drop_pct*100:.2f}%")

goog_drop, goog_drop_pct = max_drop(goog_2022)
print("GOOG max drop:", goog_drop)
print("GOOG max drawdown:", f"{goog_drop_pct*100:.2f}%")

aapl_drop, aapl_drop_pct = max_drop(aapl_2022)
print("AAPL max drop:", aapl_drop)
print("AAPL max drawdown:", f"{aapl_drop_pct*100:.2f}%")

amzn_drop, amzn_drop_pct = max_drop(amzn_2022)
print("AMZN max drop:", amzn_drop)
print("AMZN max drawdown:", f"{amzn_drop_pct*100:.2f}%")

xlp_return_2022 = annual_return_2022(xlp_2022)
xlu_return_2022 = annual_return_2022(xlu_2022)
xlv_return_2022 = annual_return_2022(xlv_2022)

print("XLP 2022 return:", f"{xlp_return_2022*100:.2f}%")
print("XLU 2022 return:", f"{xlu_return_2022*100:.2f}%")
print("XLV 2022 return:", f"{xlv_return_2022*100:.2f}%")


plt.figure(figsize=(10, 6))

plt.plot(xlp_df["Date"], xlp_df["Cumulative Return"], label="XLP (Staples)")
plt.plot(xlu_df["Date"], xlu_df["Cumulative Return"], label="XLU (Utilities)")
plt.plot(xlv_df["Date"], xlv_df["Cumulative Return"], label="XLV (Health Care)")
plt.plot(spy_df["Date"], spy_df["Cumulative Return"], label="SPY")

plt.title("Defensive Sector Cumulative Returns vs SPY")
plt.xlabel("Year")
plt.ylabel("Cumulative Growth")
plt.legend()
plt.grid()
plt.show()
