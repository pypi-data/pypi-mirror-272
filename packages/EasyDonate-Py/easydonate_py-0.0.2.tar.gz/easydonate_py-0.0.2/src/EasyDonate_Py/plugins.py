import requests


def additional_payment_settings(shop_key):
    url = "https://easydonate.ru/api/v3/plugin/EasyDonate.Surcharge/getSettings"
    headers={"Shop-Key": shop_key}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Возможно плагин отключен.")
    else:
        print({'error': f"Ошибка: {response.status_code}"})
def additional_payment_user(shop_key, username):
    url = "https://easydonate.ru/api/v3/plugin/EasyDonate.Surcharge/getDiscounts"
    headers={"Shop-Key": shop_key}
    params={'username': username}
    response = requests.get(url=url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Возможно плагин отключен.")
    else:
        print({'error': f"Ошибка: {response.status_code}"})
def additional_payment_id(shop_key, username, product_id):
    url = "https://easydonate.ru/api/v3/plugin/EasyDonate.Surcharge/getDiscounts"
    headers={"Shop-Key": shop_key}
    params={'username': username, 'product_id': product_id}
    response = requests.get(url=url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Возможно плагин отключен.")
    else:
        print({'error': f"Ошибка: {response.status_code}"})


def last_payments_settings(shop_key):
    url = "https://easydonate.ru/api/v3/plugin/EasyDonate.LastPayments/getSettings"
    headers={"Shop-Key": shop_key}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Возможно плагин отключен.")
    else:
        print({'error': f"Ошибка: {response.status_code}"})
def last_payments_get(shop_key):
    url = "https://easydonate.ru/api/v3/plugin/EasyDonate.LastPayments/getPayments"
    headers={"Shop-Key": shop_key}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Возможно плагин отключен.")
    else:
        print({'error': f"Ошибка: {response.status_code}"})


def custom_message_settings(shop_key):
    url = "https://easydonate.ru/api/v3/plugin/EasyDonate.CustomMessages/getSettings"
    headers={"Shop-Key": shop_key}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Возможно плагин отключен.")
    else:
        print({'error': f"Ошибка: {response.status_code}"})


def discord_widget_settings(shop_key):
    url = "https://easydonate.ru/api/v3/plugin/Discord.Widget/getSettings"
    headers={"Shop-Key": shop_key}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Возможно плагин отключен.")
    else:
        print({'error': f"Ошибка: {response.status_code}"})
def discord_widget_get(shop_key):
    url = "https://easydonate.ru/api/v3/plugin/Discord.Widget/getEmbed"
    headers={"Shop-Key": shop_key}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Возможно плагин отключен.")
    else:
        print({'error': f"Ошибка: {response.status_code}"})


def vk_widget_settings(shop_key):
    url = "https://easydonate.ru/api/v3/plugin/Vkontakte.Widget/getSettings"
    headers={"Shop-Key": shop_key}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Возможно плагин отключен.")
    else:
        print({'error': f"Ошибка: {response.status_code}"})
def vk_widget_get(shop_key):
    url = "https://easydonate.ru/api/v3/plugin/Vkontakte.Widget/getEmbed"
    headers={"Shop-Key": shop_key}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Возможно плагин отключен.")
    else:
        print({'error': f"Ошибка: {response.status_code}"})
def vk_news_settings(shop_key):
    url = "https://easydonate.ru/api/v3/plugin/Vkontakte.News/getSettings"
    headers={"Shop-Key": shop_key}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Возможно плагин отключен.")
    else:
        print({'error': f"Ошибка: {response.status_code}"})
def vk_news_get(shop_key):
    url = "https://easydonate.ru/api/v3/plugin/Vkontakte.News/getNews"
    headers={"Shop-Key": shop_key}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Возможно плагин отключен.")
    else:
        print({'error': f"Ошибка: {response.status_code}"})
def vk_messages_settings(shop_key):
    url = "https://easydonate.ru/api/v3/plugin/Vkontakte.MessagesWidget/getSettings"
    headers={"Shop-Key": shop_key}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Возможно плагин отключен.")
    else:
        print({'error': f"Ошибка: {response.status_code}"})
def vk_messages_widget(shop_key):
    url = "https://easydonate.ru/api/v3/plugin/Vkontakte.MessagesWidget/getEmbed"
    headers={"Shop-Key": shop_key}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Возможно плагин отключен.")
    else:
        print({'error': f"Ошибка: {response.status_code}"})


def yandex_metrika_settings(shop_key):
    url = "https://easydonate.ru/api/v3/plugin/Yandex.Metrika/getSettings"
    headers={"Shop-Key": shop_key}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Возможно плагин отключен.")
    else:
        print({'error': f"Ошибка: {response.status_code}"})
def yandex_metrika_widget(shop_key):
    url = "https://easydonate.ru/api/v3/plugin/Yandex.Metrika/getEmbed"
    headers={"Shop-Key": shop_key}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Возможно плагин отключен.")
    else:
        print({'error': f"Ошибка: {response.status_code}"})