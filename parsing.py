import requests
from bs4 import BeautifulSoup


def get_soup(url):
    page = requests.get(url).text
    return BeautifulSoup(page, 'html.parser')


def get_sched():
    soup = get_soup("https://mozgva.com/calendar")

    # создаем объект (экземпляр класса BeautifulSoup)
    # .find() - метод, позволяющий получить один блок html кода (с заданными критериями)
    games_info = soup.find_all('div', {'class':'itemGame-new2'})

    games = []

    # обрабатываем код html о каждой игре

    for item in games_info:
        
        game_id = item.find('div', {'class': 'game_id'}).text.split("#")[-1]

        game = {
            "title": item.find('div', {'class': 'name'}).text.strip(),
            "place": item.find('a', {'class': 'hide-mobile'}).text.strip(),
            "date": item.find('span', {'class': 'date_m'}).text.strip(),
            "week_day": item.find('span', {'class': 'day'}).text.strip(),
            "time": item.find('div', {'class': 'time'}).text.strip(),
            "reg_url": f"https://mozgva.com/calendar?game_id={game_id}#quick_registration_modal"
        }

        # получившийся словарь добавляем в итоговый список
        games.append(game)

    return games


def get_rating():
    """Получает данные о рейтинге команд (возвращает список словарей)"""
    soup = get_soup('https://mozgva.com/rating') 

    teams = []

    # id элемента (должен быть) уникальным во всем документе, к нему можно привязаться
    for row in soup.find(id='winnersScroll').find_all('tr'):
        # Строка (тэг tr), которая лежит в тэге thead (у которой родительский элемент - тэг thead)
        # <thead> <tr> ... </tr> </thead>
        # является заголовком таблицы, она нам не нужна, пропускаем и переходим к
        # следующей итерации (инструкцией continue)
        if row.parent.name == 'thead':
            continue

        tname = row.find("td", {"class": "tName"})

        team = {
            # Перед ссылкой на команду могут быть кнопки с наградами, которые тоже
            # ссылки <a>. Ищем все, берем последнюю, в ней название команды.
            'name': tname.find_all('a')[-1].text,
            'position': tname.find('span', {"class": "position"}).text.rstrip('.'),
            'percentage': row.find('td', {"class": "tPercent"}).text
        }

        teams.append(team)

    return teams
