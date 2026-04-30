import java.util.Random;

/**
 * the smart player class which should win 80%
 */
public class SmartPlayer implements Player {

	private static final int[][] COMBINATIONS = {
			{0, 1},
			{1, 0},
			{0, 1},
			{1, 1},
			{1, -1},
	};

	/**
	 * Plays turn for smart player.
	 * @param board board class
	 * @param mark the mark to put
	 */
	@Override
	public void playTurn(Board board, Mark mark) {
		boolean success;
		int[] moveWithLongestStreakIfExists =
				moveWithLongestMarks(board, mark);
		if(moveWithLongestStreakIfExists !=null){
			success = board.putMark(mark,
					moveWithLongestStreakIfExists[0],
					moveWithLongestStreakIfExists[1]);
			if (success) {
				return;
			}
		}
		for (int row = 0; row < board.getSize(); row++) {
			success = board.putMark(mark, row, board.getSize()-1);
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
		for (int row = 1; row < board.getSize(); row++) {
			success = board.putMark(mark, row, 0);
			if (success) {
				return;
			}
		}

		Random random = new Random();
		do {
			success = board.putMark(mark, random.nextInt(board.getSize()),
					random.nextInt(board.getSize()));
		} while (!success);
	}

	/**
	 * Retuen move with longest streak for a mark
	 * @param board the borad which is being played
	 * @param mark the mark to check
	 * @return position of best move or null if not exists
	 */
	private int[] moveWithLongestMarks(Board board, Mark mark) {
		int bestStreak = 0;
		int[] bestMove = null;
		for (int col = board.getSize()-1; col>=0; col--) {
			for (int row = 0; row < board.getSize(); row++) {
				if (board.getMark(row, col) != Mark.BLANK) {
					continue;
				}
				int streak = countMarksInARowOrDiag(board, row, col, mark);
				if (streak > bestStreak) {
					bestStreak = streak;
					bestMove = new int[]{row, col};
				}
			}
		}
		return bestMove;
	}

	/**
	 * Counts the streak of marks in each direction
	 * @param board the borad which is being played
	 * @param mark the mark to check
	 * @param row the row to check
	 * @param col the column to check
	 * @param mark the mark to check
	 * @return the longest steak exists
	 */
	private int countMarksInARowOrDiag(Board board, int row, int col, Mark mark) {
		int max = 0;
		for (int[] direction : COMBINATIONS) {
			int total = countMarks(row, col, direction[0], direction[1],
							board.getSize(), mark, board)
					+ countMarks(row, col, -direction[0], -direction[1],
							board.getSize(), mark, board);
			if (total > max) {
				max = total;
			}
		}
		return max;
	}

	/**
	 * Counts marks in a given direction
	 * @param startRow the row to start
	 * @param startCol the column to start
	 * @param movementInRow the way to move the scan in the rows
	 * @param movmentInCol the way to move the scan in the columns
	 * @param steps the number of steps to take
	 * @param mark the mark to check
	 * @param board the board to check
	 * @return the nu,ber of marks in the streak
	 */
	private int countMarks(int startRow, int startCol, int movementInRow,
						   int movmentInCol, int steps, Mark mark, Board board) {
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
