package buct;

import jdk.net.SocketFlow;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;

public class Peer {
    public static ArrayList<Peer> neighbour=new ArrayList<>();
    private Integer port;
    private BlockChain Chains;
    public Peer(Integer port){
        this.port=port;
        StartServer();
    }
    public void StartServer(){
        this.port=port;
        try {
            ServerSocket serverSocket=new ServerSocket(this.port);
            Socket socket=null;
            System.out.println("服务器等待连接");
            while(true){
                socket=serverSocket.accept();
                ServerThread thread=new ServerThread(socket);
                thread.start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    public static void main(String[] args){
        Integer port=8888;
        Peer peer=new Peer(port);
    }
}
