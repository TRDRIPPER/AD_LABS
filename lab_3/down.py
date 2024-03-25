import urllib.request
import datetime
import os

def Downloads (): 
    base_url = 'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={}&year1=1981&year2=2024&type=Mean'

    if not os.path.exists('csv_data'):
        os.makedirs('csv_data')
    else:
        files = os.listdir('csv_data')
        for file in files:
            os.remove(os.path.join('csv_data', file))

    for ID in range(1, 28):
        url = base_url.format(ID)
        DT = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = 'NOAA_{}_{}.csv'.format(ID, DT)
        filepath = os.path.join('csv_data', filename)

        try:
            urllib.request.urlretrieve(url, filepath)
            print('Файл {} успішно скачано.'.format(filename))
        except Exception as e:
            print('Помилка при скачуванні файлу для provinceID {}: {}'.format(ID, str(e)))

if __name__ == "__main__":       
    Downloads()         