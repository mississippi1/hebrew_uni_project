import java.util.Random;

/**
 * the smart player class which should win 80%
 */
public class SmartPlayer implements Player {

	/**
	 * constructs the smart plauer factory
	 */
    SmartPlayer(){
    }

	/**
	 * Plays turn for smart player.
	 * @param board board class
	 * @param mark the mark to put
	 */
    @Override
    public void playTurn(Board board, Mark mark) {
		boolean success;
		for (int index = 0; index < board.getSize(); index++) {
			success = board.putMark(mark, index, index+1);
			if (success) {
				return;
			}
		}
		for (int col = 1; col < board.getSize(); col++) {
			success = board.putMark(mark, 0, col);
			if (success) {
				return;
			}
		}

		for(int row = 1; row < board.getSize(); row++) {
			success = board.putMark(mark, row, 0);
			if (success) {
				return;
			}
		}

        Random r = new Random();

        do {
            success = board.putMark(mark, r.nextInt(board.getSize()), r.nextInt(board.getSize()));
        } while (!success);
    }

}
