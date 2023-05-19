from src.main.model.checker import Checker
from src.resources.constants import ROWS, COLS, BLACK, WHITE


class Bot:
    def __init__(self, game_mode):
        self.game_mode = game_mode
        self.deep = game_mode.difficulty.value[1]
        self.bot_turn = True

    def find_best_move(self, board):
        copied_board = self.copy_board(board)
        start_position, move = self._find_best_move(copied_board, [0, 0], [(0, 0), -1], 0)

        if start_position == [ROWS - 1, COLS - 1] and move == [(0, 0), -1]:
            for row in range(ROWS):
                for col in range(COLS):
                    if board[row][col] != 0 and board[row][col].color == BLACK:
                        piece = board[row][col]
                        moves = self._get_valid_moves(board, piece)
                        for move in moves:
                            return [row, col], [move, -1]
        return start_position, move

    def _find_best_move(self, board, start_position, first_move, deep):  # first_move = [(r,c),x]
        if self.bot_turn:
            self.bot_turn = False
            if deep == self.deep:
                return start_position, first_move
            elif deep == 0:
                best_move = first_move
                best_start_position = start_position
                for row in range(ROWS):
                    for col in range(COLS):
                        start_position[0] = row
                        start_position[1] = col
                        if board[row][col] != 0 and board[row][col].color == BLACK:
                            piece = board[row][col]
                            moves = self._get_valid_moves(board, piece)
                            for move in moves:
                                new_board = self.copy_board(board)
                                new_piece = new_board[row][col]
                                new_first_move = list(first_move)
                                self.move(new_board, new_piece, move[0], move[1])
                                new_first_move[0] = move
                                skipped = moves[move]
                                if skipped:
                                    new_first_move[1] += len(skipped)
                                    self.remove(new_board, skipped)

                                (wyn_position, wyn_move) = self._find_best_move(new_board, list(start_position),
                                                                                new_first_move, deep + 1)
                                if wyn_move[1] > best_move[1]:
                                    best_start_position = wyn_position
                                    best_move = wyn_move
                return (best_start_position, best_move)
            else:
                best_move = first_move
                best_start_position = start_position
                for row in range(ROWS):
                    for col in range(COLS):
                        if board[row][col] != 0 and board[row][col].color == BLACK:
                            piece = board[row][col]
                            moves = self._get_valid_moves(board, piece)
                            for move in moves:
                                new_board = self.copy_board(board)
                                new_piece = new_board[row][col]
                                new_first_move = list(first_move)
                                self.move(new_board, new_piece, move[0], move[1])
                                skipped = moves[move]
                                if skipped:
                                    new_first_move[1] += len(skipped)
                                    self.remove(new_board, skipped)
                                (wyn_position, wyn_move) = self._find_best_move(new_board, list(start_position),
                                                                                new_first_move, deep + 1)
                                if wyn_move[1] > best_move[1]:
                                    best_start_position = wyn_position
                                    best_move = wyn_move
                return (best_start_position, best_move)
        else:
            self.bot_turn = True
            current_best_move = [(0, 0), -1]
            from_row_col = [0, 0]
            skipped = []
            for row in range(ROWS):
                for col in range(COLS):
                    if board[row][col] != 0 and board[row][col].color == WHITE:
                        piece = board[row][col]
                        moves = self._get_valid_moves(board, piece)
                        for move in moves:
                            if len(moves[move]) > current_best_move[1]:
                                current_best_move = [move, len(moves[move])]
                                from_row_col = [row, col]
                                skipped = moves[move]
            piece = board[from_row_col[0]][from_row_col[1]]
            if piece == 0 or piece.color != WHITE:
                return (start_position, first_move)
            self.move(board, piece, current_best_move[0][0], current_best_move[0][1])
            if skipped:
                self.remove(board, skipped)
                first_move[1] -= len(skipped)
            return self._find_best_move(board, start_position, first_move, deep)

    def copy_board(self, board):
        new_board = [[0 for _ in range(ROWS)] for _ in range(COLS)]
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] == 0:
                    new_board[row][col] = 0
                elif board[row][col].color == BLACK:
                    new_board[row][col] = Checker(row, col, BLACK)
                    new_board[row][col].king = board[row][col].king
                else:
                    new_board[row][col] = Checker(row, col, WHITE)
                    new_board[row][col].king = board[row][col].king
        return new_board

    def move(self, board, piece, row, col):
        board[piece.row][piece.col], board[row][col] = board[row][col], board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 and piece.color == WHITE:
            piece.make_king()
        elif row == 0 and piece.color == BLACK:
            piece.make_king()

    def remove(self, board, pieces):
        for piece in pieces:
            board[piece.row][piece.col] = 0

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

        if self.game_mode.obligatory_beat:
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
