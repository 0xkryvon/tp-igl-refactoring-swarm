# Case 3: Code avec bugs logiques
# Ce fichier s'exécute mais produit des résultats incorrects

def divide(a, b):
    """Divise deux nombres"""
    # Bug: pas de vérification si b == 0
    return a / b

def get_average(numbers):
    """Calcule la moyenne d'une liste"""
    # Bug: division par zéro si liste vide
    return sum(numbers) / len(numbers)

def find_max(numbers):
    """Trouve le maximum dans une liste"""
    # Bug: ne gère pas les listes vides
    max_val = numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val

def factorial(n):
    """Calcule la factorielle de n"""
    # Bug: ne gère pas n = 0 (devrait retourner 1)
    # Bug: ne gère pas les nombres négatifs
    result = 1
    for i in range(1, n):  # Bug: devrait être range(1, n+1)
        result *= i
    return result

class BankAccount:
    """Représente un compte bancaire"""
    
    def __init__(self, balance=0):
        self.balance = balance
    
    def withdraw(self, amount):
        """Retire de l'argent du compte"""
        # Bug: permet de retirer plus que le solde
        self.balance -= amount
        return self.balance
    
    def deposit(self, amount):
        """Dépose de l'argent sur le compte"""
        # Bug: ne vérifie pas si amount est positif
        self.balance += amount
        return self.balance

def get_discount(price, customer_type):
    """Calcule le prix après réduction"""
    # Bug: pas de gestion du cas par défaut
    if customer_type == "premium":
        return price * 0.8  # 20% de réduction
    elif customer_type == "regular":
        return price * 0.9  # 10% de réduction
    # Bug: retourne None si customer_type n'est pas reconnu

def process_temperatures(temps):
    """Convertit Celsius en Fahrenheit"""
    fahrenheit = []
    # Bug: index hors limites
    for i in range(len(temps) + 1):  # Bug: devrait être len(temps)
        f = (temps[i] * 9/5) + 32
        fahrenheit.append(f)
    return fahrenheit

def main():
    # Ces appels vont causer des erreurs
    print(divide(10, 0))  # Division par zéro
    print(get_average([]))  # Liste vide
    print(find_max([]))  # Liste vide
    print(factorial(5))  # Résultat incorrect
    print(factorial(0))  # Devrait retourner 1
    
    account = BankAccount(100)
    account.withdraw(150)  # Solde négatif autorisé (bug)
    account.deposit(-50)  # Montant négatif autorisé (bug)
    
    print(get_discount(100, "unknown"))  # Retourne None
    
    print(process_temperatures([0, 20, 30]))  # Index hors limites

if __name__ == "__main__":
    main()