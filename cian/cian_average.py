import re
import requests


def take_integer(s):
    s = s.replace(" ", "")
    return int(s[:-3])


def find_prices_on_page(text, parameter):
    prices = re.findall(r'[\d]+ [\d]+ [\d]+\xa0₽</', text)
    prices = list(map(take_integer, prices))
    prices_per_meter = re.findall(r'[\d]+ [\d]+\xa0₽\/', text)
    prices_per_meter = list(map(take_integer, prices_per_meter))
    if parameter:
        prices = prices[:parameter]
        prices_per_meter = prices_per_meter[:parameter]
    return ((len(prices), sum(prices)),
            (len(prices_per_meter), sum(prices_per_meter)))


def find_new_pages(text):
    links = re.findall(r'--list-item--FFjMz"><a href="([^"]+)"', text)
    return links


def find_average(
        link="https://www.cian.ru/cat.php?acontext=%D0%91%D0%B0%D0%BB%D0%B0%D1%88%D0%B8%D1%85%D0%B0%7C%D0%9B%D1%8E%D0%B1%D0%B5%D1%80%D1%86%D1%8B%7C%D0%A9%D0%B5%D1%80%D0%B1%D0%B8%D0%BA%D0%B0%7C%D0%B0%D1%83%D0%BA%D1%86%D0%B8%D0%BE%D0%BD&currency=2&deal_type=sale&engine_version=2&foot_min=13&house_material%5B0%5D=1&house_material%5B1%5D=2&house_material%5B2%5D=3&house_material%5B3%5D=4&house_material%5B4%5D=6&house_material%5B5%5D=8&ipoteka=1&is_first_floor=0&maxprice=8000000&minkarea=6&mintarea=30&offer_type=flat&only_flat=1&only_foot=2&region=4593&room1=1&totime=2592000"):
    headers = {
        'User-Agent': 'Chrome 1.0',
    }
    try:
        res = requests.get(link, headers=headers)
        text = res.text
        num_of_variants = int(re.findall(r'Найдено (\d+) объявлени', text)[0])
        parameter = None
        if num_of_variants < 28:
            parameter = num_of_variants
        result = find_prices_on_page(text, parameter)

        num_of_houses = result[0][0]
        sum_cost = result[0][1]
        num_of_houses_per_meter = result[1][0]
        sum_cost_per_meter = result[1][1]

        links = find_new_pages(text)

        prefix = "https://www.cian.ru"
        for link in links:
            if prefix not in link:
                link = prefix + link
            new_res = requests.get(link, headers=headers)
            new_text = new_res.text
            if num_of_variants - num_of_houses < 28:
                parameter = num_of_variants - num_of_houses
            else:
                parameter = 28
            result = find_prices_on_page(new_text, parameter)
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


