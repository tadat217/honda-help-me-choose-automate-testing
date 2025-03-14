import pandas as pd
import json
import re
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string

def process_excel_to_json(excel_file):
    data = []
    id = 0
    excel = pd.ExcelFile(excel_file)
    df = pd.read_excel(excel_file, sheet_name=excel.sheet_names[0], header=1)
    #print(df)
    
    # Lưu trữ các câu hỏi và câu trả lời để tham chiếu sau này
    question_map = {}
    
    for index, r in df.iterrows():
        row = r.iloc[1:]
        if(pd.notna(row.iloc[1])):
            question_text = row.iloc[0].strip()
            answers = [row.iloc[i].strip() for i in range(1, len(row)) if pd.notna(row.iloc[i])]
            
            parent_info = []
            if '#' in question_text:
                parts = question_text.split('#')
                question_text = parts[0].strip()
                location_info = parts[1].strip()

                locations = re.findall(r'([A-Z]+\d+)', location_info)
                #print(locations)
                for location in locations:
                    xy = coordinate_from_string(location)
                    col = column_index_from_string(xy[0])
                    row = xy[1]
                    parent_question_id = question_map[df.iloc[row-3, 1].split('#')[0].strip()]
                    parent_answear_id = col - 3
                    parent_info.append({
                        "question_id": parent_question_id,
                        "answear_id": parent_answear_id
                    })

            current_item = {
                "id": id,
                "question": question_text,
                "answear": answers,
                "parents": parent_info
            }
            question_map[question_text] = id

            data.append(current_item)
            
            id += 1
    with open('json/question.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    process_excel_to_json("Bike Chooser _ Honda Powersports - Street.xlsx")
        