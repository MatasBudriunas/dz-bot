from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)


@app.route('/bot', methods=['GET'])
def bot():
    user_input = request.args.get('text')
    response = interact_with_website(user_input)

    return jsonify({'response': response})


def interact_with_website(input_text):
    browser = setup_selenium_browser()
    browser.get('https://chroniclesofdenzar.com/index.php?redir=/explore.php')

    # Wait for the input field to be clickable
    input_field = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[5]/input'))
    )

    # Click on the input field before interacting with it
    input_field.click()
    time.sleep(2)

    # Enter the text in the input field
    input_field.send_keys(input_text)

    # Wait for the stream of response to complete
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'response_element_id'))
    )

    # Extract the response
    response_element = browser.find_element("xpath", '/html/body/div[3]/div/div/div[6]/p')
    response_text = response_element.text

    # Clean up and return the response
    browser.quit()

    return response_text


def setup_selenium_browser():
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    browser = webdriver.Firefox(options=options)

    return browser


if __name__ == '__main__':
    app.run()
