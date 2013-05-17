
package redsunatnight.oddsnends.romanarabic;
import java.util.Scanner;

/**
 *
 * @author RedSunAtNight
 * Demonstrates the Numeral class.
 */
public class RomanArabic {

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        int enteredInt;
        String enteredString;
        Numeral num1;
        Numeral num2;
        Numeral theSum;
        Numeral theDiff;
        Numeral theProd;
        Numeral theQuot;
        
        System.out.print("Showing an example of the Numeral class\nEnter a non-negative integer\n--> ");
        enteredInt = input.nextInt();
        
        num1 = makeNumeral(enteredInt, input);
        System.out.println("\nIn Roman numerals, you entered " + num1.roman());
        
        System.out.print("\nNext, enter a Roman numeral, in all caps\n--> ");
        enteredString = input.next();
        
        num2 = makeNumeral(enteredString, input);
        System.out.println("In Arabic numerals, you entered " + num2.arabic());
        
        System.out.println("Next, let's do some simple math.");
        
        try {
            theSum = Numeral.add(num1, num2);
            theDiff = Numeral.subtract(num1, num2);
            theProd = Numeral.multiply(num1, num2);
            theQuot = Numeral.divide(num1, num2);
        } catch (BadNumeralException bne) {
            System.out.println("Exception while doing math:\n" + bne.getMessage());
            theSum = new Numeral();
            theDiff = new Numeral();
            theProd = new Numeral();
            theQuot = new Numeral();
            System.out.println("All mathematical results have been set to zero.");
        }
        System.out.println(num1.arabic()+"+"+num2.arabic()+"="+theSum.arabic());
        System.out.println(num1.roman()+"+"+num2.roman()+"="+theSum.roman());
        System.out.println("abs("+num1.arabic()+"-"+num2.arabic()+")="+theDiff.arabic());
        System.out.println("abs("+num1.roman()+"-"+num2.roman()+")="+theDiff.roman());
        System.out.println(num1.arabic()+"*"+num2.arabic()+"="+theProd.arabic());
        System.out.println(num1.roman()+"*"+num2.roman()+"="+theProd.roman());
        System.out.println(num1.arabic()+"/"+num2.arabic()+"="+theQuot.arabic());
        System.out.println(num1.roman()+"/"+num2.roman()+"="+theQuot.roman());
    }
    
    static private Numeral makeNumeral(int inInt, Scanner inputObj) {
        int usedInt = inInt;
        boolean tryAgain = true;
        Numeral madeNum = null;
        while (tryAgain) {
            try {
                madeNum = new Numeral(usedInt);
                tryAgain = false;
            } catch (BadNumeralException bne) {
                System.out.println(bne.getMessage());
                System.out.println("\nEnter a non-negative integer\n--> ");
                usedInt = inputObj.nextInt();
                tryAgain = true;
            }
        }
        return madeNum;
    }
    
    static private Numeral makeNumeral(String inStr, Scanner inputObj) {
        String usedStr = inStr;
        boolean tryAgain = true;
        Numeral madeNum = null;
        while (tryAgain) {
            try {
                madeNum = new Numeral(usedStr);
                tryAgain = false;
            } catch (BadNumeralException bne) {
                System.out.println(bne.getMessage());
                System.out.println("\nEnter a valid Roman numeral in all caps\n--> ");
                usedStr = inputObj.next();
                tryAgain = true;
            }
        }
        return madeNum;
    }
}
