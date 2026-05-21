import json
from task1_dictionary import Dictionary
from task2_spending import get_total
from task3_nth_letter import nth_char


def handler(event, context):
    """
    AWS Lambda entry point.
    Runs all 3 Python tasks and returns their results.
    """

    # --- Task 1: Dictionary ---
    d = Dictionary()
    d.newentry('Apple', 'A fruit that grows on trees')
    task1_results = {
        "Apple": d.look('Apple'),
        "Banana": d.look('Banana'),
    }

    # --- Task 2: How much will you spend? ---
    costs = {'socks': 5, 'shoes': 60, 'sweater': 30}
    task2_results = {
        "socks_and_shoes_9pct_tax": get_total(costs, ['socks', 'shoes'], 0.09),
        "sweater_only_10pct_tax": get_total(costs, ['sweater'], 0.10),
    }

    # --- Task 3: Nth letter ---
    task3_results = {
        "yoda_best_has": nth_char(["yoda", "best", "has"]),
        "empty_array": nth_char([]),
        "a_bo_cod": nth_char(["a", "bo", "cod"]),
    }

    response = {
        "task1_dictionary": task1_results,
        "task2_spending": task2_results,
        "task3_nth_letter": task3_results,
    }

    print(json.dumps(response, indent=2))
    return {"statusCode": 200, "body": json.dumps(response)}


if __name__ == "__main__":
    handler({}, {})
