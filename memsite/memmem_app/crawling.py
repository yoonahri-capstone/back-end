from bs4 import BeautifulSoup
from selenium import webdriver
import tldextract
import time

# URL = "https://www.instagram.com/p/B-lp4yghq5F/?utm_source=ig_web_copy_link"
# URL = "https://www.facebook.com/518619241508393/posts/2827717197265241/?sfnsn=mo"
# URL = "https://m.blog.naver.com/binhs9576/221788249228"
# URL = "https://www.youtube.com/watch?v=2dNc8ROMVlw"

global driver, URL, html, soup


def url_crawl(soup):
    save_list = []
    CURRENT_URL = driver.current_url
    extracted = tldextract.extract(URL)
    print(extracted)
    extracted_current_url = tldextract.extract(CURRENT_URL)
    print(extracted_current_url)
    domain = extracted.domain

    if domain == 'instagram':
        if "비공개 계정입니다" in soup.find('h2', {"class": "rkEop"}):
            return None

    if domain == 'naver' and extracted.suffix == 'me' and extracted_current_url.subdomain == 'blog':
        driver.switch_to.frame('mainFrame')
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

    try :
        title = soup.head.title.text
        title = title.replace('\n', ' ')

        try:
            thumbnail = soup.find("meta", {"property": "og:image"}).get("content")
        except:
            thumbnail = None
        save_list.append(URL)
        save_list.append(title)
        save_list.append(thumbnail)
        save_list.append(extracted.domain)

    except Exception as e:
        print(e)
        return None

    return save_list


def youtube_hashtag():
    all_hashtag = soup.find_all("a", {"class": "yt-simple-endpoint style-scope yt-formatted-string"})
    hashtag = [soup.find_all("a", {"class": "yt-simple-endpoint style-scope yt-formatted-string"})[n].string for n in range(0, len(all_hashtag))]
    # print(hashtag)
    return hashtag


def naver_hashtag():
    all_hashtag = soup.find_all("span", {"class": "ell"})
    hashtag = [soup.find_all("span", {"class": "ell"})[n].string for n in range(0, len(all_hashtag))]
    # print(hashtag)
    return hashtag


def facebook_hashtag():
    all_hashtag = soup.find('div', "_1dwg _1w_m _q7o").find_all("span", {"class": "_58cm"})
    hashtag = [soup.find('div', "_1dwg _1w_m _q7o").find_all("span", {"class": "_58cm"})[n].string for n in range(0, len(all_hashtag))]
    # print(hashtag)
    return hashtag


def instagram_hashtag():
    check_comment = len(driver.find_elements_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div[2]/div[1]/ul/ul[1]/li/ul/li/div/button/span")) > 0
    if check_comment:
        driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div[1]/ul/ul[1]/li/ul/li/div/button/span").click()
        time.sleep(0.5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        all_hashtag = soup.find_all("a", {"class": "xil3i"})
        hashtag = [soup.find_all("a", {"class": "xil3i"})[n].string for n in range(0, len(all_hashtag))]
    else:
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        all_hashtag = soup.find_all("a", {"class": "xil3i"})
        hashtag = [soup.find_all("a", {"class": "xil3i"})[n].string for n in range(0, len(all_hashtag))]
    # print(hashtag)
    return hashtag


def hashtag_crawl():
    hashtags = []
    extracted = tldextract.extract(URL)
    if extracted.domain == 'youtube':
        hashtags = youtube_hashtag()
    elif extracted.domain == 'youtu':
        hashtags = youtube_hashtag()
    elif extracted.domain == 'naver':
        hashtags = naver_hashtag()
    elif extracted.domain == 'facebook':
        hashtags = facebook_hashtag()
    elif extracted.domain == 'instagram':
        hashtags = instagram_hashtag()
    hashtags = list(set(hashtags))  #중복제거
    hashtag_list = []
    for hashtag in hashtags:        #"#"없는 항목 제거
        if "#" in hashtag:
            hashtag_list.append(hashtag)
    return hashtag_list


def crawl_request(request):
    global driver, URL, html, soup

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome('C:/Users/yoonhee/Desktop/back-end3/back-end/memsite/memmem_app/chromedriver.exe', options=chrome_options)

    # no error 가정
    URL = request
    driver.get(URL)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    save_list = url_crawl(soup)
    hash_list = hashtag_crawl()

    if len(hash_list) > 0:
        return save_list + hash_list
    else:
        return save_list