#! /usr/bin/env python3
import logging
import sys
from logging.handlers import RotatingFileHandler
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


def create_rotating_log(path):
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(path, maxBytes=40960, backupCount=8)
    logger.addHandler(handler)
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    return logger


def grab_player_by_team(team_url):
    log_file = "PFFDataCollection.log"
    logger = create_rotating_log(log_file)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    if sys.platform == 'win32':
        executable_path = "C:\\tools\\chromedriver"
    else:
        executable_path = "/usr/lib/chromium-browser/chromedriver"
    try:
        driver = webdriver.Chrome(executable_path=executable_path, options=options)
    except Exception as e:
        logger.info(str(e))
    driver.get(team_url)
    defense_table = "//*[@id=\"main\"]/div[3]/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[2]/div/div[1]/div/div/div"
    offense_table = "//*[@id=\"main\"]/div[3]/div/div/div[3]/div[2]/div/div/div/div/div[1]/div[2]/div/div[1]/div/div/div"
    list_of_players = grab_player_by_table(defense_table, driver, logger) + grab_player_by_table(offense_table, driver, logger)
    driver.close()
    return list_of_players


def get_player_attribute(driver, player_attribute_xpath):
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, player_attribute_xpath))).get_attribute("text")
        attribute = str(driver.find_element_by_xpath(player_attribute_xpath).text)
        return attribute
    except Exception as e:
        pass


def grab_player_by_table(table_xpath, driver, logger):
    close_xpath = "/html/body/div[2]/div/div/button"
    player_attribute_xpaths = [{"attribute_name": "rating",
                                "location": "/html/body/div[2]/div/div/div/div[2]/div[1]/div["
                                            "1]/div/div/div/div[3]"},
                               {"attribute_name": "position",
                                "location": "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[2]/div/div[1]"},
                               {"attribute_name": "rank",
                                "location": "/html/body/div[2]/div/div/div/div[2]/div[1]/div[1]/div/p"}
                               ]
    list_of_players = []
    table = driver.find_elements_by_xpath(table_xpath)
    player_number = 1
    not_last_player = True
    for row in table:
        while not_last_player:
            try:
                click_xpath = "div[" + str(player_number) + "]/div[2]/a"
                player_info = {"Name": row.find_element_by_xpath(click_xpath).text}
                row.find_element_by_xpath(click_xpath).click()
                for attribute_xpath in player_attribute_xpaths:
                    value = get_player_attribute(driver, attribute_xpath["location"])
                    if value is not None:
                        player_info[attribute_xpath["attribute_name"]] = value
                    else:
                        player_info[attribute_xpath["attribute_name"]] = "N/A"
                driver.find_element_by_xpath(close_xpath).click()
                list_of_players.append(player_info)
                player_number = player_number + 1
            except Exception as e:
                logger.info(str(e))
                not_last_player = False
    return list_of_players


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # driver_test()
    teams = [
        {"url": "https://www.pff.com/nfl/teams/houston-texans/13/roster",
         "name": "texans",
         "players": []},
        {"url": "https://www.pff.com/nfl/teams/los-angeles-chargers/27/roster",
         "name": "chargers",
         "players": []},
        {"url": "https://www.pff.com/nfl/teams/pittsburgh-steelers/25/roster",
         "name": "steelers",
         "players": []},
        {"url": "https://www.pff.com/nfl/teams/baltimore-ravens/3/roster",
         "name": "ravens",
         "players": []},
        {"url": "https://www.pff.com/nfl/teams/indianapolis-colts/14/roster",
         "name": "colts",
         "players": []}
    ]
    for team in teams:
        team["players"] = grab_player_by_team(team["url"])
    f = open("PFF" + str(time.time()) + ".json", "a")
    f.write(str(teams))
    f.close()
