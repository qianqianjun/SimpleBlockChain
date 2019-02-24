package buct;
import org.junit.Test;

import java.io.IOException;

public class BlockTest
{
    @Test
    public static void main(String[] args){
        HttpRequests httpRequests=new HttpRequests();
        String url="http://127.0.0.1:5000/posttest";
        try {
            String result=httpRequests.POST(url);
            System.out.println(result);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
