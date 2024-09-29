from flask import Flask, request, jsonify

app = Flask(__name__)

def create_budget(yearly_salary):
    # Define monthly budget percentages based on yearly salary
    monthly_salary = yearly_salary / 12
    savings_percentage = 0 if yearly_salary < 30000 else 0.10  # 10% savings if salary is $30k or more

    # Calculate monthly budget amounts
    budget = {
        "Housing": monthly_salary * 0.30,
        "Food": monthly_salary * 0.15,
        "Health": monthly_salary * 0.10,
        "Transportation": monthly_salary * 0.10,
        "Entertainment": monthly_salary * 0.05,
        "Miscellaneous": monthly_salary * 0.05,
        "Savings": monthly_salary * savings_percentage
    }

    return budget

@app.route('/calculate_budget', methods=['POST'])
def calculate_budget():
    data = request.get_json()
    yearly_salary = data.get('yearly_salary')
    budget = create_budget(yearly_salary)
    return jsonify(budget)

if __name__ == "__main__":
    app.run(debug=True)
