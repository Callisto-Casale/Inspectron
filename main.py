# import os
import subprocess
import os
import sys
import random
import datetime
from bs4 import BeautifulSoup

def main(folder):
    os.system("cls")
    print("[INSPECTRON] Running pylint on all files in " + folder)
    for file in os.listdir(folder):
        if file.endswith(".py"):
            cmd = "pylint " + folder + "/" + file
            process = subprocess.run(cmd, shell=True, text=True, capture_output=True)
            output = process.stdout.split("\n")[-3].split("(")[0].split("at ")[-1]
            print(f"[{file}] - {output}")
    

    path = "outputs"
    filename = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S") + ".html"
    fullPath = path + "/" + filename

    print(f"[INSPECTRON] Generating optimization report")

    with open("outputs/template.html", 'r') as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    # add the output of pylint to the html file but keep new lines
          
    tbody = soup.find(id="report-output")  
    # ...

    files = [file for file in os.listdir(folder) if file.endswith(".py")]
    for i, file in enumerate(files):
        cmd = "pylint " + folder + "/" + file
        process = subprocess.run(cmd, shell=True, text=True, capture_output=True)
        output = process.stdout.split("\n")
        for j, line in enumerate(output):
            new_row = soup.new_tag("tr")
            new_cell_num = soup.new_tag("td")
            new_cell_num.string = str(j + 1)
            new_cell_output = soup.new_tag("td")
            new_cell_output.string = line
            new_cell_checkbox = soup.new_tag("td")
            new_checkbox = soup.new_tag("input", type="checkbox", onchange="strikeThrough(this)", class_="styled-checkbox")
            new_cell_checkbox.append(new_checkbox)
            new_row.append(new_cell_num)
            new_row.append(new_cell_output)
            new_row.append(new_cell_checkbox)
            tbody.append(new_row)
        if i < len(files) - 1:  # don't add gap after the last output
            gap = soup.new_tag("tr", style="height: 50px;")  # adjust the height as needed
            tbody.append(gap)

    # ...

    with open(fullPath, 'w') as fp:
        fp.write(str(soup))

    # ...

    print(f"[INSPECTRON] Opening optimization report in browser")
    os.system(os.getcwd() + "/" + fullPath)






if __name__ == "__main__":
    folder = sys.argv[1]
    main(folder)