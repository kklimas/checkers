import pygame

from src.main.enum.game_theme import GameTheme
from src.main.model.checker import Checker
from src.resources.constants import BLACK, ROWS, SQUARE_SIZE, COLS, WHITE, LIGHT_THEME, DARK_THEME


class Board:
    def __init__(self, game_mode):
        self.board = []
        self.counter_black_left = self.counter_white_left = 12
        self.counter_black_kings = self.counter_white_kings = 0
        self.create_board()
        self.game_mode = game_mode
        self._get_theme()

    def _get_theme(self):
        if GameTheme.LIGHT == self.game_mode.theme:
            self.theme = LIGHT_THEME
            return
        self.theme = DARK_THEME

    def create_board(self):
        self.board = [[0 for _ in range(ROWS)] for _ in range(COLS)]
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.board[row][col] = Checker(row, col, WHITE)
                    elif row > 4:
                        self.board[row][col] = Checker(row, col, BLACK)

    def draw(self, window):
        self.draw_squares(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(window)

    def draw_squares(self, window):
        window.fill(BLACK)
        white_field = self.theme.get('white-field')
        black_field = self.theme.get('black-field')
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(window, white_field, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            for col in range(row % 2 - 1, COLS, 2):
                pygame.draw.rect(window, black_field, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def get_piece(self, row, col):
        return self.board[row][col]

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 and piece.color == WHITE:
            piece.make_king()
            self.counter_white_kings += 1
        elif row == 0 and piece.color == BLACK:
            piece.make_king()
            self.counter_black_kings += 1

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == BLACK:
                    self.counter_black_left -= 1
                else:
                    self.counter_white_left -= 1

    def winner(self, mode):
        if self.counter_black_left <= 0:
            return WHITE
        elif self.counter_white_left <= 0:
            return BLACK

        flag_white = True
        for row in range(ROWS):
            for col in range(COLS):
                if self.get_piece(row, col):
                    piece = self.get_piece(row, col)
                    if piece.color == WHITE:
                        if len(self._get_valid_moves(piece, mode)) > 0:
                            flag_white = False
                            break
        if flag_white:
            return BLACK

        flag_black = True
        for row in range(ROWS):
            for col in range(COLS):
                if self.get_piece(row, col):
                    piece = self.get_piece(row, col)
                    if piece.color == BLACK:
                        if len(self._get_valid_moves(piece, mode)) > 0:
                            flag_black = False
                            break
        if flag_black:
            return WHITE

        return None

    def _get_valid_moves(self, piece, mode):
        moves = {}
        col_left = piece.col - 1
        col_right = piece.col + 1
        row = piece.row

        if piece.king:
            if mode.king_multiple_moves:
                moves.update(self._traverse_left(row - 1, -1, -1, piece.color, col_left, True))
                moves.update(self._traverse_right(row - 1, -1, -1, piece.color, col_right, True))
                moves.update(self._traverse_left(row + 1, ROWS, 1, piece.color, col_left, True))
                moves.update(self._traverse_right(row + 1, ROWS, 1, piece.color, col_right, True))
            else:
                moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, col_left, False))
                moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, col_right, False))
                moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, col_left, False))
                moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, col_right, False))

        elif mode.reverse_beat:
            reverse_moves = {}
            if piece.color == BLACK:
                reverse_moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, col_left, False))
                reverse_moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, col_right, False))
                for move in reverse_moves:
                    if len(reverse_moves[move]) > 0:
                        moves[move] = reverse_moves[move]

                moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, col_left, False))
                moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, col_right, False))
            else:
                reverse_moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, col_left, False))
                reverse_moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, col_right, False))
                for move in reverse_moves:
                    if len(reverse_moves[move]) > 0:
                        moves[move] = reverse_moves[move]

                moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, col_left, False))
                moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, col_right, False))

        else:
            if piece.color == BLACK:
                moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, col_left, False))
                moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, col_right, False))
            else:
                moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, col_left, False))
                moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, col_right, False))

        if mode.obligatory_best_beat:
            best_move = 0
            for move in moves:
                best_move = max(best_move, len(moves[move]))
            available_moves = {}
            for move in moves:
                if len(moves[move]) == best_move:
                    available_moves[move] = moves[move]
            return available_moves

        return moves

    def _traverse_left(self, start, stop, step, color, col_left, king, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if col_left < 0:
                break

            current = self.board[r][col_left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, col_left)] = last + skipped
                else:
                    moves[(r, col_left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, col_left - 1, king, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, col_left + 1, king, skipped=last))

                if not king:
                    break
            elif current.color == color:
                break
            elif not last:
                last = [current]
            else:
                break
            col_left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, col_right, king, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if col_right >= COLS:
                break

            current = self.board[r][col_right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, col_right)] = last + skipped
                else:
                    moves[(r, col_right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, col_right - 1, king, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, col_right + 1, king, skipped=last))

                if not king:
                    break
            elif current.color == color:
                break
            elif not last:
                last = [current]
            else:
                break
            col_right += 1

        return moves
