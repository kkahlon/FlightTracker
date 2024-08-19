from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time
import pandas as pd

# TODO: Grab origin and destination from CLA's
origin = "SJC"
destination = "MSN"

# Keep browser window open after completion
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options = chrome_options)

# Clicks the `idx` indexed element out of the list of elements returned by the `query` of type `by`
def button(query, idx = 0, by = By.XPATH):
    element = driver.find_elements(by, query)[idx]
    element.click()
    time.sleep(0.25)
    return element

# Sends `keys` to the `idx` indexed element out of the list of elements returned by the `query` of type `by`
def textbox(query, keys, idx = 0, by = By.XPATH):
    element = driver.find_elements(by, query)[idx]
    element.send_keys(keys)
    time.sleep(0.25)
    return element

# Get to the flights page for the trip provided
def navigate():
    # Pull the webpage
    driver.get("https://www.google.com/travel/flights")
    # Maximize test browser window for easier viewing
    # NOTE: Should be removed when converted to headless
    driver.maximize_window()
    # Adds 3 seconds of polling to all element searches to account for loading times
    driver.implicitly_wait(3)

    # gives me a second to breathe
    time.sleep(1.5)

    # Shifts focus to the input box which corresponds to the trip origin
    button("//*[@aria-label='Where from?']")
    # Activates multiselect for origin options
    button("//button[@aria-label='Origin, Select multiple airports']")
    # Removes preselected origin options if there are any
    remove = driver.find_elements(By.XPATH, "//div[@aria-label='Remove']")
    if len(remove) != 0:
        remove[0].click()

    # Inputs the trip origin
    # TODO: Modify to support multiple origins
    orgn = textbox("//*[@aria-label='Where from? ']", origin)
    orgn.send_keys(Keys.ENTER)
    # Closes the origin input box popup
    button("//button[@aria-label='Done']", 1)

    # Shifts focus to the input box which corresponds to the trip destination
    button("//input[@aria-label='Where to? ']")
    # Activates multiselect for destination options
    button("//button[@aria-label='Destination, Select multiple airports']")

    # Inputs the trip destination
    # TODO: Modify to support multiple destinations
    dest = textbox("//*[@aria-label='Where to? ']", destination, 1)
    dest.send_keys(Keys.ENTER)
    # Closes the destination input box popup
    button("//button[@aria-label='Done']", 1)

    # Opens up the list of trip types
    button("//*[@aria-labelledby='i6 i7']")
    # Selects One Way as the trip type
    # TODO: Modify to support different trip types
    button("//li[@data-value='2']")
    
    # Shift focus to the departure input box
    departure = button("//input[@aria-label='Departure']")
    # Inputs the departure date
    # TODO: Account for round trip flights as well
    departure.send_keys("11/12/2024")
    # Close departure popup
    button("//button[@aria-label='Done. ']")
    
    # Advance to the query results page
    button("//button[@aria-label='Search']")

# Apply filters to the given flights
def filters():
    # Change the number of stops to 1 or fewer
    # TODO: Account for other numbers of stops
    button("//button[@aria-label='Stops, Not selected']")
    button("//input[@aria-label='1 stop or fewer']")

    # Filter to only American and United airlines
    # TODO: Support airline filtering by input 
    button("//button[@aria-label='Airlines, Not selected']")
    # Deselect all
    button("//button[@aria-label='Select all airlines']")
    button("//input[@value='American']")
    button("//input[@value='United']")
    # Close the popup
    button("//button[@aria-label='Close dialog']")

    # Give the page a second to catch up
    time.sleep(1.5)

# Parse the html table of best flights to extract the information for said flights
def get_data():
    # Find best flights table
    table_element = driver.find_elements(By.XPATH, "//ul")[4]
    
    # Get list of elements containing flight information
    flight_elements = table_element.find_elements(By.XPATH, "./li")
    
    # Extract flight info from html elements
    flight_info = []
    for flight_element in flight_elements:
        tokens = flight_element.text.split("\n")

        # Account for differing html element formats resulting from nonstop flights
        if tokens[6] == "Nonstop":
            flight_info.append([tokens[3], tokens[5], tokens[0], tokens[2], tokens[4], tokens[6], None, tokens[-1]])
        else:
            flight_info.append([tokens[3], tokens[5], tokens[0], tokens[2], tokens[4], tokens[6], tokens[7], tokens[-1]])
    
    # Convert the list of flights into a dataframe
    colNames = ["Airline", "Trip", "Departure", "Arrival", "Length", "NumStops", "Layovers", "Price"]
    flights = pd.DataFrame(flight_info, columns=colNames)

    return flights

# Execute everything
def run():
    navigate()
    filters()
    flights = get_data()

    print(flights)
    
if __name__ == "__main__":
    run()
