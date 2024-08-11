# Inspectron
Inspectron applies PyLint to a given directory and generates a report for one to check for improvements.
It uses a template located in the outputs folder to generate the report. It only works for .py files

## Usage
Clone this repo to your local machine. Navigate towards the directory you cloned it in,
Simply run the next command in the terminal to run the project.

```
python3 main.py {directory name}
```

> [!TIP]
> Check out the config.json to change the configurations


### Example output

```
[INSPECTRON] Running pylint on all files in C:\Users\user\Coding\Python\Torment
[house.py] - 3.85/10 
[inventory.py] - 6.07/10 
[main.py] - 8.33/10 
[travel.py] - 4.67/10 
[world.py] - 5.23/10 
[INSPECTRON] Generating optimization report
[INSPECTRON] Opening optimization report in browser
```

## Report

The report shows the output of PyLint and gives the option to strike out improvements.
![image](https://github.com/Callisto-Casale/Inspectron/assets/93484170/c3805b3a-1c98-47be-ad55-4f2a895c3a74)


## What does PyLint check for?
```
Pylint analyses your code without actually running it. It checks for errors, enforces a coding standard, looks for code smells,
and can make suggestions about how the code could be refactored.

@ https://pypi.org/project/pylint/
```

## Added features
- ✅ Tests for pylint and HTML report generator

## Future features
- Support for Javascript (ESLint)
- Support for Java (Checkstyle)
- Error handeling
- Performance Metrics
