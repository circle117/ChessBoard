import numpy as np

def chessBoard(array_board, row, col, cur_row, cur_col, size):
    """
    棋盘覆盖
    """
    if size==1:
        return
    num += 1
    t = num
    s = size//2
    # 左上
    if cur_row<row+s and cur_col<col+s:
        chessBoard(array_board, row, col, cur_row, cur_col, s)
    else:
        array_board[row+s-1, col+s-1] = t
        chessBoard(array_board, row, col, row+s-1, col+s-1, s)
    # 右上
    if cur_row<row+s and cur_col>=col+s:
        chessBoard(array_board, row, col+s, cur_row, cur_col, s)
    else:
        array_board[row+s-1, col+s] = t
        chessBoard(array_board, row, col+s, row+s-1, col+s, s)
    # 左下
    if cur_row>=row+s and cur_col<col+s:
        chessBoard(array_board, row+s, col, cur_row, cur_col, s)
    else:
        array_board[row+s, col+s-1] = t
        chessBoard(array_board, row+s, col, row+s, col+s-1, s)
    # 右下
    if cur_row>=row+s and cur_col>=col+s:
        chessBoard(array_board, row+s, col+s, cur_row, cur_col, s)
    else:
        array_board[row+s, col+s] = t
        chessBoard(array_board, row+s, col+s, row+s, col+s, s)
    return array_board

if __name__=="__main__":
    size = 8
    chessBoard(0,0,2,2,size)
    print(array_board)