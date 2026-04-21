/**
 * The renderer factory which creates the relevent renderer
 */
public class RendererFactory {
	/**
	 * Constructor for renderer factory
	 */
	RendererFactory() {

	}

	/**
	 * Builds a render by type and size
	 * @param type the type of renderer void or console
	 * @param size the size of the renderer if console
	 * @return renderer object or null
	 */
	public Renderer buildRenderer(String type, int size) {
		return switch (type) {
			case "void" -> new VoidRenderer();
			case "console" -> new ConsoleRenderer(size);
			default -> null;
		};
	}
}
