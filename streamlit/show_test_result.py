import streamlit as st
import pandas as pd
import numpy as np
import json
import os

st.title("Test Results 📊")

question_data = {}

with open('json/question.json', 'r') as f:
    question_data = json.load(f)
with open('json/workflow.json', 'r') as f:
    workflow_data = json.load(f)

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
            #for model in workflow['expected_models']:
            #    st.markdown(f"Model: {model}")

            st.markdown(f"#### Workflow {workflow['workflow_id']} details")
            st.markdown(f"**Expected Models**")
            st.markdown(f"{' | '.join([f'{m}' for m in workflow['expected_models']])}")
            for i, res in enumerate(workflow['result_displayed']):
                st.markdown(f":blue[**Step {i+1}**]")
                (question_id, answear_id) = eval(workflow_data[int(id)]['workflow'])[i]
                st.markdown("**Expected Q/A**")
                st.markdown(f"'{question_data[question_id]['question']}'")
                st.markdown(f"{' | '.join([f"'**{a}**'" if idx == answear_id else f"'{a}'" for idx, a in enumerate(question_data[question_id]['answear'])])}")
                st.markdown("**Received Q/A**")
                st.markdown(f"'{res['question']}'")
                st.markdown(f"{' | '.join([f"'{a}'" for a in res['answers']])}")
                st.markdown("**Received Models**")
                st.markdown(f"{' | '.join([f'{m}' for m in res['models']])}")
                #st.markdown(f"{' | '.join([f"'**{a}**'" if idx == res['answear_id'] else f"'{a}'" for idx, a in enumerate(question_data[question_id]['answear'])])}")
                missed_models = [m for m in workflow['expected_models'] if m not in res['models']]
                if len(missed_models) > 0:
                    st.markdown(f"**:red[Missed Models]**")
                    st.markdown(f"{' | '.join([f'{m}' for m in missed_models])}")

# Nội dung cho Tab B
with tab_b:
    st.header("Đây là Tab B")
    st.markdown("""
    Tab này cho phép bạn tải lên file và tùy chỉnh các thông số.
    
    *Hãy thử các tính năng tương tác!*
    """)