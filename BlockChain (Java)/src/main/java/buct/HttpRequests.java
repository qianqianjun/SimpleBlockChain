package buct;

import java.io.*;
import java.net.URL;
import java.net.URLConnection;
import java.util.List;
import java.util.Map;

public class HttpRequests {
    public String sendGet(String address) throws IOException {
        URL url=new URL(address);
        InputStream is=url.openStream();
        InputStreamReader isr=new InputStreamReader(is);
        BufferedReader br=new BufferedReader(isr);
        String line=br.readLine();
        StringBuffer sb=new StringBuffer();
        while(line!=null){
            sb.append(line);
            sb.append("\n");
            line=br.readLine();
        }
        is.close();
        isr.close();
        br.close();
        return sb.toString();
    }
    public String GET(String address) throws IOException {
        URL url=new URL(address);
        URLConnection connection=url.openConnection();
        connection.setRequestProperty("accept","*/*");
        connection.setRequestProperty("connection","Keep-Alive");
        connection.setRequestProperty("user-agent","Mozilla/4.0 (compatible; " +
                "MSIE 6.0; Windows NT 5.1;SV1)");
        connection.connect();
        Map<String, List<String>> map=connection.getHeaderFields();
        for(String key:map.keySet()){
            System.out.println(key+"--->"+map.get(key));
        }
        BufferedReader br=new BufferedReader(new InputStreamReader(
                connection.getInputStream()
        ));
        String line=br.readLine();
        StringBuffer sb=new StringBuffer();
        while(line!=null){
            sb.append(line);
            sb.append("\n");
            line=br.readLine();
        }
        return sb.toString();
    }
    public String POST(String address) throws IOException {
        URL url=new URL(address);
        URLConnection connection=url.openConnection();
        connection.setRequestProperty("accept","*/*");
        connection.setRequestProperty("connection","Keep-Alive");
        connection.setRequestProperty("user-agent","Mozilla/4.0 (compatible; " +
                "MSIE 6.0; Windows NT 5.1;SV1)");
        //发送post请求必须要调用下面两个函数：
        connection.setDoOutput(true);
        connection.setDoInput(true);

        PrintWriter out=new PrintWriter(connection.getOutputStream());
        //设置请求参数：
        //out.print(parma);
        out.print("one=gaoqian&two=gaoqianqian");
        //flush 输出流的缓冲
        out.flush();
        //读取响应：
        BufferedReader br=new BufferedReader(new InputStreamReader(connection.getInputStream()));
        StringBuffer sb=new StringBuffer();
        String line=br.readLine();
        while(line!=null){
            sb.append(line);
            sb.append("\n");
            line=br.readLine();
        }
        return sb.toString();
    }
}
