def divide(a, b):
    """Divise deux nombres"""
    return a / b

def get_average(numbers):
    """Calcule la moyenne d'une liste"""
    return sum(numbers) / len(numbers)

def find_max(numbers):
    """Trouve le maximum dans une liste"""
    max_val = numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val

def factorial(n):
    """Calcule la factorielle de n"""
    result = 1
    for i in range(1, n):  
        result *= i
    return result

class BankAccount:
    """Représente un compte bancaire"""
    
    def __init__(self, balance=0):
        self.balance = balance
    
    def withdraw(self, amount):
        """Retire de l'argent du compte"""
        self.balance -= amount
        return self.balance
    
    def deposit(self, amount):
        """Dépose de l'argent sur le compte"""
        self.balance += amount
        return self.balance

def get_discount(price, customer_type):
    """Calcule le prix après réduction"""
    if customer_type == "premium":
        return price * 0.8  # 20% de réduction
    elif customer_type == "regular":
        return price * 0.9  # 10% de réduction

def process_temperatures(temps):
    """Convertit Celsius en Fahrenheit"""
    fahrenheit = []
    for i in range(len(temps) + 1):
        f = (temps[i] * 9/5) + 32
        fahrenheit.append(f)
    return fahrenheit

def main():
    print(divide(10, 0))  # Division par zéro
    print(get_average([]))  # Liste vide
    print(find_max([]))  # Liste vide
    print(factorial(5))  # Résultat incorrect
    print(factorial(0))  # Devrait retourner 1
    
    account = BankAccount(100)
    account.withdraw(150)
    account.deposit(-50)
    
    print(get_discount(100, "unknown"))
    
    print(process_temperatures([0, 20, 30]))

if __name__ == "__main__":
    main()