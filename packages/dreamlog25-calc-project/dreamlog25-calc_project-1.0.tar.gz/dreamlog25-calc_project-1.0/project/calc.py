import numpy as np

class Calculator:
    """
    Клас калькулятор.
    Використовуються функції з NumPy.
    :ДІЇ З ЧИСЛАМИ: Стандартні дії простого калькулятора
    """

    def add(self,x,y):
        """
        :ДІЯ: Додавання чисел.
        """
        return np.add(x,y)

    def subtract(self,x,y):
        """
        :ДІЯ: Віднімання чисел.
        """
        return np.subtract()

    def multiply(self,x,y):
        """
        :ДІЯ: Множення чисел.
        """
        return np.multiply(x,y)

    def divide(self,x,y):
        """
        :ДІЯ: Ділення чисел.
        """
        return np.divide(x,y)
