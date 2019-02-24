package buct;

import java.io.UnsupportedEncodingException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;

public class BlockChain {
    public static Integer noice=4;
    public static String noiceStr="0000";
    public ArrayList<Block> chains;
    public ArrayList<Transaction> currentTransactions;
    //constructor
    public BlockChain(){
        this.chains=new ArrayList<>();
        this.currentTransactions=new ArrayList<>();
        //创建一个创世区块
        this.newBlock(100,"1");
    }
    //增加一个新的区块：
    public Block newBlock(Integer proof,String previousHash){
        Integer index=this.chains.size()+1;
        Long timestamp=System.currentTimeMillis();
        Block block=new Block(index,timestamp,this.currentTransactions,proof,previousHash);
        this.currentTransactions=new ArrayList<>();
        this.chains.add(block);
        return block;
    }
    //增加一个新的区块：
    public Block newBlock(Integer proof){
        Integer index=this.chains.size()+1;
        Long timestamp=System.currentTimeMillis();
        String previousHash=this.hash(this.getLastBlock());
        Block block=new Block(index,timestamp,this.currentTransactions,proof,previousHash);
        this.currentTransactions=new ArrayList<>();
        this.chains.add(block);
        return block;
    }
    //增减一个新的交易信息
    public Integer newTransactions(String sender,String recipient,Integer amount){
        Transaction transaction=new Transaction(sender,recipient,amount);
        this.currentTransactions.add(transaction);
        return this.getLastBlock().index+1;
    }
    //用于生成hash摘要的函数：
    public static String hash(Object block){
        MessageDigest messageDigest;
        String encodeStr = "";
        try {
            messageDigest = MessageDigest.getInstance("SHA-256");
            messageDigest.update(block.toString().getBytes("UTF-8"));
            encodeStr = byte2Hex(messageDigest.digest());
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
        return encodeStr;
    }
    //辅助生成hash摘要函数的一个函数：
    public static String byte2Hex(byte[] bytes){
        StringBuffer sb=new StringBuffer();
        String temp=null;
        for(Integer i=0;i<bytes.length;i++){
            temp=Integer.toHexString(bytes[i] & 0xFF);
            if(temp.length()==1){
                sb.append("0");
            }
            sb.append(temp);
        }
        return sb.toString();
    }
    //得到最近新形成的区块
    public Block getLastBlock(){
        return this.chains.get(this.chains.size()-1);
    }
    //实现工作量证明的函数：
    public Integer proofWord(Integer lastProof){
        Integer p=0;
        while(true){
            StringBuffer sb=new StringBuffer();
            sb.append(p.toString());
            sb.append(lastProof.toString());
            String hashStr=hash(sb.toString());
            if(hashStr.substring(0,noice).equals(noiceStr)) {
                System.out.println(hashStr);
                break;
            }
            p++;
        }
        System.out.println(p);
        return p;
    }
    public static void main(String[] args){
//        Block block=new Block(1,System.currentTimeMillis(),null,100,"good");
//        String str=hash(block);
//        Block block2=new Block(1,System.currentTimeMillis(),null,100,"good");
//        String str2=hash(block2);
//        Block block3=new Block(2,System.currentTimeMillis(),null,100,"good");
//        String str3=hash(block3);
//        System.out.println(str);
//        System.out.println(str2);
//        System.out.println(str3);
    }
}
