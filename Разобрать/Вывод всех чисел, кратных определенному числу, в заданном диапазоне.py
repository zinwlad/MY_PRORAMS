lower = int(input("Введите нижнюю границу диапазона: "))
upper = int(input("Введите верхнюю границу диапазона: "))
n = int(input("Введите делитель: "))
for i in range(lower, upper + 1):
    if(i % n == 0):
        print(i)