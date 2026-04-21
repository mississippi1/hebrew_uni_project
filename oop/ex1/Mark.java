/**
 * The options of roles in Tik Tak Toe
 */
public enum Mark {
    BLANK, X, O;

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

