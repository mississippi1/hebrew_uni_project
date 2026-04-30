/**
 * A renderer that produces no output.
 */
public class VoidRenderer implements Renderer {

	/**
	 * Does nothing.
	 * @param board the board to render.
	 */
	@Override
	public void renderBoard(Board board) {
        return;
	}
}
