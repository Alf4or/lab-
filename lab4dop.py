import numpy as np
import random
import matplotlib.pyplot as plt

# Определяем параметры
NUM_DISKS = 3
TARGET_STATE = (0, 0, NUM_DISKS)  # Целевое состояние
NUM_STATES = 5 ** NUM_DISKS  # Максимальное количество состояний
ACTIONS = 20  # Действия: 0 = перенести диск с 1 на 2, 1 = с 1 на 3, 2 = с 2 на 3

# Инициализация Q-Table и матрицы наград
q_table = np.zeros((NUM_STATES, ACTIONS))
rewards = np.zeros((NUM_STATES, ACTIONS))

# Функция для преобразования текущего состояния в индекс
def state_to_index(state):
    return state[0] + state[1] * 4 + state[2] * 16  # Преобразование состояния в индекс

# Заполнение наград за целевое состояние
reward_index = state_to_index(TARGET_STATE)
rewards[reward_index] = 1  # Награда за достижение целевого состояния

# Гиперпараметры
alpha = 0.1  # Коэффициент обучения
gamma = 0.7  # Фактор скидки
epsilon = 0.6  # Начальный ε для ε-жадной стратегии
decay = 0.999  # Уменьшение ε
episodes = 50000  # Количество эпизодов

# Функция для выполнения действия и получения следующего состояния
def perform_action(state, action):
    next_state = list(state)

    # Логика перемещения
    if action == 0:  # Перемещение с 1 на 2
        if next_state[0] > 0:  # Диск может быть перемещён
            next_state[0] -= 1
            next_state[1] += 1
    elif action == 1:  # Перемещение с 1 на 3
        if next_state[0] > 0:
            next_state[0] -= 1
            next_state[2] += 1
    elif action == 2:  # Перемещение с 2 на 3
        if next_state[1] > 0:
            next_state[1] -= 1
            next_state[2] += 1

    return tuple(next_state)

# Обучение Q-матрицы
for episode in range(episodes):
    state = (NUM_DISKS, 0, 0)  # Начальное состояние
    done = False

    while not done:
        state_index = state_to_index(state)

        # Выбор действия по ε-жадной стратегии
        if random.random() < epsilon:
            action = random.randint(0, ACTIONS - 1)  # Исследуем
        else:
            action = np.argmax(q_table[state_index])  # Используем лучшее известное действие

        # Получение следующего состояния
        next_state = perform_action(state, action)

        # Получение награды
        next_state_index = state_to_index(next_state)
        reward = rewards[next_state_index][action]

        # Обновление Q-значения с использованием уравнения Беллмана
        q_table[state_index, action] += alpha * (
                    reward + gamma * np.max(q_table[next_state_index]) - q_table[state_index, action])

        # Переход к следующему состоянию
        state = next_state

        # Проверка завершения эпизода
        if state == TARGET_STATE:
            done = True

    # Уменьшение ε
    epsilon *= decay

# Показываем полученную Q-таблицу
print("Полученная Q-таблица:")
for s in range(NUM_STATES):
    print(f"Состояние {s}: {q_table[s]}")

# Тестирование агента
def test_agent():
    state = (NUM_DISKS, 0, 0)
    moves = 0
    visited_states = set()  # Для хранения всех посещенных состояний
    done = False

    while not done:
        state_index = state_to_index(state)
        action = np.argmax(q_table[state_index])  # Выбор лучшего действия
        visited_states.add(state)  # Запоминаем посещенное состояние
        state = perform_action(state, action)

        if state == TARGET_STATE:
            done = True

        moves += 1

    return moves, len(visited_states)  # Возвращаем количество ходов и количество уникальных состояний

# Запуск тестирования
moves_to_goal, unique_states_visited = test_agent()
print(f"Количество ходов для завершения головоломки: {moves_to_goal}")
print(f"Количество уникальных состояний, через которые прошёл агент: {unique_states_visited}")

# Визуализация
def visualize_solution():
    state = (NUM_DISKS, 0, 0)
    moves_record = []

    while state != TARGET_STATE:
        state_index = state_to_index(state)
        action = np.argmax(q_table[state_index])
        next_state = perform_action(state, action)
        moves_record.append((state, next_state))
        state = next_state

    # Определяем цвета для каждого диска
    colors = ['red', 'green', 'blue']

    # Визуализация в matplotlib
    plt.figure(figsize=(10, 6))

    for i, (old, new) in enumerate(moves_record):
        plt.clf()
        plt.title(f"Ход: {i + 1} | Текущее состояние: {old} → {new}")
        plt.xlabel('Башни')
        plt.ylabel('Диски')

        # Отображаем диски на каждой башне
        for tower in range(3):
            for disk in range(old[tower]):
                plt.bar(tower + 1, disk + 1, color=colors[disk], width=0.4, edgecolor='black')

        # Добавляем текстовое отображение кол-ва ходов и уникальных состояний
        plt.figtext(0.15, 0.85, f"Количество ходов: {i + 1}", fontsize=12)
        plt.figtext(0.15, 0.80, f"Уникальные состояния: {unique_states_visited}", fontsize=12)

        plt.xlim(0.5, 3.5)
        plt.ylim(0, NUM_DISKS + 1)
        plt.xticks([1, 2, 3], ['Tower 1', 'Tower 2', 'Tower 3'])
        plt.legend(['Disk 1', 'Disk 2', 'Disk 3'])
        plt.pause(0.5)

    plt.show()

# Визуализация решения
visualize_solution()