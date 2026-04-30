import java.util.Random;

/**
 * The whatever player which uses a random strategy
 */
public class WhateverPlayer implements Player {

	/**
	 * Constructor for whatever player
	 */
    WhateverPlayer(){

    }


	/**
	 * Plays a turn and puts a mark randomly
	 * @param board board class
	 * @param mark the mark to put
	 */
    @Override
    public void playTurn(Board board, Mark mark) {
        Random random = new Random();
        boolean success;
        do {
            success = board.putMark(mark, random.nextInt(board.getSize()), random.nextInt(board.getSize()));
        } while (!success);
    }
}
