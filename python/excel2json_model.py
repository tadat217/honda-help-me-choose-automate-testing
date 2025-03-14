import pandas as pd
import json

def is_empty_row(row):
    return all(pd.isna(cell) for cell in row)

def process_excel_to_json(excel_file):

    excel = pd.ExcelFile(excel_file)

    result = {"models": []}

    vehicle_type_map = {
        "MOTORCYCLE": 0,
        "ATV": 1,
        "SIDE-BY-SIDE": 2
    }

    for sheet_name in excel.sheet_names[1:]:
        print('sheet_name', sheet_name)
        df = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
        
        current_category = None
        headers = []
        question_start_col = 4  # Cột E bắt đầu từ index 4
        #print('len: ' + str(len(df)))
        #print(df)
        # for i in range(len(df)):
        #     row = df.iloc[i]
        #     print(row)
        i = 0
        while i < len(df):
            row = df.iloc[i]

            if pd.isna(row.iloc[0]):
                current_category = None
                headers = []
                i += 1
                if(i == len(df)):
                    break
            
            # start process data for table 
            row = df.iloc[i]
            current_category = row.iloc[2] # column C
            i += 1
            data_bg = i + 1
            data_en = data_bg
            while(i < len(df)):
                row = df.iloc[i]
                i += 1
                data_en = i
                if pd.isna(row.iloc[0]):
                    break
            
        #     for j in range(data_bg, data_en):
        #         row = df.iloc[j]
        #         print(j,row)
        #         # model_data = {
        #         #     'name': row.iloc[1],
        #         #     'category': current_category,
        #         #     'type_of_vehicle': vehicle_type_map[row.iloc[2]],
        #         # }

    return result

# Sử dụng function
excel_file = "Bike Chooser _ Honda Powersports - Street.xlsx"
json_data = process_excel_to_json(excel_file)

# Ghi ra file JSON
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, indent=2, ensure_ascii=False)