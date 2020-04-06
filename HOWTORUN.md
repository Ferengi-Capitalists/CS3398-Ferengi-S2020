# Welcome to the How to setup and run ReadMe!

In this Markdown file in I will be going over the how to setup and run a django project. 
# Authors:
* Ferengi team
#  Tools Used:
* Lastest  LTS versions of Python and Django.
## How to Install Python:
* Linux:
	* Simply navigate to your terminal and run:
			$ sudo apt-get update
			$ sudo apt-get install python3
	* verify:
		$ python3 -v
* Mac OS:
	* Install homebrew and run:
		$ brew install python
	* verify:
		$ python3 -v
* Windows:
	* Installation:
		* Click [Python Download](https://www.python.org/downloads/).
		* Click the **Windows** link (two lines below the **Download Python 3.7.4** button).
		* Click on the **Download  Windows x86-64 executable installer** link under the top-left **Stable Releases**.
		* Move this file to a more permanent location, so that you can install Python (and reinstall it easily later, if necessary).
		* Double-click the icon labeling the file **python-3.7.4-amd64.exe**.
		* Ensure that the **Install launcher for all users (recommended)** and the **Add Python 3.7 to PATH** checkboxes at the bottom are checked.
		* Highlight the **Install Now** (or **Upgrade Now**) message, and then click it.
		* Click the **Yes** button.
		* Soon, a new **Python 3.7.4 (64-bit) Setup** pop-up window will appear with a **Setup was successfuly** message.
		* Click the **Close** button.
	* verify:
		* Now navigate windows CMD: Type 'python' and hit enter.
## How to setup the Virtual Environment:
#### virtualenv

In your Command Prompt enter:

`pip install virtualenv`

In your Command Prompt navigate to your project:

`cd your_project`

Within your project:

`virtualenv env`

Activate your virtualenv:

on Windows, virtualenv creates a batch file

`\env\Scripts\activate`

to activate virtualenv on Windows, activate script is in the Scripts folder :

`\path\to\env\Scripts\activate`

Example:

`C:\Users\'Username'\venv\Scripts\activate.bat`

## Now install the requirements to your venv:

`pip install django`

`pip install requirements.txt`

## Now run the project from  localhost:
* now from the project folder:
`python manage.py runserver`
