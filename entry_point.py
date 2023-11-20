# КОД ИСПОЛЬЗУЕТСЯ ДЛЯ АНАЛИЗА ТОРГОВЫХ СИГНАЛОВ НА ОСНОВЕ ИСТОРИЧЕСКИХ ДАННЫХ ЦЕНОВЫХ СВЕЧЕЙ С ИСПОЛЬЗОВАНИЕМ БИБЛИОТЕКИ CCXT ДЛЯ ВЗАИМОДЕЙСТВИЯ С БИРЖЕЙ BINANCE


# импортируем необходимые библиотеки и модули которые будем использовать в дальнейшем
import os   # модуль в данном случае используется для получения переменных окружения
import ccxt   # это библиотека которая предоставляет общий интерфейс для взаимодействия с криптовалютными биржами(у меня с Binance)
import pandas as pd   # это библиотека в данном коде она используется для обработки и анализа данных
import matplotlib.pyplot as plt   # это библиотека используется для построения графика
from configparser import ConfigParser   # в этом коде используется для сохранения и загрузки настроек


# Создаём класс для анализа торговых сигналов на основе исторических данных
class TradingSignalAnalyzer:    # этот класс используется  для анализа торговых сигналов
    def __init__(self):
        self.config = ConfigParser()         # создаем объект для работы с конфигурацией
        self.config_file = 'config.ini'      # указываем имя файла конфигурации
        self.load_config()                  # вызываем метод для загрузки настроек

        #API ключ и Secret ключ для конфиденциальности хранятся в переменных окружения(в файле .env)
        api_key = os.getenv('BINANCE_API_KEY')  # API ключ
        api_secret = os.getenv('BINANCE_API_SECRET')   # Секретный ключ
        self.exchange = ccxt.binance({        # Создаем объект для взаимодействия с биржей Binance
            'apiKey': api_key,
            'secret': api_secret,
        })

    # Этот метод используется для загрузки настроек из файла конфигураций
    def load_config(self):      # Метод для загрузки настроек из файла конфигурации
        if os.path.exists(self.config_file):    #проверяем есть ли файл конфигурации по указанному пути
            self.config.read(self.config_file)  # есть ли есть то считываем его
        else:
            # Set default values
            self.config['FilterSettings'] = {
                'deviation_threshold': '0.03'       # если такого файла нету, то устанавливаем значение по умолчанию
            }
            self.save_config()   # сохранаем настройки в новом файле конфигурации

    # Схраняем текущие настройки в новом файле конфигураций
    def save_config(self):      # Метод для сохранения текущих настроек в файл конфигурации
        with open(self.config_file, 'w') as configfile:     # открываем файл конфигурации для записи (это конструкция автоматически закрывает файл)
            self.config.write(configfile)  # записываем текущие настройки в файл

    # этот метод используется для получения исторических данных(ценовых свечей) по заданному символу, временному интервалу и лимиту
    def get_historical_data(self, symbol, interval, limit):     # Метод для получения исторических данных через API Binance
        ohlcv = self.exchange.fetch_ohlcv(symbol, interval, limit=limit)    # Получение исторических данных через API Binance
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])       # создаем DataFrame из полученных данных, указывая названия столбцов
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')   # преобразовываем столбец 'timestamp' к типу данных datetime, предполагая, что временные метки представлены в миллисекундах (unit='ms')
        return df

    # Этот метод фильтрирует точки входа на основе заданных условий и параметров и возрващает отфильтрованные данные
    def analyze_trading_signal(self, symbol, alert_price, entry_time):  # Метод для анализа торговых сигналов на основе исторических данных
        # Получение исторических данных
        historical_data = self.get_historical_data(symbol, '1h', limit=100)  # получение исторических данных с помощью метода get_historical_data, который возвращает DataFrame с информацией о цене за последние 100 часов

        # Фильтрация точек входа
        entry_point = historical_data[historical_data['timestamp'] > entry_time]  #фильтрация исторических данных для получения точек входа после указанного времени
        entry_point['future_price'] = entry_point['close'].shift(-1)   #cоздание столбца 'future_price', содержащего цены актива на следующем временном шаге.
        entry_point['price_deviation'] = (entry_point['future_price'] - alert_price) / alert_price   # вычисление отклонения будущей цены от цены сигнала (alert_price)

        deviation_threshold = float(self.config.get('FilterSettings', 'deviation_threshold'))  # Получение порогового значения отклонения из конфигурационного файла

        filtered_entries = entry_point[abs(entry_point['price_deviation']) >= deviation_threshold]  # Фильтрация точек входа на основе порогового значения отклонения

        return filtered_entries   #Возврат DataFrame с отфильтрованными точками входа

    # Этот метод используется для визуализации данных. Здесь он строит график цены закрытия с выделением точек входа
    def visualize_data(self, data):   # Метод для визуализации данных, в данном случае, строит график цены закрытия с выделением точек входа
        # Визуализация данных
        plt.plot(data['timestamp'], data['close'], label='Closing Price')           # Строим график цены закрытия
        plt.scatter(data['timestamp'], data['close'], c='r', marker='x', label='Entry Point')   # Выделяем точки входа
        plt.legend()   # Добавляем легенду (содержит информацию о линии графика ('Closing Price') и маркерах ('Entry Point'))
        plt.show()  # Отображаем график


# Этот блок кода выполняется только при запуске кода напрямую
if __name__ == "__main__":      # Блок, который выполнится только при запуске скрипта напрямую. Создает экземпляр класса, настраивает параметры точки входа, проводит анализ и визуализацию
    # Пример использования
    analyzer = TradingSignalAnalyzer()

    # Настройка параметров точки входа
    symbol = 'RAD/USDT'
    alert_price = 1.319
    entry_time = pd.to_datetime('2023-10-23 19:53:15.536000')

    # Анализ и визуализация точек входа
    filtered_entries = analyzer.analyze_trading_signal(symbol, alert_price, entry_time)
    analyzer.visualize_data(filtered_entries)
