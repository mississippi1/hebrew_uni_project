/**
 * The options of roles in Tik Tak Toe
 */
public enum Mark {
    /** Represents an empty cell */
    BLANK,
    /** Represents the X player */
    X,
    /** represents the O player mark */
    O;

	/**
	 * the string formatting of marks
	 * @return the marks as strings
	 */
    @Override
    public String toString(){
        return switch (this) {
            case BLANK -> null;
            case X -> "X";
            case O -> "O";
        };
    }
};

