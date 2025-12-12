from menu.menu import (
    menu_user
)

if __name__ == "__main__":
    print("Hello :D")
    
    try:
        
        print("\n     Menu")
        print("---------------")
        print("0 -> exit")
        print("1 -> Profile")
        print("---------------")
        
        choise = int(input("Input your choise -> "))
        
        if choise == 0:
            print("Completion of the program")
            pass
        
        elif choise == 1:
            menu_user()
    except ValueError:
        print("Your input incorect")
    except Exception as e:
        print(f"Error -> {e}")