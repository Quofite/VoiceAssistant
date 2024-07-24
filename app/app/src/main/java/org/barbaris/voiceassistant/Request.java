package org.barbaris.voiceassistant;

import android.widget.TextView;

import org.apache.hc.client5.http.classic.HttpClient;
import org.apache.hc.client5.http.classic.methods.HttpPost;
import org.apache.hc.client5.http.entity.mime.FileBody;
import org.apache.hc.client5.http.entity.mime.MultipartEntityBuilder;
import org.apache.hc.client5.http.impl.classic.BasicHttpClientResponseHandler;
import org.apache.hc.client5.http.impl.classic.HttpClientBuilder;
import org.apache.hc.core5.http.ClassicHttpResponse;
import org.apache.hc.core5.http.HttpEntity;
import org.apache.hc.core5.http.HttpResponse;

import java.io.File;
import java.net.URL;

public class Request extends Thread {
    private String filePath = "";
    private final TextView transcriptionBox;

    public Request(String filePath, TextView transcriptionBox) {
        this.filePath = filePath;
        this.transcriptionBox = transcriptionBox;
    }

    @Override
    public void run() {
        super.run();

        try {
            URL url = new URL("http://192.168.100.4:8000/upload");
            File file = new File(filePath);
            HttpEntity entity = MultipartEntityBuilder.create().addPart("file", new FileBody(file)).build();
            HttpPost request = new HttpPost(String.valueOf(url));
            request.setEntity(entity);
            HttpClient client = HttpClientBuilder.create().build();
            HttpResponse response = client.execute(request);
            String responseBody = new BasicHttpClientResponseHandler().handleResponse((ClassicHttpResponse) response);
            responseBody = responseBody.replace("\"", "")
                                        .replace("[", "")
                                        .replace("]", "")
                                        .replace("\\n\\n", "\n\n");
            transcriptionBox.setText(responseBody);
        } catch (Exception ex) {
            System.out.println(ex.getMessage());
        }
    }
}
