import copy

from src.resources.constants import ROWS, COLS, WHITE, BLACK


class Bot2:
    def __init__(self, board, game_mode):
        self.game_mode = game_mode
        self.number_of_WHITE = self.count_WHITE(board)

    def evaluate(self, board):
        score = 0
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] == 0:
                    continue
                if board[row][col].color == BLACK:
                    score += 5
                    if board[row][col].king:
                        score += 45
                    if row < 6:
                        score += 1
                    if row < 4:
                        score += 3
                    if row < 2:
                        score += 20
        score += (self.number_of_WHITE - self.count_WHITE(board)) * 30
        return score

    # Funkcja wykonująca algorytm minimax z alfa-beta cięciami
    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.game_over(board):
            return self.evaluate(board), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            moves = self.get_all_valid_moves(board, BLACK)
            for start, move in moves.items():
                for position, captured_pieces in move.items():
                    new_board = copy.deepcopy(board)
                    self.make_move(new_board, new_board[start[0]][start[1]], position[0], position[1])
                    self.remove(new_board, captured_pieces)

                    eval, returned_move = self.minimax(new_board, depth - 1, alpha, beta, False)
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (start, position)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            moves = self.get_all_valid_moves(board, WHITE)
            for start, move in moves.items():
                for position, captured_pieces in move.items():
                    new_board = copy.deepcopy(board)
                    self.make_move(new_board, new_board[start[0]][start[1]], position[0], position[1])
                    self.remove(new_board, captured_pieces)

                    eval, returned_move = self.minimax(new_board, depth - 1, alpha, beta, True)
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (start, position)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval, best_move

    def make_best_move(self, board, depth):
        new_board = copy.deepcopy(board)
        best_eval, best_move = self.minimax(new_board, depth, float('-inf'), float('inf'), True)
        return best_move

    def make_move(self, board, piece, row, col):
        board[piece.row][piece.col], board[row][col] = board[row][col], board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 and piece.color == WHITE:
            piece.make_king()
        elif row == 0 and piece.color == BLACK:
            piece.make_king()

    def remove(self, board, pieces):
        for piece in pieces:
            board[piece.row][piece.col] = 0


    def game_over(self, board):
        if not self.get_all_valid_moves(board, WHITE):
            return True
        if not self.get_all_valid_moves(board, BLACK):
            return True
        return False

    def count_WHITE(self, board):
        number_of_WHITE = 0
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] != 0 and board[row][col].color == WHITE:
                    number_of_WHITE += 1
        return number_of_WHITE

    # {(row, kol): {(row, kol): [pieces,]}} - słownik zawierający wszystkie możliwe ruchy
    def get_all_valid_moves(self, board, color):
        moves = {}
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] != 0 and board[row][col].color == color:
                    piece = board[row][col]
                    valid_moves = self._get_valid_moves(board, piece)
                    if valid_moves:
                        moves[(row, col)] = valid_moves
        return moves

    def _get_valid_moves(self, board, piece):
        moves = {}
        col_left = piece.col - 1
        col_right = piece.col + 1
        row = piece.row

        if piece.king:
            if self.game_mode.king_multiple_moves:
                moves.update(self._traverse_left(board, row - 1, -1, -1, piece.color, col_left, True))
                moves.update(self._traverse_right(board, row - 1, -1, -1, piece.color, col_right, True))
                moves.update(self._traverse_left(board, row + 1, ROWS, 1, piece.color, col_left, True))
                moves.update(self._traverse_right(board, row + 1, ROWS, 1, piece.color, col_right, True))
            else:
                moves.update(self._traverse_left(board, row - 1, max(row - 3, -1), -1, piece.color, col_left, False))
                moves.update(self._traverse_right(board, row - 1, max(row - 3, -1), -1, piece.color, col_right, False))
                moves.update(self._traverse_left(board, row + 1, min(row + 3, ROWS), 1, piece.color, col_left, False))
                moves.update(self._traverse_right(board, row + 1, min(row + 3, ROWS), 1, piece.color, col_right, False))

        elif self.game_mode.reverse_beat:
            reverse_moves = {}
            if piece.color == BLACK:
                reverse_moves.update(
                    self._traverse_left(board, row + 1, min(row + 3, ROWS), 1, piece.color, col_left, False))
                reverse_moves.update(
                    self._traverse_right(board, row + 1, min(row + 3, ROWS), 1, piece.color, col_right, False))
                for move in reverse_moves:
                    if len(reverse_moves[move]) > 0:
                        moves[move] = reverse_moves[move]

                moves.update(self._traverse_left(board, row - 1, max(row - 3, -1), -1, piece.color, col_left, False))
                moves.update(self._traverse_right(board, row - 1, max(row - 3, -1), -1, piece.color, col_right, False))
            else:
                reverse_moves.update(
                    self._traverse_left(board, row - 1, max(row - 3, -1), -1, piece.color, col_left, False))
                reverse_moves.update(
                    self._traverse_right(board, row - 1, max(row - 3, -1), -1, piece.color, col_right, False))
                for move in reverse_moves:
                    if len(reverse_moves[move]) > 0:
                        moves[move] = reverse_moves[move]

                moves.update(self._traverse_left(board, row + 1, min(row + 3, ROWS), 1, piece.color, col_left, False))
                moves.update(self._traverse_right(board, row + 1, min(row + 3, ROWS), 1, piece.color, col_right, False))

        else:
            if piece.color == BLACK:
                moves.update(self._traverse_left(board, row - 1, max(row - 3, -1), -1, piece.color, col_left, False))
                moves.update(self._traverse_right(board, row - 1, max(row - 3, -1), -1, piece.color, col_right, False))
            else:
                moves.update(self._traverse_left(board, row + 1, min(row + 3, ROWS), 1, piece.color, col_left, False))
                moves.update(self._traverse_right(board, row + 1, min(row + 3, ROWS), 1, piece.color, col_right, False))

        if self.game_mode.obligatory_best_beat:
            best_move = 0
            for move in moves:
                best_move = max(best_move, len(moves[move]))
            available_moves = {}
            for move in moves:
                if len(moves[move]) == best_move:
                    available_moves[move] = moves[move]
            return available_moves

        return moves

    def _traverse_left(self, board, start, stop, step, color, col_left, king, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if col_left < 0:
                break

            current = board[r][col_left]
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
                    moves.update(
                        self._traverse_left(board, r + step, row, step, color, col_left - 1, king, skipped=last))
                    moves.update(
                        self._traverse_right(board, r + step, row, step, color, col_left + 1, king, skipped=last))

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

    def _traverse_right(self, board, start, stop, step, color, col_right, king, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if col_right >= COLS:
                break

            current = board[r][col_right]
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
                    moves.update(
                        self._traverse_left(board, r + step, row, step, color, col_right - 1, king, skipped=last))
                    moves.update(
                        self._traverse_right(board, r + step, row, step, color, col_right + 1, king, skipped=last))

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
