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
		int[] moveWithLongestStreakIfExists = moveWithLongestMarks(board, mark);
		if(moveWithLongestStreakIfExists !=null){
			success = board.putMark(mark, moveWithLongestStreakIfExists[0], moveWithLongestStreakIfExists[1]);
			if (success) {
				return;
			}
		}
		for(int row = 0; row < board.getSize(); row++) {
			success = board.putMark(mark, row, 1);
			if (success) {
				return;
			}
		}
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

	private int[] moveWithLongestMarks(Board board, Mark targetMark) {
		int bestStreak = 0;
		int[] bestMove = null;
		for (int row = 0; row < board.getSize(); row++) {
			for (int col = 0; col < board.getSize(); col++) {
				if (board.getMark(row, col) != Mark.BLANK) continue;
				int streak = countMarksInARowOrDiag(board, row, col, targetMark);
				if (streak > bestStreak) {
					bestStreak = streak;
					bestMove = new int[]{row, col};
				}
			}
		}
		return bestMove;
	}
	private int countMarksInARowOrDiag(Board board, int row, int col, Mark mark) {
		int max = 0;
		int[][] combinations = {{0,1}, {0,1}, {1,1}, {1,0}, {1,-1}};
		for(int[] option : combinations){
			int countStrekInTwoWay = countMarks(row, col, option[0], option[1], board.getSize(), mark, board)
					+ countMarks(row, col, -1*option[0], -1*option[1], board.getSize(), mark, board);
			if(countStrekInTwoWay > max){
				max = countStrekInTwoWay;
			}
		}
		return max;
	}

	private int countMarks(int startRow, int startCol, int movementInRow, int movmentInCol, int steps, Mark mark, Board board) {
		int maxCount = 0;
		for (int index = 1; index < steps; index++) {
			Mark currentMark = board.getMark(startRow + movementInRow * index,
					startCol + movmentInCol * index);
			if(mark != currentMark) {return maxCount;}
			else {
				maxCount++;
			}
		}
		return maxCount;
	}
}
