from meteo_functions import *

def main():
 
 ## --- VARIABLES DEFINITION --- ##
 # ------------------------------ #

 COORDINATES = {
    "Madrid": {"latitude": 40.416775, "longitude": -3.703790},
    "London": {"latitude": 51.507351, "longitude": -0.127758},
    "Rio": {"latitude": -22.906847, "longitude": -43.172896},
 }
 VARIABLES = ["temperature_2m_mean", "precipitation_sum", "wind_speed_10m_max"]

 START_DATE = "2010-01-01"
 END_DATE = "2020-12-31"

 ## --- DATA ACQUISITION --- ##
 # -------------------------- #
 df_dict_daily = {}
 df_dict_monthly = {}
 for city in COORDINATES.keys():

    data = get_data_meteo_api(city, generate_api_urls(COORDINATES, START_DATE, END_DATE, VARIABLES))
    df_dict_daily[city] = postproc_meteo_dataframe_daily(data)
    df_dict_monthly[city] = postproc_meteo_dataframe_monthly(data)

 df_madrid_daily = df_dict_daily['Madrid']
 df_madrid_monthly = df_dict_monthly['Madrid']
 print(df_madrid_monthly)
 plot_temperature(df_madrid_daily, 'Daily evolution of temperatures')
 plot_temperature(df_madrid_monthly, 'Monthly evolution of temperatures')

   
   
if __name__ == "__main__":
 main()





