"""
    File name: binarycalculator.py
    Author: Katherine, Ashton, Tallon
    Date created: 02/26/2021
    Python version: 3.8
"""

# input must be in the following format: NUM1*operator*NUM2= because the user will use the keypad to enter
# the input and thus there will be no spaces in the input, and the user will hit the equals sign key to indicate
# the end of the input

import re
from gpiozero import LEDBoard, LED
from time import sleep


def get_input():
    """
    Requests input from the user and parses the input String into a numerical operand one, String character, and
    numerical operand two

    :return: The integer value of operand 1 in base-2, the String operator, and the integer value of operand 2 in
    base-2
    """
    input_val = input('Please enter calculation: ')

    # get index of operator
    operator = re.search('[+\\-*/]', input_val)
    operator_start, operator_end = operator.span()

    # operand 1 is a number located between the beginning of the input string and the operator. The "2" parameter
    # in the int() function indicates that the integer is base-2
    binary_operand_1 = int(input_val[0:operator_start], 2)

    operator = input_val[operator_start:operator_end]

    # operand 2 is a number located after the operator. The "2" parameter
    # in the int() function indicates that the integer is base-2
    binary_operand_2 = int(input_val[operator_end:], 2)

    return binary_operand_1, operator, binary_operand_2


def calculate(binary_operand_1, operator, binary_operand_2):
    """
    Determines which mathematical function needs to be called based on the input provided by the user and calls this
    function

    :param binary_operand_1: Operand 1 in base-2
    :param operator: Mathematical operator
    :param binary_operand_2: Operand 2 in base-2

    :return: The final result of the calculation as a String
    """

    if operator == '+':
        return add(binary_operand_1, binary_operand_2, 0)
    elif operator == '-':
        # carry in is 1 because we have to account for the 1 that needs to be added to the one's complement
        # representation of binary_operand_2
        return add(binary_operand_1, ~binary_operand_2, 1)
    elif operator == '*':
        return multiply(binary_operand_1, binary_operand_2)
    elif operator == '/':
        return divide(binary_operand_1, binary_operand_2)
    else:
        return '0'


def add(binary_operand_1, binary_operand_2, carry_in):
    """
    Performs bitwise addition to two signed binary numbers by implementing the logic of a full adder circuit.
    :param binary_operand_1: Operand 1 in base-2 format
    :param binary_operand_2: Operand 2 in base-2 format
    :param carry_in: The initial value of the carry in input
    :return: A signed binary number that represents the sum of binary_operand_1 and binary_operand_2, as well as the
    value of the overflow_flag
    """
    final_result = ''
    overflow_flag = False
    iterations = 8  # there are 8 LED lights on the breadboard to represent the output. The MSB is the sign bit

    while iterations > 0:
        a = binary_operand_1 & 1  # isolates the LSB of binary_operand_1
        b = binary_operand_2 & 1  # isolates the LSB of binary_operand_2

        output_1 = a ^ b  # A XOR B
        sum_val = carry_in ^ output_1  # carry_in XOR output_1

        output_2 = carry_in & output_1  # carry_in AND output_1
        output_3 = a & b  # a AND b
        carry_in = output_2 | output_3  # output_2 OR output_3

        # overflow occurs when the sum on the last iteration = 11 (binary), resulting in
        # a carry_in value of 1.
        if iterations == 1 and carry_in == 1:
            overflow_flag = True

        # if final result is currently "001" and sum_val is "1" then final_result becomes "1001"
        final_result = str(sum_val) + final_result

        # modifies the value of binary_num_1 by shifting one bit to the right, thereby removing the current LSB
        binary_operand_1 = binary_operand_1 >> 1

        # modifies the value of binary_num_2 by shifting one bit to the right, thereby removing the current LSB
        binary_operand_2 = binary_operand_2 >> 1

        iterations -= 1

    return final_result, overflow_flag


def multiply(binary_operand_1, binary_operand_2):
    return binary_operand_1 * binary_operand_2


def divide(binary_operand_1, binary_operand_2):
    return binary_operand_1 / binary_operand_2


def control_lights(final_result, overflow_flag):

    leds = LEDBoard(
        4,   # 2^7 MSB/sign bit
        17,   # 2^6
        27,   # 2^5
        22,  # 2^4
        12,  # 2^3
        16,  # 2^2
        20,  # 2^1
        21   # 2^0 LSB
    )
    
    overflow_led = LED(24)
    
    for i, l in zip(final_result, leds):
        if i == '1':
            l.on()
    
    if overflow_flag:
        overflow_led.on()
    
    sleep(10)
    

def main():
    binary_operand_1, operator, binary_operand_2 = get_input()

    final_result, overflow_flag = calculate(binary_operand_1, operator, binary_operand_2)

    print('Final result: ' + final_result)
    print('Overflow?', end=" ")

    if overflow_flag:
        print('Yes')
    else:
        print('No')

    control_lights(final_result, overflow_flag)


if __name__ == '__main__':
    main()
