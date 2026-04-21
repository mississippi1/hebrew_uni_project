/**
 * The tournament class which is responsible for running a multi game tournament and processing user input
 */
public class Tournament {
	private int rounds;
	private Renderer renderer;
	private Player player1;
	private Player player2;

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
		for(int round = 0; round < rounds; round++) {
			Player playerX = round % 2 == 0 ? player1 : player2;
			Player playerO = round % 2 == 1 ? player1 : player2;
			Game game = new Game(playerX, playerO, size, winStreak, renderer);
			Mark result = game.run();
			switch (result) {
				case BLANK:
					ties++;
					break;
				case X:
					if(round % 2 == 0){
						winsForPlayer1++;
					}else{
						winsForPlayer2++;
					}
					break;
				case O:
					if(round % 2 == 0){
						winsForPlayer2++;
					}else{
						winsForPlayer1++;
					}
					break;
			}
		}

		System.out.println("######### Results #########");
		System.out.println("Player 1, " + playerName1 + " won: " + winsForPlayer1 + " rounds");
		System.out.println("Player 2, " + playerName2 + " won: " + winsForPlayer2 + " rounds");
		System.out.println("Ties: " + ties);
	}

	/**
	 * The main program, responsible for getting input from user about how to run the program
	 * @param args the array of strings from user for configuration
	 */
	public static void main(String[] args){
		PlayerFactory pf = new PlayerFactory();
		RendererFactory  rf = new RendererFactory();
		int roundCount = Integer.parseInt(args[0]);
		int size = Integer.parseInt(args[1]);
		int winStreak = Integer.parseInt(args[2]);
		Renderer renderer = rf.buildRenderer(args[3], size);
		String p1Name = args[4];
		String p2Name = args[5];
		Player player1 = pf.buildPlayer(p1Name);
		Player player2 = pf.buildPlayer(p2Name);
		new Tournament(roundCount, renderer, player1, player2)
				.playTournament(size, winStreak, p1Name, p2Name);
	}
}
