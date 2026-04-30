/**
 * The tournament class which is responsible for running a multi game tournament and processing user input
 */
public class Tournament {

	private static final int PLAYERS_IN_A_GAME = 2;
	private static final int POSITION_IN_INPUT_OF_ROUNDS = 0;
	private static final int POSITION_IN_INPUT_OF_SIZE = 1;
	private static final int POSITION_IN_INPUT_OF_WIN_STREAK = 2;
	private static final int POSITION_IN_INPUT_OF_RENDERER = 3;
	private static final int POSITION_IN_INPUT_OF_PLAYER_1 = 4;
	private static final int POSITION_IN_INPUT_OF_PLAYER_2 = 5;

	private static final String RESULTS_STRING_START = "######### Results #########";
	private static final String PLAYER_1_RESULT_STRING = "Player 1, %s won: %d rounds%n";
	private static final String PLAYER_2_RESULT_STRING = "Player 2, %s won: %d rounds%n";
	private static final String TIES_STRING = "Ties: %d%n";

	private final int rounds;
	private final Renderer renderer;
	private final Player player1;
	private final Player player2;

	/**
	 * Constructor for tournament
	 * @param rounds the rounds to run
	 * @param renderer the renderer to use
	 * @param player1 the player type 1
	 * @param player2 player type 2
	 */
	public Tournament(int rounds, Renderer renderer, Player player1, Player player2) {
		this.rounds = rounds;
		this.renderer = renderer;
		this.player1 = player1;
		this.player2 = player2;
	}

	/**
	 * Executing a tournament until all rounds have been run. Will input statistics afterwards.
	 * @param size the size of the board
	 * @param winStreak the number of same marks in a row / column / diagonal to win
	 * @param playerName1 the name of player 1
	 * @param playerName2 the name of player 2
	 */
	public void playTournament(int size, int winStreak, String playerName1, String playerName2) {
		int winsForPlayer1 = 0;
		int winsForPlayer2 = 0;
		int ties = 0;
		for (int round = 0; round < rounds; round++) {
			boolean isPlayer1X = round % PLAYERS_IN_A_GAME == 0;
			Player playerX = isPlayer1X ? player1 : player2;
			Player playerO = isPlayer1X ? player2 : player1;
			Game game = new Game(playerX, playerO, size, winStreak, renderer);
			Mark result = game.run();
			switch (result) {
				case BLANK:
					ties++;
					break;
				case X:
					if (isPlayer1X) {
						winsForPlayer1++;
					} else {
						winsForPlayer2++;
					}
					break;
				case O:
					if (isPlayer1X) {
						winsForPlayer2++;
					} else {
						winsForPlayer1++;
					}
					break;
			}
		}

		System.out.println(RESULTS_STRING_START);
		System.out.printf(PLAYER_1_RESULT_STRING, playerName1, winsForPlayer1);
		System.out.printf(PLAYER_2_RESULT_STRING, playerName2, winsForPlayer2);
		System.out.printf(TIES_STRING, ties);
	}

	/**
	 * The main program, responsible for getting input from user about how to run the program
	 * @param args the array of strings from user for configuration
	 */
	public static void main(String[] args) {
		PlayerFactory playerFactory = new PlayerFactory();
		RendererFactory rendererFactory = new RendererFactory();
		int roundCount = Integer.parseInt(args[POSITION_IN_INPUT_OF_ROUNDS]);
		int size = Integer.parseInt(args[POSITION_IN_INPUT_OF_SIZE]);
		int winStreak = Integer.parseInt(args[POSITION_IN_INPUT_OF_WIN_STREAK]);
		Renderer renderer = rendererFactory.buildRenderer(args[POSITION_IN_INPUT_OF_RENDERER], size);
		String playerName1 = args[POSITION_IN_INPUT_OF_PLAYER_1];
		String playerName2 = args[POSITION_IN_INPUT_OF_PLAYER_2];
		Player player1 = playerFactory.buildPlayer(playerName1);
		Player player2 = playerFactory.buildPlayer(playerName2);
		new Tournament(roundCount, renderer, player1, player2)
				.playTournament(size, winStreak, playerName1, playerName2);
	}
}
