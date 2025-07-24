from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd


flipkartUrl = "https://www.flipkart.com/"


def scrapeHtml(html):
    laptopSoup = BeautifulSoup(html, 'html.parser')

    allLaptops = laptopSoup.css.select('a.CGtC98')

    laptopDetails = []

    for laptop in allLaptops:
        laptopTitle = laptop.css.select_one('div.yKfJKb > div.col-7-12 > div.KzDlHZ').text
        laptopConfigs = laptop.css.select('div.yKfJKb > div.col-7-12 > div._6NESgJ > ul > li')
        laptopRating = float(laptop.css.select_one('div.yKfJKb > div.col-7-12 > div._5OesEi > span > div.XQDdHH').text)
        laptopOriginalPrice = laptop.css.select_one('div.yKfJKb > div.col-5-12.BfVC2z > div.cN1yYO > div.hl05eU > div.yRaY8j.ZYYwLA').text.replace('₹', '').replace(',', '')
        laptopDiscountedPrice = laptop.css.select_one('div.yKfJKb > div.col-5-12.BfVC2z > div.cN1yYO > div.hl05eU > div.Nx9bqj._4b5DiR').text.replace('₹', '').replace(',', '')
        laptopDiscount = laptop.css.select_one('div.yKfJKb > div.col-5-12.BfVC2z > div.cN1yYO > div.hl05eU > div.UkUFwK').text.replace('%', '')
        laptopConfigText = [x.text for x in laptopConfigs]

    



        laptopData = {
            'title': laptopTitle,
            'config': laptopConfigText,
            'rating': laptopRating,
            'originalPrice': laptopOriginalPrice,
            'Discountedprice': laptopDiscountedPrice,
            'discount': laptopDiscount
            
        }
        print(laptopData)
        print('-' * 50)
        laptopDetails.append(laptopData)

    laptop_df = pd.DataFrame(laptopDetails)
    laptop_df.to_csv('laptops.csv', index=False)

def scapeflipkart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(flipkartUrl)
        
        page.wait_for_timeout(3000)

        page.screenshot(path="flipkart.png", full_page=True)
        searchInput = page.query_selector("input.Pke_EE")
        searchInput.fill("laptop")

        page.wait_for_timeout(1000)

        searchButton = page.query_selector("button._2iLD__")
        searchButton.click()
        page.wait_for_load_state('domcontentloaded')

        page.wait_for_timeout(4000)

        page.screenshot(path="flipkart_search_results.png", full_page=True)
        
        scrapeHtml(page.inner_html('body'))

scapeflipkart() 