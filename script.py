from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
from datetime import datetime
import smtplib
import sqlite3 as sql


# --- update_progress() : Displays or updates a console progress bar ---
def update_progress(progress):
    barLength = 20
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()


# --- Inputs ---
print("Please enter the email and name of the TV Series carefully\n")
email_ids = [sttr.strip() for sttr in input('Email Address: ').split(',')]
series = [str.strip() for str in input('TV Series: ').split(',')]

# --- Inputs saved in mydb.sqlite3 ---
db="mydb.sqlite3"
con = sql.connect(db)
try:
    con.execute("CREATE TABLE IF NOT EXISTS EMAIL(address VARCHAR(20))")
    for email in email_ids:
        con.execute(f"INSERT INTO EMAIL VALUES('{email}')")
    con.commit()

    con.execute("CREATE TABLE IF NOT EXISTS SITCOMS(name VARCHAR(20))")
    for names in series:
        con.execute(f"INSERT INTO SITCOMS VALUES('{names}')")
    con.commit()
except Exception as e:
    print(e)
con.close()

# --- Scraping information about Series ---
print('Fetching details...')
msg = []
name = []

update_progress(0)

driver = webdriver.Firefox()
driver.minimize_window()

update_progress(0.3)

base_url = "https://www.google.com/"
for keyword in series:
    driver.get(base_url)
    search = str(keyword)+" imdb"
    search_bar = driver.find_element_by_id("lst-ib")
    search_bar.send_keys(search)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(2)

    update_progress(0.5)

    choice = driver.find_element_by_class_name('r')
    link_container = choice.find_element_by_tag_name('a')
    link = link_container.get_attribute('href')
    driver.get(link)

    update_progress(0.75)

    season_container = driver.find_element_by_class_name('seasons-and-year-nav')
    season = season_container.find_element_by_tag_name('a')
    season_link = season.get_attribute('href')
    driver.get(season_link)

    name_container = driver.find_element_by_class_name('parent')
    name_subc = name_container.find_element_by_tag_name('a')
    name.append(name_subc.text)
    episodes_dates = driver.find_elements_by_class_name('airdate')
    date_list = []

    update_progress(0.85)

    for e_date in episodes_dates:
        if len(e_date.text) == 4:
            year = e_date.text
            msg.append("The next season begins in "+str(year))
            break
        else:
            date_strpd = "".join(c for c in e_date.text if c not in ('.'))  # removing extra punctuations from date
            try:
                datetime_object = datetime.strptime(date_strpd, '%d %b %Y')
                date_list.append(datetime_object.date())
            except:
                pass

    update_progress(0.98)

    present_date = datetime.now().date()
    for i in date_list:
        if i > present_date:
            msg.append("The next episode airs on "+str(i))
            break
        else:
            msg.append("The show has finished streaming all its episodes(or no new info about further seasons is available).")
            break

update_progress(1)

driver.close()
content = "\n"
for j in range(len(series)):
    content = content + "TV Series name: "+name[j]+'\n'+'Status: '+msg[j]+'\n'+'\n'

# --- Mailing details ---
mail = smtplib.SMTP('smtp.gmail.com',587)   # The port may change in the future
mail.ehlo()    # extended hello
mail.starttls()     # Creates a secure connection
mail.login('notatestingbot@gmail.com','definitelyatestingbot')   # Please change the credentials after testing.
mail.sendmail('notatestingbot@gmail.com',email_ids,content)
mail.close()
print("\nDo check the Spam folder if the mail doesn'y appear in the inbox.")

# End of Script
