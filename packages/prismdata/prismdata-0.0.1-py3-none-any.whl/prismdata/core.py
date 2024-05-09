from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
from pathlib import Path
import requests
import rioxarray
from typing import Optional
import zipfile

# create a function to download prism data
def download_prism(start: str = None, end: Optional[str] = None, variable: str = None,
                   freq: Optional[str] = "daily", download_dir: Optional[str] = None,
                   unzip: Optional[bool] = True, remove_zip: Optional[bool] = True) -> None:
    """
    Downloads PRISM data within a specified time range and frequency.

    Args:
        start (str): The start date of the data range in 'YYYYMMDD' | 'YYYYMM' | 'YYYY' format. Defaults to None.  

        end (str, optional): The end date of the data range in 'YYYYMMDD' | 'YYYYMM' | 'YYYY' format. Defaults to None.  

        variable (str): The PRISM variable to be downloaded. Options are: "ppt", "tmin", "tmax", "tmean", "tdmean", "vpdmin" and "vpdmax". 

        freq (str, optional): The frequency of the data to be downloaded. Options: daily, monthly and annual. Defaults to "daily".  

        download_dir (str, optional): The directory where the downloaded data will be saved. Defaults to "data" under current directory.  

        unzip (bool, optional): If True, the downloaded zip files will be unzipped. Defaults to True.  

        remove_zip (bool, optional): If True, the downloaded zip files will be removed. Defaults to True.  

    """
    
    # Download will occur only once
    onetime_download = False

    # Validate the variable input
    valid_variables = ["ppt", "tmin", "tmax", "tmean", "tdmean", "vpdmin", "vpdmax"]
    if variable not in valid_variables:
        raise ValueError(f"Invalid variable: {variable}. Valid options are: {', '.join(valid_variables)}")
    
    # Validate the frequency input
    valid_frequencies = ["daily", "monthly", "annual"]
    if freq not in valid_frequencies:
        raise ValueError(f"Invalid frequency: {freq}. Valid options are: {', '.join(valid_frequencies)}")   
    

    # Validate: each frequency type check the appropriate start and end arguments are provided 
    if freq == "daily":
        if start is None:
            raise ValueError("For daily data, start date must be provided.")
        try:
            start_date = datetime.strptime(start, "%Y%m%d")
            if start_date < datetime(1981, 1, 1):
                raise ValueError("Invalid start date range for daily data.")
        except ValueError as e:
            raise ValueError("Invalid date format")
        
        if end is None:
            onetime_download = True
        else:
            try:
                end_date = datetime.strptime(end, "%Y%m%d")
                if end_date > datetime.now() - timedelta(days=1):
                    raise ValueError("Invalid end date range for daily data.")
            except ValueError as e:
                raise ValueError("Invalid date format")
                
        if end is not None:
            if start_date > end_date:
                raise ValueError("Start date cannot be after end date.")
            
    elif freq == "monthly":
        if start is None:
            raise ValueError("For monthly data, start date must be provided.")
        try:
            start_date = datetime.strptime(start, "%Y%m")
            if start_date < datetime(1981, 1, 1):
                raise ValueError("Invalid start date for monthly data.")
        except ValueError as e:
            raise ValueError("Invalid date format")
        
        if end is None:
            onetime_download = True
        else:
            try:
                end_date = datetime.strptime(end, "%Y%m")
                last_month = datetime.now() - timedelta(days=datetime.now().day)
                if end_date > last_month:
                    raise ValueError("Invalid end date for monthly data.")
            except ValueError as e:
                raise ValueError("Invalid date format")
                
        if end is not None:
            if start_date > end_date:
                raise ValueError("Start date cannot be after end date.")
            
    else:  # freq == "annual"
        if start is None:
            raise ValueError("For annual data, start date must be provided.")
        try:
            start_date = datetime.strptime(start, "%Y")
            if start_date < datetime(1981, 1, 1):
                raise ValueError("Invalid start date for annual data.")
        except ValueError as e:
            raise ValueError("Invalid date format")
        
        if end is None:
            onetime_download = True
        else:
            try:
                end_date = datetime.strptime(end, "%Y")
                last_year = datetime.strptime(str(datetime.now().year-1), "%Y")
                if end_date > last_year:
                    raise ValueError("Invalid end date for annual data.")
            except ValueError as e:
                raise ValueError("Invalid date format")
                
        if end is not None:
            if start_date > end_date:
                raise ValueError("Start date cannot be after end date.")
        

    # Set the default download directory if not provided
    if download_dir is None:
        download_dir = Path.cwd() / "data"
    else:
        download_dir = Path(download_dir)

    # Check if directory exist, if not create it
    if not download_dir.exists():
        download_dir.mkdir()

    # Create a subdirectory for the specific variable if it doesn't exist
    variable_dir = download_dir / variable
    variable_dir.mkdir(exist_ok=True)


    # Create a date range based on the frequency and onetime_download
    if freq == "daily":
        if onetime_download:
            date_range = [start_date]  # only one date
        else:
            date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]  # all dates in range
    elif freq == "monthly":
        if onetime_download:  # only one date
            date_range = [start_date]  # only one date
        else:
            date_range = [start_date + relativedelta(months=x) for x in range((end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1)]  # all dates in range
    else:  # freq == "annual"
        if onetime_download:  # only one date
            date_range = [start_date]  # only one date
        else:
            date_range = [start_date + relativedelta(years=x) for x in range(end_date.year - start_date.year + 1)]  # all dates in range
        


    # date formate based on frequency
    if freq == "daily":
        date_format_read = "%Y%m%d"
        date_format_write = "%Y-%m-%d"
        file_prepfix = 'daily_'
    elif freq == "monthly":
        date_format_write = "%Y-%m"
        date_format_read = "%Y%m"
        file_prepfix = 'monthly_'
    else:  # freq == "annual"
        date_format_write = "%Y"
        date_format_read = "%Y"
        file_prepfix = 'annual_'

    # Construct the base URL for PRISM data
    base_url = "https://services.nacse.org/prism/data/public/4km"        

    # Download the data for each date in the range
    for date in date_range:
        date_read = date.strftime(date_format_read)
        date_write = date.strftime(date_format_write)
        url = f"{base_url}/{variable}/{date_read}"
        filename = f"{file_prepfix}{date_read}.zip"
        file_path = variable_dir / filename

        # Download the file if it doesn't already exist
        if not file_path.exists():
            response = requests.get(url)
            if response.status_code == 200:
                with open(file_path, "wb") as file:
                    file.write(response.content)
                print(f"Downloaded: {filename}")
                if unzip:  # unzip the file
                    with zipfile.ZipFile(file_path, "r") as zip_ref:  # unzip the file
                        zip_ref.extractall(variable_dir)  # extract to the same directory
                    if remove_zip:  # remove the zip file
                        file_path.unlink()  # remove the zip file
                        print(f"Unzipped: {filename}")

                    # Process the extracted files
                    pattern = f"PRISM_*_{date_read}_bil"
                    bil_file = list(variable_dir.glob(f"{pattern}.bil"))[0]  # assuming there's only one .bil file per date

                    # Open the .bil file with rioxarray and convert to netcdf
                    data = rioxarray.open_rasterio(bil_file, mask_and_scale=True).rio.reproject("EPSG:4326").sel(
                        band=1).reset_coords('band', drop=True).assign_coords(date=pd.to_datetime(date_write)).expand_dims('date')
                    netcdf_filename = f"{file_prepfix}{date_read}.nc"
                    data.to_netcdf(variable_dir / netcdf_filename)

                    # Remove the extracted files
                    for file in variable_dir.glob(f"{pattern}*"):
                        file.unlink()

            else:
                print(f"Error downloading: {filename}")
        else:
            print(f"File already exists: {filename}")