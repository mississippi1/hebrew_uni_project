/**
 * The class which is responsible for managing the board of the game
 * @author Tomer Peker
 */
public class Board {

	private final static int DEFAULT_SIZE = 4;
	private int size = DEFAULT_SIZE;
    private Mark[][] board;

	private boolean isFree(int row, int col) {
		return board[row][col] == null || board[row][col] == Mark.BLANK ;
	}

	private void initializeBoardAsBlank(int size) {
		for (int i = 0; i < size; i++) {
			for (int j = 0; j < size; j++) {
				board[i][j] = Mark.BLANK;
			}
		}
	}

	/**
	 * The constroctor for default values
	 */
    Board() {
        board = new Mark[size][size];
        initializeBoardAsBlank(size);
    }

	/**
	 * The constructor for input size
	 * @param size the size * size of the board
	 */
    Board(int size) {
        this.size = size;
        board = new Mark[size][size];
        initializeBoardAsBlank(size);
    }

	/**
	 * Returns the size of the board
	 * @return size
	 */
    int getSize() {
        return size;
    }

	/**
	 * Puts the mark in position if possible
	 * @param mark the mark to put
	 * @param row the row of the desired position
	 * @param col the col of the desired position
	 * @return true if succeeded, false else
	 */
    public boolean putMark(Mark mark, int row, int col) {
        if(isCoordsOK(row, col) && isFree(row, col)){
            board[row][col] = mark;
            return true;
        }
        return false;

    }

	/**
	 * Fetching a mark from a position in the board
	 * @param row the row of the desired mark
	 * @param col the col of the desired mark
	 * @return the relevant mark, Mark.BLANK if row / col not legal
	 */
	public Mark getMark(int row, int col) {
        if(isCoordsOK(row, col)){
            return board[row][col];
        }
        return Mark.BLANK;
    }

	private boolean isCoordsOK(int  inputRow, int inputCol) {
		if(inputRow < 0 || inputRow >= size){
			return false;
		}
		return inputCol >= 0 && inputCol < size;
	}

}
