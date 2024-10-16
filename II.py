import random

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # Пустое поле
        self.current_player = 'X'  # Начинает X

    def print_board(self):
        for i in range(3):
            print(f"| {' | '.join(self.board[i*3:(i+1)*3])} |")
            print('-' * 13)

    def is_winner(self, player):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Горизонтали
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Вертикали
            [0, 4, 8], [2, 4, 6]               # Диагонали
        ]
        return any(all(self.board[i] == player for i in condition) for condition in win_conditions)

    def is_draw(self):
        return ' ' not in self.board

    def make_move(self, position):
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            return True
        return False

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def play(self):
        while True:
            self.print_board()
            if self.current_player == 'X':
                position = int(input("Введите позицию для X (0-8): "))
            else:
                position = self.ai_move()

            if self.make_move(position):
                if self.is_winner(self.current_player):
                    self.print_board()
                    print(f"{self.current_player} выиграл!")
                    return
                elif self.is_draw():
                    self.print_board()
                    print("Ничья!")
                    return
                self.switch_player()

    def ai_move(self):
        best_score = float('-inf')
        best_move = None

        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'O'  # Бот делает ход
                score = self.minimax(self.board, 0, False)
                self.board[i] = ' '  # Возвращаем назад
                if score > best_score:
                    best_score = score
                    best_move = i

        return best_move if best_move is not None else random.choice([i for i in range(9) if self.board[i] == ' '])

    def minimax(self, board, depth, is_maximizing):
        if self.is_winner('O'):
            return 1  # Бот выигрывает
        elif self.is_winner('X'):
            return -1  # Игрок выигрывает
        elif self.is_draw():
            return 0  # Ничья

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'O'  # Бот делает ход
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ' '  # Возвращаем назад
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'X'  # Игрок делает ход
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ' '  # Возвращаем назад
                    best_score = min(score, best_score)
            return best_score

if __name__ == "__main__":
    mode = input("Выберите режим (1 - Человек против Человека, 2 - Человек против Бота, 3 - Бот против Бота): ")

    game = TicTacToe()
    if mode == '1':
        game.play()
    elif mode == '2':
        game.play()
    elif mode == '3':
        while True:
            game.print_board()
            position = game.ai_move()
            game.make_move(position)
            if game.is_winner(game.current_player):
                game.print_board()
                print(f"{game.current_player} выиграл!")
                break
            elif game.is_draw():
                game.print_board()
                print("Ничья!")
                break
            game.switch_player()
    else:
        print("Неверный режим.")
