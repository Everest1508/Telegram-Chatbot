from bs4 import BeautifulSoup
import requests

def event():
    r = requests.get("https://nationaltoday.com/what-is-today/")
    soup = BeautifulSoup(r.content,'html.parser')

    events_section = soup.find('div', class_ ='twelve-grids today-grid')
    event_elements = events_section.find_all('div', class_='title-box')

    event_list = []
    count = 0
    for event_element in event_elements:
        event_title = event_element.find('h3', class_='holiday-title').text.strip()
        if ("National" in event_title):
            event_list.append("USA "+ event_title)
        else:
            event_list.append(event_title)
        count += 1
        if count == 3:break

    return(event_list)