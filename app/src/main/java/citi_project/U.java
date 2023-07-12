package citi_project;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class U {
    public static void main(String[] args) {
        String text = "[{\"symbol\":\"TITAN\",\"identifier\":\"TITANEQN\",\"open\":3114,\"dayHigh\":3124,\"dayLow\":3087.65,\"lastPrice\":3098,\"previousClose\":3087.6,\"change\":10.4,\"pChange\":0.34,\"totalTradedVolume\":1300168,\"totalTradedValue\":4033290157.84,\"lastUpdateTime\":\"12-Jul-2023 15:59:55\",\"yearHigh\":3210,\"yearLow\":2107.45,\"perChange365d\":42.71,\"perChange30d\":7.35}]";
        String pattern = "(?<=open\":)\\d+(?=,)";

        Pattern regex = Pattern.compile(pattern);
        Matcher matcher = regex.matcher(text);

        if (matcher.find()) {
            String number = matcher.group();
            System.out.println("Number found: " + number);
        } else {
            System.out.println("No number found.");
        }
    }
}

