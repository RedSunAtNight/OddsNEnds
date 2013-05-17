/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package redsunatnight.oddsnends.romanarabic;

/**
 * Numeral class
 * @author RedSunAtNight
 * 
 * @param: String romanIn [optional]
 *      Roman numeral, in all caps
 * @param: int arabicIn [optonal]
 *      Positive integer
 * 
 * Public methods:
 *      setValue
 *          @param: either String romanIn or int arabicIn
 *          sets the value of the numeral. Performs validation and conversion.
 *      roman
 *          returns the Roman numeral representation of the number
 *      arabic
 *          returns the Arabic representation of the number
 * Static public methods
 *      add
 *          @param: two Numeral objects
 *          @returns: a Numeral object, whose value is the sum of the two parameters
 *      subtract
 *          @param: two Numeral objects
 *          @returns: a Numeral object, whose value is the difference between the two parameters
 *              Always positive.
 *      multiply
 *          @param: two Numeral objects
 *          @returns: a Numeral object, whose value is the product of the two parameters
 *      divide
 *          @param: two Numeral objects
 *          @returns: a Numeral object, whose value is the first param divided by the second
 *          Works via integer division, and any remainder is lost. 
 * Private methods
 *      arabicToRoman
 *          @param: a non-negative integer
 *          @returns: a String, containing a Roman numeral version of the input integer
 *      romanToarabic
 *          @param: a String, containing a Roman numeral
 *          @returns: a non-negative integer form of the Roman numeral
 *      validateArabic
 *          @param: int
 *          @returns: boolean, true if the int is not negative
 *          @throws: BadNumeralException
 *          If the int is not negative, returns  true, indicating that the int
 *          can be converted to a Roman numeral. Throws BadNumeralException otherwise.
 *      validateRoman
 *          @param: String, representing a Roman numeral in all caps
 *          @returns: boolean, true if the input string is a valid Roman numeral
 *          @throws: BadNumeralException
 *          If the String is a valid Roman numeral, returns true, indicating that
 *          the Roman numeral can be converted to an Arabic numeral. Throws
 *          BadNumeralException otherwise.
 * 
 * Allows conversion between Arabic and Roman numerals.
 * For the sake of practice, uses public, private, and final methods.
 *      Uses multiple constructors, including a default constructor.
 *      Uses regular expressions, two different ways.
 *      If/else and switch/case.
 *      For loops.
 *      Exceptions.
 * 
 * Java does not have operator overloading.
 * Random thought: enums are useful when you want a type that can only vary 
 * among certain values: planets in the solar system, or days of the week, etc.
 * 
 * TODO: deal with the fact that the constructor can throw an exception.
 *      This can result in a partially initialized object.
 *      This is not really a security problem for this class, but it could be
 *      for other classes. So, for good practice, deal with it here.
 */
import java.util.regex.*;
import java.io.Serializable;
public class Numeral implements Serializable {
    private int arabicForm;
    private String romanForm;
    public Numeral(String romanIn) throws BadNumeralException {
        // constructor for starting with a Roman numeral
        // The work is all done in setValue() and romanToArabic()
        setValue(romanIn); // setValue is final
    }
    
    public Numeral(int arabicIn) throws BadNumeralException {
        // constructor for starting with an Arabic numeral
        // The work is all done in setValue() and romanToArabic()
        setValue(arabicIn);
    }
    
    public Numeral() {
        // default constructor, sets data members to default values
        arabicForm = 0;
        romanForm = "";
    }
    // done with all constructors
    
    public final void setValue(String romanIn) throws BadNumeralException {
        // set the value of this numeral, based on a Roman numeral
        // validate Roman numeral, set values of data members
        boolean allowedRoman;
        try {
            allowedRoman = validateRoman(romanIn); // validateRoman() always returns true, unless it throws an exception
            romanForm = romanIn;
            arabicForm = romanToArabic(romanIn);
        } catch (BadNumeralException ne) {
            allowedRoman = false;
            romanForm = "#INVALID";
            arabicForm = -9999;
            throw ne; // re-throw the exception, to make sure it gets noticed by whoever called setValue
        }
    }
    
