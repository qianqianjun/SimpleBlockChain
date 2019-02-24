package buct;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;

public class ServerThread extends Thread{
    private Socket socket;
    public ServerThread(Socket socket){
        this.socket=socket;
    }

    @Override
    public void run() {
        PrintWriter printWriter=null;
        try {
            printWriter=new PrintWriter(socket.getOutputStream());
            printWriter.write("你好，这是一个get请求");
            printWriter.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
        finally {
            if(printWriter!=null){
                printWriter.close();
            }
        }
    }
}
