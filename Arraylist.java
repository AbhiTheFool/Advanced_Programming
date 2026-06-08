// Name - Abhishek Verma
// Roll No. - CSB24072

import java.util.ArrayList;
import java.util.Scanner;

public class BookSearch {
    public static void main(String[] args) {

        ArrayList<String> books = new ArrayList<String>();

        books.add("Lord of the Mysteries");
        books.add("Reverend Insanity");
        books.add("Shadow Slave");
        books.add("Omniscient Reader");
        books.add("The Beginning After The End");

        Scanner sc = new Scanner(System.in);
        System.out.print("Enter word to search: ");
        String word = sc.nextLine();

        System.out.println("Matching books:");

        for (int i = 0; i < books.size(); i++) {
            String title = books.get(i);

            if (title.toLowerCase().contains(word.toLowerCase())) {
                System.out.println(title);
            }
        }

        sc.close();
    }
}
