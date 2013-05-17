/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package redsunatnight.oddsnends.romanarabic;

/**
 *
 * @author RedSunAtNight
 */
public class BadNumeralException extends Exception {

    /**
     * Creates a new instance of <code>BadNumeralException</code> without detail message.
     */
    public BadNumeralException() {
        super("An unspecified Numeral error occurred");
    }

    /**
     * Constructs an instance of <code>BadNumeralException</code> with the specified detail message.
     * @param msg the detail message.
     */
    public BadNumeralException(String msg) {
        super(msg);
    }
    
    public BadNumeralException(String msg, String badRoman) {
        super(badRoman + ": " + msg);
    }
    
    public BadNumeralException(String msg, int badArabic) {
        super(badArabic + ": " + msg);
    }
}
