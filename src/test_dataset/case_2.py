# Case 2: Code avec erreurs de syntaxe

def add_numbers(x, y)  # Erreur: manque le ":"
    return x + y

def greet(name):
    """Salue une personne"""
    print(f"Hello {name}"  # Erreur: parenthèse non fermée

def calculate_area(width, height):
    """Calcule l'aire d'un rectangle"""
    area = width * height
    return area

class Calculator
    """Calculatrice simple"""  # Erreur: manque le ":"
    
    def __init__(self):
        self.result = 0
    
    def add(self, value):
        self.result += value
        return self.result
    
    def subtract(self, value)
        """Soustrait une valeur"""  # Erreur: manque le ":"
        self.result -= value
        return self.result

def process_items(items):
    """Traite une liste d'items"""
    results = []
    for item in items:
        if item > 10:
            results.append(item * 2
        else:  # Erreur: parenthèse non fermée ci-dessus
            results.append(item)
    return results

def main():
    # Test des fonctions
    sum_result = add_numbers(5, 3)
    print(f"Sum: {sum_result}")
    
    greet("Alice")
    
    calc = Calculator()
    calc.add(10)
    calc.subtract(3)
    print(f"Result: {calc.result}")

if __name__ == "__main__":
    main()
