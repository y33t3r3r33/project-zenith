import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.json.gson.GsonFactory;
import com.google.api.services.customsearch.CustomSearchAPI;
import com.google.api.services.customsearch.CustomSearchAPIRequest;
import com.google.api.services.customsearch.model.Result;
import com.google.api.services.customsearch.model.Search;

import java.io.IOException;
import java.util.Scanner;

public class Chatbot {

    private CustomSearchAPI customSearchAPI;

    public Chatbot(String apiKey, String searchEngineId) throws Exception {
        GsonFactory gsonFactory = GsonFactory.getDefaultInstance();
        customSearchAPI = new CustomSearchAPI(GoogleNetHttpTransport.newTrustedTransport(), gsonFactory, request -> request);
        customSearchAPI.setApplicationName("Chatbot");
        customSearchAPI.setKey(apiKey);
        customSearchAPI.setCx(searchEngineId);
    }

    public String respond(String input) {
        try {
            CustomSearchAPIRequest request = customSearchAPI.cse().list(input);
            Search search = request.execute();
            for (Result result : search.getItems()) {
                return result.getTitle() + ": " + result.getLink();
            }
        } catch (IOException e) {
            return "Error: " + e.getMessage();
        }
        return "No results found.";
    }

    public void start() {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Welcome to the chatbot! Type 'exit' to quit.");

        while (true) {
            System.out.print("You: ");
            String input = scanner.nextLine();

            if (input.equalsIgnoreCase("exit")) {
                System.out.println("Chatbot: Goodbye!");
                break;
            }

            String response = respond(input);
            System.out.println("Chatbot: " + response);
        }

        scanner.close();
    }

    public static void main(String[] args) throws Exception {
        String apiKey = "YOUR_API_KEY"; // Replace with your API key
        String searchEngineId = "YOUR_SEARCH_ENGINE_ID"; // Replace with your search engine ID

        Chatbot chatbot = new Chatbot(apiKey, searchEngineId);
        chatbot.start();
    }
}