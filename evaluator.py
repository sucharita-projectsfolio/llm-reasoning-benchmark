import json

def load_dataset(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def evaluate_exact_match(ai_response, expected):
    return ai_response.strip().lower() == expected.strip().lower()

def evaluate_instruction_following(ai_response, expected):
    return (expected in ai_response) and ("#" not in ai_response) and ('"""' not in ai_response)

def run_benchmark(dataset_path, responses):
    dataset = load_dataset(dataset_path)
    passed = 0
    for item in dataset:
        resp = responses.get(item["id"], "")
        ok = evaluate_exact_match(resp, item["expected"]) if item["category"] == "logical_reasoning" else evaluate_instruction_following(resp, item["expected"])
        if ok:
            passed += 1
        print(f"[{'PASS' if ok else 'FAIL'}] {item['id']} ({item['category']})")
    print(f"Final Score: {(passed / len(dataset)) * 100:.2f}%")

if __name__ == "__main__":
    res = {"test_001": "1/8", "test_002": "def secure_hash(x):\n    return hash(x)"}
    run_benchmark("dataset.json", res)
