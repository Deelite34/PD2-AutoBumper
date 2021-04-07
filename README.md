# PD2 AutoBumper
 Command line program, that automates tedious process of bumping many trades.  
 Download: https://github.com/Deelite34/PD2-AutoBumper/releases/tag/1.0.0
 
 ![WIP1](https://user-images.githubusercontent.com/35972878/113863728-4bfc6a00-97aa-11eb-929e-46e3b73a4fbb.gif)


 ### Requirements
 - project diablo 2 website account
 - chrome or firefox browser  
 - webdriver file for chosen browser, that allows automation. You can download it from https://pypi.org/project/selenium/#drivers
 ### Usage
 0. Download the program here https://github.com/Deelite34/PD2-AutoBumper/releases/tag/1.0.0  
 1. Close any other project diablo 2 website window you have open, to prevent too many requests issue
 2. Put webdriver in the program directory.  
 ![image](https://user-images.githubusercontent.com/35972878/113875920-84567500-97b7-11eb-8902-c94521472706.png)
 4. When you launch Autobumper.exe for the first time, settings.ini file will be created. Add selected browser name(chrome or firefox), and add path to browsername.exe file  
 ![image](https://user-images.githubusercontent.com/35972878/113876099-b36ce680-97b7-11eb-9fd0-b876d96283c5.png)

 6. When you launch the program, the browser will pop up. In command line program input login and password. Password that you put in is hidden, press enter when you are ready. If credentials are  correct, program will start doing the stuff. Do **not**   minimize browser where automation is happening - minimized browser does not accept automated commands, therefore program will break and you'll need to launch it again.
 7. You can do different things like browser internet or play diablo 2. Browser window can be inactive and bumping will keep going, just remember to not minimize it.  
 

## For contributors
Project made with Python and selenium library. It is open for bugfixes, contributions and enhancements.
### Installation:
Create virtual environment `python -m venv venv_autobumper`  
Launch virtual environment `.\venv_autobumper\scripts\activate` (powershell command)  
Install required modules `pip install -r requirements.txt`  
Run `python AutoBumper.py`  
