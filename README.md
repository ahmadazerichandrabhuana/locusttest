# Locust Test
Sample usage of Locust

## Website Test

API Collection retrieved from this Website : https://www.demoblaze.com/

You can also check the API Collection by importing `.json` file from this repository into Postman.

## Requirements

Install [Locust](https://docs.locust.io/en/stable/installation.html)

    pip install locust

## Run Test

CD into folder where you store the downloaded `demoblaze.py`

    cd [your_path_where_you_store_downloaded_demoblaze.py_file]

and run command : 

    locust -f demoblaze.py

Then open this address on your Web Browser : 

    http://0.0.0.0:8089/

The Locust's Web Interface should be opened. Put `Number of users` and `Ramp up`, for example `10` and `1`, respectively : 

<img width="1440" alt="Screenshot 2024-11-06 at 10 23 40 AM" src="https://github.com/user-attachments/assets/f83b0850-8f07-4051-bd43-a0ddf63ef3e9">

And hit button `Start`

_NOTE_ : Please use **low number** for both `Number of users` and `Ramp up`, we don't want this website for learning becomes laggy, right? 😃

<img width="1440" alt="Screenshot 2024-11-06 at 10 31 53 AM" src="https://github.com/user-attachments/assets/d4d6a699-b9b4-4ec9-870e-07353add9f53">

Stop the test by hitting button `Stop`. And you can start analyze the performance data.

## Statistics

<img width="1440" alt="Screenshot 2024-11-06 at 10 32 13 AM" src="https://github.com/user-attachments/assets/c3d8bcdd-fdbe-4d82-8117-c74eb44604ff">

## Charts

<img width="1440" alt="Screenshot 2024-11-06 at 10 32 35 AM" src="https://github.com/user-attachments/assets/b30cde5b-cdef-4f1a-b7f7-bc266a160456">

## Logs

<img width="1440" alt="Screenshot 2024-11-06 at 10 34 48 AM" src="https://github.com/user-attachments/assets/e459d19c-ecef-4583-b9ea-fc3f80ba702b">

Or you can run this command when start Locust to save the log into specific file

    locust -f demoblaze.py --logfile=locustfile.log
