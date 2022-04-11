import requests
from bs4 import BeautifulSoup
from time import sleep
from kafka import KafkaProducer

def fetch_raw(recipe_url):
    html = None
    print(f'Processing..{recipe_url}')
    try:
        r = requests.get(recipe_url)
        if r.status_code == 200:
            html = r.text
    except Exception as ex:
        print('Exception while accessing raw html')
        print(str(ex))
    finally:
        return html.strip()

def get_recipes():
    recipies = []
    salad_url = 'https://www.allrecipes.com/recipes/96/salad/'
    url = 'https://www.allrecipes.com/recipes/96/salad/'
    print('Accessing list')

    try:
        r = requests.get(url)
        if r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html, 'lxml')
            links = soup.select('.fixed-recipe-card__h3 a')
            idx = 0
            for link in links:

                sleep(2)
                recipe = fetch_raw(link['href'])
                recipies.append(recipe)
                idx += 1
                if idx > 2:
                    break
    except Exception as ex:
        print('Exception in get_recipes')
        print(str(ex))
    finally:
        return recipies


def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))


def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10))
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer