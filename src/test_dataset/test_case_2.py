def add_numbers(x, y)  
    return x + y

def greet(name):
    """Salue une personne"""
    print(f"Hello {name}"  

def calculate_area(width, height):
    """Calcule l'aire d'un rectangle"""
    area = width * height
    return area

class Calculator
    """Calculatrice simple"""  
    
    def __init__(self):
        self.result = 0
    
    def add(self, value):
        self.result += value
        return self.result
    
    def subtract(self, value)
        """Soustrait une valeur"""  
        self.result -= value
        return self.result

def process_items(items):
    """Traite une liste d'items"""
    results = []
    for item in items:
        if item > 10:
            results.append(item * 2
        else:  
            results.append(item)
    return results

def main():
    
    sum_result = add_numbers(5, 3)
    print(f"Sum: {sum_result}")
    
    greet("Alice")
    
    calc = Calculator()
    calc.add(10)
    calc.subtract(3)
    print(f"Result: {calc.result}")

if __name__ == "__main__":
    main()
