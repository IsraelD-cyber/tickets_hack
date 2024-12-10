from datetime import datetime
import time

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By

import os
import sys


def dual_print(*args, sep=' ', end='\n', file=None, flush=False):
    # Print to terminal
    print(*args, sep=sep, end=end, flush=flush)

    # If file is specified, print to the file
    if file:
        print(*args, sep=sep, end=end, file=file, flush=flush)


def send_notification(message):
    token = "7061160734:AAGcmCRNOBmDiKejsow87k6ewFR7MJpdfz8"
    chat_id = "1905295439"
    command = ("curl -s -X POST https://api.telegram.org/bot" + token + "/sendMessage -d chat_id=" + chat_id +
               " -d text=\"" + message + "\" > /dev/null")
    os.system(command)


def run():
    driver = webdriver.Chrome()
    url = sys.argv[1]
    xpath = sys.argv[2]
    secs = int(sys.argv[3])
    str_to_find = sys.argv[4]
    notify_num = 0
    error_num = 0
    not_found_num = 0
    filename = "tickets_hack_" + datetime.now().strftime("%H:%M:%S") + ".log"
    log_file = open(filename, "w")

    while notify_num < 5 and error_num < 5:
        time.sleep(secs)

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        dual_print(" [", current_time, "] ", end='', file=log_file)

        try:
            driver.get(url)
        except Exception as error:
            msg = "An exception occurred in driver.get(url)"
            dual_print(msg, file=log_file)
            error_num += 1
            continue

        driver.implicitly_wait(0.5)

        try:
            target = driver.find_element(By.XPATH, xpath)
        except selenium.common.exceptions.NoSuchElementException:
            msg = "An exception occurred: NoSuchElementException"
            dual_print(msg, file=log_file)
            not_found_num += 1
            if not_found_num > 5:
                dual_print("send_notification!", file=log_file)
                send_notification("Tickets Avialable!")
                secs = 3.0
                notify_num += 1
            continue
        except Exception as e:
            msg = "An exception occurred:"
            dual_print(msg, e, file=log_file)
            error_num += 1
            continue

        not_found_num = 0
        error_num = 0

        text = target.get_attribute("alt")
        if text.find(str_to_find) != -1:
            dual_print(str_to_find, file=log_file)
            notify_num = 0
        else:
            dual_print("send_notification!", file=log_file)
            send_notification("Tickets Avialable!")
            secs = 3.0
            notify_num += 1

    log_file.close()
    driver.quit()
    send_notification("Program closed!")

def main():
    run()


if __name__ == "__main__":
    main()
