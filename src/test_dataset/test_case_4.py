counter = 0
data_list = []

def increment():
    global counter
    counter+=1
    return counter

def fonction(x,y,z,a,b,c,d):
    if x>0:
        if y>0:
            if z>0:
                if a>0:
                    if b>0:
                        return c+d
    return 0

def process(data):
    a=data
    b=[]
    for c in a:
        if c>10:
            d=c*2
            b.append(d)
        else:
            b.append(c)
    return b

class myclass:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def calc(self):
        return self.x+self.y

def use_global():
    return counter*2

def long_function(param1, param2, param3, param4, param5, param6, param7, param8):
    """Fonction avec trop de paramètres et trop longue"""
    result = param1 + param2
    result = result + param3
    result = result + param4
    result = result + param5
    result = result + param6
    result = result + param7
    result = result + param8
    if result > 100:
        print("Greater than 100")
    elif result > 50:
        print("Greater than 50")
    elif result > 25:
        print("Greater than 25")
    else:
        print("Less than 25")
    temp = result * 2
    temp = temp + 10
    temp = temp / 2
    return temp

def calculate_price_student(base_price):
    tax = base_price * 0.2
    discount = base_price * 0.1
    final = base_price + tax - discount
    return final

def calculate_price_teacher(base_price):
    tax = base_price * 0.2
    discount = base_price * 0.15
    final = base_price + tax - discount
    return final

def calculate_price_admin(base_price):
    tax = base_price * 0.2
    discount = base_price * 0.2
    final = base_price + tax - discount
    return final

def main():
    increment()
    fonction(1,2,3,4,5,6,7)
    process([5,10,15,20])
    obj=myclass(10,20)
    obj.calc()

if __name__=="__main__":
    main()
