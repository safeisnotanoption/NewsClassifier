import lxml.html
import lxml.html.soupparser
import lxml.etree
from tqdm import tqdm
from aiohttp import ClientSession
import itertools as it
import asyncio
import urllib.parse
import sqlite3
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
import numpy
import pickle


db = sqlite3.connect('Database.db')
db.execute("CREATE TABLE IF NOT EXISTS fontanka (id INTEGER PRIMARY KEY UNIQUE NOT NULL, article TEXT, category TEXT)")


async def get_page(url, session):
    try:
        async with session.get(url) as response:
            return await response.read()
    except Exception:
        return '<html></html>'


async def get_pages(urls):
    tasks = []
    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(get_page(url, session))
            tasks.append(task)
        return await asyncio.gather(*tasks)


async def grab():
    years_urls = list(map(lambda y: 'http://www.fontanka.ru/fontanka/arc/' + str(y) + '/all.html', (2015, 2017)))
    years_pages = map(lxml.html.fromstring, await get_pages(years_urls))
    days_urls = list(it.chain.from_iterable(map(lambda y: y.xpath('//table[contains(@class, \'blank_year\')]//a/@href'), years_pages)))
    days_urls = list(map(lambda u: urllib.parse.urljoin('http://www.fontanka.ru/', u), days_urls))
    del years_pages
    days_pages = map(lxml.html.fromstring, await get_pages(days_urls))
    news_urls = list(it.chain.from_iterable(map(lambda y: y.xpath('//div[contains(@class, \'calendar-item-title\')]/a/@href'), days_pages)))
    news_urls = list(map(lambda u: urllib.parse.urljoin('http://www.fontanka.ru/', u), news_urls))
    del days_pages
    k = len(news_urls) // 1000
    for j in tqdm(range(k)):
        news_pages = list(map(lxml.html.fromstring, await get_pages(news_urls[j * 1000:(j + 1) * 1000])))
        categories = map(lambda p: p.xpath('normalize-space(//div[contains(@class, \'article_cat\')])'), news_pages)
        articles = map(lambda p: p.xpath('normalize-space(//div[contains(@class, \'article_fulltext\')])'), news_pages)
        db.executemany('INSERT INTO fontanka (article, category) VALUES (?, ?)', zip(articles, categories))
        db.commit()


