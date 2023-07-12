package citi_project;

public class MainApp {
    public static void main(String[] args) {
        ApiRequester apireq = new ApiRequester("DJIA");
        try{
            apireq.getStockPrice(5);
        }
        catch (Exception e){
            System.out.println(e);
        }
    }
}
