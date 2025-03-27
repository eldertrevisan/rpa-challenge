import os
from time import sleep
import pandas as pd
import logging
from datetime import datetime
from pathlib import Path
from src.resources.roboSelenium import RoboSelenium


def read_xlsx(file):
    """Get data from Excel file"""
    log_rpa.info("Getting data from the spreadsheet...")
    df = pd.read_excel(file, engine="openpyxl", header=1)
    return df.values


def run_bot(d):
    """Solve the challlenge"""
    robo = RoboSelenium()
    log_rpa.info("Opening browser and accessing website")
    robo.open_url('https://www.rpachallenge.com/') # open website
    robo.document_ready_state() # wait to page load
    robo.check_title('Rpa Challenge')

    "Loop to find the fields, fill them in and submit."
    for i in d:
        log_rpa.info('Finding and filling in the "First Name" field')
        first_name_label = robo.find_by_attribute('xpath',"//label[contains(text(), 'First Name')]")
        first_name_field = robo.find_by_label(first_name_label)
        first_name_field.send_keys(i[0])

        log_rpa.info('Finding and filling in the "Last Name" field')
        last_name_label = robo.find_by_attribute('xpath',"//label[contains(text(), 'Last Name')]")
        last_name_field = robo.find_by_label(last_name_label)
        last_name_field.send_keys(i[1])

        log_rpa.info('Finding and filling in the "Company Name" field')
        company_name_label = robo.find_by_attribute('xpath',"//label[contains(text(), 'Company Name')]")
        company_name_field = robo.find_by_label(company_name_label)
        company_name_field.send_keys(i[2])

        log_rpa.info('Finding and filling in the "Role in Company" field')
        role_in_company_label = robo.find_by_attribute('xpath',"//label[contains(text(), 'Role in Company')]")
        role_in_company_field = robo.find_by_label(role_in_company_label)
        role_in_company_field.send_keys(i[3])

        log_rpa.info('Finding and filling in the "Address" field')
        address_label = robo.find_by_attribute('xpath',"//label[contains(text(), 'Address')]")
        address_field = robo.find_by_label(address_label)
        address_field.send_keys(i[4])

        log_rpa.info('Finding and filling in the "E-mail" field')
        email_label = robo.find_by_attribute('xpath',"//label[contains(text(), 'Email')]")
        email_field = robo.find_by_label(email_label)
        email_field.send_keys(i[5])

        log_rpa.info('Finding and filling in the "Phone Number" field')
        phone_number_label = robo.find_by_attribute('xpath',"//label[contains(text(), 'Phone Number')]")
        phone_number_field = robo.find_by_label(phone_number_label)
        phone_number_field.send_keys(i[6])

        log_rpa.info('Sending data...')
        bt_submit_xpath = "/html/body/app-root/div[2]/app-rpa1/div/div[2]/form/input"
        robo.scroll_to_element(bt_submit_xpath)
        bt_submit_send = robo.find_by_attribute("xpath", bt_submit_xpath)
        sleep(1)
        bt_submit_send.click()
        sleep(2)

    log_rpa.info('Closing browser...')
    robo.close_browser()
    robo.quit_driver()


if __name__ == "__main__":
    log_rpa = logging.getLogger('log_rpa')
    log_rpa.setLevel(logging.INFO)
    log_dir = os.path.join(Path(__file__).parent, '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)  # Create the log directory if it doesn't exist
    file_handler_rpa = logging.FileHandler(os.path.join(log_dir, f'rpa-challenge - {datetime.now().strftime("%Y-%m-%d")}.log'), encoding="utf-8")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s -- %(message)s')
    file_handler_rpa.setFormatter(formatter)
    log_rpa.addHandler(file_handler_rpa)

    data_dir = os.path.join(Path(__file__).parent, '..', 'data')
    log_rpa.info("Starting RPA...")
    data = read_xlsx(os.path.join(data_dir, 'challenge.xlsx'))
    if data.size > 0:
        run_bot(data)
        log_rpa.info('Ending execution...')
    else:
        log_rpa.warning("No information obtained from spreadsheet.")
