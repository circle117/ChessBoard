import numpy as np
import math

def chessBoard(array_board, row, col, cur_row, cur_col, size):
    """
    棋盘覆盖
    """
    if size==1:
        return
    global num
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
    while(True):
        size, x, y = map(int, input("输入棋盘大小及坐标：").split(' '))
        size = int(math.pow(2,size))
        num = 0
        array_board = np.zeros((size,size), dtype='int32')
        chessBoard(array_board,0,0,x-1,y-1,size)
        #print(array_board)
        for i in range(size):
            for j in range(size-1):
                if array_board[i,j]==0:
                    print("#",end=" ")
                else:
                    print(array_board[i,j],end=' ')
            if array_board[i,size-1]==0:
                print("#",end=" ")
            else:
                print(array_board[i,size-1],end=' ')
            print()