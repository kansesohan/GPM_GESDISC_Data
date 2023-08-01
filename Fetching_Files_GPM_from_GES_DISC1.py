import requests
import getpass
import os
from datetime import datetime, timedelta
from netCDF4 import Dataset
from osgeo import gdal
from osgeo import gdal_array
from osgeo import osr

# Set the URL string to point to a specific data URL. Some generic examples are:

base_url = 'https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGDL.06'

# Set the start and end dates for the data to download
# start_date = input('Enter start date (YYYY-MM-DD): ')
# end_date = input('Enter end date (YYYY-MM-DD): ')
start_date = '2022-09-12'
end_date = '2022-09-22'
# Convert the input strings to datetime objects
start_dt = datetime.strptime(start_date, '%Y-%m-%d')
end_dt = datetime.strptime(end_date, '%Y-%m-%d')

# Create the directory where the downloaded files will be stored, if it doesn't exist
download_dir = "E:\\GPM_Data_Download\\Data\\"
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Create the directory where the converted TIFF files will be stored, if it doesn't exist
tif_dir = "E:\\GPM_Data_Download\\TIFF\\"
if not os.path.exists(tif_dir):
    os.makedirs(tif_dir)

# Define a function to generate the URLs for a given date
def generate_urls(date):
    urls = []
    url = f'{base_url}/{date.year}/{date.month:02d}/3B-DAY-L.MS.MRG.3IMERG.{date.strftime("%Y%m%d")}-S000000-E235959.V06.nc4'
    print(url)
    urls.append(url)
    return urls

# Define a function to convert Nc4 to TIFF
def convert_to_tiff(nc4_file, tiff_file):
    ds = gdal.Open(nc4_file)
    subds = ds.GetSubDatasets()[0][0]
    ds_sub = gdal.Open(subds)

    driver = gdal.GetDriverByName("GTiff")
    dst_ds = driver.CreateCopy(tiff_file, ds_sub, 0)
    dst_ds = None

# Call generate_urls() for each date in the range and add the URLs to a list
urls = []
date = start_dt
while date <= end_dt:
    urls += generate_urls(date)
    date += timedelta(days=1)

# Set the FILENAME string to the data file name, the LABEL keyword value, or any customized name.
for url in urls:
    FILENAME = download_dir + "\\" + os.path.basename(url)
    if os.path.exists(FILENAME):
        print(f"{FILENAME} already exists, hence skipping download for {url}")
        continue
    result = requests.get(url)
    try:
        result.raise_for_status()
        with open(FILENAME, 'wb') as f:
            f.write(result.content)
        print(f'Contents of {url} saved in {FILENAME}')

        # Convert Nc4 to TIFF
        tiff_file = tif_dir + "\\" + os.path.splitext(os.path.basename(url))[0] + ".tiff"
        convert_to_tiff(FILENAME, tiff_file)
        print(f'{FILENAME} converted to {tiff_file}')
    except:
        print(f'requests.get() returned an error code {result.status_code} for URL {url}')

print("Task Completed")
