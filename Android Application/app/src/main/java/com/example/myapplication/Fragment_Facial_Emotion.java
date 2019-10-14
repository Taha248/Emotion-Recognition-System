package com.example.myapplication;

import android.content.Context;
import android.net.Uri;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import org.w3c.dom.Text;


public class Fragment_Facial_Emotion extends Fragment {
    LayoutInflater inflater;
    String emotion;
    int emoji;
    // TODO: Rename parameter arguments, choose names that match
    public Fragment_Facial_Emotion(String emotion,int emoji) {
        // Required empty public constructor
        this.emotion= emotion;
        this.emoji = emoji;
    }



    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        this.inflater= inflater;
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_fragment__facial__emotion, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        TextView textView = (TextView) view.findViewById(R.id.txtEmotion);
        ImageView imageView = (ImageView) view.findViewById(R.id.imgEmotion);
        textView.setText(emotion);
        imageView.setImageResource(emoji);
        super.onViewCreated(view, savedInstanceState);
    }



}
