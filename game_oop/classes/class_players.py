class Player:
    
    def __init__(self, name: str, player_class: str):
        self.user_name = name
        self.player_class = player_class
        self.HP = 0
        self.damage = 0
        self.magic_damage = 0
        self.armor = 0
        self.weapon = []
        self.backpack = []
        
    def get_stats(self):
        print(f"Name: {self.user_name}")
        print(f"Class: {self.player_class}")
        print(f"HP: {self.HP}")
        print(f"Damage: {self.damage}")
        print(f"magic_damage: {self.magic_damage}")
        print(f"armor: {self.armor}")

class User:
    
    def __init__(self):
        self.account = {} # имя_аккаунта -> {'password': пароль, 'player': персонаж}
        
        self.current_account = None
        self.current_player = None
        
    def create_account(self, username: str, password: str):
        if username in self.account:
            print("It's username already used")
            return False
        
        self.account[username] = {
            "password": password,
            "player": None
        }
        
        print("The account was created successfully!")
        print("-------------------------------------")
        return True
    
    def login(self, username: str, password: str):
        if username not in self.account:
            print("Not found this user")
            return False
        
        if self.account[username]["password"] != password:
            print("Incorect password")
            return False
        
        self.current_account = username
        self.current_player = None
        print(f"The entrance is completed. Welcome {username}")
        print("-----------------------------------------")
        return True
    
    def logout(self):
        self.current_account = None
        
    def create_character(self, name: str, player_class: int):
        if self.current_account == None:
            print("Login in account")
            return False
        
        if player_class == 1:
            player = Warrior(name)
        elif player_class == 2:
            player = Mage(name)
        elif player_class == 3:
            player = Arrow(name)
        elif player_class == 4:
            player = Tank(name)
        
        
        self.account[self.current_account]["player"] = player

# Mage Class
class Mage(Player):
    def __init__(self, name: str):
        super().__init__(name, "Mage")
        
        self.user_class = "Mage"
        self.HP = 80
        self.damage = 3
        self.magic_damage = 15
        self.armor = 3
        self.weapon = ["Emerald Wand"]
        self.backpack = ["Emerald Wand","Power Potion"]
        
# Arrow Class
class Arrow(Player):
    
    def __init__(self, name: str):
        super().__init__(name, "Arrow")
        
        self.user_class = "Arrow"
        self.HP = 80
        self.damage = 10
        self.magic_damage = 10
        self.armor = 3
        self.weapon = ["Onion"]
        self.backpack = ["Onion", "Ordinary arrows","Magic Arrows"]

# Tank Class
class Tank(Player):
    def __init__(self, name: str):
        super().__init__(name, "Tank")
        
        self.user_class = "Tank"
        self.HP = 200
        self.damage = 5
        self.magic_damage = 5
        self.armor = 15
        self.weapon = ["Shield"]
        self.backpack = ["Shield","A Health Potion"] 

# Warrior Class
class Warrior(Player):
    
    def __init__(self, name: str):
        
        super().__init__(name, "Warrior")
        
        self.user_class = "Warrior"
        self.HP = 150
        self.damage = 15
        self.magic_damage = 0
        self.armor = 10
        self.weapon = ["Sword"]
        self.backpack = ["Sword", "Beer"]
        