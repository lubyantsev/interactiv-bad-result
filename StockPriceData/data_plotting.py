import matplotlib.pyplot as plt
import pandas as pd
import os
import plotly.graph_objs as go


def create_and_save_plot(data, ticker, period, filename=None, style='default'):
    """
    Создает график, отображающий цены закрытия, скользящие средние, RSI и MACD.

    :param data: DataFrame с историческими данными акций.
    :param ticker: Тикер акции.
    :param period: Период для графика.
    :param filename: Имя файла для сохранения графика.
    :param style: Стиль графика.
    """
    # Применяем выбранный стиль
    plt.style.use(style)

    # Создаем папку 'charts', если она не существует
    if not os.path.exists('charts'):
        os.makedirs('charts')

    plt.figure(figsize=(14, 10))

    # График цен закрытия и скользящих средних
    plt.subplot(4, 1, 1)
    if 'Date' in data.columns:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.plot(data['Date'], data['Close'], label='Цена закрытия', color='blue')
        plt.plot(data['Date'], data['Moving_Average'], label='Скользящее среднее', color='orange')
        plt.title(f'{ticker} - Цена закрытия и скользящее среднее за {period}')
        plt.xlabel("Дата")
    else:
        plt.plot(data['Close'], label='Цена закрытия', color='blue')
        plt.plot(data['Moving_Average'], label='Скользящее среднее', color='orange')
        plt.title(f'{ticker} - Цена закрытия и скользящее среднее за {period}')

    plt.ylabel("Цена")
    plt.legend()

    # График RSI
    plt.subplot(4, 1, 2)
    plt.plot(data['RSI'], label='RSI', color='purple')
    plt.axhline(70, linestyle='--', alpha=0.5, color='red', label='Перепроданность')
    plt.axhline(30, linestyle='--', alpha=0.5, color='green', label='Перепроданность')
    plt.title('Индекс относительной силы (RSI)')
    plt.xlabel("Дата")
    plt.ylabel("RSI")
    plt.legend()

    # График MACD
    plt.subplot(4, 1, 3)
    plt.plot(data['MACD'], label='MACD', color='blue')
    plt.plot(data['Signal_Line'], label='Сигнальная линия', color='orange')
    plt.title('MACD')
    plt.xlabel("Дата")
    plt.ylabel("MACD")
    plt.legend()

    # График полос Боллинджера
    plt.subplot(4, 1, 4)
    plt.plot(data['Close'], label='Цена закрытия', color='blue')
    plt.plot(data['MA'], label='Скользящее среднее', color='orange')
    plt.plot(data['Upper_Band'], label='Верхняя полоса Боллинджера', color='green', linestyle='--')
    plt.plot(data['Lower_Band'], label='Нижняя полоса Боллинджера', color='red', linestyle='--')
    plt.fill_between(data.index, data['Lower_Band'], data['Upper_Band'], color='gray', alpha=0.2)

    plt.title(f'График акций {ticker} с индикаторами Боллинджера')
    plt.xlabel('Дата')
    plt.ylabel('Цена')
    plt.legend()
    plt.grid()

    # Сохранение графика
    filename = filename or f"{ticker}_{period}.png"
    filepath = os.path.join('charts', filename)
    plt.tight_layout()  # Улучшаем компоновку графиков
    plt.savefig(filepath)
    plt.close()  # Закрываем фигуру после сохранения
    print(f"График сохранен как {filepath}")


def plot_interactive_graph(stock_data, filename):
    # Проверяем, что в данных есть колонка 'Close'
    if 'Close' not in stock_data.columns:
        print("В предоставленных данных нет колонки 'Close'.")
        return

    # Вычисляем среднее значение колонки 'Close'
    average_close = stock_data['Close'].mean()
    print(f"Среднее значение 'Close': {average_close}")

    # Создаем интерактивный график
    fig = go.Figure()

    # Добавляем линию графика
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Цена закрытия'))

    # Добавляем линию для среднего значения
    fig.add_trace(go.Scatter(x=stock_data.index, y=[average_close] * len(stock_data),
                             mode='lines', name='Среднее значение закрытия', line=dict(dash='dash')))

    # Настройки графика
    fig.update_layout(title='Интерактивный график цен закрытия',
                      xaxis_title='Дата',
                      yaxis_title='Цена закрытия',
                      legend=dict(x=0, y=1))

    # Отображаем график
    fig.show()

    # Пример использования
    # if __name__ == "__main__":
    # Создаем пример DataFrame с данными акций
    # data = {
    #     'Date': pd.date_range(start='2023-01-01', periods=10),
    #     'Close': [100, 102, 101, 105, 104, 107, 106, 110, 108, 111],
    #     'Moving_Average': [None, None, None, 102.67, 103.33, 104.67, 105.00, 106.33, 107.00, 108.00],
    #     'RSI': [30, 40, 50, 60, 70, 80, 90, 40, 30, 20],
    #     'MACD': [0.1, 0.2, 0.1, 0.3, 0.4, 0.3, 0.2, 0.1, 0.0, -0.1],
    #     'Signal_Line': [0.0] * 10,
    #     'MA': [None, None, None, None, None, None, None, None, None, None],
    #     'Upper_Band': [None] * 10,
    #     'Lower_Band': [None] * 10
    # }
    # stock_data = pd.DataFrame(data)
    # stock_data.set_index('Date', inplace=True)

    # Вызываем функцию для построения статического графика
    #create_and_save_plot(stock_data, ticker="AAPL", period="10 дней")

    # Вызываем функцию для построения интерактивного графика
    plot_interactive_graph(stock_data)
