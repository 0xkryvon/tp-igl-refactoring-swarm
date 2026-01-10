# Case 4: Mauvaises pratiques de programmation

# Variables globales (mauvaise pratique)
counter = 0
data_list = []

def increment():
    global counter
    counter+=1  # Pas d'espaces
    return counter

def fonction(x,y,z,a,b,c,d):  # Trop de paramètres
    if x>0:  # Pas d'espaces
        if y>0:
            if z>0:  # Imbrication excessive
                if a>0:
                    if b>0:
                        return c+d
    return 0

def process(data):
    # Noms de variables non descriptifs
    a=data
    b=[]
    for c in a:
        if c>10:
            d=c*2
            b.append(d)
        else:
            b.append(c)
    return b

class myclass:  # Nom de classe non conforme (devrait être MyClass)
    def __init__(self,x,y):  # Pas d'espaces après les virgules
        self.x=x
        self.y=y
    
    def calc(self):
        return self.x+self.y  # Pas d'espaces autour des opérateurs

def use_global():
    return counter*2  # Utilise une variable globale

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
    # Fonction trop longue, devrait être divisée
    temp = result * 2
    temp = temp + 10
    temp = temp / 2
    return temp

# Code dupliqué
def calculate_price_student(base_price):
    tax = base_price * 0.2
    discount = base_price * 0.1
    final = base_price + tax - discount
    return final

def calculate_price_teacher(base_price):
    tax = base_price * 0.2
    discount = base_price * 0.15  # Seule différence
    final = base_price + tax - discount
    return final

def calculate_price_admin(base_price):
    tax = base_price * 0.2
    discount = base_price * 0.2  # Seule différence
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
