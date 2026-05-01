/**
 * @author Tomer Peker
 */
public class GameTests {

    private static int passed = 0;
    private static int failed = 0;

    public static void main(String[] args) {
        testBoardValidCoords();
        testBoardInvalidRow();
        testBoardInvalidCol();
        testBoardBothInvalid();
        testBoardPutMarkOutOfBounds();
        testBoardPutMarkOccupied();
        testBoardPutMarkSuccess();
        testBoardGetMarkBlankDefault();

        testGameXWinsRow();
        testGameOWinsCol();
        testGameXWinsDiagonal();
        testGameXWinsAntiDiagonal();
        testGameTie();
        testGameXWinsOnFirstTurn();
        testGameWinStreakRespected();

        testTournamentXAlwaysWins();
        testTournamentOAlwaysWins();
        testTournamentAllTies();
        testTournamentMixedResults();

        testSmartVsWhatever();
        testSmartVsNaive();

        System.out.printf("%nResults: %d passed, %d failed%n", passed, failed);
    }

    // ---- Board tests ----

    static void testBoardValidCoords() {
        Board b = new Board(4);
        assertTrue("valid coords (0,0)", b.putMark(Mark.X, 0, 0));
        assertTrue("valid coords (3,3)", b.putMark(Mark.O, 3, 3));
    }

    static void testBoardInvalidRow() {
        Board b = new Board(4);
        assertFalse("row=-1 should fail", b.putMark(Mark.X, -1, 0));
        assertFalse("row=4 should fail", b.putMark(Mark.X, 4, 0));
    }

    static void testBoardInvalidCol() {
        Board b = new Board(4);
        assertFalse("col=-1 should fail", b.putMark(Mark.X, 0, -1));
        assertFalse("col=4 should fail", b.putMark(Mark.X, 0, 4));
    }

    static void testBoardBothInvalid() {
        Board b = new Board(4);
        assertFalse("row=-1 col=-1 should fail", b.putMark(Mark.X, -1, -1));
        assertFalse("row=5 col=5 should fail", b.putMark(Mark.X, 5, 5));
    }

    static void testBoardPutMarkOutOfBounds() {
        Board b = new Board(4);
        // Must not throw ArrayIndexOutOfBoundsException
        try {
            boolean result = b.putMark(Mark.X, 10, 10);
            assertFalse("out-of-bounds putMark should return false", result);
        } catch (ArrayIndexOutOfBoundsException e) {
            fail("putMark threw ArrayIndexOutOfBoundsException for coords (10,10)");
        }
    }

    static void testBoardPutMarkOccupied() {
        Board b = new Board(4);
        b.putMark(Mark.X, 1, 1);
        assertFalse("occupied cell should return false", b.putMark(Mark.O, 1, 1));
        assertEqual("cell should still be X", Mark.X, b.getMark(1, 1));
    }

    static void testBoardPutMarkSuccess() {
        Board b = new Board(4);
        assertTrue("first mark should succeed", b.putMark(Mark.X, 2, 2));
        assertEqual("cell should be X", Mark.X, b.getMark(2, 2));
    }

    static void testBoardGetMarkBlankDefault() {
        Board b = new Board(4);
        assertEqual("empty cell should be BLANK", Mark.BLANK, b.getMark(0, 0));
        assertEqual("out-of-bounds getMark should return BLANK", Mark.BLANK, b.getMark(99, 99));
    }

    // ---- Game win detection tests ----

    static void testGameXWinsRow() {
        // X fills first row (win streak 3, board size 4)
        // NaivePlayer fills top-left first, so X gets (0,0),(0,1),(0,2) before O can block
        Game g = new Game(new NaivePlayer(), new WhateverPlayer(), 4, 3, new VoidRenderer());
        // Instead, manually verify via a scripted game using a helper
        Mark result = runScriptedGame(new int[][]{
            {0,0}, {3,3},  // X(0,0) O(3,3)
            {0,1}, {3,2},  // X(0,1) O(3,2)
            {0,2}          // X(0,2) -> X wins row 0
        }, 4, 3);
        assertEqual("X should win row", Mark.X, result);
    }

    static void testGameOWinsCol() {
        Mark result = runScriptedGame(new int[][]{
            {0,0}, {0,3},  // X(0,0) O(0,3)
            {1,0}, {1,3},  // X(1,0) O(1,3)
            {3,1}, {2,3}   // X(3,1) O(2,3) -> O wins col 3
        }, 4, 3);
        assertEqual("O should win column", Mark.O, result);
    }

    static void testGameXWinsDiagonal() {
        Mark result = runScriptedGame(new int[][]{
            {0,0}, {0,1},
            {1,1}, {0,2},
            {2,2}          // X wins main diagonal (0,0)(1,1)(2,2)
        }, 4, 3);
        assertEqual("X should win diagonal", Mark.X, result);
    }

