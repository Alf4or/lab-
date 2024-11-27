import numpy as np
import random

# Функция для перемещения диска из одного стержня в другой
def move_disk(state, from_peg, to_peg):
    state = [list(peg) for peg in state]  # Преобразуем кортеж в список для изменения
    # Проверяем, что в стержне есть диски
    if state[from_peg]:
        disk = state[from_peg][-1]  # Берем верхний диск
        state[from_peg].pop()  # Удаляем диск из исходного стержня
        state[to_peg].append(disk)  # Добавляем диск на целевой стержень
    return tuple(tuple(peg) for peg in state)  # Преобразуем обратно в кортеж

# Функция для получения награды в зависимости от состояния и действия
def get_reward(state, action):
    if state == ((1, 2, 3), (), ()):
        return 10  # Награда за выигрыш
    elif action not in valid_moves(state):
        return -10  # Штраф за незаконный ход
    return -1  # Награда за любой другой ход

# Функция для проверки, является ли состояние конечным
def is_terminal(state):
    return state == ((1, 2, 3), (), ())

# Функция для получения всех допустимых перемещений
def valid_moves(state):
    moves = []
    for i in range(3):  # Для каждого стержня
        if state[i]:  # Если в стержне есть диски
            disk = state[i][-1]  # Берем верхний диск
            for j in range(3):  # Проверяем возможность перемещения на другой стержень
                if i != j and (not state[j] or state[j][-1] > disk):  # Проверка правил
                    moves.append((i, j))  # Добавляем допустимое перемещение
    return moves

# Инициализация Q-матрицы с использованием словаря
Q = {}

# Q-обучение
def q_learning(episodes, alpha, gamma):
    for _ in range(episodes):
        state = ((3,), (), ())  # Начальное состояние с 3 дисками на первом стержне
        while not is_terminal(state):
            if random.uniform(0, 1) < epsilon:
                action = random.choice(valid_moves(state))  # Случайное действие
            else:
                action = max(valid_moves(state), key=lambda a: Q.get((state, a), 0))  # Используем Q-матрицу для выбора действия

            new_state = move_disk(state, action[0], action[1])  # Получаем новое состояние
            reward = get_reward(new_state, action)  # Получаем награду

            # Обновление Q-матрицы
            Q[(state, action)] = Q.get((state, action), 0) + alpha * (
                reward + gamma * max(Q.get((new_state, a), 0) for a in valid_moves(new_state)) - Q.get((state, action), 0)
            )
            state = new_state  # Переход к новому состоянию

# Тестирование агента
def test_agent():
    state = ((3,), (), ())  # Начальное состояние
    steps = 0  # Счетчик шагов
    while not is_terminal(state):
        action = max(valid_moves(state), key=lambda a: Q.get((state, a), 0))  # Используем Q-матрицу для выбора действия
        state = move_disk(state, action[0], action[1])  # Переход к новому состоянию
        steps += 1  # Увеличиваем счетчик шагов
    return steps  # Возвращаем количество шагов для завершения

# Параметры обучения
epsilon = 0.1  # Вероятность случайного выбора действия
alpha = 0.9  # Коэффициент обучения
gamma = 0.95  # Коэффициент дисконтирования
episodes = 1000  # Количество эпизодов обучения

# Запуск Q-обучения
q_learning(episodes, alpha, gamma)

# Тестирование обученного агента
steps_needed = test_agent()
print(f"Количество ходов для завершения: {steps_needed}")