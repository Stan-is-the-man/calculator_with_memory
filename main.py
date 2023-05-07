import time
import psycopg2

connection = psycopg2.connect(
    host='localhost',
    database='calculator_with_memory',
    user='postgres',
    password='1123QwER'
)

cursor_object = connection.cursor()

cursor_object.execute(
    """CREATE TABLE IF NOT EXISTS calculator_statistics (    
    action_type VARCHAR(10),
    results FLOAT,   
    execution_time FLOAT
)"""
)

connection.commit()


def basic_operators(first_number, second_number, action):
    result = 0
    if action == "*":
        result = first_number * second_number
    elif action == "+":
        result = first_number + second_number
    elif action == "-":
        result = first_number - second_number
    elif action == "%":
        result = first_number % second_number

    elif action == '^':
        result = first_number ** second_number
    elif action == '/':
        result = first_number / second_number
    return result


def factorial(any_integer):
    the_result = 1
    for num in range(1, any_integer + 1):
        the_result *= num
    return the_result


def calculate_execution_time(func, *args):
    start_time = time.time()
    func(*args)
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time


def data_to_db(the_action, the_result, the_total_time):
    cursor_object.execute("""
    INSERT INTO calculator_statistics(
    action_type,
    results,
    execution_time
    )
    VALUES(%s, %s, %s)
    """, (the_action, the_result, the_total_time))

    connection.commit()


while True:
    operator = input("\nPlease enter one of the following actions to perform:\n"
                     "( +, -, *, /, ^, %, ! ) or type 'exit' to quit. \n")
    if operator == 'exit':
        break
    elif operator in ['+', '-', '*', '%']:
        number_1 = float(input("Please enter the first number:\n"))
        number_2 = float(input("Please enter the second number:\n"))
        res = basic_operators(number_1, number_2, operator)
        exec_time = calculate_execution_time(basic_operators, number_1, number_2, operator)
        data_to_db(operator, res, exec_time)
        print(res)

    elif operator == '/':
        number_1 = float(input("Please enter the first number:\n"))
        number_2 = float(input("Please enter the second number, other than ZERO:\n"))
        try:
            if number_1 != 0 and number_2 != 0:
                res = basic_operators(number_1, number_2, operator)
                exec_time = calculate_execution_time(basic_operators, number_1, number_2, operator)
                data_to_db(operator, res, exec_time)
                print(res)
        except ZeroDivisionError:
            print('Zero division not possible')

    elif operator == "^":
        try:
            number = int(input("Please enter an integer number:\n"))
            power = int(input("Please enter the power - integer number:\n"))
            if isinstance(number, int) and isinstance(power, int):
                res = basic_operators(number, power, operator)
                exec_time = calculate_execution_time(basic_operators, number, power, operator)
                data_to_db(operator, res, exec_time)
                print(res)

        except ValueError:
            print("Please enter only integers numbers for the power !!!\n")

    elif operator == "!":
        try:
            the_number = int(input("Please enter just ONE INTEGER number:\n"))
            if isinstance(the_number, int):
                res = factorial(the_number)
                exec_time = calculate_execution_time(factorial, the_number)
                data_to_db(operator, res, exec_time)
                print(res)
        except ValueError:
            print("The entered number should be an integer !!!\n")
    else:
        print('Operation not allowed !!!\n')