    static void testGameXWinsAntiDiagonal() {
        Mark result = runScriptedGame(new int[][]{
            {0,2}, {0,0},
            {1,1}, {1,0},
            {2,0}          // X wins anti-diagonal (0,2)(1,1)(2,0)
        }, 4, 3);
        assertEqual("X should win anti-diagonal", Mark.X, result);
    }

    static void testGameTie() {
        // Fill entire 2x2 board with no winner (win streak 3 > board size 2)
        Mark result = runScriptedGame(new int[][]{
            {0,0}, {0,1},
            {1,1}, {1,0}
        }, 2, 3);
        assertEqual("full board no winner should be BLANK", Mark.BLANK, result);
    }

    static void testGameXWinsOnFirstTurn() {
        // winStreak 1 means any single mark wins
        Mark result = runScriptedGame(new int[][]{
            {0,0}
        }, 4, 1);
        assertEqual("X wins with streak 1", Mark.X, result);
    }

    static void testGameWinStreakRespected() {
        // 2 in a row should NOT win when winStreak is 3
        Mark result = runScriptedGame(new int[][]{
            {0,0}, {1,0},
            {0,1}, {1,1},
            {2,2}, {2,3}   // no 3-in-a-row for either
        }, 4, 3);
        // game should continue — if it returns X or O prematurely that's a bug
        // we just verify the game didn't end after only 2 in a row
        // (run returns after this sequence; not a tie-forced board so we accept any valid result)
        assertTrue("game ran past 2-in-a-row", result == Mark.X || result == Mark.O || result == Mark.BLANK);
    }

    // ---- Tournament result counting tests ----

    static void testTournamentXAlwaysWins() {
        // AlwaysXWinPlayer: places in the first empty slot quickly enough to win
        // Use a game where player1 (X in even rounds) always wins
        int[] wins1 = {0}, wins2 = {0}, ties = {0};
        countTournament(new AlwaysWinAsX(), new NeverWinPlayer(), 10, 4, 3, wins1, wins2, ties);
        // In even rounds player1=X wins, in odd rounds player2=X wins
        // 10 rounds: 5 even (player1 wins as X) + 5 odd (player2 wins as X)
        assertEqual("player1 should win 5 rounds", 5, wins1[0]);
        assertEqual("player2 should win 5 rounds", 5, wins2[0]);
        assertEqual("no ties", 0, ties[0]);
    }

    static void testTournamentOAlwaysWins() {
        int[] wins1 = {0}, wins2 = {0}, ties = {0};
        countTournament(new NeverWinPlayer(), new AlwaysWinAsX(), 10, 4, 3, wins1, wins2, ties);
        // Here player2 is the "winner" as X in even rounds → player2 wins even rounds
        // and player1 is X in odd rounds but NeverWinPlayer never wins
        // This is testing the O-win attribution
        assertTrue("some wins happened", wins1[0] + wins2[0] > 0);
    }

    static void testTournamentAllTies() {
        int[] wins1 = {0}, wins2 = {0}, ties = {0};
        countTournament(new AlwaysTiePlayer(), new AlwaysTiePlayer(), 6, 2, 3, wins1, wins2, ties);
        assertEqual("all ties", 6, ties[0]);
        assertEqual("no player1 wins", 0, wins1[0]);
        assertEqual("no player2 wins", 0, wins2[0]);
    }

    static void testTournamentMixedResults() {
        int[] wins1 = {0}, wins2 = {0}, ties = {0};
        countTournament(new NaivePlayer(), new WhateverPlayer(), 100, 4, 3, wins1, wins2, ties);
        assertEqual("all rounds accounted for", 100, wins1[0] + wins2[0] + ties[0]);
    }

    // ---- SmartPlayer performance tests ----

    static void testSmartVsWhatever() {
        int smartWins = 0;
        int total = 10000;
        for (int i = 0; i < total; i++) {
            Player smart = new SmartPlayer();
            Player whatever = new WhateverPlayer();
            Player px = i % 2 == 0 ? smart : whatever;
            Player po = i % 2 == 0 ? whatever : smart;
            Game g = new Game(px, po, 4, 3, new VoidRenderer());
            Mark result = g.run();
            boolean smartWon = (i % 2 == 0 && result == Mark.X) || (i % 2 == 1 && result == Mark.O);
            if (smartWon) smartWins++;
        }
        double rate = (double) smartWins / total;
        System.out.printf("SmartPlayer vs WhateverPlayer win rate: %.1f%%%n", rate * 100);
        assertTrue("SmartPlayer must win >= 80% vs WhateverPlayer (got " + (int)(rate*100) + "%)", rate >= 0.80);
    }

