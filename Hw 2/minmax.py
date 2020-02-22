import time


class Game:
    def __init__(self):
        self.row = 0
        self.column = 0
        self.score_first_player = 0
        self.score_second_player = 0
        self.initialize_game()
        self.player_turn = '1'

    def initialize_game(self):
        f = open("input_11.txt", "r")
        self.row = int(f.readline()) + 1
        self.column = int(f.readline()) + 1

        self.current_state = [['*' for i in range(self.column * 2)] for j in range(2 * self.row - 1)]

        for ix in range(0, self.row):
            for jx in range(1, self.column):
                self.current_state[2 * ix][2 * jx] = f.readline()[0][0]

        for jy in range(0, self.column):
            for iy in range(1, self.row):
                self.current_state[2 * iy - 1][2 * jy + 1] = f.readline()[0][0]

        self.score_first_player = int(f.readline())
        self.score_second_player = int(f.readline())

    def change_turn(self):
        if self.player_turn == '1':
            self.player_turn = '2'
        else:
            self.player_turn = '1'

    def draw_board(self):
        for i in range(0, 2 * self.row - 1):
            for j in range(0, 2 * self.column):
                print('{}'.format(self.current_state[i][j]), end=" ")
            print()
        print()

    def is_end(self):
        for i in range(0, 2 * self.row - 1):
            for j in range(0, 2 * self.column):
                if self.current_state[i][j] == '0':
                    return False

        return True

    def is_score(self, row, column):
        score = 0

        if row % 2 == 1:
            if ((column - 2 >= 0 and self.current_state[row][column - 2] == '1') and
                    (row - 1 >= 0 and self.current_state[row - 1][column - 1] == '1') and
                    (row + 1 < (2 * self.row - 1) and self.current_state[row + 1][column - 1] == '1')):
                score += 1

            if ((column + 2 < (2 * self.column) and self.current_state[row][column + 2] == '1') and
                    (row - 1 >= 0 and self.current_state[row - 1][column + 1] == '1') and
                    (row + 1 < (2 * self.row - 1) and self.current_state[row + 1][column + 1] == '1')):
                score += 1
        else:
            if((row - 2 >= 0 and self.current_state[row - 2][column] == '1') and
                    (column - 1 >= 0 and self.current_state[row - 1][column - 1] == '1') and
                    (column + 1 < (2 * self.column) and self.current_state[row - 1][column + 1] == '1')):
                score += 1

            if ((row + 2 < (2 * self.row - 1) and self.current_state[row + 2][column] == '1') and
                    (column - 1 >= 0 and self.current_state[row + 1][column - 1] == '1') and
                    (column + 1 < (2 * self.column) and self.current_state[row + 1][column + 1] == '1')):
                score += 1

        return score

    def max(self):
        score_first_max = 0
        score_second_max = 0
        x = None
        y = None

        for i in range(0, 2 * self.row - 1):
            for j in range(0, 2 * self.column):
                if self.is_end():
                    return self.score_first_player, self.score_second_player, x, y
                if self.current_state[i][j] == '0':
                    score = self.is_score(i, j)
                    if score > 0:
                        self.score_first_player += score
                        self.current_state[i][j] = '1'
                        (score_first, score_second, x, y) = self.max()
                    else:
                        self.current_state[i][j] = '1'
                        (score_first, score_second, x, y) = self.min()

                    if score_first - score_second > score_first_max - score_second_max:
                        score_first_max = score_first
                        score_second_max = score_second
                        x = i
                        y = j

                    self.current_state[i][j] = '0'

                    if score > 0:
                        self.score_first_player -= score

        return score_first_max, score_second_max, x, y

    def min(self):
        score_first_max = 0
        score_second_max = 0
        x = None
        y = None

        for i in range(0, 2 * self.row - 1):
            for j in range(0, 2 * self.column):
                if self.is_end():
                    return self.score_first_player, self.score_second_player, 0, 0
                if self.current_state[i][j] == '0':
                    score = self.is_score(i, j)
                    if score > 0:
                        self.score_second_player += score
                        self.current_state[i][j] = '1'
                        (score_first, score_second, x, y) = self.min()
                    else:
                        self.current_state[i][j] = '1'
                        (score_first, score_second, x, y) = self.max()

                    if score_second - score_first > score_second_max - score_first_max:
                        score_second_max = score_second
                        score_first_max = score_first
                        x = i
                        y = j

                    self.current_state[i][j] = '0'

                    if score > 0:
                        self.score_second_player -= score

        return score_first_max, score_second_max, x, y

    def play(self):
        start = time.time()

        while True:
            self.draw_board()
            if self.is_end():
                print('Game Over! First Player: ' + str(self.score_first_player) + ' Second Player: ' + str(self.score_second_player))
                end = time.time()
                print('Evaluation time: {}s'.format(round(end - start, 5)))
                self.initialize_game()
                return

            if self.player_turn == '1':
                (score_first, score_second, x, y) = self.max()

                self.current_state[x][y] = '1'

                score = self.is_score(x, y)
                if score == 0:
                    self.change_turn()
                else:
                    self.score_first_player += 1

                print('First player is playing now.')

            else:
                (score_first, score_second, x, y) = self.min()

                self.current_state[x][y] = '1'

                score = self.is_score(x, y)
                if score == 0:
                    self.change_turn()
                else:
                    self.score_second_player += 1

                print('Second player is playing now.')


def main():
    g = Game()
    g.play()


if __name__ == "__main__":
    main()