import os

import dotenv
import xarray as xr
from tqdm import tqdm
from joblib import Parallel, delayed

from timer import Timer
from utils import get_nc_link

dotenv.load_dotenv()



CSV_PATH = os.getenv("CSV_PATH")
nc_link = get_nc_link()
os.system(f"wget -P {CSV_PATH} {nc_link}")



#list in ./downloadData
nc_filepaths = [i for i in os.listdir(CSV_PATH) if i.endswith(".nc")]
nc_filepaths = [os.path.join(CSV_PATH, i) for i in nc_filepaths]

cols_renamed = {
    "tp": "total_precipitation",
}

def latlon_to_location_id(lats, lons, dlat=0.25, dlon=0.25, min_lat=-30, min_lon=166.5):
    #NZ specifc; 
    n_lats = 79 #WARNING: hardcoded
    n_lons = 51
    lat_indices = ((-lats + min_lat) / dlat).astype(int) # reverse latitudes order
    lon_indices = ((lons - min_lon) / dlon).astype(int)
    return lat_indices * n_lons + lon_indices + 1

def weather_dataframe(n):
    with Timer(f"Loading data for hour {n}"):
        ds = xr.open_mfdataset(nc_filepaths) #TODO: to benchmark against duckdb later
        df = ds.isel(valid_time=n).to_dataframe().reset_index()

        # df.drop(columns=["utc_date"], inplace=True)
        df.rename(columns=cols_renamed, inplace=True)

        df["total_precipitation"] *= 1000  # m to mm

        # Convert latitude from [0, 360) degrees East to [-180, 180) degrees East.
        df.rename(columns={"longitude": "longitude_east",
                           "valid_time": "time"
                           }, inplace=True)
        df["longitude"] = df["longitude_east"].apply(lambda x: x - 360 if x > 180 else x)
        df.drop(columns=["longitude_east"], inplace=True)

        df["location_id"] = latlon_to_location_id(df.latitude, df.longitude)

        df = df[[
            "time",
            "location_id",
            "latitude",
            "longitude",
            "total_precipitation",
        ]]
    
    return df

def write_csv(df, filepath):
    with Timer(f"Saving {filepath}", n=df.shape[0]):
        df.to_csv(
            filepath,
            index=False,
            header=False,
            date_format="%Y-%m-%d %H:%M:%S"
        )
    return filepath

