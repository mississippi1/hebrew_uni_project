/**
* The player factory which creates the relevent player
 */
public class PlayerFactory {
	/**
	 * constructs the plauer factory
	 */
	PlayerFactory() {}
	private static final String TYPE_HUMAN = "human";
	private static final String TYPE_WHATEVER = "whatever";
	private static final String TYPE_NAIVE = "naive";
	private static final String TYPE_SMART = "smart";

	/**
	 * Initializing the correct player by type
	 * @param type human / whatever / naive / smart
	 * @return Player or null
	 */
	public Player buildPlayer(String type) {
		return switch (type) {
			case TYPE_HUMAN -> new HumanPlayer();
			case TYPE_WHATEVER -> new WhateverPlayer();
			case TYPE_NAIVE -> new NaivePlayer();
			case TYPE_SMART -> new SmartPlayer();
			default -> null;
		};
	}
}
