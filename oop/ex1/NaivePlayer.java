/**
 * The naive player which uses a predictable strategy
 */
public class NaivePlayer implements Player {

	/**
	 * Constroctur for Naive player
	 */
    NaivePlayer(){
    }

	/**
	 * Plaus turn and puts mark, starts with row 0 and col 0 and puts marks where can.
	 * If not availble increments col. If not possible, increment row and set col = 0
	 * @param board board class
	 * @param mark the mark to put
	 */
	@Override
	public void playTurn(Board board, Mark mark) {
		int row = 0;
		int col = 0;
		boolean success;
		do {
			success = board.putMark(mark, row, col);
			col++;
			if (col == board.getSize()) {
				row++;
				col = 0;
			}
		} while (!success);
	}
}
