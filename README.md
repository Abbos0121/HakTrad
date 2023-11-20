# Trading Signal Analyzer

Этот проект представляет собой программу для анализа торговых сигналов на основе исторических данных ценовых свечей с использованием библиотеки ccxt для взаимодействия с биржей Binance.

## Установка зависимостей

Для установки зависимостей выполните следующие шаги:

1. Создайте виртуальное окружение (рекомендуется, но не обязательно).
   
   ```bash
   python -m venv venv
   
2. Активируйте виртуальное окружение.
    

    venv/bin/activate  # для Linux/Mac
   
    venv\Scripts\activate  # для Windows

3. Установите зависимости из файла requirements.txt.

    ```bash
    pip install -r requirements.txt
   
# Использование

1. Создайте файл конфигурации config.ini (пример настроек можно найти в файле config_example.ini).

2. Установите переменные окружения для вашего API-ключа и секретного ключа Binance в файле .env.
    ```
    BINANCE_API_KEY=ваш_ключ
    BINANCE_API_SECRET=ваш_секрет
   
3. Запустите программу, указав необходимые параметры точки входа в разделе if __name__ == "__main__" в файле entry_point.py.
    
   ```bash
   python entry_point.py
   
   
# Структура проекта
* entry_point.py: Класс TradingSignalAnalyzer и его методы.
* config.ini: Файл конфигурации с настройками программы.
* config_example.ini: Пример файла конфигурации.
* requirements.txt: Файл зависимостей проекта.

# Тестирование
Для запуска тестов используйте следующую команду:
   
    
     python -m unittest test_trading_signal_analyzer.py


# Лицензия
MIT License
