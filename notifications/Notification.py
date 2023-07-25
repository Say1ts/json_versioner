import requests


class Notification:
    def __init__(self, url):
        self.url = url

    def notify(self, user, message: dict) -> bool:
        try:
            response = requests.post(self.url + str(user), json=message)
            if response.status_code == 200:
                return True
            print('Не удалось отправить уведомление пользователю. Код ошибки:', response.status_code)
            return False
        except Exception as e:
            print(e, '\nНе удалось отправить уведомление пользователю')
            return False


notification_server_url = 'http://localhost:33020/notify/'
notificator = Notification(notification_server_url)
