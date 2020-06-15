package electre.resource;


import java.io.IOException;
import java.net.URI;

import org.glassfish.grizzly.http.server.HttpServer;
import org.glassfish.jersey.grizzly2.httpserver.GrizzlyHttpServerFactory;
import org.glassfish.jersey.server.ResourceConfig;

public class servidor {
	public static void main(String[] args) throws IOException {
		ResourceConfig config = new ResourceConfig().packages("electre");
		URI uri = URI.create("http://localhost:8080/");
		HttpServer server = GrizzlyHttpServerFactory.createHttpServer(uri, config);
		System.out.println("Servidor na linha e ouvindo na porta 8080");
		System.in.read();
		server.stop();
	}
}
