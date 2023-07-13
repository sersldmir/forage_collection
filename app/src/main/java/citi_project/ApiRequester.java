package citi_project;

import java.io.IOException;
import java.net.URI;
import java.net.http.*;
import java.util.regex.*;

public class ApiRequester {

    private String identifier;

    public ApiRequester(String identifier){
        this.identifier = identifier;
    }

    public double getStockRealPrice() throws IOException, InterruptedException{

        double price;

        // request data
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://latest-stock-price.p.rapidapi.com/price?Indices=NIFTY%2050&Identifier="+this.identifier))
            .header("X-RapidAPI-Key", "65c155fd51msh901b00387edc8d4p143062jsnb71408090645")
            .header("X-RapidAPI-Host", "latest-stock-price.p.rapidapi.com")
            .method("GET", HttpRequest.BodyPublishers.noBody())
            .build();
        HttpResponse<String> response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
        // System.out.println("-------------");
        String raw = response.body().toString();
        // System.out.println(raw);

        // find price
        String pricePattern = "(?<=lastPrice\\\":)\\d+(?:\\.\\d+)?(?=,)";
        Pattern priceRegex = Pattern.compile(pricePattern);
        Matcher priceMatch = priceRegex.matcher(raw);
        if (priceMatch.find()) {
            String number = priceMatch.group();
            // System.out.println("Number found: " + number);
            price = Double.parseDouble(number);
        } else {
            // System.out.println("No number found.");
            price = Double.parseDouble("99.99");
        }

        return price;
    }
    
}

class Main{
    public static void main(String[] args)  throws IOException, InterruptedException{
        ApiRequester api = new ApiRequester("TITANEQN");
        System.out.println("TITANEQN");
        System.out.println(api.getStockRealPrice());

        ApiRequester api_ = new ApiRequester("LTEQN");
        System.out.println("LTEQN");
        System.out.println(api_.getStockRealPrice());

        ApiRequester api__ = new ApiRequester("LTIMEQN");
        System.out.println("LTIMEQN");
        System.out.println(api__.getStockRealPrice());
    }
}