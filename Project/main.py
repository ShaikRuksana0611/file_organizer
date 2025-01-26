import os
from file_organizer import organize_files
from calculator_gui import CalculatorApp
from console_calculator import perform_calculation
import tkinter as tk


def main():
    while True:  # This creates a loop, so the program will run until the user chooses to exit
        print("Welcome to the Project!")
        print("1. File Organizer")
        print("2. Calculator (GUI)")
        print("3. Calculator (Console)")
        print("4. Exit")  # Added the Exit option
        choice = input("Enter your choice (1/2/3/4): ").strip()

        if choice == "1":
            directory = input("Enter the directory to organize: ").strip()
            if os.path.isdir(directory):
                organize_files(directory)
            else:
                print("Invalid directory. Please try again.")
        elif choice == "2":
            root = tk.Tk()
            app = CalculatorApp(root)
            root.mainloop()
        elif choice == "3":
            perform_calculation()
        elif choice == "4":
            print("Exiting the program. Goodbye!")
            break  # Exit the loop and stop the program
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
    