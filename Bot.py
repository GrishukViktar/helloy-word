from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from data import username, password
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import random


class InstagramBot():
    """Instagram Bot на Python"""

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome("../chromedriver/chromedriver")

    def close_browser(self):

        self.browser.close()
        self.browser.quit()
# Метод логина

    def login(self):

        browser = self.browser
        browser.get('https://www.instagram.com')
        time.sleep(random.randrange(3, 5))

        username_input = browser.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(2)

        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)
        time.sleep(10)
#Ставит лайки по хештегам
        
        def like_photo_by_hashtag(self, hashtag):
            
            browser = self.browser
            browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
            time.sleep(5)

            for i in range(1, 4):
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(3, 5))

            hrefs = browser.find_elements_by_tag_name('a')
            posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]


            for url in posts_urls:
                try:
                    browser.get(url)
                    time.sleep(3)
                    like_button = browser.find_element_by_xpath(
                        '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
                    time.sleep(random.randrange(80, 100))
                except Exception as ex:
                    print(ex)
                    self.cloes_browser()
# проверяем по хpath существует ли элемент на странице
    
    def xpath_exists(self, url):

        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

#Метод собирает все сыллкаи на посты пльзователя
    def get_all_post_urls(self, userpage):
        browser = self.browser
        browser.get(userpage)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого пользователя нету!")
            self.close_browser()
        else:
            print("пользователь успешно найден, ставим лайк!")
            time.sleep(2)

            post_count = int(browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[1]/div/span").text)
            loops_count = int(post_count / 12)
            print(loops_count)

            posts_urls = []
            for i in range(0, loops_count):
                hrefs = browser.find_elements_by_tag_name('a')
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')
                         ]
                for href in hrefs:
                    posts_urls.append(href)

                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(3, 5))
                print(f" Итерация #{i}")

            file_name = userpage.split("/")[-2]

            with open(f'{file_name}.txt', 'a') as file:
                for post_url in posts_urls:
                    file.write(post_url + "\n")

            set_posts_urls = set(posts_urls)
            set_posts_urls = list(set_posts_urls)

            with open(f'{file_name}_set.txt', 'a') as file:

                for post_url in set_posts_urls:
                    file.write(post_url + '\n')



# ставим лайки на посты по прямой ссылке
    
    def put_exactly_like(self, userpost):

        browser = self.browser
        browser.get(userpost)
        time.sleep(5)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого пользователя нету!")
            self.close_browser()
        else:
            print("пользователь успешно найден, ставим лайк!")
            time.sleep(2)

            like_button = "/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button/div/span/svg/path"
            browser.find_element_by_xpath(like_button).click()

            print(f"Лайк на пост: {userpost} поставлен!")
            self.close_browser()

    def put_many_likes(self, userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого пользователя нету!")
            self.close_browser()
        else:
            print("пользователь успешно найден, ставим лайк!")
            time.sleep(2)

            post_count = int(browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[1]/div/span").text)
            loops_count = int(post_count / 12)
            print(loops_count)

            posts_urls = []
            for i in range(0, loops_count):
                hrefs = browser.find_elements_by_tag_name('a')
                hrefs = [item.get_attribute('href')for item in hrefs if "/p/" in item.get_attribute('href')
                         ]
                for href in hrefs:
                    posts_urls.append(href)

                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(3, 5))
                print(f" Итерация #{i}")

            file_name = userpage.split("/")[-2]

            with open(f'{file_name}.txt', 'a') as file:
                for post_url in posts_urls:
                    file.write(post_url + "\n")

            set_posts_urls = set(posts_urls)
            set_posts_urls = list(set_posts_urls)


            with open(f'{file_name}_set.txt', 'a') as file:

                for post_url in set_posts_urls:
                    file.write(post_url + '\n')

            with open(f'{file_name}_set.txt') as file:
                urls_list = file.readlines()

                for post_url in urls_list:
                    try:
                        browser.get(post_url)
                        time.sleep(2)

                        #like_button = "/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/button"
                       # browser.find_element(By.XPATH, """like_button""").click()
                        #time.sleep(random.randrange(80, 100))
                        time.sleep(2)

                        print(f"Лайк на пост: {post_url} успешно поставлен!")
                    except Exception as ex:
                        print(ex)
                        self.close_browser()

            self.close_browser()

my_bot = InstagramBot(username, password)
my_bot.login()
my_bot.put_many_likes("https://www.instagram.com/xoxo.english/")







