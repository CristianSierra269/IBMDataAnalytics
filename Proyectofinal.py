import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects   as go
from plotly.subplots import make_subplots
import warnings

warnings.filterwarnings("ignore",category=FutureWarning)

## Extract information from yfinance and convert to DataFrame

ticker_tesla = yf.Ticker("TSLA")
Ticker = ticker_tesla.history(period="max")
tesla_data = pd.DataFrame(Ticker)
tesla_data.reset_index(inplace= True)
print("Con reset_index Tesla")
print(tesla_data.head())

## Extract information from an URL through the request
html_data_TSLA = requests.get("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm").text
bs_html_data_TSLA = BeautifulSoup (html_data_TSLA, 'html5lib')

tesla_revenue = pd.DataFrame(columns=["Date","Revenue"])

## Whit the informatio extracted using BS, we must to create a DataFrame for the Revenue
for row in bs_html_data_TSLA.find('tbody').find_all('tr'):
    cols = row.find_all('td')
    date = cols[0].text
    revenue = cols[1].text
    
    tesla_revenue = tesla_revenue._append({"Date":date, "Revenue": revenue}, ignore_index = True)
    
tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace('[$,]', '', regex=True)
tesla_revenue["Revenue"] = pd.to_numeric(tesla_revenue["Revenue"], errors='coerce')
tesla_revenue.dropna(inplace=True)
print(" ")
print("Dataframe Tesla with BeautifulSoup: ") 
print(" ")
print(tesla_revenue.tail(5))
print(" ")

## Make DataFrame using Pandas
# read_html_pandas_date = pd.read_html(str(bs_html_data))
# tesla_df = read_html_pandas_date[0]
# tesla_df.reset_index(inplace=True)
# print("Dataframe with Pandas:")
# print(" ")
# print(tesla_df.head())


# Now we have to extrac the information about stock for GameStop using yfinance. We havce to create a DataFrame
ticker_GameStop = yf.Ticker("GME")
ticker_GameStop = ticker_GameStop.history(period="max")
gme_data = pd.DataFrame(ticker_GameStop)
gme_data.reset_index(inplace=True)
print(f"Dataframe  GameStop with reset_index:\n \n {gme_data.head()}")

#Also, trought BeautifulSoup we bring the information need 
html_data_GME = requests.get("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html").text
bs_html_data_GME = BeautifulSoup(html_data_GME, 'html5lib')

gme_revenue = pd.DataFrame(columns=["Date","Revenue"])

for row in bs_html_data_GME.find('tbody').find_all('tr'):
    cols = row.find_all('td')
    date = cols[0].text
    revenue = cols[1].text
   
    gme_revenue = gme_revenue._append({"Date":date, "Revenue": revenue}, ignore_index = True)
    
gme_revenue["Revenue"] = gme_revenue["Revenue"].str.replace('[$,]', '', regex=True)
gme_revenue["Revenue"] = pd.to_numeric(gme_revenue["Revenue"], errors='coerce')
gme_revenue.dropna(inplace=True)
print(" ")
print("Dataframe GameStop with BeautifulSoup: ") 
print(" ")
print(gme_revenue.tail(5))
print(" ")

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
     
     #Filtrar datos por fecha
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
     
     #Añadir trazos al gráfico
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, format='mixed'), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, format='mixed'), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
     
     #Actualizar etiquetas de ejes
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
     
     #Actualizar diseño del gráfico
    fig.update_layout(showlegend=False,
                        height=900,
                        title=stock,
                        xaxis_rangeslider_visible=True)
    #mostrar
    fig.show()
    
make_graph(tesla_data, tesla_revenue, 'Tesla')
make_graph(gme_data, gme_revenue, 'GameStop')
    