    public final void setValue(int arabicIn) throws BadNumeralException {
        // the Romans did not use zero or negative numbers
        boolean allowedArabic;
        try {
            allowedArabic = validateArabic(arabicIn);
            arabicForm = arabicIn;
            romanForm = arabicToRoman(arabicIn);
        } catch (BadNumeralException ne) {
            allowedArabic = false;
            romanForm = "#INVALID";
            arabicForm = -9999;
            throw ne;
        }
    }
    
    public String roman() {
        return romanForm;
    }
    
    public int arabic() {
        return arabicForm;
    }
    
    // Here are some static math methods:
    
    public static Numeral add(Numeral inOne, Numeral inTwo) throws BadNumeralException {
        // the throws statement is there for safety; this thing really shouldn't throw
        // NumeralException, because anything you put in has already been validated.
        int arabOne = inOne.arabic();
        int arabTwo = inTwo.arabic();
        int sum = arabOne + arabTwo;
        
        return (new Numeral(sum));
    }
    
    public static Numeral subtract(Numeral inOne, Numeral inTwo) throws BadNumeralException {
        // the throws statement is there for safety; this thing really shouldn't throw
        // BadNumeralException, because anything you put in has already been validated.
        int arabOne = inOne.arabic();
        int arabTwo = inTwo.arabic();
        int diff = arabOne - arabTwo;
        
        if (diff > 0) {
            return (new Numeral(diff));
        } else if (diff < 0) {
            return (new Numeral(-1*diff));
        } else {
            return (new Numeral());
        }
        
    }
    
    public static Numeral multiply(Numeral inOne, Numeral inTwo) throws BadNumeralException {
        int arabOne = inOne.arabic();
        int arabTwo = inTwo.arabic();
        int product = arabOne * arabTwo;
        
        return new Numeral(product);
    }
    
    public static Numeral divide(Numeral inNum, Numeral inDenom) throws BadNumeralException {
        int arabNum = inNum.arabic();
        int arabDenom = inDenom.arabic();
        int quotient = arabNum / arabDenom; // both are integers, so this will be integer division
        
        return new Numeral(quotient);
    }
    
    // begin private methods
    
    private boolean validateRoman(String romanIn) throws BadNumeralException {
        boolean hasForbidden = Pattern.matches("[IVXLCDM]*[^IVXLCDM]+[IVXLCDM]*", romanIn);
        if (hasForbidden) {
            throw new BadNumeralException("Input Roman numeral contains forbidden characters and is invalid", romanIn);
        }
        Pattern patOrder = Pattern.compile("CCM|DM|LM|XM|VM|IM|CCD|LD|XD|VD|ID|XXC|LC|VC|IC|XXL|VL|IL|VX|IIX|IIV");
        Matcher mOrder = patOrder.matcher(romanIn);
        boolean wrongOrder = mOrder.find(); // tries to find a matching substring, rather than matching the whole string
        if (wrongOrder) {
            throw new BadNumeralException("Input Roman numeral contains characters in the wrong order and is invalid", romanIn);
        }
        Pattern patOrder2 = Pattern.compile("([IV].*[CLDM])|([XL].*[DM])");
        Matcher mOrder2 = patOrder2.matcher(romanIn);
        boolean wrongOrder2 = mOrder2.find();
        if (wrongOrder2) {
            throw new BadNumeralException("Input Roman numeral contains characters in the wrong order and is invalid", romanIn);
        }
        Pattern patTooMany = Pattern.compile("I{4,}|V{2,}|X{4,}|L{2,}|C{4,}|D{2,}");
        Matcher mMany = patTooMany.matcher(romanIn);
        boolean tooMany = mMany.find();
        if (tooMany) {
            throw new BadNumeralException("Input Roman numeral contains too many of a certain character in a row and is invalid", romanIn);
        }
        // either throws or returns true
        return true;
    }
    
