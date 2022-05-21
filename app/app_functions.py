################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
## This project can be used freely for all uses, as long as they maintain the
## respective credits only in the Python scripts, any information in the visual
## interface (GUI) can be modified without any implication.
##
## There are limitations on Qt licenses if you want to use your products
## commercially, I recommend reading them on the official website:
## https://doc.qt.io/qtforpython/licenses.html
##
################################################################################

## ==> GUI FILE
from main import *


class Functions(MainWindow):
    def display(self,s):
        for row in range(len(s)):
            for column in range(len(s[row])): 
                item = QTableWidgetItem(s[row][column])
                self.ui.tableWidget_2.setItem(row,column,item)
            cur_total_row = self.ui.tableWidget_2.rowCount()
            cur_row = cur_total_row + 1
            self.ui.tableWidget_2.setRowCount(cur_row) 

    def btn_search_is_clicked(self,db):
        self.ui.tableWidget_2.clear()
        self.ui.tableWidget_2.setRowCount(3)
        current_state = self.ui.comboBox_2.currentIndex()
        c = db.cursor()
        s = Functions.combo_state(self,current_state,c)
        # print(len(s))
        if len(s)>0:
            self.ui.label_issue.setText(s[0][0])
            str = ""
            if s[0][1] is not None:
                choice  = s[0][1].split('\n')
                for i in range(len(choice)):
                    str += choice[i]+'\n\n'
            self.ui.label_choice.setText(str)
            self.ui.label_res.setText(s[0][2])
            Functions.display(self,s)
    
    def get_pos_content(self):
        try:
            row = self.ui.tableWidget_2.currentIndex().row()
            content = [self.ui.tableWidget_2.item(row,col).text() for col in range(3)]
            self.ui.label_issue.setText(content[0])
            str = ""
            if content[1] is not None:
                choice  = content[1].split('\n')
                for i in range(len(choice)):
                    str += choice[i]+'\n\n'
            self.ui.label_choice.setText(str)
            self.ui.label_res.setText(content[2])
        except Exception as e:
            pass

    def combo_state(self,current_state,c):
        if current_state == 0:
            text = self.ui.lineEdit_2.text()
            sql = "SELECT * FROM QUESTIONS WHERE ISSUE LIKE '%"+text+"%' Order by choice"
        # print(text)
            c.execute(sql)
            s = list(c.fetchall())
        elif current_state == 1:
            text = self.ui.lineEdit_2.text()
            sql = "SELECT * FROM QUESTIONS WHERE ISSUE LIKE '%"+text+"%' and CHOICE is null"
        # print(text)
            c.execute(sql)
            s = list(c.fetchall())
        elif current_state==2:
            text = self.ui.lineEdit_2.text()
            sql = "SELECT * FROM QUESTIONS WHERE ISSUE LIKE '%"+text+"%' and CHOICE is not null"
        # print(text)
            c.execute(sql)
            s = list(c.fetchall())
        return s
    
    def combo_select(self,db):
        current_state = self.ui.comboBox_2.currentIndex()
        c = db.cursor()
        s=[]
        self.ui.tableWidget_2.clear()
        self.ui.tableWidget_2.setRowCount(3)
        
        s = Functions.combo_state(self,current_state,c)
        
        Functions.display(self,s)
            
    def enter_is_pressed(self,db):
        Functions.btn_search_is_clicked(self,db)