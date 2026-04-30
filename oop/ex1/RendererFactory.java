/**
 * The renderer factory which creates the relevent renderer
 */
public class RendererFactory {
	/**
	 * Constructor for renderer factory
	 */
	RendererFactory() {}
	private static final String TYPE_VOID = "void";
	private static final String TYPE_CONSOLE = "console";

	/**
	 * Builds a render by type and size
	 * @param type the type of renderer void or console
	 * @param size the size of the renderer if console
	 * @return renderer object or null
	 */
	public Renderer buildRenderer(String type, int size) {
		return switch (type) {
			case TYPE_VOID -> new VoidRenderer();
			case TYPE_CONSOLE -> new ConsoleRenderer(size);
			default -> null;
		};
	}
}
