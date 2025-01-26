import sqlite3
import math
import os

# Initialize SQLite database
def init_db():
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect("db/calculator_history.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expression TEXT,
            result TEXT
        )
        """
    )
    conn.commit()
    conn.close()


# Save calculation to the database
def save_to_db(expression, result):
    conn = sqlite3.connect("db/calculator_history.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history (expression, result) VALUES (?, ?)", (expression, result))
    conn.commit()
    conn.close()


# Fetch calculation history
def fetch_history():
    conn = sqlite3.connect("db/calculator_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT expression, result FROM history ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


# Perform calculations
def perform_calculation():
    print("\nAvailable Operations:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("5. Square Root (sqrt)")
    print("6. Exponentiation (**)")
    print("7. Logarithm (log)")
    print("8. Sine (sin)")
    print("9. Cosine (cos)")
    print("10. Tangent (tan)")
    print("11. View History")
    print("12. Exit")

    while True:
        try:
            choice = input("\nEnter the operation (1-12): ").strip()
            if choice == "12":
                print("Exiting the calculator. Goodbye!")
                break
            elif choice == "11":
                history = fetch_history()
                if not history:
                    print("No calculations in history.")
                else:
                    print("\nCalculation History:")
                    for expr, result in history:
                        print(f"{expr} = {result}")
                continue

            if choice in ["5", "7", "8", "9", "10"]:
                # Single input operations
                num = float(input("Enter the number: "))
                if choice == "5":
                    result = math.sqrt(num)
                    expr = f"sqrt({num})"
                elif choice == "7":
                    result = math.log10(num)
                    expr = f"log({num})"
                elif choice == "8":
                    result = math.sin(math.radians(num))
                    expr = f"sin({num})"
                elif choice == "9":
                    result = math.cos(math.radians(num))
                    expr = f"cos({num})"
                elif choice == "10":
                    result = math.tan(math.radians(num))
                    expr = f"tan({num})"
            else:
                # Double input operations
                num1 = float(input("Enter the first number: "))
                num2 = float(input("Enter the second number: "))
                if choice == "1":
                    result = num1 + num2
                    expr = f"{num1} + {num2}"
                elif choice == "2":
                    result = num1 - num2
                    expr = f"{num1} - {num2}"
                elif choice == "3":
                    result = num1 * num2
                    expr = f"{num1} * {num2}"
                elif choice == "4":
                    if num2 == 0:
                        print("Error: Division by zero is not allowed.")
                        continue
                    result = num1 / num2
                    expr = f"{num1} / {num2}"
                elif choice == "6":
                    result = num1 ** num2
                    expr = f"{num1} ** {num2}"
                else:
                    print("Invalid choice. Try again.")
                    continue

            # Save and display result
            save_to_db(expr, result)
            print(f"Result: {expr} = {result}")
        except ValueError:
            print("Invalid input. Please enter numeric values.")
        except Exception as e:
            print(f"Error: {e}")


# Run the console calculator
if __name__ == "__main__":
    init_db()
    print("Welcome to the Console Calculator!")
    perform_calculation()
