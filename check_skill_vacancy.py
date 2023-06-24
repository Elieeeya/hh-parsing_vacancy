import json
import requests
import fake_useragent
from bs4 import BeautifulSoup
import time


def get_links(text):
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=f'https://hh.ru/search/vacancy?text={text}&from=suggest_post&salary=&area=1&professional_role=124&ored_clusters=true&page=1',
        headers={"user-agent": ua.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, "lxml")
    try:
        page_count = int(
            soup.find("div", attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("a").find(
                "span").text)
    except:
        return
    for page in range(page_count):
        try:
            data = requests.get(
                url=f'https://hh.ru/search/vacancy?text={text}&from=suggest_post&salary=&area=1&professional_role=124&ored_clusters=true&page={page}',
                headers={"user-agent": ua.random}
            )
            if data.status_code != 200:
                continue
            soup = BeautifulSoup(data.content, "lxml")
            for a in soup.find_all("a", attrs={"class": "serp-item__title"}):
                full_url = f"{a.attrs['href'].split('?')[0]}"
                # print(full_url)
                yield full_url
        except Exception as e:
            print(f"{e}")
            time.sleep(1)


def get_vacancy(link):
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=link,
        headers={"user-agent": ua.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, "lxml")
    try:
        name = soup.find(attrs={"class": "bloko-header-section-1"}).text
    except:
        name = ""
    try:
        skills = [skill.text for skill in
                  soup.find(attrs={"class": "bloko-tag-list"}).find_all(attrs={"class": "bloko-tag__section_text"})]
    except:
        skills = []
    vacancy = {
        "name": name,
        "skills": skills
    }
    return vacancy


if __name__ == "__main__":
    data = []
    # для поиска инфы, для тругих специльности необходимо изменить значение в get_links
    for a in get_links("Qa+engineer"):
        data.append(get_vacancy(a))
        time.sleep(1)
        with open("Qa engineer.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
