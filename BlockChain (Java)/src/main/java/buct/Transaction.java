package buct;

public class Transaction {
    public String sender;
    public String recipient;
    public Integer amount;
    public Transaction(String sender,String recipient,Integer amount){
        this.sender=sender;
        this.recipient=recipient;
        this.amount=amount;
    }
}
