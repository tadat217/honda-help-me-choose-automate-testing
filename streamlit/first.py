import streamlit as st
import pandas as pd
import numpy as np
import json
import os

st.title("Test Results 📊")

# Tạo 2 tab với st.tabs
tab_a, tab_b = st.tabs(["Workflow", "Models"])

# Nội dung cho Tab A
with tab_a:

    # Lấy tất cả các file JSON có chứa "test_result_workflow_" trong thư mục json
    json_files = [f for f in os.listdir('json') if f.startswith('test_result_workflow_') and f.endswith('.json')]
    
    workflow_results = {}
    for file in json_files:
        file_path = os.path.join('json', file)
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                workflow_results.update(data)
        except Exception as e:
            st.error(f"Error when read file {file}: {str(e)}")
    
    cnt_passed_workflow = 0
    cnt_failed_workflow = 0

    st.header("Summary", divider=True)
    for id, workflow in workflow_results.items():
        if workflow['status'] == 'passed':  
            cnt_passed_workflow += 1
        else:
            cnt_failed_workflow += 1

    st.write(f"Total workflow: {len(workflow_results)}")
    st.markdown(f":green[Passed workflow: {cnt_passed_workflow}]")
    st.markdown(f":red[Failed workflow: {cnt_failed_workflow}]")

    st.header("Detail", divider=True)
    for id, workflow in workflow_results.items():
        status = workflow['status']
        if status == 'passed':
            status_color = "green"
            icon = "✅"
        else:
            status_color = "red"
            icon = "❌"
        with st.expander(f":{status_color}[Workflow {id} - {status}] {icon}"):
            st.write(workflow)
    # Thêm expander để hiển thị nội dung có thể mở rộng/thu gọn
    # with st.expander("Nhấn vào đây để xem chi tiết về kết quả workflow"):
    #     st.markdown("""
    #     ### Chi tiết kết quả workflow
        
    #     Đây là phần nội dung chi tiết về kết quả workflow mà bạn có thể xem khi mở rộng phần này.
        
    #     #### Các thông số quan trọng:
    #     - **Tỷ lệ thành công**: 85%
    #     - **Thời gian trung bình**: 2.5 giây
    #     - **Số lượng workflow đã chạy**: 120
        
    #     #### Lưu ý:
    #     Các workflow được kiểm tra dựa trên dữ liệu từ file JSON và được xác thực thông qua các bước kiểm tra tự động.
        
    #     ```python
    #     # Ví dụ về cách workflow được xử lý
    #     async def process_workflow(page, workflow, models):
    #         for question_id, answer_id in workflow:
    #             # Xác thực câu hỏi và câu trả lời
    #             await validate_question_answer(page, question_id, answer_id)
    #             # Xác thực các model được hiển thị
    #             await validate_model_cards(page, models)
    #     ```
    #     """)
        
    #     # Hiển thị bảng dữ liệu mẫu về workflow
    #     workflow_data = pd.DataFrame({
    #         'ID': [1, 2, 3, 4, 5],
    #         'Workflow': ['[(0, 1), (7, 0)]', '[(0, 2), (11, 2)]', '[(0, 1), (8, 5)]', '[(0, 2), (13, 1)]', '[(0, 2), (12, 0)]'],
    #         'Thời gian (s)': [2.1, 3.4, 1.8, 2.7, 2.2],
    #         'Trạng thái': ['Thành công', 'Thành công', 'Lỗi', 'Thành công', 'Thành công']
    #     })
    #     st.dataframe(workflow_data)

# Nội dung cho Tab B
with tab_b:
    st.header("Đây là Tab B")
    st.markdown("""
    Tab này cho phép bạn tải lên file và tùy chỉnh các thông số.
    
    *Hãy thử các tính năng tương tác!*
    """)