import aiohttp
import asyncio
from bs4 import BeautifulSoup


def take_integer(s):
    s = s.replace(" ", "")
    for i in range(len(s) - 1, -1, -1):
        if s[i].isdigit():
            s = s[:i + 1]
            break
    return int(s)


async def async_find_prices_on_page(session, page, parameter):
    headers = {
        'User-Agent': 'Chrome 1.0',
    }
    prefix = "https://www.cian.ru"
    if prefix not in page:
        page = prefix + page
    async with session.get(url=page, headers=headers) as response:
        soup = BeautifulSoup(await response.text(), 'lxml')

        prices = soup.find_all("span", {'data-mark': 'MainPrice'})
        prices = [take_integer(price.text) for price in prices]

        prices_per_meter = soup.find_all("p", {'data-mark': 'PriceInfo'})
        prices_per_meter = [take_integer(price.text[:-2]) for price in prices_per_meter]
        if parameter:
            prices = prices[:parameter]
            prices_per_meter = prices_per_meter[:parameter]
        return ((len(prices), sum(prices)),
                (len(prices_per_meter), sum(prices_per_meter)))


async def async_find_average(link):
    headers = {
        'User-Agent': 'Chrome 1.0',
    }
    async with aiohttp.ClientSession() as session:
        try:
            response = await session.get(url=link, headers=headers)
            soup = BeautifulSoup(await response.text(), 'lxml')

            num_of_variants = int(soup.find('h5', class_='_93444fe79c--color_black_100--kPHhJ _93444fe79c--lineHeight'
                                                         '_20px--tUURJ _93444fe79c--fontWeight_bold--ePDnv _93444fe79c'
                                                         '--fontSize_14px--TCfeJ _93444fe79c--display_block--pDAEx _9'
                                                         '3444fe79c--text--g9xAG _93444fe79c--text_letterSpacing__nor'
                                                         'mal--xbqP6').text.split()[1])
            if num_of_variants <= 28:
                tasks = [asyncio.create_task(async_find_prices_on_page(session, link, num_of_variants))]
            else:
                parameter = num_of_variants % 28

                links = soup.find_all("a", class_='_93444fe79c--list-itemLink--BU9w6')
                links = [link.get('href') for link in links]

                tasks = []
                for page in [link] + links[:-1]:
                    task = asyncio.create_task(async_find_prices_on_page(session, page, 28))
                    tasks.append(task)
                if links:
                    task = asyncio.create_task(async_find_prices_on_page(session, links[-1], parameter))
                    tasks.append(task)

            num_of_houses = 0
            sum_cost = 0
            num_of_houses_per_meter = 0
            sum_cost_per_meter = 0

            for future in asyncio.as_completed(tasks):
                # получаем результаты по готовности
                result = await future
                num_of_houses += result[0][0]
                sum_cost += result[0][1]
                num_of_houses_per_meter += result[1][0]
                sum_cost_per_meter += result[1][1]
            res_text = "Средняя цена: " + str(sum_cost // num_of_houses) + "\n" + \
                       "Средняя цена за метр: " + str(sum_cost_per_meter // num_of_houses_per_meter) + "\n" + \
                       "Всего было квартир: " + str(num_of_houses_per_meter)
            return res_text
        except Exception as err:
            return "Ошибка на сайте..."
