# TV-TRACK

This is the readme file for the script TV-Track.
It is an open source project made using mutliple python libraries, which mails the user the date when the next episode/season of the specified TV series will be aired.

## Following are the prerequisites for running the script:-

- It was built on Linux platform and will run better on it.(I say this because I have not tried running it on Windows or MacOS)
- The script is written using python 3.x.
- The script uses Selenium, so make sure its installed before running the script.
- The webdriver for selenium here is Firefox(therefore there is a geckodriver driver file in the repository).
   If you must use any other browser, modify line 59 in the script.py and change the name to the desired browser.
   Also, include the driver file for the respected browser in the driver folder.

## FUNCTIONING

The main objective of the script is to accept the email address and a list of TV series name from the user 
and mail to that email address, one of the following information about each TV Series:

- Date when the next episode of the Series will be aired.
- Year when the next season of the Series will be aired.
- Whether there will be anymore season for that particular Series in the future.

## INPUT FORMAT

Email address: xyz@abc.com
TV Series: game of thrones

## OUTPUT FORMAT

The mail send to xyz@abc.com would look like:

Tv series name: Game of thrones
Status: The next season begins in 2019


