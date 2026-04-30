/**
 * The options of roles in Tik Tak Toe
 */
public enum Mark {
	/** Represents an empty cell. */
	BLANK,
	/** Represents the X player's mark. */
	X,
	/** Represents the O player's mark. */
	O;

	private static final String X_STRING = "X";
	private static final String O_STRING = "O";
	private static final String BLANK_STRING = " ";

	/**
	 * the string formatting of marks
	 * @return the marks as strings
	 */
	@Override
	public String toString() {
		return switch (this) {
			case BLANK -> BLANK_STRING;
			case X -> X_STRING;
			case O -> O_STRING;
		};
	}
}
