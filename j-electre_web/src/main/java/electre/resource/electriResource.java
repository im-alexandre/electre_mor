package electre.resource;

import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;

import com.google.gson.Gson;

import electre.modelo.ElectreModel;


@Path("electre")
public class electriResource {
	@POST
	@Produces(MediaType.APPLICATION_JSON)
	public String roda(String conteudo) {
		ElectreModel model =  new Gson().fromJson(conteudo, ElectreModel.class);
		String resposta = model.main();
		return resposta;
	}
	
}