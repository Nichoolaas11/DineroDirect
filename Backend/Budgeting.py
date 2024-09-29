def create_budget(yearly_salary):
    # Define budget percentages based on yearly salary
    if yearly_salary < 30000:
        savings_percentage = 0
    else:
        savings_percentage = 0.10  # 10% savings if salary is $30k or more

    housing_percentage = 0.30  # 30% for housing
    food_percentage = 0.15  # 15% for food
    health_percentage = 0.10  # 10% for health
    transportation_percentage = 0.10  # 10% for transportation
    entertainment_percentage = 0.05  # 5% for entertainment
    misc_percentage = 0.05  # 5% for miscellaneous

    # Calculate budget amounts
    housing = yearly_salary * housing_percentage
    food = yearly_salary * food_percentage
    health = yearly_salary * health_percentage
    transportation = yearly_salary * transportation_percentage
    entertainment = yearly_salary * entertainment_percentage
    misc = yearly_salary * misc_percentage
    savings = yearly_salary * savings_percentage

    # Create a budget dictionary
    budget = {
        "Yearly Salary": yearly_salary,
        "Housing": housing,
        "Food": food,
        "Health": health,
        "Transportation": transportation,
        "Entertainment": entertainment,
        "Miscellaneous": misc,
        "Savings": savings
    }

    return budget


# Example usage
if __name__ == "__main__":
    salary_input = float(input("Enter your yearly salary: "))
    budget = create_budget(salary_input)

    print("\nYour Expense Budget:")
    for category, amount in budget.items():
        print(f"{category}: ${amount:,.2f}")
