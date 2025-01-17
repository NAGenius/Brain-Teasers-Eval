import json


results = []
with open('task2_model_output_glm-4-plus.json', 'r', encoding='utf-8') as file:
    results = json.load(file)

correct_count = sum(1 for result in results if result.get('is_correct') == True)
total_count = len(results)
accuracy = correct_count / total_count if total_count > 0 else 0
print(f"Number of correct responses / total count: {correct_count}/{total_count}")
print(f"Accuracy: {accuracy:.2%}")