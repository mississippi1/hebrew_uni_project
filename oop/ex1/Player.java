/**
* A player interface for the Tic Tak Toe game
* @author Tomer Peker
* */
public interface Player {
	/**
	 * Plays tuen by putting mark
	 * @param board board class
	 * @param mark the mark to put
	 */
	void playTurn(Board board, Mark mark);
}
