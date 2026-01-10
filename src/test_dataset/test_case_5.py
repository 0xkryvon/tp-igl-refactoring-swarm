# Case 5: Combinaison de problèmes complexes
# Syntaxe + Logique + Mauvaises pratiques

import json

# Bug: Variable globale mutable
config = {"debug": True}

def load_data(filename)  # Bug: manque ":"
    # Bug: pas de gestion d'erreur
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

class DataProcessor:
    # Pas de docstring
    
    def __init__(self, data):
        self.data = data
        self.processed = []
    
    def filter_data(self, threshold):
        # Bug logique: modifie la liste pendant l'itération
        for item in self.data:
            if item['value'] < threshold:
                self.data.remove(item)  # Bug: modification pendant iteration
    
    def calculate_stats(self):
        # Bug: division par zéro possible
        total = sum([item['value'] for item in self.data])
        average = total / len(self.data)
        return average
    
    def transform(self, factor)
        # Bug: manque ":"
        results = []
        for item in self.data:
            # Bug: pas de vérification si 'value' existe
            new_val = item['value'] * factor
            results.append(new_val
        return results  # Bug: parenthèse non fermée

def process_user_input(user_data):
    # Mauvaise pratique: modification de paramètre mutable
    user_data['processed'] = True
    # Bug: pas de validation des données
    age = user_data['age']
    if age < 0:  # Bug: condition non gérée
        pass
    return user_data

def merge_lists(list1, list2):
    # Mauvaise pratique: utilisation inefficace
    result = []
    for i in range(len(list1)):  # Mauvaise pratique
        result.append(list1[i])
    for j in range(len(list2)):
        result.append(list2[j])
    return result

class UserManager
    # Bug: manque ":"
    
    def __init__(self):
        self.users = {}
    
    def add_user(self, user_id, name, email):
        # Bug: pas de validation
        self.users[user_id] = {
            'name': name,
            'email': email
        }
    
    def get_user(self, user_id):
        # Bug: KeyError si user_id n'existe pas
        return self.users[user_id]
    
    def delete_user(self, user_id):
        # Bug: pas de vérification d'existence
        del self.users[user_id]
    
    def list_users(self):
        # Mauvaise pratique: expose l'objet interne
        return self.users

def calculate_discount(price, discount_percent):
    # Bug logique: pas de validation des paramètres
    # discount_percent devrait être entre 0 et 100
    discount = price * (discount_percent / 100)
    final_price = price - discount
    # Bug: peut retourner un prix négatif
    return final_price

def fetch_api_data(url):
    # Simulation d'appel API
    # Bug: pas de gestion d'erreur réseau
    # Bug: pas de timeout
    import urllib.request
    response = urllib.request.urlopen(url)  # Bug: peut bloquer indéfiniment
    data = response.read()
    return json.loads(data)  # Bug: peut échouer si pas du JSON

def main():
    # Code qui va planter
    data = load_data("nonexistent.json")  # Fichier inexistant
    
    processor = DataProcessor([
        {'value': 10},
        {'value': 20},
        {'value': 5}
    ])
    processor.filter_data(15)  # Bug: modification pendant itération
    processor.calculate_stats()
    
    processor2 = DataProcessor([])  # Liste vide
    processor2.calculate_stats()  # Division par zéro
    
    user_data = {'name': 'John'}  # Manque 'age'
    process_user_input(user_data)  # KeyError
    
    manager = UserManager()
    manager.get_user('unknown')  # KeyError
    
    print(calculate_discount(100, 150))  # Prix négatif

if __name__ == "__main__":
    main()
