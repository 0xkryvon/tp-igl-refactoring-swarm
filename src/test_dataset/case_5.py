import json

config = {"debug": True}

def load_data(filename)
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

class DataProcessor:
    
    def __init__(self, data):
        self.data = data
        self.processed = []
    
    def filter_data(self, threshold):
        for item in self.data:
            if item['value'] < threshold:
                self.data.remove(item)
    
    def calculate_stats(self):
        total = sum([item['value'] for item in self.data])
        average = total / len(self.data)
        return average
    
    def transform(self, factor)
        results = []
        for item in self.data:
            new_val = item['value'] * factor
            results.append(new_val
        return results

def process_user_input(user_data):
    user_data['processed'] = True
    age = user_data['age']
    if age < 0:
        pass
    return user_data

def merge_lists(list1, list2):
    result = []
    for i in range(len(list1)):
        result.append(list1[i])
    for j in range(len(list2)):
        result.append(list2[j])
    return result

class UserManager
    
    def __init__(self):
        self.users = {}
    
    def add_user(self, user_id, name, email):
        self.users[user_id] = {
            'name': name,
            'email': email
        }
    
    def get_user(self, user_id):
        return self.users[user_id]
    
    def delete_user(self, user_id):
        del self.users[user_id]
    
    def list_users(self):
        return self.users

def calculate_discount(price, discount_percent):
    discount = price * (discount_percent / 100)
    final_price = price - discount
    return final_price

def fetch_api_data(url):
    import urllib.request
    response = urllib.request.urlopen(url)
    data = response.read()
    return json.loads(data)

def main():
    data = load_data("nonexistent.json")
    
    processor = DataProcessor([
        {'value': 10},
        {'value': 20},
        {'value': 5}
    ])
    processor.filter_data(15)
    processor.calculate_stats()
    
    processor2 = DataProcessor([])
    processor2.calculate_stats()
    
    user_data = {'name': 'John'}
    process_user_input(user_data)
    
    manager = UserManager()
    manager.get_user('unknown')
    
    print(calculate_discount(100, 150))

if __name__ == "__main__":
    main()
