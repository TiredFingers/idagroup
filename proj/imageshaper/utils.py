from urllib.request import Request, urlopen
from urllib.error import URLError
from io import BytesIO
from PIL import Image, UnidentifiedImageError


def download_img(url, formats=None):

    if url is None or url == '':
        return None

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0'}
        req = Request(url, headers=headers)
        resp = urlopen(req)
    except ValueError as e:
        raise Exception(e)
    except URLError as e:
        if hasattr(e, 'reason'):
            raise Exception('Не удалось установить подключение. Причина: ' + str(e.reason))
        if hasattr(e, 'code'):
            raise Exception('Сервер не может обработать запрос. Код ошибки: ' + str(e.code))
    else:
        try:
            data = BytesIO(resp.read())
            img = Image.open(data, formats=formats)
        except UnidentifiedImageError as e:
            raise Exception(e)
        except FileNotFoundError as e:
            raise Exception(e)
        except ValueError as e:
            raise Exception(e)
        except TypeError as e:
            raise Exception(e)
        else:
            return img, url.split('/')[-1]
