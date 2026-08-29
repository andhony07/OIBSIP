"""
BMI Calculator — Phase 1: Beginner Tier
OASIS Infobyte Python Internship 

A clean, beginner-level command-line BMI Calculator application in Python.
Calculates Body Mass Index (BMI) based on weight (kg) and height (m),
classifies into categories, and handles input validation cleanly.
"""


def get_positive_float(prompt: str) -> float:
    """
    Prompts the user for input until a valid positive numeric value (> 0) is entered.
    
    Args:
        prompt: The text prompt to display to the user.
        
    Returns:
        float: A positive floating-point number.
    """
    while True:
        user_input = input(prompt).strip()
        try:
            val = float(user_input)
            if val <= 0:
                print("Invalid value. Value must be greater than 0.")
                continue
            return val
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def calculate_bmi(weight: float, height: float) -> float:
    """
    Calculates Body Mass Index (BMI) using weight (kg) and height (m).
    Formula: BMI = weight / (height ** 2)
    """
    return weight / (height ** 2)


def classify_bmi(bmi: float) -> str:
    """
    Classifies the BMI value into Underweight, Normal, Overweight, or Obese categories.
    
    Boundaries:
        BMI < 18.5      -> Underweight
        18.5 - 24.9     -> Normal
        25 - 29.9       -> Overweight
        BMI >= 30       -> Obese
    """
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25.0:
        return "Normal"
    elif bmi < 30.0:
        return "Overweight"
    else:
        return "Obese"


def run_bmi_calculator() -> None:
    """Runs a single round of the BMI calculation."""
    print("\n--- BMI Calculator ---")
    weight = get_positive_float("Enter your weight in kilograms: ")
    height = get_positive_float("Enter your height in meters: ")
    
    bmi = calculate_bmi(weight, height)
    category = classify_bmi(bmi)
    
    print(f"\nBMI: {bmi:.2f}")
    print(f"Category: {category}")


def main() -> None:
    """Main application entry point with repeat calculation loop."""
    print("Welcome to the BMI Calculator!")
    
    while True:
        run_bmi_calculator()
        
        while True:
            repeat = input("\nWould you like to calculate another BMI? (y/n): ").strip().lower()
            if repeat in ["y", "yes"]:
                break
            elif repeat in ["n", "no"]:
                print("Thank you for using the BMI Calculator. Goodbye!")
                return
            else:
                print("Invalid response. Please enter 'y' for yes or 'n' for no.")


if __name__ == "__main__":
    main()