def clear_the_database():
    db.execute('DELETE FROM fontanka WHERE trim(category) = "" OR trim(article) = ""')
    db.execute('DELETE FROM fontanka WHERE category = "Хорошо! Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Финансы Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Туризм Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Технологии Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Точка опоры"')
    db.execute('DELETE FROM fontanka WHERE category = "Территория права"')
    db.execute('DELETE FROM fontanka WHERE category = "Театральная гостиная"')
    db.execute('DELETE FROM fontanka WHERE category = "Строительство Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Спроси сам"')
    db.execute('DELETE FROM fontanka WHERE category = "СПб - 2014 в людях и цифрах"')
    db.execute('DELETE FROM fontanka WHERE category = "Русфонд"')
    db.execute('DELETE FROM fontanka WHERE category = "Рецепты шеф-поваров"')
    db.execute('DELETE FROM fontanka WHERE category = "Ретро-советы"')
    db.execute('DELETE FROM fontanka WHERE category = "Расскажи о солдате"')
    db.execute('DELETE FROM fontanka WHERE category = "Пресс-релизы"')
    db.execute('DELETE FROM fontanka WHERE category = "Петербург.LIVE"')
    db.execute('DELETE FROM fontanka WHERE category = "Открытое письмо Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Общество Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Новости компаний Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Недвижимость Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Материнский инстинкт"')
    db.execute('DELETE FROM fontanka WHERE category = "Личная жизнь Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Лахта центр"')
    db.execute('DELETE FROM fontanka WHERE category = "Культурный поводырь"')
    db.execute('DELETE FROM fontanka WHERE category = "Итоги недели с Константиновым"')
    db.execute('DELETE FROM fontanka WHERE category = "ЗЕНИТУ 90 ЛЕТ"')
    db.execute('DELETE FROM fontanka WHERE category = "Деньги Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Город Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Говорим и показываем"')
    db.execute('DELETE FROM fontanka WHERE category = "Водитель Петербурга Live"')
    db.execute('DELETE FROM fontanka WHERE category = "Водитель Петербурга"')
    db.execute('DELETE FROM fontanka WHERE category = "Вкус жизни"')
    db.execute('DELETE FROM fontanka WHERE category = "В Теме"')
    db.execute('DELETE FROM fontanka WHERE category = "Бизнес-трибуна Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Бизнес в кризис"')
    db.execute('DELETE FROM fontanka WHERE category = "Бизнес Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Афиша Plus"')
    db.execute('DELETE FROM fontanka WHERE category = "Адвита"')
    db.execute('DELETE FROM fontanka WHERE category = ""')
    db.execute('DELETE FROM fontanka WHERE category = "NULL"')
    db.execute('DELETE FROM fontanka WHERE category = "47новостей из Ленинградской Области"')
    db.execute('DELETE FROM fontanka WHERE category = "Эксперты"')
    db.execute('DELETE FROM fontanka WHERE category = "Экипаж"')
    db.execute('DELETE FROM fontanka WHERE category = "Хорошо! Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Хорошо!"')
    db.execute('DELETE FROM fontanka WHERE category = "Фото"')
    db.execute('DELETE FROM fontanka WHERE category = "Фонтанка.fi"')
    db.execute('DELETE FROM fontanka WHERE category = "Авто Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Адвита"')
    db.execute('DELETE FROM fontanka WHERE category = "Андрей Заостровцев"')
    db.execute('DELETE FROM fontanka WHERE category = "Афиша Plus"')
    db.execute('DELETE FROM fontanka WHERE category = "Бизнес Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Бизнес в кризис"')
    db.execute('DELETE FROM fontanka WHERE category = "Бизнес-трибуна Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Большое интервью"')
    db.execute('DELETE FROM fontanka WHERE category = ""')
    db.execute('DELETE FROM fontanka WHERE category = "Андрей Заостровцев"')
    db.execute('DELETE FROM fontanka WHERE category = "В Теме"')
    db.execute('DELETE FROM fontanka WHERE category = "Видео"')
    db.execute('DELETE FROM fontanka WHERE category = "Водитель Петербурга.Live"')
    db.execute('DELETE FROM fontanka WHERE category = "Год N300"')
    db.execute('DELETE FROM fontanka WHERE category = "Квадрат"')
    db.execute('DELETE FROM fontanka WHERE category = "Конкурсы"')
    db.execute('DELETE FROM fontanka WHERE category = "Контур культуры"')
    db.execute('DELETE FROM fontanka WHERE category = "Лушников"')
    db.execute('DELETE FROM fontanka WHERE category = "Марианна Баконина"')
    db.execute('DELETE FROM fontanka WHERE category = "Новости компаний"')
    db.execute('DELETE FROM fontanka WHERE category = "Опасная передача"')
    db.execute('DELETE FROM fontanka WHERE category = "Охта центр"')
    db.execute('DELETE FROM fontanka WHERE category = "Профессионал"')
    db.execute('DELETE FROM fontanka WHERE category = "Реклама"')
    db.execute('DELETE FROM fontanka WHERE category = "Театры"')
    db.execute('DELETE FROM fontanka WHERE category = "Фото"')
    db.execute('DELETE FROM fontanka WHERE category = "Хорошо!"')
    db.execute('DELETE FROM fontanka WHERE category = "Хорошо! Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Авто Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Домашний очаг"')
    db.execute('DELETE FROM fontanka WHERE category = "ЖКХ Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Открытое письмо Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Пока все в офисе"')
    db.execute('DELETE FROM fontanka WHERE category = "Расскажи о солдате"')
    db.execute('DELETE FROM fontanka WHERE category = "Федор Погорелов"')
    db.execute('DELETE FROM fontanka WHERE category = "Эксперты"')
    db.execute('DELETE FROM fontanka WHERE category = "Большое интервью"')
    db.execute('DELETE FROM fontanka WHERE category = "Вкус жизни"')
    db.execute('DELETE FROM fontanka WHERE category = "Власть Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Доктор Питер"')
    db.execute('DELETE FROM fontanka WHERE category = "Итоги недели с Андреем Константиновым"')
    db.execute('DELETE FROM fontanka WHERE category = "Итоги недели с Константиновым"')
    db.execute('DELETE FROM fontanka WHERE category = "Первая страница"')
    db.execute('DELETE FROM fontanka WHERE category = "Ретро-советы"')
    db.execute('DELETE FROM fontanka WHERE category = "Рецепты шеф-поваров"')
    db.execute('DELETE FROM fontanka WHERE category = "Среда джаза с Давидом Голощекиным"')
    db.execute('DELETE FROM fontanka WHERE category = "Театральная гостиная"')
    db.execute('DELETE FROM fontanka WHERE category = "Тревожный город"')
    db.execute('DELETE FROM fontanka WHERE category = "Водитель Петербурга Live"')
    db.execute('DELETE FROM fontanka WHERE category = "Выставки"')
    db.execute('DELETE FROM fontanka WHERE category = "Петербург.LIVE"')
    db.execute('DELETE FROM fontanka WHERE category = "Происшествия Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Книги"')
    db.execute('DELETE FROM fontanka WHERE category = "Очевидец"')
    db.execute('DELETE FROM fontanka WHERE category = "Экипаж"')
    db.execute('DELETE FROM fontanka WHERE category = "Адвита"')
    db.execute('DELETE FROM fontanka WHERE category = "Территория права"')
    db.execute('DELETE FROM fontanka WHERE category = "Доступная среда"')
    db.execute('DELETE FROM fontanka WHERE category = "Культурный поводырь"')
    db.execute('DELETE FROM fontanka WHERE category = "Бизнес в кризис"')
    db.execute('DELETE FROM fontanka WHERE category = "Здоровье и красота"')
    db.execute('DELETE FROM fontanka WHERE category = "Кино"')
    db.execute('DELETE FROM fontanka WHERE category = "Пресс-релизы"')
    db.execute('DELETE FROM fontanka WHERE category = "СПб - 2014 в людях и цифрах"')
    db.execute('DELETE FROM fontanka WHERE category = "Спорт Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Теракты"')
    db.execute('DELETE FROM fontanka WHERE category = "Материнский инстинкт"')
    db.execute('DELETE FROM fontanka WHERE category = "Музыка"')
    db.execute('DELETE FROM fontanka WHERE category = "Викторины"')
    db.execute('DELETE FROM fontanka WHERE category = "Личная жизнь Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Мужчина и женщина"')
    db.execute('DELETE FROM fontanka WHERE category = "Новый год"')
    db.execute('DELETE FROM fontanka WHERE category = "Фонтанка-SUP"')
    db.execute('DELETE FROM fontanka WHERE category = "ЗЕНИТУ 90 ЛЕТ"')
    db.execute('DELETE FROM fontanka WHERE category = "Новости компаний Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Финансы Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Фонтанка.Office"')
    db.execute('DELETE FROM fontanka WHERE category = "Афиша Plus"')
    db.execute('DELETE FROM fontanka WHERE category = "Лахта центр"')
    db.execute('DELETE FROM fontanka WHERE category = "Водитель Петербурга"')
    db.execute('DELETE FROM fontanka WHERE category = "Фонтанка.fi"')
    db.execute('DELETE FROM fontanka WHERE category = "День Победы"')
    db.execute('DELETE FROM fontanka WHERE category = "Личная жизнь"')
    db.execute('DELETE FROM fontanka WHERE category = "Недвижимость Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Туризм Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Спроси сам"')
    db.execute('DELETE FROM fontanka WHERE category = "Русфонд"')
    db.execute('DELETE FROM fontanka WHERE category = "Дороги"')
    db.execute('DELETE FROM fontanka WHERE category = "Говорим и показываем"')
    db.execute('DELETE FROM fontanka WHERE category = "Бизнес-трибуна Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Точка опоры"')
    db.execute('DELETE FROM fontanka WHERE category = "Общество Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Бизнес Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Технологии Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "47новостей из Ленинградской Области"')
    db.execute('DELETE FROM fontanka WHERE category = "Город Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category = "Деньги Публикуется на правах рекламы"')
    db.execute('DELETE FROM fontanka WHERE category IS NULL')
    db.commit()


