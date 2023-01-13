import threading
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium import webdriver


def scrap(filename, interval):
    # the function to be called by the timer in a new thread.
    # It will scrap the data once and then set a new thread to the timer, to be invoked after interval seconds.
    driver = webdriver.Chrome(executable_path="./chromedriver")
    driver.get('https://weather.gc.ca/city/pages/on-143_metric_e.html')
    delay = 3
    # The data element is not in static html and is created by javascript so it is not available after html is
    # loaded. We have to wait until javascript finish creating it by using 'presence_of_element_located'. We set
    # timeout to 3 seconds which should be enough so we do not handle the exception.

    # scrap TODAY weather data.
    condition_ele = WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="wb-auto-4"]/div[2]/div/div[1]/dl/dd[1]')))

    temp_ele = WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="wb-auto-4"]/div[2]/div/div[2]/dl/dd[1]')))

    wind_ele = driver.find_element_by_xpath('//*[@id="wb-auto-4"]/div[2]/div/div[3]/dl/dd[1]')
    wind = wind_ele.text

    record = {'scrap_time': str(datetime.now()), 'date': str(datetime.today()), 'day_night': 'realtime',
              'condition': condition_ele.text,
              'temperature': temp_ele.text,
              'wind': wind}
    print(record)  # print the record for logging info. Not necessary.

    # scrape 5 days forecast weather data
    table = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="mainContent"]/section[2]/details/div')))

    with open(filename, mode='a+', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file, delimiter=',')
        # Write today's weather data to file.
        csv_writer.writerow([record['scrap_time'], record['date'], record['day_night'], record['condition'],
                             record['temperature'], record['wind']])

        children = table.find_elements_by_xpath('./*')
        # scrap all available forecast data, which should be 5 days. 'day' and 'night' conditions are forecasted in
        # each day.
        for ele in children:
            rows = ele.find_elements_by_xpath('./div')
            date_text = rows[0].text.strip()
            if date_text:
                row = rows[1]
                paragraphs = row.find_elements_by_xpath('./p')
                temperature_text = paragraphs[0].text
                condition_text = paragraphs[2].text
                record = {'scrap_time': str(datetime.now()), 'date': date_text, 'day_night': 'day',
                          'condition': condition_text, 'temperature': temperature_text, 'wind': ''}
                print(record)  # print the record for logging info. Not necessary.
                # write the DAY condition to file.
                csv_writer.writerow([record['scrap_time'], record['date'], record['day_night'], record['condition'],
                                     record['temperature'], record['wind']])

                row = rows[2]
                row = rows[1]
                paragraphs = row.find_elements_by_xpath('./p')
                temperature_text = paragraphs[0].text
                condition_text = paragraphs[2].text
                record = {'scrap_time': str(datetime.now()), 'date': date_text, 'day_night': 'night',
                          'condition': condition_text, 'temperature': temperature_text, 'wind': ''}

                print(record)  # print the record for logging info. Not necessary.
                # Write the NIGHT condition to file.
                csv_writer.writerow([record['scrap_time'], record['date'], record['day_night'], record['condition'],
                                     record['temperature'], record['wind']])
    driver.close()
    file.close()
    # set a new thread to be invoked interval seconds later.
    threading.Timer(interval, scrap, [filename, interval]).start()


file_name = 'daily_weatherReport.csv'
# start a new thread 6h later.
thread = threading.Timer(0, scrap, [file_name, 3600*6]).start()


