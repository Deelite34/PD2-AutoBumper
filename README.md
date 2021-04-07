# PD2 AutoBumper
 Command line program, that automates tedious process of bumping many trades.
 
 ![WIP1](https://user-images.githubusercontent.com/35972878/113863728-4bfc6a00-97aa-11eb-929e-46e3b73a4fbb.gif)


 ### Requirements
 - project diablo 2 website account
 - chrome or firefox browser  
 - browser driver for chosen browser, that allows automation. You can download it from https://pypi.org/project/selenium/#drivers
 ### Usage
 1. Close any other project diablo 2 website window you have open, to prevent too many requests issue
 2. Put webdriver in the program directory.
 3. When you launch Autobumper.exe for the first time, settings.ini file will be created. Add selected browser name(chrome or firefox), and add path to browsername.exe file
 4. When you launch the program, the browser will pop up. In command line program input login and password, if it's correct, program will start doing the stuff. Do **not** minimize browser where automation is happening, or program will break and you'll need to launch it again.
 5. You can do different things like browser internet or play diablo 2. Browser window can be inactive and bumping will keep going, just remember to not minimize it.  
 

## For contributors
Project made with Python and selenium library. It is open for bugfixes, contributions and enhancements.
### Installation:
Create virtual environment `python -m venv venv_autobumper`  
Launch virtual environment `.\venv_autobumper\scripts\activate` (powershell command)  
Install required modules `pip install -r requirements.txt`  
Run `python AutoBumper.py`  
