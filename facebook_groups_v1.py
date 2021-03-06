"""
    __author__ == Anthony Mirely

    This Program passes facebook groups from one user to another

"""

import mechanicalsoup
import time
from bs4 import BeautifulSoup
import re

login_url = "https://m.facebook.com/"
login =  "Change this with Username, email or ID of sender"# "//THIS IS THE USERNAME/EMAIL/USER-ID OF THE SENDER
password = "Change this with Password of the sender" # // THIS IS THE PASSWORD OF THE SENDER
home = "https://m.facebook.com/home.php"                # URL IS ON MOBILE BECAUSE IT DOESN'T CONTAIN AJAX


def login_to_fb(browser):  # function for login in to fb, takes the browser object created at main()
    login_page = browser.get(login_url)  # navigates to the login url
    soup = BeautifulSoup(login_page.text, "html.parser")  # parse the html of the login page
    login_form = soup.find("form", {"id": "login_form"})  # find the form
    # print(login_form)

    login_form.find("input", {"name": "email"})["value"] = login  # find the input tag and create a value element
    login_form.find("input", {"name": "pass"})["value"] = password  # same as above

    browser.submit(login_form, login_page.url)  # submit the form
    go_home = browser.get(home)  # go navigate home

    if "friends/center" in go_home.text:  # checks if you are logged in by
        print("You are Logged in!!")
    else:  # if the string friends/center is not in within the html then we are not logged in
        print("Could not login to your account")
    # print(go_home.text)  //This is for debugging purpose


def write_groups_to_text(browser):  # write down the groups to the linea.txt file // only use it once
    groups_url = "https://m.facebook.com/groups/?seemore&refid=27"  # the base url for getting the list of groups
    get_groups = browser.get(groups_url)  # navigates to the groups_url
    soup = BeautifulSoup(get_groups.text, "html.parser")  # parse the html of the groups page
    # soup = soup.prettify()
    # with open('linea.txt', 'a') as f:  # opens linea.txt and read
    for link in soup.findAll('a'):  # gets all the links on the page
        url = link.get("href")
        with open('linea.txt', 'a') as f:  # opens linea.txt to append text
            f.write(str(url.encode(encoding='utf8')))  # writes all found url to the linea.txt file
    f.close()  # close file


def get_all_groups():  # gets only numbers from the linea file and writes them down in to a file called groups.txt
    group_list = []
    with open('linea.txt', 'r') as f:  # reads the html file 'linea.txt' which is in html
        my_s = f.readlines()
    lines = str(my_s)
    count = re.findall(r'\b\d+\b', lines)  # TODO I need to get to know what this peace of code do
    for number in count:
        if len(number) > 12:
            # print(number)
            # test = browser.get(test_group_url + number)
            # if "groups/members" in test.text:
            with open("groups.txt", 'a') as f:
                f.write(number+'\n')
            group_list.append(number)
        else:
            pass
    return group_list


def send_groups(browser, groups, receiver_id):
    send_group_url = "https://m.facebook.com/groups/members/search/?group_id="
    # name_of_input = "addees[" + str(receiver_id) + "]"

    print(groups)
    for group_id in groups:
        time.sleep(0.1)
        send_page = browser.get(send_group_url + str(group_id))
        soup = BeautifulSoup(send_page.text, "html.parser")
        checkbox_form = soup.find("form", {"method": "post"})
        try:
            # this one works without sugested_friends list
            # finds the input thats type text --- not the one with sugested friends
            checkbox_form.find('input', {"type": "text"})["checked"] = "checked"
            checkbox_form.find('input', {"type": "text"})["name"] = "addees[" + str(receiver_id) + "]"
            checkbox_form.find('input', {"type": "text"})["value"] = str(receiver_id)
            resp = browser.submit(checkbox_form, send_page.url) # use res = my_browser.submit & print response for debug
            # soup = BeautifulSoup(resp.text, "html.parser") //for debug
            # print(soup.prettify())  //for debug
            print("pasando group number: " + str(group_id))
        except Exception as e:
            # print("grupo " + group_id + " no tranferido.")
            # print(e)
            pass

# print(get_all_groups(browser))  //for debug


def main():    
    browser = mechanicalsoup.Browser()
    print("created browser")
    recibidor = int(input("Entre ID del recibidor: "))
    login_to_fb(browser)
    print("used login func, now going o getallgroups")
    # write_groups_to_text(browser)  # //Use this function only to write the down the groups to a file
    groups = get_all_groups()
    print("entering the if")
    if groups:
        print("Pasando grupos... Favor espere!  ")
        send_groups(browser, groups, recibidor)
        print("Creo que todo salio bien!!")
    print("exiting the if")


if __name__ == "__main__":
    main()
