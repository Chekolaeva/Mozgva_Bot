def game_info_str(info):
    """Сформировать строку, содержащую информацию об одной игре"""
    message = f'*{info["title"]}*\n{info["place"]}\n{info["date"]}\n{info["week_day"]}\n[Регистрация]({info["reg_url"]})'
    return message


def form_sched_str(schedule):
    """Формирует итоговую строку с расписанием всех игр
    (функция, формирующая строку для одной игры повторяется в цикле)
    """
    message = 'Расписание игр:\n\n'
    for game in schedule:
        message += game_info_str(game) + '\n\n'
    return message


def form_rating(rating_data):
    """Формирует строку с сообщением о рейтинге команд"""
    message = 'Рейтинг:\n\n'
    for team in rating_data:
        message += f'{team["position"]}. {team["name"]} {team["percentage"]}\n' 
    return message


def form_albums_vk(albums):
    message = '**Фотографии с игр**\\n\\n'
    for album in albums:
        message += f'• [{album["name"]}]({album["url"]})\n'

    return message
