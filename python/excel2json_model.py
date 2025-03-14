import pandas as pd
import json

qa_map = {}

def is_empty_row(row):
    return all(pd.isna(cell) for cell in row)

def process_excel_to_json(excel_file):
    
    global qa_map

    excel = pd.ExcelFile(excel_file)

    result = {}

    vehicle_type_map = {
        "MOTORCYCLE": 0,
        "ATV": 1,
        "SIDE-BY-SIDE": 2
    }

    i = 0

    for sheet_name in excel.sheet_names[1:]:
        #print('sheet_name', sheet_name)
        df = pd.read_excel(excel_file, sheet_name=sheet_name, header=0)
        
        headers = list(df.columns.values)
        print(headers)

        for idx, row in df.iterrows():
            model_name = row.iloc[1]
            model_type = row.iloc[2]
            if pd.isna(model_type) or pd.isna(model_name):
                continue
            
            i += 1
            last_question = None
            filters = [(0, vehicle_type_map[model_type])]
            for col_idx, col_name in enumerate(headers):
                if col_idx > 2:
                    assert pd.notna(col_name), f"Sheet {sheet_name} row {idx} col {col_idx} is empty"
                    if col_name[-1] == '#': #is question
                        last_question = col_name[:-1].strip()
                    else:
                        assert pd.isna(row.iloc[col_idx]) or row.iloc[col_idx].strip() != '' or row.iloc[col_idx].strip() == 'X', f"Sheet {sheet_name} row {idx} col {col_idx} is not valid (X or empty)"
                        if  pd.notna(row.iloc[col_idx]) and row.iloc[col_idx].strip() != '' and row.iloc[col_idx].strip() == 'X':
                            answear = col_name.strip()
                            assert last_question is not None, f"Sheet {sheet_name} no question before {col_name}"
                            assert (last_question, answear) in qa_map, f"Error: Sheet {sheet_name} question {last_question} answear {answear}"
                            filters.append(qa_map[(last_question, answear)])
            
            result[model_name] = {
                "id": i,
                "name": model_name,
                "type_of_vehicle": model_type,
                "filters": str(filters)
            }

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
#print(qa_map)
#Ghi ra file JSON
with open('json/model.json', 'w', encoding='utf-8') as f:
     json.dump(json_data, f, indent=2, ensure_ascii=False)