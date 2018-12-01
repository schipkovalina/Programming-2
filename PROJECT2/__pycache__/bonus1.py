def numbers():
#    numbers = []
    quantity = 0
    a = input("Введите число: ")
    s = int(a)
    while a != "":
        a = input("Введите число: ") 
        if a != "":
            s = s + int(a)
            quantity += 1
#    number = sum(numbers)
    print("Среднее арифметическое: ", (s)/quantity)
    print("Минимальное число: ", min(s))
    print("Максимальное число: ", max(s))

numbers()
       
        
          
    
