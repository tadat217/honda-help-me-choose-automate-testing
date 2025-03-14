import pandas as pd
import json

qa_map = {}

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
        df = pd.read_excel(excel_file, sheet_name=sheet_name, header=0)
        
        headers = list(df.columns.values)
        print(headers)

        for col_idx, col_name in enumerate(headers):
            if col_idx < 1: 
                continue
                
            if col_idx == 1:
                for row_idx, value in enumerate(df.iloc[:, col_idx]):
                    if pd.notna(value) and not is_empty_row(df.iloc[row_idx]):
                        print(value)

    return result

    qa_map = json.load(f)
with open('json/question.json', 'r') as f:
    question_data = json.load(f)
for question in question_data:
    #qa_map[question['id']] = question['question']
    for idx, answer in enumerate(question['answear']):
        tpl = ((question['question'], answer))
        qa_map[tpl] = (question['id'], idx)

# Sử dụng function
excel_file = "Bike Chooser _ Honda Powersports - Street.xlsx"

json_data = process_excel_to_json(excel_file)

#Ghi ra file JSON
with open('json/model.json', 'w', encoding='utf-8') as f:
     json.dump(json_data, f, indent=2, ensure_ascii=False)