from tkinter import *
from tkinter.ttk import *

#风险识别因素
#A类
A1 = 'A1'
A2 = 'A2'
A3 = 'A3'
A4 = 'A4'
A5 = 'A5'
A6 = 'A5'
#B类
B1 = 'B1'
B2 = 'B2'
B3 = 'B3'
B4 = 'B4'
B5 = 'B5'
B6 = 'B6'
B7 = 'B7'
B8 = 'B8'
B9 = 'B9'
B10 = '10'
B11 = '11'
B12 = '12'
#C类
C1 = 'C1'
C2 = 'C2'
C3 = 'C3'
C4 = 'C4'
C5 = 'C5'
C6 = 'C6'
#D类
D1 = 'D1'
D2 = 'D2'
D3 = 'D3'
#E类，探索性质
E1 = 'E1'
E2 = 'E2'
E3 = 'E3'
E4 = 'E4'
E5 = 'E5'
E6 = 'E6'

#风险评估表
highest_risk_list = [A1, A2, A3, A4, A5, A6]
higher_risk_list1 = [B4, B5, B6, B7, B8, B9, B10, B11, B12]
higher_risk_list2 = [B2, B3, C1, C2, C3, C4, C5, C6, B12, D1, D2, D3]

class GUI():
    def __init__(self, button_dict):
        self.root = Tk()
        self.root.title("Risk Tool")
        self.root.resizable(0, 0)
        self.button_dict = button_dict
        self.row = len(self.button_dict) + 1


        Label(self.root, text=' ( 请选择以下符合用户信息的选项, 每次提交后请点击【重置选项】按钮) ').grid(row=0, sticky=W)
        for i, key in enumerate(self.button_dict, 1):
            self.button_dict[key] = IntVar()
            c = Checkbutton(self.root, text=key, variable=self.button_dict[key])
            if i % 2 == 0:
                col = 1
                c.grid(row=i-1, column=col, sticky=W)
            else:
                col = 0
                c.grid(row=i, column=col, sticky=W)

        self.include = Button(self.root, text='提交',
                              command=self.query_include, state='active').grid(row=self.row+1, sticky=E)
        self.clear = Button(self.root, text='重置选项',
                            command=self.clear_select, state='active').grid(row=self.row+2, sticky=E)

    def clear_select(self):
        for i, key in enumerate(self.button_dict, 1):
            self.button_dict[key].set(0)
        self.label1.destroy()
        self.label2.destroy()
        self.label3.destroy()
        self.include = Button(self.root, text='提交',
                              command=self.query_include, state='active').grid(row=self.row + 1, sticky=E)

    def query_include(self):
        higher_risk_list2_times = 0
        self.result_status = 0
        self.label1 = Label(self.root, text='测试结果：高风险', background='OrangeRed')
        self.label2 = Label(self.root, text='测试结果：较高风险', background='Yellow')
        self.label3 = Label(self.root, text='测试结果：一般风险', background='Lawngreen')
        for key, value in self.button_dict.items():
            if value.get() and key in higher_risk_list2:
                higher_risk_list2_times += 1
        for key, value in self.button_dict.items():
            if value.get() and key in highest_risk_list:
                self.label1.grid(row=self.row + 1, column=1, sticky=W, padx=50)
                self.result_status = 1
            elif self.button_dict[B1].get() == 1 and value.get() and key in higher_risk_list1 and higher_risk_list2_times >= 2:
                self.label2.grid(row=self.row + 1, column=1, sticky=W, padx=50)
                self.result_status = 1
        if self.result_status == 0:
            self.label3.grid(row=self.row + 1, column=1, sticky=W, padx=50)
        self.include = Button(self.root, text='提交',
                              command=self.query_include, state='disabled').grid(row=self.row+1, sticky=E)

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    button_dict = {A1:0, A2:0, A3:0, A4:0, A5:0, A6:0,
                   B1:0, B2:0, B3:0, B4:0, B5:0, B6:0, B7:0, B8:0, B9:0, B10:0, B11:0, B12:0,
                   C1:0, C2:0, C3:0, C4:0, C5:0, C6:0,
                   D1:0, D2:0, D3:0,}
    gui = GUI(button_dict)
    gui.main()