import os
import datetime
import subprocess
import time
from bs4 import BeautifulSoup

def test_generate_html_report():
    # Create a temporary folder for testing
    test_folder = "test_outputs"
    os.makedirs(test_folder, exist_ok=True)

    # Call the function with the test folder
    generate_html_report(test_folder)

    # Verify that the HTML report file is generated
    filename = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S") + ".html"
    full_path = os.path.join("outputs", filename)
    assert os.path.exists(full_path)

    # Verify that the HTML report file is not empty
    with open(full_path, 'r') as fp:
        content = fp.read()
        assert len(content) > 0

    # Clean up the temporary folder
    os.remove(full_path)
    os.rmdir(test_folder)

# Run the test
test_generate_html_report()