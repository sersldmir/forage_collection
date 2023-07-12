package citi_project;

import java.io.IOException;
import java.math.BigDecimal;
import java.util.HashMap;
import java.util.concurrent.TimeUnit;
import java.net.URI;
import java.net.http.*;
import java.sql.Timestamp;
import java.util.regex.*;

public class ApiRequester {

    private String stockName;
    private HashMap<Timestamp, BigDecimal> info;

    public ApiRequester(String nameStock){
        this.stockName = nameStock;
        this.info = new HashMap<>();
    }

    public String getStockName() {
        return stockName;
    }

    public void setStockName(String stockName) {
        this.stockName = stockName;
    }

    public void getStockPrice(int seconds) throws IOException, InterruptedException{
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://latest-stock-price.p.rapidapi.com/price?Indices=NIFTY%2050&Identifier=TITANEQN"))
            .header("X-RapidAPI-Key", "65c155fd51msh901b00387edc8d4p143062jsnb71408090645")
            .header("X-RapidAPI-Host", "latest-stock-price.p.rapidapi.com")
            .method("GET", HttpRequest.BodyPublishers.noBody())
            .build();
        HttpResponse<String> response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println("-------------");
        String raw = response.body().toString();
        System.out.println(raw);

        // find price
        String pricePattern = "(?<=open\":)\\d+(?=,)";
        Pattern priceRegex = Pattern.compile(pricePattern);
        Matcher priceMatch = priceRegex.matcher(raw);
        BigDecimal price;
        if (priceMatch.find()) {
            String number = priceMatch.group();
            System.out.println("Number found: " + number);
            price = new BigDecimal(priceMatch.group());
        } else {
            System.out.println("No number found.");
            price = new BigDecimal("99.99");
        }

        Timestamp timestamp = new Timestamp(System.currentTimeMillis());
        this.info.put(timestamp, price);
        System.out.println("Sleeping");
        TimeUnit.SECONDS.sleep(seconds);
        System.out.println("Awake");
        for (Timestamp key: this.info.keySet()){
            System.out.println(key.toString());
            System.out.println(this.info.get(key).toString());
        }
    }
    
    
}
