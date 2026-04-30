/**
 * The human player which is responsible for managing human players and processing their actions
 */
public class HumanPlayer implements Player {
	/**
	 * Constructor
	 */
    HumanPlayer (){}

	private static final int
			BASE_OF_INPUT_STRING_TO_GET_POS_OF_X_AND_Y = 10;
	private static final String INPUT_FROM_PLAYER_STRING = "Player %s, type coordinates: ";
	private static final String INVALID_POSITION_STRING =
			"Invalid mark position. Please choose a valid position: ";
	private static final String UNAVAILABLE_POSITION_STRING =
			"Mark position is already occupied. Please choose a valid position: ";

	/**
	 * Playing turn for human player
	 * @param board board class
	 * @param mark the mark to put
	 */
	@Override
	public void playTurn(Board board, Mark mark) {
		printToScreen(String.format(INPUT_FROM_PLAYER_STRING, mark));
		boolean success = false;
		do {
			int input = KeyboardInput.readInt();
			int inputRow = input / BASE_OF_INPUT_STRING_TO_GET_POS_OF_X_AND_Y;
			int inputCol = input % BASE_OF_INPUT_STRING_TO_GET_POS_OF_X_AND_Y;
			if (inputRow < 0 || inputRow >= board.getSize()
					|| inputCol < 0 || inputCol >= board.getSize()) {
				printToScreen(INVALID_POSITION_STRING);
				continue;
			}
			success = board.putMark(mark, inputRow, inputCol);
			if (!success) {
				printToScreen(UNAVAILABLE_POSITION_STRING);
			}
		} while (!success);
	}

	private void printToScreen(String message) {
		System.out.print(message);
	}
}
