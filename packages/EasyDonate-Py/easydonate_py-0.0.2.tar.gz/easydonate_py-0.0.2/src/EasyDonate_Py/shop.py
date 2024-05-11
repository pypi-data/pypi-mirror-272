import requests


def shop_info(shop_key):
    url = "https://easydonate.ru/api/v3/shop"
    headers={"Shop-Key": shop_key}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Не найдена информация!")
    else:
        print({'error': f"Ошибка: {response.status_code}"})


def get_products(shop_key):
    url = "https://easydonate.ru/api/v3/shop/products"
    headers={"Shop-Key": shop_key}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Не найдена информация!")
    else:
        print({'error': f"Ошибка: {response.status_code}"})

def get_product(shop_key, id):
    url = f"https://easydonate.ru/api/v3/shop/product/{id}"
    headers={"Shop-Key": shop_key}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Не найдена информация!")
    else:
        print({'error': f"Ошибка: {response.status_code}"})


def get_servers(shop_key):
    url = "https://easydonate.ru/api/v3/shop/servers"
    headers={"Shop-Key": shop_key}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Не найдена информация!")
    else:
        print({'error': f"Ошибка: {response.status_code}"})

def get_server(shop_key, id):
    url = f"https://easydonate.ru/api/v3/shop/server/{id}"
    headers={"Shop-Key": shop_key}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Не найдена информация!")
    else:
        print({'error': f"Ошибка: {response.status_code}"})


def mass_sales(shop_key):
    url = "https://easydonate.ru/api/v3/shop/massSales"
    headers={"Shop-Key": shop_key}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Не найдена информация!")
    else:
        print({'error': f"Ошибка: {response.status_code}"})

def coupons(shop_key, where_active):
    url = f"https://easydonate.ru/api/v3/shop/coupons"
    headers={"Shop-Key": shop_key}
    params = {
        'where_active': where_active
    }
    if where_active:
        response = requests.get(url=url, headers=headers, params=params)
    else:
        response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Не найдена информация!")
    else:
        print({'error': f"Ошибка: {response.status_code}"})


def payments(shop_key):
    url = "https://easydonate.ru/api/v3/shop/payments"
    headers={"Shop-Key": shop_key}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Не найдена информация!")
    else:
        print({'error': f"Ошибка: {response.status_code}"})
        
def payment(shop_key, id):
    url = f"https://easydonate.ru/api/v3/shop/payment/{id}"
    headers={"Shop-Key": shop_key}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Не найдена информация!")
    else:
        print({'error': f"Ошибка: {response.status_code}"})

def create_payment(shop_key, customer, server_id, products, email, coupon, success_url):
    url = "https://easydonate.ru/api/v3/shop/payment/create"
    headers={"Shop-Key": shop_key}
    params = {
        'customer': customer,
        'server_id': server_id,
        'products': products
    }
    if email:
        params['email'] = email
    if coupon:
        params['coupon'] = coupon
    if success_url:
        params['success_url'] = success_url
    response = requests.get(url=url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["success"] == "true":
            return data
        else:
            print("Не найдена информация или неправильно введены параметры.")
    else:
        print({'error': f"Ошибка: {response.status_code}"})