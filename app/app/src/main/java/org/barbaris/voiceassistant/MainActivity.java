package org.barbaris.voiceassistant;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.content.pm.PackageManager;
import android.media.MediaRecorder;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import static android.Manifest.permission.RECORD_AUDIO;
import static android.Manifest.permission.INTERNET;

import java.util.Random;

public class MainActivity extends AppCompatActivity {

    private TextView startRecBox;
    private TextView transcriptionBox;
    private MediaRecorder recorder;
    private static String filePath = null;
    private static String fileName = null;
    private boolean isRecording = false;
    public static final int REQUEST_AUDIO_PERMISSION_CODE = 1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        startRecBox = findViewById(R.id.startRecording);
        transcriptionBox = findViewById(R.id.transcription);

        startRecBox.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View V) {

                if(isRecording) {
                    isRecording = false;
                    recorder.stop();
                    recorder.release();
                    recorder = null;
                    startRecBox.setText(R.string.start_rec);

                    Request request = new Request(filePath, transcriptionBox);

                    try {
                        request.start();
                        request.join();
                    } catch (Exception ex) {
                        System.out.println(ex.getMessage());
                    }

                } else {
                    if(hasPermissions()) {
                        fileName = "/" + randomPrefix() + "record.ogg";
                        filePath = getExternalFilesDir(null).getAbsolutePath() + fileName;

                        recorder = new MediaRecorder();
                        recorder.setAudioSource(MediaRecorder.AudioSource.MIC);
                        recorder.setOutputFormat(MediaRecorder.OutputFormat.OGG);
                        recorder.setAudioEncoder(MediaRecorder.AudioEncoder.OPUS);
                        recorder.setOutputFile(filePath);

                        try {
                            recorder.prepare();
                        } catch (Exception ex) {
                            System.out.println(ex.getMessage());
                        }

                        recorder.start();
                        isRecording = true;
                        startRecBox.setText(R.string.stop_rec);
                    } else {
                        ActivityCompat.requestPermissions(MainActivity.this, new String[]{RECORD_AUDIO,  INTERNET}, REQUEST_AUDIO_PERMISSION_CODE);
                    }
                }
            }
        });
    }

    private boolean hasPermissions() {
        int b = ContextCompat.checkSelfPermission(getApplicationContext(), RECORD_AUDIO);
        int c = ContextCompat.checkSelfPermission(getApplicationContext(), INTERNET);

        return b == PackageManager.PERMISSION_GRANTED && c == PackageManager.PERMISSION_GRANTED;
    }

    private int randomPrefix() {
        Random random = new Random();
        return random.nextInt(7000);
    }



}