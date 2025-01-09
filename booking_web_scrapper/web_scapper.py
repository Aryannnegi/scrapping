from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

driver = webdriver.Chrome()
driver.get( 'https://www.booking.com/index.en-gb.html?label=gen173nr-1BCAEoggI46AdIM1gEaGyIAQGYAQm4ARfIAQzYAQHoAQGIAgGoAgO4AvmoxrkGwAIB0gIkMzBkMWJmNWItZGFkZS00N2Q4LWE2NmEtOWQzMzM5ZTBlZDA32AIF4AIB&sid=9ade8fd3cb49a1d6170dd6807da4860f&aid=304142')
driver.maximize_window()
driver.implicitly_wait(10)


try:
    close_button = driver.find_element(By.XPATH,"//*[@id='bodyconstraint-inner']/div[1]/div[3]/div/div/div/div/div[1]/div[1]/div/button/span")
    close_button.click()
except Exception as e:
    print("Popup close button not found or another error occurred", e)

search_bar = driver.find_element(By.XPATH, "//*[@id=':rh:']")
search_bar.click()
search_bar.send_keys("Rishi")
time.sleep(2)

try:
    first_result = driver.find_element(By.XPATH, "//*[@id='autocomplete-result-0']/div/div/div/div[2]")
    first_result.click()
except Exception as e:
    print("First dropdown result not found or another error occurred", e)

time.sleep(2)

# Select the check-out dat
try:
    checkin_date = driver.find_element(By.XPATH,
                                       "//*[@id='calendar-searchboxdatepicker']/div/div[1]/div/div[1]/table/tbody/tr[4]/td[4]/span")
    checkin_date.click()
except Exception as e:
    print("Check-in date not found or another error occurred", e)

# Select the check-out date
try:
    checkout_date = driver.find_element(By.XPATH,
                                        "//*[@id='calendar-searchboxdatepicker']/div/div[1]/div/div[2]/table/tbody/tr[1]/td[4]/span")
    checkout_date.click()
except Exception as e:
    print("Check-out date not found or another error occurred", e)

# Open the dropdown for guest selection
try:
    dropdown_button = driver.find_element(By.XPATH,
                                          "//*[@id='indexsearch']/div[2]/div/form/div/div[3]/div/button/span[1]")
    dropdown_button.click()
except Exception as e:
    print("Dropdown button not found or another error occurred", e)



def set_number_of_adults(target_adult_count):
    current_adult_count = 2
    decrease_button = driver.find_element(By.XPATH, "//*[@id=\":ri:\"]/div/div[1]/div[2]/button[1]")
    increase_button = driver.find_element(By.XPATH, "//*[@id=\":ri:\"]/div/div[1]/div[2]/button[2]")

    # Calculate the number of clicks needed
    clicks_needed = target_adult_count - current_adult_count

    if clicks_needed < 0:
        # Click the minus button to decrease the count
        for _ in range(abs(clicks_needed)):
            decrease_button.click()
    elif clicks_needed > 0:
        # Click the plus button to increase the count
        for _ in range(clicks_needed):
            increase_button.click()

time.sleep(2)
set_number_of_adults(6)
def click_search_button():
    try:
        # Locate and click the search button
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Search']"))
        )
        search_button.click()
        time.sleep(2)  # Allow time for the search results to load
    except Exception as e:
        print("Error while clicking the search button:", e)

def filter_by_free_wifi():
    try:
        radio_button = driver.find_element(By.XPATH, "(//label[normalize-space()='Entire stay'])[1]" )
        radio_button.click()
        time.sleep(2)
        print("Clicked on the radio button successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def scroll_to_element():
    try:
        radio_button_2 = driver.find_element(By.XPATH, "(//*[name()='svg'])[29]")
        radio_button_2.click()
        time.sleep(2)
        print("Clicked after scroll successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def clean_hotel_names(hotel_names):
    clean_names = []
    for name in hotel_names:
        # Remove unwanted text, assuming it's a consistent phrase
        clean_name = name.replace("Opens in new window", "").strip()
        clean_names.append(clean_name)
    return clean_names

def hotel_list():
    try:
        # Locate the first parent div
        parent_div = driver.find_element(By.XPATH, "(//div[@class='dcf496a7b9 bb2746aad9'])[1]")

        # Locate all child anchor elements within the parent div
        hotel_anchors = parent_div.find_elements(By.XPATH, ".//a[@class='a78ca197d0']")

        price_anchors = parent_div.find_elements(By.XPATH, "(//span[@class='f6431b446c fbfd7c1165 e84eb96b1f'])")

        # Extract text from each child anchor
        hotel_names_anchors = [hotel_anchor.text for hotel_anchor in hotel_anchors]
        price_value_anchors = [price_anchors.text for price_anchors in price_anchors]

        # Combine and print all names
        hotel_names = hotel_names_anchors + price_value_anchors
        hotel_names = clean_hotel_names(hotel_names)
        prices= price_value_anchors

        for name in hotel_names:
            print(name)

        if len(hotel_names) == len(prices):
            data = {'Hotel name': hotel_names, 'Price': prices}
            df = pd.DataFrame(data)
            df.to_csv('hotels.csv', index=False)
            print("Data successfully exported to hotels.csv")
        else:
            print("Mismatch between hotel names and prices. Data not exported.")

    except Exception as e:
        print(f"An error occurred: {e}")


click_search_button()
filter_by_free_wifi()
scroll_to_element()
hotel_list()



# Keep the browser open (optional, for demonstration purposes)
input("Press Enter to close the browser...")

# Optionally, quit the driver if this is the end of your script
#driver.quit()