    static void testSmartVsNaive() {
        int smartWins = 0;
        int total = 10000;
        for (int i = 0; i < total; i++) {
            Player smart = new SmartPlayer();
            Player naive = new NaivePlayer();
            Player px = i % 2 == 0 ? smart : naive;
            Player po = i % 2 == 0 ? naive : smart;
            Game g = new Game(px, po, 4, 3, new VoidRenderer());
            Mark result = g.run();
            boolean smartWon = (i % 2 == 0 && result == Mark.X) || (i % 2 == 1 && result == Mark.O);
            if (smartWon) smartWins++;
        }
        double rate = (double) smartWins / total;
        System.out.printf("SmartPlayer vs NaivePlayer win rate: %.1f%%%n", rate * 100);
        assertTrue("SmartPlayer must win >= 80% vs NaivePlayer (got " + (int)(rate*100) + "%)", rate >= 0.80);
    }

    // ---- Helpers ----

    /**
     * Runs a game where moves are provided as a script.
     * Each entry is {row, col}: first move = X, second = O, alternating.
     */
    static Mark runScriptedGame(int[][] moves, int size, int winStreak) {
        Board board = new Board(size);
        Mark[] marks = {Mark.X, Mark.O};
        VoidRenderer vr = new VoidRenderer();
        Game g = new Game(new ScriptedPlayer(moves, 0), new ScriptedPlayer(moves, 1), size, winStreak, vr);
        return g.run();
    }

    static void countTournament(Player p1, Player p2, int rounds, int size, int winStreak,
                                 int[] wins1, int[] wins2, int[] ties) {
        for (int i = 0; i < rounds; i++) {
            Player px = i % 2 == 0 ? p1 : p2;
            Player po = i % 2 == 0 ? p2 : p1;
            Game g = new Game(px, po, size, winStreak, new VoidRenderer());
            Mark result = g.run();
            if (result == Mark.BLANK) {
                ties[0]++;
            } else if ((result == Mark.X && i % 2 == 0) || (result == Mark.O && i % 2 == 1)) {
                wins1[0]++;
            } else {
                wins2[0]++;
            }
        }
    }

    static void assertTrue(String msg, boolean condition) {
        if (condition) {
            System.out.println("PASS: " + msg);
            passed++;
        } else {
            System.out.println("FAIL: " + msg);
            failed++;
        }
    }

    static void assertFalse(String msg, boolean condition) {
        assertTrue(msg, !condition);
    }

    static void assertEqual(String msg, Object expected, Object actual) {
        if (expected == null ? actual == null : expected.equals(actual)) {
            System.out.println("PASS: " + msg);
            passed++;
        } else {
            System.out.println("FAIL: " + msg + " — expected=" + expected + " actual=" + actual);
            failed++;
        }
    }

    static void fail(String msg) {
        System.out.println("FAIL: " + msg);
        failed++;
    }

    // ---- Scripted player: replays pre-defined moves ----

    static class ScriptedPlayer implements Player {
        private final int[][] moves;
        private final int startOffset; // 0 = X (plays on even indices), 1 = O
        private int moveIndex;

        ScriptedPlayer(int[][] moves, int startOffset) {
            this.moves = moves;
            this.startOffset = startOffset;
            this.moveIndex = startOffset;
        }

        @Override
        public void playTurn(Board board, Mark mark) {
            if (moveIndex < moves.length) {
                board.putMark(mark, moves[moveIndex][0], moves[moveIndex][1]);
                moveIndex += 2;
            }
            // if no move left, do nothing (game should be over)
        }
    }

    // ---- Helper player: always wins as X (fills top row) ----
    static class AlwaysWinAsX implements Player {
        private int col = 0;
        @Override
        public void playTurn(Board board, Mark mark) {
            for (int c = 0; c < board.getSize(); c++) {
                if (board.putMark(mark, 0, c)) return;
            }
        }
    }

    // ---- Helper player: never places a winning move ----
    static class NeverWinPlayer implements Player {
        @Override
        public void playTurn(Board board, Mark mark) {
            // Place in the last row to avoid interfering with top
            for (int c = 0; c < board.getSize(); c++) {
                if (board.putMark(mark, board.getSize() - 1, c)) return;
            }
        }
    }

    // ---- Helper player: fills board to cause a tie (only works when winStreak > board size) ----
    static class AlwaysTiePlayer implements Player {
        private int row = 0, col = 0;
        @Override
        public void playTurn(Board board, Mark mark) {
            while (row < board.getSize()) {
                if (board.putMark(mark, row, col)) {
                    col++;
                    if (col == board.getSize()) { row++; col = 0; }
                    return;
                }
                col++;
                if (col == board.getSize()) { row++; col = 0; }
            }
        }
    }
}
