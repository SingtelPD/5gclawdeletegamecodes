#======SUBJECT TO CHANGE===========
url = "https://fsm.sg.formulasquare.com/fsm_api/wawaji_cms/"
#==================================

import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

options = Options()
options.headless = True


st.title("❌ Delete game codes")
st.write("Please use the form below to delete the game codes in the system.")
st.write("Note: You can only delete the X latest game codes")

form = st.form("range_form")
username = form.text_input("Please enter the CMS username")
password = form.text_input("Please enter the CMS password")
num_codes_to_delete = form.text_input("Enter the number of codes to delete")
submit = form.form_submit_button("Delete coupon codes from CMS")

if submit:
    st.info("Running. Please do NOT click on the button again.")

    #convert start_num and end_num to integer
    num_codes_to_delete = int(num_codes_to_delete)

    web = webdriver.Chrome(options=options)
    web.get(url)
    time.sleep(3)

    #Login
    username_field = web.find_element("xpath", '/html/body/div/div/main/div/div/div/div/form/div[1]/input')
    username_field.send_keys(username)
    password_field = web.find_element("xpath", '/html/body/div/div/main/div/div/div/div/form/div[3]/input')
    password_field.send_keys(password)
    submit_login_button = web.find_element("xpath", '/html/body/div/div/main/div/div/div/div/form/div[5]/input')
    submit_login_button.click()
    time.sleep(2)

    #navigate to coupon codes page
    coupon_codes = web.find_element("xpath", '/html/body/div/div/main/div/div[1]/button[3]')
    coupon_codes.click()
    time.sleep(1)
    
    #define wait
    wait = WebDriverWait(web, 20)

    #enter coupon codes within range
    for i in range (num_codes_to_delete):
        current_coupon_code = web.find_element("xpath", '/html/body/div/div/main/div/div[2]/div/table/tbody/tr[1]/td[3]'.getText())
        delete_button = web.find_element("xpath", '/html/body/div/div/main/div/div[2]/div/table/tbody/tr[1]/td[1]/input')
        delete_button.click()
        time.sleep(1)
        wait.until(expected_conditions.alert_is_present())
        alert = web.switch_to.alert.accept()
        time.sleep(1)
        st.write(f"Coupon code {current_coupon_code} has been deleted from the CMS system.")

    num_codes_to_delete = num_codes_to_delete-1
    st.success(f"{num_codes_to_delete} codes have been added to the CMS system.")
