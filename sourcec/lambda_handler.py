import json
from task1_dictionary import Dictionary
from task2_spending import get_total
from task3_nth_letter import nth_char
 
 
def handler(event, context):
 
    # Task 1: Dictionary 
    d = Dictionary()
    d.newentry('Apple', 'A fruit that grows on trees')
    d.newentry('Car', 'A vehicle with four wheels')
    task1_results = {
        "entries": {
            "Apple": d.look('Apple'),
            "Car": d.look('Car'),
            "Banana": d.look('Banana'),
        }
    }
 
    # Task 2: How much will you spend? 
    costs = {'socks': 5, 'shoes': 60, 'sweater': 30}
    subtotal1 = costs['socks'] + costs['shoes']
    subtotal2 = costs['sweater']
    tax1, tax2 = 0.09, 0.10
 
    task2_results = {
        "prices": costs,
        "calculations": [
            {
                "label": "Socks + Shoes (9% tax)",
                "items": ["socks", "shoes"],
                "subtotal": subtotal1,
                "tax_pct": "9%",
                "tax_amount": round(subtotal1 * tax1, 2),
                "total": get_total(costs, ['socks', 'shoes'], tax1)
            },
            {
                "label": "Sweater (10% tax)",
                "items": ["sweater"],
                "subtotal": subtotal2,
                "tax_pct": "10%",
                "tax_amount": round(subtotal2 * tax2, 2),
                "total": get_total(costs, ['sweater'], tax2)
            }
        ]
    }
 
    # Task 3: Nth letter
    examples = [
        ["yoda", "best", "has"],
        ["hello", "world", "python"],
        []
    ]
    task3_results = []
    for words in examples:
        breakdown = [
            {"word": w, "index": i, "letter": w[i]}
            for i, w in enumerate(words)
        ]
        task3_results.append({
            "input": words,
            "breakdown": breakdown,
            "result": nth_char(words) or "(empty)"
        })
 
    response_body = {
        "task1_dictionary": task1_results,
        "task2_spending": task2_results,
        "task3_nth_letter": task3_results,
    }
 
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(response_body)
    }
 
 
if __name__ == "__main__":
    result = handler({}, {})
    print(json.dumps(json.loads(result["body"]), indent=2))