# Этот тест проверяет корректность работы метода analyze_trading_signal класса TradingSignalAnalyzer в различных сценариях


from datetime import datetime
import unittest
from entry_point import TradingSignalAnalyzer
import pandas as pd


class TestTradingSignalAnalyzer(unittest.TestCase):
    def setUp(self):
        # Инициализация TradingSignalAnalyzer для тестирования
        self.analyzer = TradingSignalAnalyzer()

    def test_analyze_trading_signal(self):
        # Тестирование с использованием образца исторических данных в виде DataFrame
        sample_data = {
            'timestamp': [datetime(2023, 1, 1), datetime(2023, 1, 2)],
            'open': [1.0, 1.5],
            'high': [1.2, 1.7],
            'low': [0.8, 1.3],
            'close': [1.1, 1.6],
            'volume': [100, 150]
        }
        sample_df = pd.DataFrame(sample_data)

        # Установка исторических данных для анализатора
        self.analyzer.get_historical_data = lambda *args, **kwargs: sample_df

        # Установка порога отклонения для тестирования
        self.analyzer.config['FilterSettings']['deviation_threshold'] = '0.1'

        # Параметры теста
        symbol = 'TEST/USDT'
        alert_price = 1.5
        entry_time = datetime(2023, 1, 1)

        # Выполнение анализа
        result = self.analyzer.analyze_trading_signal(symbol, alert_price, entry_time)

        # Проверка, что результат - это DataFrame
        self.assertIsInstance(result, pd.DataFrame)

        # Добавьте более конкретные проверки на основе ожидаемых результатов
        # Например, можно проверить, присутствуют ли определенные столбцы или нет


if __name__ == '__main__':
    unittest.main()
