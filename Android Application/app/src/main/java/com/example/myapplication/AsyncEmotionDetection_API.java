package com.example.myapplication;

import android.content.Context;
import android.opengl.Visibility;
import android.os.AsyncTask;
import android.os.Environment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;


import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.Iterator;
import java.util.List;
import java.util.Map;



public class AsyncEmotionDetection_API extends AsyncTask<String, Void, JSONObject> {
    // This is the JSON body of the post
    JSONObject postData;
    Context context;
    FragmentManager supportFragmentManager;
    // This is a constructor that allows you to pass in the JSON body
    public AsyncEmotionDetection_API(Context context, FragmentManager supportFragmentManager) {
        this.context=context;
        this.supportFragmentManager=supportFragmentManager;
    }

    // This is a function that we are overriding from AsyncTask. It takes Strings as parameters because that is what we defined for the parameters of our async task


    private String convertInputStreamToString(InputStream inputStream) {
        BufferedReader bufferedReader = new BufferedReader( new InputStreamReader(inputStream));
        StringBuilder sb = new StringBuilder();
        String line;
        try {
            while((line = bufferedReader.readLine()) != null) {
                sb.append(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return sb.toString();
    }

    @Override
    protected JSONObject doInBackground(String... str) {
        JSONObject jsonResponse=null;
        try {
            URL url = new URL(str[0]);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setDoOutput(true);
            conn.setDoInput(true);
            conn.connect();
            DataOutputStream os = new DataOutputStream(conn.getOutputStream());
            os.writeBytes("img="+URLEncoder.encode(str[1],"UTF-8"));
            Log.i("STATUS", String.valueOf(conn.getResponseCode()));

            // get response
            InputStream responseStream = new BufferedInputStream(conn.getInputStream());
            BufferedReader responseStreamReader = new BufferedReader(new InputStreamReader(responseStream));
            String line = "";
            StringBuilder stringBuilder = new StringBuilder();
            while ((line = responseStreamReader.readLine()) != null) {
                stringBuilder.append(line);
            }
            responseStreamReader.close();

            String response = stringBuilder.toString();
            jsonResponse = new JSONObject(response);

            os.flush();
            os.close();

            conn.disconnect();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        return jsonResponse;
    }

    @Override
    protected void onPostExecute(JSONObject jsonObject) {

        String txt_emotion="";
        String emotionDetected = getMaxEmotion(jsonObject);
        String emotion = emotionDetected.split(",")[0];
        double accuracy =Double.parseDouble( emotionDetected.split(",")[1]);
        int emoji= 0;

        if(emotion.equalsIgnoreCase("happy")){
            emoji= R.drawable.happy;
            txt_emotion="Happy";
        }
        else if (emotion.equalsIgnoreCase("angry")){
            emoji= R.drawable.angry;
            txt_emotion="Angry";
        }
        else if (emotion.equalsIgnoreCase("disgusted")){
            txt_emotion="Disgusted";
            emoji= R.drawable.disgusted;
        }
        else if (emotion.equalsIgnoreCase("fearful")){
            emoji= R.drawable.fearful;
            txt_emotion="Fearful";
        }
        else if (emotion.equalsIgnoreCase("sad")){
            emoji= R.drawable.sad;
            txt_emotion="Sad";
        }
        else if (emotion.equalsIgnoreCase("surprised")){
            txt_emotion="Surprised";
            emoji= R.drawable.surprised;
        }

        else if (emotion.equalsIgnoreCase("neutral")){
            txt_emotion="Neutral";
            emoji= R.drawable.neutral;
        }

        Fragment fragment= new Fragment_Facial_Emotion(txt_emotion,emoji);
        FragmentManager fm = supportFragmentManager;
        FragmentTransaction ft = fm.beginTransaction();
        ft.replace(R.id.fragment_facial_emotion,fragment);
        ft.commit();

        Toast.makeText(context,accuracy+"%",Toast.LENGTH_LONG).show();
        super.onPostExecute(jsonObject);
    }

    private String getMaxEmotion(JSONObject jsonObject) {
        double max = 0;
        String emotion ="";
        String json = jsonObject.toString();
        try {
            jsonObject = new JSONObject(json.trim());
        } catch (JSONException e) {
            e.printStackTrace();
        }
        Iterator<String> keys = jsonObject.keys();

        while(keys.hasNext()) {
            String key = keys.next();
            try {
                double value = Double.parseDouble(jsonObject.get(key).toString());
                if(value>max){
                    max=value;
                    emotion = key;
                }
                max = value>max?value:max;
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
        return emotion+","+(max);
    }
}
