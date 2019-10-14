package com.example.myapplication;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentActivity;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;
import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Base64;
import android.view.View;
import android.widget.Button;
import org.json.JSONObject;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.util.concurrent.ExecutionException;

public class MainActivity extends AppCompatActivity {
    public Fragment fragment;
    Button btnEmotion;
    Button btnEmotionBack;
    int TAKE_PHOTO_CODE = 0;
    String img;
    public static int count = 0;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        getSupportActionBar().hide();

        Fragment fragment_homepage= new fragment_homepage();
        FragmentManager fm = getSupportFragmentManager();
        FragmentTransaction ft = fm.beginTransaction();
        ft.replace(R.id.fragment_facial_emotion,fragment_homepage);
        ft.commit();
        final String dir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES) + "/picFolder/";
        File newdir = new File(dir);
        newdir.mkdirs();

        btnEmotion = (Button) findViewById(R.id.btn_detect_emotion);
        btnEmotionBack = (Button) findViewById(R.id.btn_detect_emotion_again);
        btnEmotion.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE); //IMAGE CAPTURE CODE
                startActivityForResult(intent, 0);

            }
        });

        btnEmotionBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                fragment_homepage fragment= new fragment_homepage();
                FragmentManager fm = getSupportFragmentManager();
                FragmentTransaction ft = fm.beginTransaction();
                ft.replace(R.id.fragment_facial_emotion,fragment);
                ft.commit();
                btnEmotionBack.setVisibility(View.GONE);
                btnEmotion.setVisibility(View.VISIBLE);

            }
        });

    }
    @Override
    protected void onActivityResult(int requestCode,int resultCode,Intent data){
        super.onActivityResult(requestCode,resultCode,data);
        Bitmap bitmap=(Bitmap)data.getExtras().get("data");

        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.PNG, 100, byteArrayOutputStream);
        byte[] byteArray = byteArrayOutputStream .toByteArray();
        img = Base64.encodeToString(byteArray, Base64.DEFAULT);
        AsyncEmotionDetection_API api = new AsyncEmotionDetection_API(getBaseContext(),getSupportFragmentManager());

         JSONObject jsonObject = null;
        api.execute("http://168.211.28.6:5000/Img_Emotion/", img);
        btnEmotionBack.setVisibility(View.VISIBLE);
        btnEmotion.setVisibility(View.GONE);
        //Toast.makeText(getBaseContext(),encoded,Toast.LENGTH_LONG);
    }

}
