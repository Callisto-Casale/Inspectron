import os
import subprocess
import sys
import datetime
import time
from bs4 import BeautifulSoup
import json

with open("config.json", 'r') as fp:
    config = json.load(fp)


def run_autopep8(folder):
    print("[INSPECTRON] Running autopep8 on all files in", folder)
    for file in os.listdir(folder):
        if file.endswith(".py"):
            cmd = f"autopep8 --in-place --aggressive --aggressive {folder}/{file}"
            subprocess.run(cmd, shell=True, text=True)
            print(f"[INSPECTRON] Applied autopep8 to {file}")


def run_pylint(folder):
    print("[INSPECTRON] Running pylint on all files in", folder)
    for file in os.listdir(folder):
        if file.endswith(".py"):
            cmd = f"pylint {folder}/{file}"
            process = subprocess.run(
                cmd, shell=True, text=True, capture_output=True)
            output_lines = process.stdout.splitlines()
            error_info = output_lines[-3].split("(")[0].split("at ")[-1]
            print(f"[INSPECTRON] Applied pylint to {file}")


def generate_html_report(folder):
    path = "outputs"
    filename = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S") + ".html"
    full_path = os.path.join(path, filename)
    print("[INSPECTRON] Generating optimization report")

    with open("outputs/template.html", 'r') as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    tbody = soup.find(id="report-output")

    files = [file for file in os.listdir(folder) if file.endswith(".py")]
    for i, file in enumerate(files):
        cmd = f"pylint {folder}/{file}"
        process = subprocess.run(
            cmd, shell=True, text=True, capture_output=True)
        output = process.stdout.splitlines()
        for j, line in enumerate(output):
            new_row = soup.new_tag("tr")
            new_cell_num = soup.new_tag("td")
            new_cell_num.string = str(j + 1)
            new_cell_output = soup.new_tag("td")
            new_cell_output.string = line
            new_cell_checkbox = soup.new_tag("td")
            new_checkbox = soup.new_tag(
                "input",
                type="checkbox",
                onchange="strikeThrough(this)",
                class_="styled-checkbox")
            new_cell_checkbox.append(new_checkbox)
            new_row.append(new_cell_num)
            new_row.append(new_cell_output)
            new_row.append(new_cell_checkbox)
            tbody.append(new_row)
        if i < len(files) - 1:
            gap = soup.new_tag("tr", style="height: 50px;")
            tbody.append(gap)

    with open(full_path, 'w') as fp:
        fp.write(str(soup))

    if (config["OPEN_FILE"]):
        print("[INSPECTRON] Opening optimization report in browser")
        os.system(os.path.join(os.getcwd(), full_path))


    if (config["DELETE_FILE_AFTER_OPEN"]):
        time.sleep(1)
        print("[INSPECTRON] Deleting optimization report")
        os.remove(full_path)


def main(folder, autopep8=False):
    os.system("cls")

    if autopep8:
        run_autopep8(folder)

    run_pylint(folder)
    generate_html_report(folder)


if __name__ == "__main__":
    folder = sys.argv[1]

    main(folder, autopep8=config["EXTRAS"]["AUTOPEP8"])
