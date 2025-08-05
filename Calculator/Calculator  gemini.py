import math

# --- Helper Functions for Robust Input ---

def get_float_input(prompt: str) -> float:
    """Gets a floating-point number from the user, handling invalid input."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_menu_choice(menu: str, valid_choices: list[int]) -> int:
    """Displays a menu and gets a valid integer choice from the user."""
    print(menu)
    while True:
        try:
            choice = int(input("Your choice: "))
            if choice in valid_choices:
                return choice
            else:
                print(f"Invalid choice. Please select one of {valid_choices}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# --- Calculation Functions for y = ax + b ---

def calc_a_b_from_points():
    """Calculates 'a' and 'b' for y = ax + b from two points."""
    print("\n--- Calculate a, b from P1(x1, y1) and P2(x2, y2) ---")
    x1 = get_float_input("Enter x1: ")
    y1 = get_float_input("Enter y1: ")
    x2 = get_float_input("Enter x2: ")
    y2 = get_float_input("Enter y2: ")

    if x1 == x2:
        print("\nError: Cannot calculate slope 'a' because x1 and x2 are the same (vertical line).")
        return

    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1
    print(f"\nResults:\n  a = {a}\n  b = {b}")
    print(f"The function is: y = {a}x + {b}")

def calc_y_from_x_ax_b():
    """Calculates y given a, x, and b."""
    print("\n--- Calculate y = ax + b ---")
    a = get_float_input("Enter a: ")
    x = get_float_input("Enter x: ")
    b = get_float_input("Enter b: ")
    y = a * x + b
    print(f"\nResult: y = {y}")

def calc_x_from_y_ax_b():
    """Calculates x given a, y, and b."""
    print("\n--- Calculate x from y = ax + b ---")
    a = get_float_input("Enter a: ")
    y = get_float_input("Enter y: ")
    b = get_float_input("Enter b: ")
    
    if a == 0:
        print(f"\nError: Cannot solve for x when a is 0. (y would always be {b})")
        return
        
    x = (y - b) / a
    print(f"\nResult: x = {x}")
    
# --- Calculation Functions for other modules (add as needed) ---

def calc_y_from_x_abs_ax_plus_b():
    """Calculates y for y = |ax| + b"""
    print("\n--- Calculate y = |ax| + b ---")
    a = get_float_input("Enter a: ")
    x = get_float_input("Enter x: ")
    b = get_float_input("Enter b: ")
    y = abs(a * x) + b
    print(f"\nResult: y = {y}")

def calc_x_from_y_abs_ax_plus_b():
    """Calculates x for y = |ax| + b"""
    print("\n--- Calculate x from y = |ax| + b ---")
    a = get_float_input("Enter a: ")
    y = get_float_input("Enter y: ")
    b = get_float_input("Enter b: ")
    
    if a == 0:
        print("\nError: Cannot solve for x when a is 0.")
        return

    # We need to solve |ax| = y - b
    val = y - b
    if val < 0:
        print(f"\nResult: No real solution for x because |ax| cannot be negative ({val}).")
        return

    x1 = val / a
    x2 = -val / a
    
    if x1 == x2:
        print(f"\nResult: There is one solution: x = {x1}")
    else:
        print(f"\nResult: There are two solutions: x = {x1} and x = {x2}")

def calc_y_from_x_abs_ax_plus_b_v2():
    """Calculates y for y = |ax + b|"""
    print("\n--- Calculate y = |ax + b| ---")
    a = get_float_input("Enter a: ")
    x = get_float_input("Enter x: ")
    b = get_float_input("Enter b: ")
    y = abs(a * x + b)
    print(f"\nResult: y = {y}")

def calc_x_from_y_abs_ax_plus_b_v2():
    """Calculates x for y = |ax + b|"""
    print("\n--- Calculate x from y = |ax + b| ---")
    a = get_float_input("Enter a: ")
    y = get_float_input("Enter y: ")
    b = get_float_input("Enter b: ")

    if a == 0:
        print("\nError: Cannot solve for x when a is 0.")
        return
    
    # We need to solve ax + b = y  OR  ax + b = -y
    if y < 0:
        print(f"\nResult: No real solution for x because |ax+b| cannot be negative.")
        return
        
    # First solution: ax = y - b
    x1 = (y - b) / a
    # Second solution: ax = -y - b
    x2 = (-y - b) / a
    
    if x1 == x2:
        print(f"\nResult: There is one solution: x = {x1}")
    else:
        print(f"\nResult: There are two solutions: x = {x1} and x = {x2}")

# --- Menu Handlers ---

def handle_linear_functions():
    """Handles the y = ax + b module."""
    menu = """
--- Module: y = ax + b ---
Please select an action:
1 -> Calculate a, b from 2 points
2 -> Calculate y from x
3 -> Calculate x from y
4 -> Back to main menu
"""
    # Dictionary mapping choice to function
    actions = {
        1: calc_a_b_from_points,
        2: calc_y_from_x_ax_b,
        3: calc_x_from_y_ax_b,
    }
    
    while True:
        choice = get_menu_choice(menu, [1, 2, 3, 4])
        if choice == 4:
            break
        
        action_func = actions.get(choice)
        if action_func:
            action_func()
        print("-" * 20) # Separator for next action

def handle_abs_ax_plus_b():
    """Handles the y = |ax| + b module."""
    menu = """
--- Module: y = |ax| + b ---
Please select an action:
1 -> Calculate y from x
2 -> Calculate x from y
3 -> Back to main menu
"""
    actions = {
        1: calc_y_from_x_abs_ax_plus_b,
        2: calc_x_from_y_abs_ax_plus_b,
    }

    while True:
        choice = get_menu_choice(menu, [1, 2, 3])
        if choice == 3:
            break
        
        action_func = actions.get(choice)
        if action_func:
            action_func()
        print("-" * 20)

def handle_abs_ax_plus_b_v2():
    """Handles the y = |ax + b| module."""
    menu = """
--- Module: y = |ax + b| ---
Please select an action:
1 -> Calculate y from x
2 -> Calculate x from y
3 -> Back to main menu
"""
    actions = {
        1: calc_y_from_x_abs_ax_plus_b_v2,
        2: calc_x_from_y_abs_ax_plus_b_v2,
    }

    while True:
        choice = get_menu_choice(menu, [1, 2, 3])
        if choice == 3:
            break
        
        action_func = actions.get(choice)
        if action_func:
            action_func()
        print("-" * 20)

# --- Main Program ---
def main():
    """Main function to run the program."""
    main_menu = """
=== Function Calculator ===
Select a program:
1 -> Linear functions (y = ax + b)
2 -> Absolute value (y = |ax| + b)
3 -> Absolute value (y = |ax + b|)
4 -> Exit
"""
    # Note: I've omitted the y=ax module as it's a subset of y=ax+b where b=0.
    # It could be added back easily by creating a new handler function.
    
    programs = {
        1: handle_linear_functions,
        2: handle_abs_ax_plus_b,
        3: handle_abs_ax_plus_b_v2
    }

    while True:
        choice = get_menu_choice(main_menu, [1, 2, 3, 4])
        if choice == 4:
            print("Exiting program. Goodbye!")
            break
        
        program_func = programs.get(choice)
        if program_func:
            program_func()

if __name__ == "__main__":
    main()