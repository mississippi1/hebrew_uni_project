/**
 * The human player which is responsible for managing human players and processing their actions
 */
public class HumanPlayer implements Player {
	/**
	 * Constructor
	 */
    HumanPlayer (){

    }

	/**
	 * Playing turn for human player
	 * @param board board class
	 * @param mark the mark to put
	 */
    @Override
	public void playTurn(Board board, Mark mark) {
        String stringToPrint = String.format("Player %s, type coordinates: ", mark);
        printToScreen(stringToPrint);
        boolean success = false;
        do {
            int input = KeyboardInput.readInt();

			int inputRow = input / 10;
			int inputCol = input % 10;
			if (inputRow< 0 || board.getSize() <= inputRow || inputCol< 0 || board.getSize() <= inputCol) {
                printToScreen("Invalid mark position. Please choose a valid position: ");
				continue;
            }
            success = board.putMark(mark, inputRow, inputCol);
            if (!success) {
                printToScreen("Mark position is already occupied. Please choose a valid position: ");
            }
        } while (!success);

    }

    private void printToScreen(String s) {
        System.out.print(s);
    }
}
