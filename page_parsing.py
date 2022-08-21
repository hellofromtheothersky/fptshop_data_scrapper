import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import re


def split_(s, delimeter=None):
    # test='   nguyen \n\n\n\n hung       \n\n    trung   \n hieu la toi   \n   '
    return [x.strip() for x in s.strip().split(delimeter) if x]


def create_web_driver(url, wait_condition_classname_clickable=""):
    edgedriver_path = "msedgedriver.exe"
    options = Options()
    # options.page_load_strategy = "eager"  # get only html DOM, but not working well
    options.headless = True
    # options.add_argument("--disable-web-security") #to pass the CORS in some situations
    driver = webdriver.Edge(executable_path=edgedriver_path, options=options)
    driver.get(url)
    if wait_condition_classname_clickable != "":
        try: 
            element = WebDriverWait(driver, 4).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, wait_condition_classname_clickable)
                )
            )
        except TimeoutException:
            raise NoSuchElementException
    return driver


def get_content(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e) from None
    else:
        return r.content


class any_elements_has_text(object):
    # Custom Wait Conditions
    def __init__(self, locator, text):
        self.locator = locator
        self.text = text

    def __call__(self, driver):
        elements = driver.find_elements(*self.locator)  # note
        for element in elements:
            if self.text in element.text:
                return element
        return False


def get_products_overview(url):
    driver = create_web_driver(url)
    button = any_elements_has_text((By.CLASS_NAME, "view-more"), "Xem thêm")(driver)
    if button != False:
        button.click()
        wait = WebDriverWait(driver, 10)
        while "can click button":
            try:
                button = wait.until(
                    any_elements_has_text((By.CLASS_NAME, "view-more"), "Xem thêm")
                )
            except:
                # run out of time
                break
            else:
                print("+1 Page: ", button.text)
                button.click()

    soup = BeautifulSoup(driver.page_source, features="lxml")
    driver.close()

    temp = soup.select("div.mc-lpcol > a")  # link may
    links = ["https://fptshop.com.vn/" + k["href"] for k in temp]
    temp = soup.select("span.mc-lpttm-i")  # so luong may cu
    num_of_old_prod = [k.string for k in temp]
    temp = soup.select("h3.mc-lpiname > a")  # ten may
    names = [k.string for k in temp]
    temp = soup.select("p.mc-lpri1")  # gia may moi
    prices = [re.search(r"[0-9.]+", k.string).group(0) for k in temp]

    return list(
        map(
            lambda x, y, z, t: {"Tên": x, "Link": y, "Giá": z, "SL máy cũ": t},
            names,
            links,
            prices,
            num_of_old_prod,
        )
    )


def get_product_detail(url):
    def get_configuration():
        button = driver.find_element(By.CLASS_NAME, "st-pd-table-viewDetail")
        button.click()
        soup = BeautifulSoup(driver.page_source, features="lxml")
        row = {}
        for table in soup.find("div", class_="c-modal__content").find_all("table"):
            group_name = ""
            e = table
            while True:
                e = e.parent
                try:
                    p = e.find(
                        "div", class_="st-table-title", recursive=False
                    ).text.strip()
                    group_name = p + "." + group_name
                except AttributeError:
                    pass
                if e.get("class")[0] == "c-modal__row":
                    break
            for info in table.find_all("tr"):
                criteria = info.td.text.strip()
                content = info.td.nextSibling.findAll(text=True)
                row[group_name + criteria] = ", ".join(content)
        return row

    driver = create_web_driver(url, "st-pd-table-viewDetail")
    soup = BeautifulSoup(driver.page_source, features="lxml")
    #with open("temp.txt", "w", encoding="utf-8") as f:
    #    f.write(soup.prettify())
    # get laptop name, price
    row = get_configuration()
    driver.close()
    return row


#s=get_product_detail('https://fptshop.com.vn/may-tinh-xach-tay/lenovo-ideapad-slim-5-15itl05-i5-1135g7')
#print(s)
# create_web_driver("https://fptshop.com.vn/may-tinh-xach-tay/lenovo-ideapad-slim-5-15itl05-i5-1135g7")
