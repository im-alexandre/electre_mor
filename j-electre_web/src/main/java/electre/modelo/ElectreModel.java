package electre.modelo;

import java.util.Arrays;
import java.util.StringJoiner;

import com.google.gson.Gson;

public class ElectreModel {
	
	/*
	 * x => Relação atributos por alternativas. Cada array dentro do x é uma alternativa contendo seus respectivos valores
	 * p => Preferência forte
	 * q => Preferência Fraca
	 * v => Veto
	 * w => são os pesos atribuídos aos critérios.
	 * e => número de availiadores
	 * bh => Limites por critério. Cada array interno são os valores superiores dos critérios para determinada classe
	 * 		As colunas devem estar em ordem crescente.
	 * 
	 * exemplo de bh:
	 * {{'Limite inferior', 10, 35},
	 *  {'Limite 2', 		20, 50},
	 *  {'Limite 3', 		30, 70}
	 * }
	 */
	private double [][] x;
	private double [] p;
	private double [] q;
	private double [] v;
	private double [] w;
	private int e;
	private double [][] bh;
	
	
	 
	public String main (){
		ELECTRE_Tri electre = new ELECTRE_Tri();
		String[][] resultado = electre.e_Tri_Algorithm(this.x, this.p, this.q, this.v, this.w, this.e, this.bh);
		StringJoiner sj = new StringJoiner(System.lineSeparator());
		for (String[] row : resultado) {
		    sj.add(Arrays.toString(row));
		}
		return new Gson().toJson(sj);
	}
	public double[][] getX() {
		return x;
	}
	public void setX(double[][] x) {
		this.x = x;
	}
	public double[] getP() {
		return p;
	}
	public void setP(double[] p) {
		this.p = p;
	}
	public double[] getQ() {
		return q;
	}
	public void setQ(double[] q) {
		this.q = q;
	}
	public double[] getV() {
		return v;
	}
	public void setV(double[] v) {
		this.v = v;
	}
	public double[] getW() {
		return w;
	}
	public void setW(double[] w) {
		this.w = w;
	}
	public double[][] getBh() {
		return bh;
	}
	public void setBh(double[][] bh) {
		this.bh = bh;
	}
	
}
