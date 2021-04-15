"""
    File name: binarycalculator.py
    Author: Katherine, Ashton, Tallon
    Date created: 02/26/2021
    Python version: 3.8
"""

import re


# from gpiozero import LEDBoard, LED
# from time import sleep


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
    :return: A signed binary number that represents the sum of the first binary operand and the second binary operand,
    as well as the value of the overflow flag
    """
    final_result = ''
    overflow_flag = False
    iterations = 8  # there are 8 LED lights on the breadboard to represent the output. The MSB is the sign bit

    for i in range(iterations):
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

    return final_result, overflow_flag


def multiply(binary_operand_1, binary_operand_2):
    """
    Performs multiplication of two signed binary numbers.
    :param binary_operand_1: Operand 1 in base-2 format
    :param binary_operand_2: Operand 2 in base-2 format
    :return: A signed binary number that represents the product of the first binary operand and the second binary
    operand, as well as the value of the overflow flag
    """
    total = 0
    iterations = len(bin(binary_operand_2)[2:])
    overflow_flag = False

    for i in range(iterations):
        # isolates the LSB of binary_operand_2
        lsb_binary_operand_2 = binary_operand_2 & 1
        if lsb_binary_operand_2 == 1:
            # shifts binary_operand_1 to the left 'i' bits, the equivalent of adding a 'i' zeros to the end of the
            # number
            partial_product = binary_operand_1 << i
        else:
            partial_product = 0

        # returns total as a String
        total, overflow_flag = add(partial_product, total, 0)

        # The "2" parameter in the int() function indicates that the integer is base-2
        total = int(total, 2)

        # shifts binary_operand_2 one bit to the right, thereby removing the current LSB
        binary_operand_2 = binary_operand_2 >> 1

    total = bin(total)[2:]

    total = total.rjust(8, '0')

    return total, overflow_flag


def divide(dividend, divisor):
    """
    Performs division of two signed binary numbers.
    :param dividend: The dividend (operand 1) in base-2 format
    :param divisor: The divisor (operand 2) in base-2 format
    :return: A signed binary number that represents the quotient of the first operand and the second operand, as well
    as the value of the overflow flag
    """
    quotient = ''
    dividend_negative = False
    divisor_negative = False
    overflow_flag = False
    iterations = 8

    # If dividend is negative, convert it to its positive form using 2s complement because division requires
    # checks for remainders < 0
    if dividend >> 7 == 1:
        dividend_negative = True
        dividend, overflow_flag = add(0, ~dividend, 1)
        dividend = int(dividend, 2)

    # If divisor is negative, convert it to its positive form using 2s complement because division requires checks
    # for remainders < 0
    if divisor >> 7 == 1:
        divisor_negative = True
        divisor, overflow_flag = add(0, ~divisor, 1)
        divisor = int(divisor, 2)

    # Modified/upgraded implementation in which the dividend is split in half and only the the left half is used
    # for the subtraction. In addition, only the dividend is shifted to the left one bit after each iteration.
    # The divisor is never shifted / modified.
    for i in range(iterations):
        dividend = bin(dividend)[2:]
        dividend = dividend.rjust(15, '0')
        dividend_left_half = dividend[:8]
        dividend_right_half = dividend[8:]
        dividend_left_half = int(dividend_left_half, 2)
        dividend_left_half, overflow_flag = add(dividend_left_half, ~divisor, 1)
        # if the result from the subtraction is negative
        if dividend_left_half[0] == '1':
            quotient = quotient + '0'
        # if the result from the subtraction is positive
        elif dividend_left_half[0] == '0':
            quotient = quotient + '1'
            dividend = dividend_left_half + dividend_right_half

        dividend = int(dividend, 2) << 1

    # convert result back to negative using 2s complement if the dividend or the divisor, but not both, were originally
    # negative
    if dividend_negative != divisor_negative:
        quotient = int(quotient, 2)
        quotient, overflow_flag = add(0, ~quotient, 1)

    return quotient, overflow_flag


def control_lights(final_result, overflow_flag):
    """
    This function controls the LED lights on the breadboard. There are 9 LED lights, including one to indicate overflow,
    lined up in a single row on the breadboard. Each of the other 8 lights represents a bit position in the final
    result. If the number for a bit position is 1, the corresponding LED light will illuminate. If the number for a bit
    position is 0, the corresponding LED light will remain off.
    :param final_result: The binary result from the calculation, as a String
    :param overflow_flag: A boolean value indicating whether or not the calculation generated overflow
    :return: The illumination of the correct LED lights on the breadboard to represent the final result
    """
    # leds = LEDBoard(
    #     20,  # 2^7 MSB/sign bit
    #     16,  # 2^6
    #     12,  # 2^5
    #     22,  # 2^4
    #     27,  # 2^3
    #     17,  # 2^2
    #     4,  # 2^1
    #     24  # 2^0 LSB
    # )
    #
    # overflow_led = LED(21)
    #
    # for i, l in zip(final_result, leds):
    #     if i == '1':
    #         l.on()
    #
    # if overflow_flag:
    #     overflow_led.on()
    #
    # sleep(5)


def main():
    binary_operand_1, operator, binary_operand_2 = get_input()

    final_result, overflow_flag = calculate(binary_operand_1, operator, binary_operand_2)

    print('Final result: ' + final_result)
    print('Overflow?', end=" ")

    if overflow_flag:
        print('Yes')
    else:
        print('No')

    # control_lights(final_result, overflow_flag)


if __name__ == '__main__':
    main()