    private boolean validateArabic(int arabicIn) throws BadNumeralException {
        // the Romans did not use negative numbers
        if (arabicIn < 0) {
            throw new BadNumeralException("Input Arabic numeral is negative. This cannot be converted to Roman numerals", arabicIn);
        }
        // either throws or returns true
        return true;
    }
    
    private int romanToArabic(String romanIn) {
        int arabicOut = 0;
        
        // starting at the beginning, look at each character in the string
        // and decide what it means
        for (int i = 0; i < romanIn.length(); i++) {
            char theLetter = romanIn.charAt(i);
            switch (theLetter) {
                case 'M':
                    arabicOut += 1000;
                    break;
                case 'D':
                    arabicOut += 500;
                    break;
                case 'C':
                    // if the next character is an M, CM is 900, not 1100.
                    if (i < romanIn.length() - 1 && (romanIn.charAt(i+1) == 'D' || romanIn.charAt(i+1) == 'M')) {
                        arabicOut -= 100;
                    }
                    else {
                        arabicOut += 100;
                    }
                    break;
                case 'L':
                    arabicOut += 50;
                    break;
                case 'X':
                    // XL is 40, not 60
                    if (i < romanIn.length() - 1 && (romanIn.charAt(i+1) == 'L' || romanIn.charAt(i+1) == 'C')) {
                        arabicOut -= 10;
                    }
                    else {
                        arabicOut += 10;
                    }
                    break;
                case 'V':
                    arabicOut += 5;
                    break;
                case 'I':
                    // IX is 9, not 11.
                    if (i < romanIn.length() - 1 && (romanIn.charAt(i+1) == 'V' || romanIn.charAt(i+1) == 'X')) {
                        arabicOut -= 1;
                    }
                    else {
                        arabicOut += 1;
                    }
                    break;
            }
        }
        
        return arabicOut;
    }
    
    private String arabicToRoman(int arabicIn) {
        // This works because method arguments are passed by value
        String romanOut = "";
        // thousands
        int thousands = arabicIn / 1000; // integer division
        for (int i = 0; i < thousands; i++) {
            romanOut += "M";
        }
        arabicIn = arabicIn - (1000*thousands); // remove the thousands part
        // hundreds
        int hundreds = arabicIn / 100;
        if (hundreds < 4) {
            for (int i = 0; i < hundreds; i++) {
                romanOut += "C";
            }
        } else if (hundreds == 4) {
            romanOut += "CD";
        }
        else if (hundreds == 9) {
            romanOut += "CM";
        }
        else {
            romanOut += "D";
            for (int i = 0; i < hundreds - 5; i++) {
                romanOut += "C";
            }
        }
        arabicIn = arabicIn - (100 * hundreds);
        // tens
        int tens = arabicIn / 10;
        if (tens < 4) {
            for (int i = 0; i < tens; i++) {
                romanOut += "X";
            }
        } else if (tens == 4) {
            romanOut += "XL";
        }
        else if (tens == 9) {
            romanOut += "XC";
        }
        else {
            romanOut += "L";
            for (int i = 0; i < tens - 5; i++) {
                romanOut += "X";
            }
        }
        arabicIn = arabicIn - (10 * tens);
        // all that's left is ones
        if (arabicIn < 4) {
            for (int i = 0; i < arabicIn; i++) {
                romanOut += "I";
            }
        } else if (arabicIn == 4) {
            romanOut += "IV";
        }
        else if (arabicIn == 9) {
            romanOut += "IX";
        }
        else {
            romanOut += "V";
            for (int i = 0; i < arabicIn - 5; i++) {
                romanOut += "I";
            }
        }
        return romanOut;
    }
}
