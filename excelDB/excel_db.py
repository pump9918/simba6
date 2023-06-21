import os
import pandas as pd

class ExcelDB:
    def __init__(self):
        self.file_path = self.get_file_path()
        self.sheet_name = '동국대'
        self.columns = ['classid', 'classNum', 'className', 'professor', 'time', 'classroom', 'credit']
          
    def get_file_path(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = 'Dongguksheet.xlsx'  # 엑셀 파일의 이름을 업데이트하세요
        return os.path.join(current_dir, file_name)
    
    def read_data(self):
        try:
            data = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
            data = data[self.columns].to_dict('records')
            return data
        except FileNotFoundError:
            return []
    
    def write_data(self, data):
        df = pd.DataFrame(data, columns=self.columns)
        df.to_excel(self.file_path, index=False, sheet_name=self.sheet_name)
