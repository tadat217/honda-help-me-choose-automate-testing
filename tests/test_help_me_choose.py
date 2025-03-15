import re
import pytest
from playwright.async_api import Page, expect, Locator
import json

question_data = None
model_data = None
workflow_data = None
with open('json/question.json', 'r') as f:  
    question_data = json.load(f)

with open('json/model.example.json', 'r') as f:
    model_data = json.load(f)

with open('json/workflow.json', 'r') as f:
    workflow_data = json.load(f)

test_result = {}
    
async def process_workflow(page: Page, workflow: dict):
    global question_data, test_result
    models = workflow['models']

    print('~~~~~~~~~~~~~~~~~~~~~~~~~ WORK FLOW ~~~~~~~~~~~~~~~~~~~~~~~~~')
    
    print(str(workflow))
    
    print('~~~~~~~~~~~~~~~~~~~~~~~~~ Q/A ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    
    for question_id, answer_id in workflow['workflow']:
        print(str(question_data[question_id]['question']) + ' - ' + str(question_data[question_id]['answear'][answer_id]))
    
    print('~~~~~~~~~~~~~~~~ MODELS EXPECT TO SHOW ~~~~~~~~~~~~~~~~~~~~~~~~')
    
    print(models.keys())
    
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    models_name_expected = [key.strip() for key in models.keys()]

    test_result[workflow['id']] = {
        'workflow_id': workflow['id'],
        'status': 'failed',
        'expected_models': models_name_expected,
        'result_displayed': []
    }

    for question_id, answer_id in workflow['workflow']:

        options = page.locator('.hmc-option button')
        questionnair = page.locator('.hmc-questionnaire')
        models_locator = page.locator('.item-price h3.h6')

        models_name_displayed = []
        count = await models_locator.count()
        assert count != 0, "Models displayed are not correct."
        for i in range(count):
            text = await models_locator.nth(i).text_content()
            models_name_displayed.append(text.strip())
        
        test_result[workflow['id']]['result_displayed'].append({
            'models': models_name_displayed,
            'question': question_data[question_id]['question'],
            'answers': question_data[question_id]['answear'],
        })
        with open(f'json/test_result_workflow_{workflow["id"]}.json', 'w') as f:
            json.dump(test_result, f, indent=2)

        # Validate question and answear
        print('question_id: ' + str(question_id) + ' answer_id: ' + str(answer_id))

        await expect(questionnair, 'Question text is not correct.').to_contain_text(question_data[question_id]['question'])
        opc = await options.count()
        for j in range(opc):
            option = options.nth(j)
            await expect(option, 'Answer text is not correct.').to_contain_text(question_data[question_id]['answear'][j])

        # Validate models displayed correctly
        print('models_name_expected: ' + str(models_name_expected))
        print('models_name_displayed: ' + str(models_name_displayed))
        assert len(set(models_name_expected).intersection(set(models_name_displayed))) == len(models_name_expected), "Models displayed arn't correct."

        # Click to next question
        await options.nth(answer_id).click()
        if (question_id, answer_id) == workflow['workflow'][-1]: # last question
            nxt_questionnair = page.locator('.hmc-questionnaire') 
            # when click in last option, the question text must stay the same
            await expect(nxt_questionnair, 'This is not last question.').to_contain_text(question_data[question_id]['question'])
        
    test_result[workflow['id']]['status'] = 'passed'
    with open(f'json/test_result_workflow_{workflow["id"]}.json', 'w') as f:
        json.dump(test_result, f, indent=2)


workflow_to_test = {}
for workflow in workflow_data:
    workflow_tuples = eval(workflow['workflow'])
    models = {}
    for key, value in model_data.items():
        filters = eval(value['filters'])   
        if len(set(workflow_tuples).intersection(set(filters))) == len(set(workflow_tuples)):
            models[key] = value
    
    if len(models) > 0:
        id = workflow['id']
        workflow_to_test[id] = {
            'id': id,
            'workflow': workflow_tuples,
            'models': models
        }

@pytest.mark.asyncio
@pytest.mark.parametrize("idx", list(workflow_to_test.keys()))
async def test_workflow(page: Page, idx):
    global workflow_to_test
    await process_workflow(page, workflow_to_test[idx])