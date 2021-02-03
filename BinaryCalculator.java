package com.reedk55;

public class BinaryCalculator {

    public static void main(String[] args) {

        int binaryNum1 = 0b0101;  // binary 5
        int binaryNum2 = 0b1111;  // binary 15
        char operator = '-';

        String finalResult = calculate(binaryNum1, binaryNum2, operator);

        System.out.println(finalResult);

    }

    /**
     * Perform a mathematical calculation based on the input provided by the user.
     * @param binaryNum1
     * @param binaryNum2
     * @return The final mathematical result of the operation entered into the keyboard by the user.
     */
    public static String calculate(int binaryNum1, int binaryNum2, char operator) {

        String finalResult = "";

        switch(operator) {
            case '+':
                finalResult = add(binaryNum1, binaryNum2, 0);
                break;
            case '-':
                //carry in is 1 because we have to account for the 1 that needs to be added to the one's complement
                //representation of binaryNum2
                finalResult = add(binaryNum1, ~binaryNum2, 1);
                break;
            case '*':
                finalResult = multiply(binaryNum1, binaryNum2);
                break;
            case '/':
                finalResult = divide(binaryNum1, binaryNum2);
                break;
            default:
                finalResult = "0";
        }

        return finalResult;
    }

    /**
     * Bitwise addition of two signed binary numbers by implementing a full adder circuit.
     * @param binaryNum1
     * @param binaryNum2
     * @return The sum of binaryNum1 and binaryNum2
     */
    public static String add(int binaryNum1, int binaryNum2, int cIn) {

        String finalResult = "";
        int iterations = 8;  

        //the addition calculation will be performed bit-wise, starting with the LSB and moving to the left towards
        //the MSB
        while (iterations > 0) {
            int A = binaryNum1 & 1;     // isolates the LSB of binaryNum1
            int B = binaryNum2 & 1;     // isolates the LSB of binaryNum2

            int output1 = A ^ B;        // A XOR B
            int sum = cIn ^ output1;    // cIn XOR output1

            int output2 = cIn & output1;    // cIn AND output1
            int output3 = A & B;           // A AND B
            cIn = output2 | output3;        // output2 OR output3

            finalResult = sum + finalResult;  //if finalResult is currently "001" and sum is "1" then finalResult becomes "1001"

            binaryNum1 = binaryNum1>>1;        // modifies the value of binaryNum1 by shifting one bit to the right, thereby removing the current LSB
            binaryNum2 = binaryNum2>>1;        // modifies the value of binaryNum2 by shifting one bit to the right, thereby removing the current LSB

            iterations--;
        }

        return finalResult;
    }

    /**
     * Multiply two signed binary numbers
     * @param binaryNum1
     * @param binaryNum2
     * @return The product of binaryNum1 and binaryNum2
     */
    private static String multiply(int binaryNum1, int binaryNum2) {
        return "";
    }

    /**
     * Divide two signed binary numbers
     * @param binaryNum1
     * @param binaryNum2
     * @return The quotient of binaryNum1 and binaryNum2
     */
    private static String divide(int binaryNum1, int binaryNum2) {
        return "";
    }

}
