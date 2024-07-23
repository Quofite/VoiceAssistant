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

public class MainActivity extends AppCompatActivity {

    private TextView startRec;
    private MediaRecorder recorder;
    private static String fileName = null;
    private boolean isRecording = false;
    public static final int REQUEST_AUDIO_PERMISSION_CODE = 1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        startRec = findViewById(R.id.startRecording);

        startRec.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View V) {

                if(isRecording) {
                    isRecording = false;
                    recorder.stop();
                    recorder.release();
                    recorder = null;
                    startRec.setText(R.string.start_rec);

                    Request request = new Request(getExternalFilesDir(null).getAbsolutePath() + "/record.ogg");

                    try {
                        request.start();
                        request.join();
                    } catch (Exception ex) {
                        System.out.println(ex.getMessage());
                    }

                } else {
                    if(hasPermissions()) {
                        fileName = getExternalFilesDir(null).getAbsolutePath() + "/record.ogg";
                        System.out.println(getExternalFilesDir(null).getAbsolutePath());

                        recorder = new MediaRecorder();
                        recorder.setAudioSource(MediaRecorder.AudioSource.MIC);
                        recorder.setOutputFormat(MediaRecorder.OutputFormat.OGG);
                        recorder.setAudioEncoder(MediaRecorder.AudioEncoder.OPUS);
                        recorder.setOutputFile(fileName);

                        try {
                            recorder.prepare();
                        } catch (Exception ex) {
                            System.out.println(ex.getMessage());
                        }

                        recorder.start();
                        isRecording = true;
                        startRec.setText(R.string.stop_rec);
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





}