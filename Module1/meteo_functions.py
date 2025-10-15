import requests
import pandas as pd
import matplotlib.pyplot as plt
import time
import logging

logger = logging.getLogger(__name__)

logger.level = logging.INFO

def generate_api_urls(coordinates: dict[str, dict[str, float]], start: str, end: str, variables: list[str]):

    API_URL_TEMPLATE = "https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&daily={variable}"

    api_urls = {}

    variable_str = ",".join(variables)

    for city, coords in coordinates.items():
       lat = coords['latitude']
       lon = coords['longitude']

       api_url = API_URL_TEMPLATE.format(
          latitude = lat,
          longitude = lon,
          start_date = start,
          end_date = end,
          variable = variable_str
       )

       api_urls[f'{city}'] = api_url

    return api_urls



def get_data_meteo_api(city: str, apis: dict[str, str], max_tries: int=3, cooldown_time: int=15):
    
    url_name = apis[city]

    tries = 0
    while tries < max_tries:
        try:

            response = requests.get(url_name)

            if response.status_code == 200:
                print(f"API of {city} read successful! \n")
                
                data = response.json() 
                return data
            elif response.status_code == 429:
                print(f"Rate limit exceeded, waiting for {cooldown_time} seconds...")

                time.sleep(cooldown_time)
                tries += 1

            elif response.status_code == 404:
                print(f'Error: city {city} not found (404)')

            elif response.status_code == 500:
                print(f"Error: Server error (500). Retrying...")
                tries += 1
                time.sleep(2)  # Brief wait before retrying
                
            else:
                # Handle other status codes (e.g., 401 Unauthorized, 403 Forbidden)
                print(f"API request failed with status code {response.status_code}.")
                return None

        except requests.exceptions.RequestException as e:

            print(f"Request failed with error: {e}")
            tries += 1
            time.sleep(2)

def postproc_meteo_dataframe_daily(data, variables = None):
   
   dataframe = pd.DataFrame(data)
   dates = dataframe.loc['time', 'daily']

   daily_df = pd.DataFrame(index=pd.to_datetime(dates))

   if variables is None:
        variables = [col for col in dataframe.index if col != 'time']

   for var in variables:
      daily_df[var] = dataframe.loc[var, 'daily']

   daily_df.index.name = 'Date'

   return daily_df

def postproc_meteo_dataframe_monthly(data, variables = None):
   
   dataframe = pd.DataFrame(data)
   dates = dataframe.loc['time', 'daily']

   monthly_df = pd.DataFrame(index=pd.to_datetime(dates))

   if variables is None:
        variables = [col for col in dataframe.index if col != 'time']

   for var in variables:
      monthly_df[var] = dataframe.loc[var, 'daily']


   monthly_df = monthly_df.resample('ME').mean()
   monthly_df.index = monthly_df.index.strftime('%Y-%m')

   return monthly_df

def postproc_meteo_dataframe_yearly(data, variables = None):
   
   dataframe = pd.DataFrame(data)
   dates = dataframe.loc['time', 'daily']

   yearly_df = pd.DataFrame(index=pd.to_datetime(dates))

   if variables is None:
        variables = [col for col in dataframe.index if col != 'time']

   for var in variables:
      yearly_df[var] = dataframe.loc[var, 'daily']


   yearly_df = yearly_df.resample('YE').mean()
   yearly_df.index = yearly_df.index.strftime('%Y')

   return yearly_df

def plot_temperature(df, fig_title: str, temp_column='temperature_2m_mean'):
    plt.figure(figsize=(12,6))
    plt.plot(df.index, df[temp_column], linestyle='-', label='Temperature')
    
    plt.title(fig_title, fontsize=16)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Temperature (°C)', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()