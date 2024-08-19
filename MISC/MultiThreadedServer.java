import java.io.*;
import java.net.*;
import java.util.concurrent.*;

public class MultiThreadedServer {

    private static final int PORT = 49153;

    public static void main(String[] args) {
        ExecutorService threadPool = Executors.newCachedThreadPool();
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("Server now listening on port: " + PORT);
            while (true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println(
                    "Accepted connection from " +
                    clientSocket.getInetAddress().getHostAddress() +
                    ":" +
                    clientSocket.getPort()
                );
                threadPool.execute(new ClientHandler(clientSocket));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

class ClientHandler implements Runnable {

    private final Socket clientSocket;

    public ClientHandler(Socket socket) {
        this.clientSocket = socket;
    }

    @Override
    public void run() {
        System.out.println("Inside thread " + Thread.currentThread().getName());
        try (
            BufferedReader in = new BufferedReader(
                new InputStreamReader(clientSocket.getInputStream())
            );
            PrintWriter out = new PrintWriter(
                clientSocket.getOutputStream(),
                true
            )
        ) {
            String data;
            while ((data = in.readLine()) != null) {
                System.out.println("Received: " + data);
                if (data.trim().equalsIgnoreCase("quit")) {
                    out.println("closed");
                    break;
                }
                String response = new StringBuilder(data).reverse().toString();
                out.println(response);
                System.out.println("Sent: " + response);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                clientSocket.close();
                System.out.println("Connection to client closed");
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
