import re
import pytest
from playwright.async_api import Page, expect
import json

question_data = None
model_data = None
with open('question.json', 'r') as f:
    question_data = json.load(f)

with open('model.json', 'r') as f:
    model_data = json.load(f)

async def process_workflow(page: Page, workflow: tuple):
    global question_data
    print('workflow: ' + str(workflow))
    for question_id, answer_id in workflow:
        print('question_id: ' + str(question_id) + ' answer_id: ' + str(answer_id))
        questionnair = page.locator('.hmc-questionnaire')
        await expect(questionnair, 'Question text is not correct.').to_contain_text(question_data[question_id]['question'])
        options = page.locator('.hmc-option button')
        opc = await options.count()
        for j in range(opc):
            option = options.nth(j)
            await expect(option, 'Answer text is not correct.').to_contain_text(question_data[question_id]['answear'][j])

        moto_card = page.locator('.item-price')
        moto_card_count = await moto_card.count()
        found_correct_model = False
        for k in range(moto_card_count):
            moto_card_option = moto_card.nth(k)
            model_text = await moto_card_option.text_content()
            if 'FourTrax Recon' in model_text:
                found_correct_model = True
                break
        assert found_correct_model, "Can't find FourTrax Recon in the list"
        
        await options.nth(answer_id).click(timeout=2000)
        if (question_id, answer_id) == workflow[-1]: # last question
            nxt_questionnair = page.locator('.hmc-questionnaire') 
            # when click in last option, the question text must stay the same
            await expect(nxt_questionnair, 'This is not last question.').to_contain_text(question_data[question_id]['question'])
        


@pytest.mark.asyncio
async def test_question_order(page: Page):
    global model_data
    with open('workflow.json', 'r') as f:
       workflow_json = json.load(f)
    want_to_test_list = [_ for _ in range(70, 110)]
    filters = eval(model_data['FourTrax Recon']['filters'])
    for workflow in workflow_json:
         workflow_tuples = eval(workflow['workflow'])
         if len(set(workflow_tuples).intersection(set(filters))) == len(set(workflow_tuples)):
            await page.reload()
            await page.wait_for_load_state('networkidle')
            await process_workflow(page, eval(workflow['workflow']))
            
            
        
        
    
    
        
        

    
    
