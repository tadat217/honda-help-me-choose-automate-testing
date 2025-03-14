import json

with open('json/question.json', 'r') as f:
    question_data = json.load(f)

current_workflow = []
workflow_json = []
idx = 0
def build_workflow(i):
    global current_workflow, workflow_json, idx
    
    if i == len(question_data):
       # print(current_workflow)
        data_str = {'id' : idx, 'workflow' : str(current_workflow)}
        workflow_json.append(data_str)
        idx += 1
        return
    data = question_data[i]
    for j in range(len(data['answear'])):
        parents = data['parents']
        parent_id = [(parent['question_id'], parent['answear_id']) for parent in parents]
        if len(parent_id) == 0 or any(parent in current_workflow for parent in parent_id):
            current_workflow.append((data['id'], j))
            build_workflow(i + 1)
            current_workflow.pop()
        else:
            build_workflow(i + 1)
            break

for i in range(len(question_data)):
    if(len(question_data[i]['parents']) == 0):
        build_workflow(i)
with open('json/workflow.json', 'w') as f:
    json.dump(workflow_json, f)