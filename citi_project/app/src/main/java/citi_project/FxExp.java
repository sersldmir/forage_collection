package citi_project;

import java.util.Date;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Timer;
import java.util.TimerTask;
// import java.util.concurrent.ThreadLocalRandom;
import java.util.ArrayList;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.scene.Scene;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.CategoryAxis;
import javafx.scene.chart.XYChart;
import javafx.stage.Stage;
 
 
public class FxExp extends Application {

    public static final int WINDOW_SIZE = 10;
    
    @Override
    public void start(Stage stage) {
        stage.setTitle("Stock Dashboard");

        //X and Y axis
        final CategoryAxis xAxis = new CategoryAxis();
        final NumberAxis yAxis = new NumberAxis();
        xAxis.setLabel("Time");
        xAxis.setAnimated(false);
        yAxis.setLabel("Price");
        yAxis.setAnimated(false);

        //creating the chart
        final LineChart<String, Number> lineChart = new LineChart<>(xAxis, yAxis);
        lineChart.setAnimated(false);
        lineChart.setTitle("Real time price monitoring chart");

        // stock identifiers
        ArrayList<String> stocks = new ArrayList<>();
        stocks.add("TITANEQN");
        stocks.add("LTEQN");
        stocks.add("LTIMEQN");

        // api requesters
        ArrayList<ApiRequester> requesters = new ArrayList<>();
        for (String stockName: stocks){
            requesters.add(new ApiRequester(stockName));
        }

        // creating series for stocks
        ArrayList<XYChart.Series<String, Number>> stocksSeries = new ArrayList<>();
        for (String stockName: stocks){
            XYChart.Series<String, Number> series = new XYChart.Series<>();
            series.setName(stockName);
            stocksSeries.add(series);
        }

        // real-life updates every five seconds
        Timer timer = new Timer();
        TimerTask task = new TimerTask() {
            @Override
            public void run(){
                final SimpleDateFormat simpleDateFormat = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss");
                Date now = new Date();
                Platform.runLater(() -> {
                    for (int i = 0; i<stocksSeries.size(); i++){
                        double price = 0;
                        // double price = ThreadLocalRandom.current().nextInt(10);
                        try {
                            price = requesters.get(i).getStockRealPrice();
                        } catch (IOException e) {
                            // TODO Auto-generated catch block
                            e.printStackTrace();
                        } catch (InterruptedException e) {
                            // TODO Auto-generated catch block
                            e.printStackTrace();
                        }
                        // System.out.printf("Stock: %s, price %f\n", stocks.get(i), price);
                        XYChart.Series<String, Number> series = stocksSeries.get(i);
                        series.getData().add(new XYChart.Data<>(simpleDateFormat.format(now), price));
                        if (series.getData().size() > WINDOW_SIZE)
                            series.getData().remove(0);
                    }
                });
            }
        };
        timer.scheduleAtFixedRate(task, 0, 5000);


        Scene scene = new Scene(lineChart,800,600);
        for (XYChart.Series<String, Number> series: stocksSeries){
            lineChart.getData().add(series);
        }

        stage.setScene(scene);
        stage.show();
    }
 
    public static void main(String[] args) {
        launch(args);
    }
}