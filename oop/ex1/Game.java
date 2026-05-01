/**
 * The game class which is used to play a single game
 * @author Tomer Peker
 */
public class Game {

	private static final int DEFAULT_WIN_STREAK = 3;

	private final Player playerX;
	private final Player playerO;
	private final Renderer renderer;
	private final Board board;
	private final int winStreak;

	private enum WinType {
		PLAYER_X_WIN, PLAYER_O_WIN, NO_WIN
	}

	/**
	 * Constructor for game
	 * @param playerX Player which plays X
	 * @param playerO Player which plays O
	 * @param renderer Render which renders the board
	 */
	Game(Player playerX, Player playerO, Renderer renderer) {
		this.playerX = playerX;
		this.playerO = playerO;
		this.renderer = renderer;
		this.winStreak = DEFAULT_WIN_STREAK;
		this.board = new Board();
	}

	/**
	 * Constructor for game
	 * @param playerX Player which plays X
	 * @param playerO Player which plays O
	 * @param size The size of the board
	 * @param winStreak the number of marks to write in a line
	 * @param renderer Render which renders the board
	 */
	Game(Player playerX, Player playerO, int size, int winStreak, Renderer renderer) {
		this.playerX = playerX;
		this.playerO = playerO;
		this.renderer = renderer;
		this.winStreak = winStreak;
		this.board = new Board(size);
	}

	/**
	 * Get the win streak
	 * @return win streak to win
	 */
	public int getWinStreak() {
		return winStreak;
	}

	/**
	 * Get the board size
	 * @return the size of the board
	 */
	public int getBoardSize() {
		return board.getSize();
	}

	/**
	 * Execute the game by calling the player.turn method
	 * @return The mark of the player which won
	 */
	public Mark run() {
		WinType isPlayerWin = checkPlayerWin();
		while (isPlayerWin == WinType.NO_WIN && stillHasEmptyCells()) {
			playerX.playTurn(board, Mark.X);
			renderer.renderBoard(board);
			isPlayerWin = checkPlayerWin();
			if (isPlayerWin != WinType.NO_WIN || !stillHasEmptyCells()) {
				break;
			}
			playerO.playTurn(board, Mark.O);
			renderer.renderBoard(board);
			isPlayerWin = checkPlayerWin();
		}
		return switch (isPlayerWin) {
			case PLAYER_X_WIN -> Mark.X;
			case PLAYER_O_WIN -> Mark.O;
			default -> Mark.BLANK;
		};
	}

	private boolean stillHasEmptyCells() {
		for (int row = 0; row < board.getSize(); row++) {
			for (int col = 0; col < board.getSize(); col++) {
				if (board.getMark(row, col) == Mark.BLANK) {
					return true;
				}
			}
		}
		return false;
	}

	private WinType checkPlayerWin() {
		int size = board.getSize();
		for (int row = 0; row < size; row++) {
			WinType result = checkLine(row, 0, 0, 1, size);
			if (result != WinType.NO_WIN) {
				return result;
			}
		}
		for (int col = 0; col < size; col++) {
			WinType result = checkLine(0, col, 1, 0, size);
			if (result != WinType.NO_WIN) {
				return result;
			}
		}
		WinType diag = checkDiagNormal(size);
		if (diag != WinType.NO_WIN) {
			return diag;
		}
		return checkDiagAntiNormal(size);
	}

	private WinType checkDiagAntiNormal(int size) {
		for (int start = 0; start <= size - winStreak; start++) {
			WinType result = checkLine(0, size - 1 - start, 1, -1, size - start);
			if (result != WinType.NO_WIN) {
				return result;
			}
			result = checkLine(start, size - 1, 1, -1, size - start);
			if (result != WinType.NO_WIN) {
				return result;
			}
		}
		return WinType.NO_WIN;
	}

	private WinType checkDiagNormal(int size) {
		for (int start = 0; start <= size - winStreak; start++) {
			WinType result = checkLine(0, start, 1, 1, size - start);
			if (result != WinType.NO_WIN) {
				return result;
			}
			result = checkLine(start, 0, 1, 1, size - start);
			if (result != WinType.NO_WIN) {
				return result;
			}
		}
		return WinType.NO_WIN;
	}

	private WinType checkLine(int startRow, int startCol, int movementInRow, int movmentInCol, int steps) {
		Mark previousMarkSeen = Mark.BLANK;
		int playerXCount = 0;
		int playerOCount = 0;
		for (int index = 0; index < steps; index++) {
			Mark currentMark = board.getMark(startRow + movementInRow * index,
					startCol + movmentInCol * index);
			if (currentMark != previousMarkSeen) {
				previousMarkSeen = currentMark;
				playerXCount = 0;
				playerOCount = 0;
			} else if (previousMarkSeen == Mark.X) {
				playerXCount++;
			} else if (previousMarkSeen == Mark.O) {
				playerOCount++;
			}
            if (playerXCount == winStreak - 1) return WinType.PLAYER_X_WIN;
            if (playerOCount == winStreak - 1) return WinType.PLAYER_O_WIN;
			}
        return WinType.NO_WIN;
	}
}
