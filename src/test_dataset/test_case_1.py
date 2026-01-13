def calcul(a, b):
    return a + b

def process_data(items):
    result = []
    for item in items:
        if item > 0:
            result.append(item * 2)
    return result

class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    def filter_positive(self):
        return [x for x in self.data if x > 0]
    
    def get_sum(self):
        total = 0
        for num in self.data:
            total += num
        return total

def transform_list(input_list):
    output = []
    for i in range(len(input_list)):
        if input_list[i] % 2 == 0:
            output.append(input_list[i] * 2)
        else:
            output.append(input_list[i] + 1)
    return output

def main():
    numbers = [1, 2, 3, 4, 5]
    result = process_data(numbers)
    print(result)
    
    processor = DataProcessor([10, -5, 20, -3, 15])
    filtered = processor.filter_positive()
    print(filtered)

if __name__ == "__main__":
    main()
