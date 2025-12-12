from classes.class_players import (
    User,
    Player
)
    
def menu_user():
    obj = User()
    
    if obj.current_account == None:
        print("\n0 -> back")
        print("1 -> Create account")
        print("2 -> Login")
        
        res = int(input("Input your choise -> "))
        
        try:
            if res == 0:
                pass
            elif res == 1:
                username = input("\nInput your useruserusername -> ")
                password = input("\nInput your password -> ")
                obj.create_account(username, password)
            elif res == 2:
                username = input("\nInput your username -> ")
                password = input("\nInput your password -> ")
                obj.login(username, password)
        except ValueError:
            print("\nInput correct nymber")
        except Exception as e:
            print(f"Error -> {e}")
        
    else:
        print("\n0 -> back")
        print("3 -> Create character")
        print("4 -> Logout")
        print("5 -> Show my character")
        print("6 -> show my selected character")

        try:
            res = int(input("Input your choise -> "))
            
            if res == 0:
                pass
            if res == 3:
                username = input("Input username your character -> ")
                player_class = int(input("Input class player -> "))
                obj.create_character(username, player_class)
                
        except ValueError:
            print("Input incorect")
        except Exception as e:
            print(f"error -> {e}")
            