import cdsapi

c = cdsapi.Client()

months = [f"{m:02d}" for m in range(1, 13)]
days = [f"{d:02d}" for d in range(1, 32)]
times = [f"{h:02d}:00" for h in range(0, 24)]
years = [str(y) for y in range(2000, 2024)]

def download_data_from_cds(var):
    import os
    pwd = os.getcwd()
    for year in years:
        print(f"Data for New Zealand on {year} starts downloading to {var}_{year}.nc.")
        result= c.retrieve(
            "reanalysis-era5-single-levels",
            {
                "product_type": ["reanalysis"],
                "data_format": "netcdf",
                "download_format": "unarchived",
                "variable": [var],
                "year": year,
                "month": months,
                "day": days,
                "time": times,
                "area": [-30.0, 166.5, -50, 179.0],
            },
            # f"./downloadData/{var}_{year}.nc")
 
            f"{pwd}/downloadData/{var}_{year}.nc")
        # result.download()
        print(f"Data for New Zealand on {year} has been saved to {var}_{year}.nc.")

if __name__ == "__main__":
    download_data_from_cds("total_precipitation")
    # download_data_from_cds("snowfall")
