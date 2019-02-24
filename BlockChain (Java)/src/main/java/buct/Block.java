package buct;
import com.alibaba.fastjson.JSON;

import java.util.ArrayList;
public class Block{
    public Integer index;
    public long timestamp;
    public ArrayList<Transaction> transactions;
    public Integer proof;
    public String previousHash;
    public Block(Integer index,long timestamp,ArrayList<Transaction> transactions,Integer proof,String previousHash){
        this.index=index;
        this.timestamp=timestamp;
        this.transactions=transactions;
        this.proof=proof;
        this.previousHash=previousHash;
    }
    @Override
    public String toString() {
        return JSON.toJSONString(this);
    }
}
