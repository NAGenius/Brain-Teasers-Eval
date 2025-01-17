import json
from zhipuai import ZhipuAI
from api import Zhipu_API
import concurrent.futures

client = ZhipuAI(api_key=Zhipu_API)
model_name = "glm-4-plus"
task_name = "task2"
with open(f'../task/{task_name}.json', 'r', encoding='utf-8') as file:
    tasks = json.load(file)

results = []

def generate_response(task):
    question_id = task['question_id']
    question = task['question']
    answer = task['answer']
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "以下是脑筋急转弯测试，保证答案简洁，符合脑筋急转弯的答案"},
            {"role": "user", "content": question},
        ],
    )
    response_content = response.choices[0].message.content
    print(question_id)
    return {
        "question_id": question_id,
        "question": question,
        "answer": answer,
        "response": response_content,
        "is_correct": False
    }

with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    futures = [executor.submit(generate_response, task) for task in tasks]
    for future in concurrent.futures.as_completed(futures):
        results.append(future.result())

with open(f'{task_name}_model_output_{model_name}.json', 'w', encoding='utf-8') as file:
    sorted_results = sorted(results, key=lambda x: x['question_id'])
    json.dump(sorted_results, file, ensure_ascii=False, indent=4)