def test():
    headers = {
        'User-Agent': 'Chrome 1.0',
    }
    link = "https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&region=1&offer_type=flat&is_first_floor=0&ipoteka=1&only_flat=1&only_foot=2&metro%5B0%5D=2&metro%5B100%5D=140&metro%5B101%5D=141&metro%5B102%5D=142&metro%5B103%5D=143&metro%5B104%5D=145&metro%5B105%5D=146&metro%5B106%5D=147&metro%5B107%5D=148&metro%5B108%5D=149&metro%5B109%5D=150&metro%5B10%5D=13&metro%5B110%5D=151&metro%5B111%5D=154&metro%5B112%5D=155&metro%5B113%5D=156&metro%5B114%5D=159&metro%5B115%5D=229&metro%5B116%5D=236&metro%5B117%5D=237&metro%5B118%5D=272&metro%5B119%5D=275&metro%5B11%5D=14&metro%5B120%5D=281&metro%5B121%5D=283&metro%5B122%5D=286&metro%5B123%5D=287&metro%5B124%5D=289&metro%5B125%5D=290&metro%5B126%5D=291&metro%5B127%5D=296&metro%5B128%5D=309&metro%5B129%5D=311&metro%5B12%5D=15&metro%5B130%5D=337&metro%5B131%5D=338&metro%5B132%5D=339&metro%5B133%5D=350&metro%5B134%5D=351&metro%5B135%5D=352&metro%5B136%5D=361&metro%5B137%5D=362&metro%5B138%5D=363&metro%5B13%5D=16&metro%5B14%5D=18&metro%5B15%5D=20&metro%5B16%5D=21&metro%5B17%5D=27&metro%5B18%5D=29&metro%5B19%5D=30&metro%5B1%5D=3&metro%5B20%5D=33&metro%5B21%5D=35&metro%5B22%5D=36&metro%5B23%5D=37&metro%5B24%5D=38&metro%5B25%5D=40&metro%5B26%5D=42&metro%5B27%5D=43&metro%5B28%5D=44&metro%5B29%5D=44&metro%5B2%5D=4&metro%5B30%5D=45&metro%5B31%5D=46&metro%5B32%5D=46&metro%5B33%5D=47&metro%5B34%5D=49&metro%5B35%5D=50&metro%5B36%5D=53&metro%5B37%5D=54&metro%5B38%5D=55&metro%5B39%5D=56&metro%5B3%5D=4&metro%5B40%5D=57&metro%5B41%5D=58&metro%5B42%5D=60&metro%5B43%5D=61&metro%5B44%5D=62&metro%5B45%5D=63&metro%5B46%5D=64&metro%5B47%5D=66&metro%5B48%5D=68&metro%5B49%5D=70&metro%5B4%5D=5&metro%5B50%5D=71&metro%5B51%5D=71&metro%5B52%5D=72&metro%5B53%5D=73&metro%5B54%5D=74&metro%5B55%5D=75&metro%5B56%5D=77&metro%5B57%5D=78&metro%5B58%5D=79&metro%5B59%5D=80&metro%5B5%5D=8&metro%5B60%5D=81&metro%5B61%5D=84&metro%5B62%5D=85&metro%5B63%5D=86&metro%5B64%5D=87&metro%5B65%5D=91&metro%5B66%5D=93&metro%5B67%5D=96&metro%5B68%5D=97&metro%5B69%5D=98&metro%5B6%5D=8&metro%5B70%5D=100&metro%5B71%5D=102&metro%5B72%5D=103&metro%5B73%5D=104&metro%5B74%5D=105&metro%5B75%5D=107&metro%5B76%5D=108&metro%5B77%5D=110&metro%5B78%5D=112&metro%5B79%5D=113&metro%5B7%5D=9&metro%5B80%5D=114&metro%5B81%5D=115&metro%5B82%5D=115&metro%5B83%5D=116&metro%5B84%5D=117&metro%5B85%5D=118&metro%5B86%5D=119&metro%5B87%5D=120&metro%5B88%5D=121&metro%5B89%5D=122&metro%5B8%5D=11&metro%5B90%5D=123&metro%5B91%5D=124&metro%5B92%5D=125&metro%5B93%5D=128&metro%5B94%5D=129&metro%5B95%5D=130&metro%5B96%5D=131&metro%5B97%5D=132&metro%5B98%5D=133&metro%5B99%5D=134&metro%5B9%5D=12&room2=1&room3=1&minprice=5&maxprice=8000000&foot_min=13&mintarea=42&minkarea=6&maxkarea=12"
    # link = "https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&region=1&offer_type=flat&is_first_floor=0&ipoteka=1&only_flat=1&only_foot=2&metro%5B0%5D=2&metro%5B100%5D=140&metro%5B101%5D=141&metro%5B102%5D=142&metro%5B103%5D=143&metro%5B104%5D=145&metro%5B105%5D=146&metro%5B106%5D=147&metro%5B107%5D=148&metro%5B108%5D=149&metro%5B109%5D=150&metro%5B10%5D=13&metro%5B110%5D=151&metro%5B111%5D=154&metro%5B112%5D=155&metro%5B113%5D=156&metro%5B114%5D=159&metro%5B115%5D=229&metro%5B116%5D=236&metro%5B117%5D=237&metro%5B118%5D=272&metro%5B119%5D=275&metro%5B11%5D=14&metro%5B120%5D=281&metro%5B121%5D=283&metro%5B122%5D=286&metro%5B123%5D=287&metro%5B124%5D=289&metro%5B125%5D=290&metro%5B126%5D=291&metro%5B127%5D=296&metro%5B128%5D=309&metro%5B129%5D=311&metro%5B12%5D=15&metro%5B130%5D=337&metro%5B131%5D=338&metro%5B132%5D=339&metro%5B133%5D=350&metro%5B134%5D=351&metro%5B135%5D=352&metro%5B136%5D=361&metro%5B137%5D=362&metro%5B138%5D=363&metro%5B13%5D=16&metro%5B14%5D=18&metro%5B15%5D=20&metro%5B16%5D=21&metro%5B17%5D=27&metro%5B18%5D=29&metro%5B19%5D=30&metro%5B1%5D=3&metro%5B20%5D=33&metro%5B21%5D=35&metro%5B22%5D=36&metro%5B23%5D=37&metro%5B24%5D=38&metro%5B25%5D=40&metro%5B26%5D=42&metro%5B27%5D=43&metro%5B28%5D=44&metro%5B29%5D=44&metro%5B2%5D=4&metro%5B30%5D=45&metro%5B31%5D=46&metro%5B32%5D=46&metro%5B33%5D=47&metro%5B34%5D=49&metro%5B35%5D=50&metro%5B36%5D=53&metro%5B37%5D=54&metro%5B38%5D=55&metro%5B39%5D=56&metro%5B3%5D=4&metro%5B40%5D=57&metro%5B41%5D=58&metro%5B42%5D=60&metro%5B43%5D=61&metro%5B44%5D=62&metro%5B45%5D=63&metro%5B46%5D=64&metro%5B47%5D=66&metro%5B48%5D=68&metro%5B49%5D=70&metro%5B4%5D=5&metro%5B50%5D=71&metro%5B51%5D=71&metro%5B52%5D=72&metro%5B53%5D=73&metro%5B54%5D=74&metro%5B55%5D=75&metro%5B56%5D=77&metro%5B57%5D=78&metro%5B58%5D=79&metro%5B59%5D=80&metro%5B5%5D=8&metro%5B60%5D=81&metro%5B61%5D=84&metro%5B62%5D=85&metro%5B63%5D=86&metro%5B64%5D=87&metro%5B65%5D=91&metro%5B66%5D=93&metro%5B67%5D=96&metro%5B68%5D=97&metro%5B69%5D=98&metro%5B6%5D=8&metro%5B70%5D=100&metro%5B71%5D=102&metro%5B72%5D=103&metro%5B73%5D=104&metro%5B74%5D=105&metro%5B75%5D=107&metro%5B76%5D=108&metro%5B77%5D=110&metro%5B78%5D=112&metro%5B79%5D=113&metro%5B7%5D=9&metro%5B80%5D=114&metro%5B81%5D=115&metro%5B82%5D=115&metro%5B83%5D=116&metro%5B84%5D=117&metro%5B85%5D=118&metro%5B86%5D=119&metro%5B87%5D=120&metro%5B88%5D=121&metro%5B89%5D=122&metro%5B8%5D=11&metro%5B90%5D=123&metro%5B91%5D=124&metro%5B92%5D=125&metro%5B93%5D=128&metro%5B94%5D=129&metro%5B95%5D=130&metro%5B96%5D=131&metro%5B97%5D=132&metro%5B98%5D=133&metro%5B99%5D=134&metro%5B9%5D=12&object_type=2&room3=1&minprice=4&maxprice=15000000&foot_min=13&mintarea=42&minkarea=6&maxkarea=12"
    res = requests.get(link, headers=headers)
    text = res.text
    return "Найдено" in text
    # return text
print(test())