print("Download start")
asyncio.get_event_loop().run_until_complete(asyncio.ensure_future(grab()))
print("Download complete")
print("Clean start")
clear_the_database()
print("Clean complete")
print("Tokenization start")
rows = db.execute('SELECT article, category FROM fontanka').fetchall()
i = 0
db.execute("CREATE TABLE IF NOT EXISTS cleanka (id INTEGER PRIMARY KEY UNIQUE NOT NULL, article TEXT, category TEXT)")
for i in tqdm(range(len(rows) // 1000)):
    start = i * 1000
    end = (i + 1) * 1000
    x = list(map(lambda z: z[0], rows))[start:end]
    y = list(map(lambda z: z[1], rows))[start:end]
    for j in range(len(x)):
        t = RegexpTokenizer(r'\w+').tokenize(x[j])
        t = map(lambda z: z.lower(), t)
        t = filter(lambda z: z not in stopwords.words('russian'), t)
        t = filter(lambda z: len(z) > 2, t)
        t = map(SnowballStemmer('russian').stem, t)
        t = map(lambda z: '#' if z.isdigit() else z, t)
        x[j] = ' '.join(t)
    db.executemany('INSERT INTO cleanka (article, category) VALUES (?, ?)', zip(x, y))
    db.commit()
del rows
print("Tokenization complete")
print("Pickle start")
rows = db.execute('SELECT article, category FROM cleanka')
data = rows.fetchall()
x = list(map(lambda z: z[0], data))
y = list(map(lambda z: z[1], data))
y = numpy.array(y)
db.close()
with open('Data_X.pickle', 'wb') as f:
    pickle.dump(x, f)
with open('Data_Y.pickle', 'wb') as f:
    pickle.dump(y, f)
print("Pickle complete")
