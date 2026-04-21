/**
* The player factory which creates the relevent player
 */
public class PlayerFactory {
	/**
	 * constructs the plauer factory
	 */
	PlayerFactory() {

	}

	/**
	 * Initializing the correct player by type
	 * @param type human / whatever / naive / smart
	 * @return Player or null
	 */
	public Player buildPlayer(String type) {
		return switch (type) {
			case "human" -> new HumanPlayer();
			case "whatever" -> new WhateverPlayer();
			case "naive" -> new NaivePlayer();
			case "smart" -> new SmartPlayer();
			default -> null;
		};
	}
}
