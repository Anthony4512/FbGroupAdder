"""
    __author__ == Anthony Mirely

    This program takes a txt file on html that already has facebook data
    and inspect it for group and user IDs that are valid and output the ID's
    on a file in the current directory named file.txt

"""

import re
import mechanicalsoup
from bs4 import BeautifulSoup


# read a file in html and returns a list with  all possible  group and ID numbers
def get_all_groups():
    group_list = []
    unique_list = []
    with open('linea.txt', 'r') as f:  # reads the html file 'linea.txt' which is in html
        my_s = f.readlines()
    lines = str(my_s)
    count = re.findall(r'\b\d+\b', lines)  # TODO check this line
    for number in count:
        if len(number) > 9:
            if number not in group_list:
                group_list.append(number)
            else:
                pass
    for group in group_list:
        unique_list.append(group)
    return unique_list


# Takes a list of groups and return only a list of valid groups
def check_group(groups):
    valid_groups = []
    lookupUrl = "http://findmyfbid.com/"  # This is the website that validates the IDs
    fburl = "https://www.facebook.com/"

    browser = mechanicalsoup.Browser()
    login_page = browser.get(lookupUrl)
    soup = BeautifulSoup(login_page.text, "html.parser")
    login_form = soup.find("form", {"method": "POST"})
    # print(login_form)
    for group in groups:
        login_form.find("input", {"name": "url"})["value"] = fburl + group
        response = browser.submit(login_form, login_page.url)
        if "Success!" in response.text:
            # print("this is a group")
            valid_groups.append(group)
        else:
            pass
            # print("this is not a group")
    return valid_groups


def main():
    groups = get_all_groups()
    grupos_validos = check_group(groups)
    for group in grupos_validos:
        with open('file.txt', 'a') as file:
            file.write("\n" + group)


if __name__ == "__main__":
    main()
