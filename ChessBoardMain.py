import sys
import numpy as np
import math
import time

from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QScrollArea
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QPolygon, QFont
from MainWindow import Ui_MainWindow
from ChessBoard import chessBoard

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setupUi(self)
        self.canvas_size = 300
        self.rect_size = 0
        self.grid = False
        self.cur_num = 0
        self.num = 0
        self.color_R = []
        self.color_G = []
        self.color_B = []
        self.btn_next.setEnabled(False)

        self.btn_show.clicked.connect(self.board_show)
        self.btn_next.clicked.connect(self.next_step)

    def board_show(self):
        """
        显示棋盘
        """
        self.rect_size = 0
        self.grid = False
        self.cur_num = 0
        self.num = 0
        self.color_R = []
        self.color_G = []
        self.color_B = []
        self.btn_next.setEnabled(True)

        # 获取棋盘大小以及特殊格子坐标
        self.size = int(math.pow(2, int(self.spinBox_size.text())))
        print("size:", self.size)
        self.special_x = int(self.spinBox_x.text()) - 1
        self.special_y = int(self.spinBox_y.text()) - 1
        print("location:", self.special_x , "," , self.special_y)
        self.array_board = np.zeros((self.size, self.size),dtype=np.int8)
        self.count = 0
        self.chessBoard(0, 0, self.special_x, self.special_y, self.size)
        print(self.array_board)

        # 初始化颜色列表
        self.set_color()
        """
        for i in range(0, self.array_board.max()):
            self.color_R.append(128 + (255-128)*i/self.array_board.max())
            self.color_G.append(128 + (255-128)*i/self.array_board.max())
            self.color_B.append(255)
        """

        # 绘制棋盘
        if self.size<=16:
            self.rect_size = self.canvas_size//self.size
        else:
            self.rect_size = 10
        self.grid = True
        self.update()

    def next_step(self):
        """
        显示下一步结果
        """
        self.num += 1
        self.update()                       # 刷新窗口
        if self.num==self.array_board.max():
            self.btn_next.setEnabled(False)

    def paintEvent(self,event):
        painter = QPainter(self)
        if self.grid:
            #painter.begin(self)
            # 绘制棋盘
            self.draw_grid(painter)
            self.draw_rect(painter, self.special_x, self.special_y)
            #painter.end()
        for i in range(1, self.num+1):
            self.draw_L(painter,np.where(self.array_board==i), i)
            #self.draw_rect(painter, x, y)


    def draw_grid(self, qp):
        """
        绘制棋盘
        """
        pen = QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)

        if self.size>16:
            self.desktop = QApplication.desktop()
            self.screenRect = self.desktop.screenGeometry()
            height = self.screenRect.height()
            width = self.screenRect.width()
            self.resize(width, height)
        else:
            self.resize(510,400)
        width = self.rect_size*self.size
        for i in range(80, 80+self.rect_size*(self.size+1), self.rect_size):
            qp.drawLine(105, i, 105+width, i)
        for i in range(105, 105+self.rect_size*(self.size+1), self.rect_size):
            qp.drawLine(i, 80, i, 80+width)

    def draw_rect(self, qp, x, y):
        """
        绘制特殊方格
        """
        brush = QBrush(QtCore.Qt.SolidPattern)
        brush.setColor(QColor(0,0,0))
        qp.setBrush(brush)
        qp.drawRect(105+y*self.rect_size, 80+x*self.rect_size,
                    self.rect_size, self.rect_size)

    def draw_L(self, qp, points, num):
        """
        绘制L
        """
        row = points[0]
        col = points[1]
        begin_x = 105+col[0]*self.rect_size
        begin_y = 80+row[0]*self.rect_size
        points = [QPoint(begin_x, begin_y)]
        
        if row[1]==row[0] and col[1]>col[0] and row[2]>row[0] and col[2]==col[0]:
            #1
            points.append(QPoint(begin_x, begin_y+2*self.rect_size))
            points.append(QPoint(begin_x+self.rect_size, begin_y+2*self.rect_size))
            points.append(QPoint(begin_x+self.rect_size, begin_y+self.rect_size))
            points.append(QPoint(begin_x+2*self.rect_size, begin_y+self.rect_size))
            points.append(QPoint(begin_x+2*self.rect_size, begin_y))
        elif row[1]==row[0] and col[1]>col[0] and row[2]>row[0] and col[2]>col[0]:
            #2
            points.append(QPoint(begin_x, begin_y+self.rect_size))
            points.append(QPoint(begin_x+self.rect_size, begin_y+self.rect_size))
            points.append(QPoint(begin_x+self.rect_size, begin_y+2*self.rect_size))
            points.append(QPoint(begin_x+2*self.rect_size, begin_y+2*self.rect_size))
            points.append(QPoint(begin_x+2*self.rect_size, begin_y))
        elif row[1]>row[0] and col[1]==col[0] and row[2]>row[0] and col[2]>col[0]:
            #3
            points.append(QPoint(begin_x, begin_y+2*self.rect_size))
            points.append(QPoint(begin_x+2*self.rect_size, begin_y+2*self.rect_size))
            points.append(QPoint(begin_x+2*self.rect_size, begin_y+self.rect_size))
            points.append(QPoint(begin_x+self.rect_size, begin_y+self.rect_size))
            points.append(QPoint(begin_x+self.rect_size, begin_y))
        else:
            points.append(QPoint(begin_x, begin_y+self.rect_size))
            points.append(QPoint(begin_x-self.rect_size, begin_y+self.rect_size))
            points.append(QPoint(begin_x-self.rect_size, begin_y+2*self.rect_size))
            points.append(QPoint(begin_x+self.rect_size, begin_y+2*self.rect_size))
            points.append(QPoint(begin_x+self.rect_size, begin_y))
        brush = QBrush(QtCore.Qt.SolidPattern)
        color_control = int(math.sqrt(row[0]*row[0]+col[0]*col[0]))-1
        brush.setColor(QColor(self.color_R[color_control],self.color_G[color_control],self.color_B[color_control]))
        qp.setBrush(brush)
        qp.drawPolygon(QPolygon(points))

        # 标注顺序
        qp.setPen(QColor(0,0,0))
        qp.setFont(QFont('SimSun', 10))
        qp.drawText(QRect(begin_x, begin_y, self.rect_size, self.rect_size), QtCore.Qt.AlignCenter, str(num))

    def set_color(self):
        """
        设定颜色
        """
        len = self.size-1
        full = int(math.sqrt(len*len+len*len))
        for i in range(0, full):
            if i<full/3:
                self.color_R.append(255)
                self.color_G.append(math.ceil(255*3*i/full))
                self.color_B.append(0)
            elif i<full/2:
                self.color_R.append(math.ceil(750-i*(250*6/full)))
                self.color_G.append(255)
                self.color_B.append(0)
            elif i<full*2/3:
                self.color_R.append(0)
                self.color_G.append(255)
                self.color_B.append(math.ceil(i*(250*6/full)-750))
            elif i<full*5/6:
                self.color_R.append(0)
                self.color_G.append(math.ceil(1250-i*(250*6/full)))
                self.color_B.append(255)
            else:
                self.color_R.append(math.ceil(150*i*(6/full)-750))
                self.color_G.append(0)
                self.color_B.append(255)
    
    def chessBoard(self, row, col, cur_row, cur_col, size):
        """
        棋盘覆盖
        """
        if size==1:
            return
        self.count += 1
        t = self.count
        s = size//2
        # 左上
        if cur_row<row+s and cur_col<col+s:
            self.chessBoard(row, col, cur_row, cur_col, s)
        else:
            self.array_board[row+s-1, col+s-1] = t
            self.chessBoard(row, col, row+s-1, col+s-1, s)
        # 右上
        if cur_row<row+s and cur_col>=col+s:
            self.chessBoard(row, col+s, cur_row, cur_col, s)
        else:
            self.array_board[row+s-1, col+s] = t
            self.chessBoard(row, col+s, row+s-1, col+s, s)
        # 左下
        if cur_row>=row+s and cur_col<col+s:
            self.chessBoard(row+s, col, cur_row, cur_col, s)
        else:
            self.array_board[row+s, col+s-1] = t
            self.chessBoard(row+s, col, row+s, col+s-1, s)
        # 右下
        if cur_row>=row+s and cur_col>=col+s:
            self.chessBoard(row+s, col+s, cur_row, cur_col, s)
        else:
            self.array_board[row+s, col+s] = t
            self.chessBoard(row+s, col+s, row+s, col+s, s)


if __name__=="__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())