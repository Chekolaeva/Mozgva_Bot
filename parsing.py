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


def get_last_albums_vk():
    """Получение списка альбомов группы с помощью парсинга мобильной версии
       вконтакте. Мобильные версии сайтов чаще всего проще парсить: там меньше
       мусора, в них реже меняется дизайн."""

    soup = get_soup('https://m.vk.com/albums-95512899?act=all')

    albums = []

    for link in soup.find_all('a', {'class': 'AlbumItem al_album'}):
        if link["href"].endswith("_0"):
            continue
        
        album = {
            "name": link.find('div', {"class": "AlbumItemInfo"}).find('div').text,
            "url": f'https://vk.com{link["href"]}'
        }
        
        albums.append(album)

    return albums
