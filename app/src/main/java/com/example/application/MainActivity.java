package com.example.application;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.SwitchCompat;

import android.app.ActivityOptions;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import java.util.Timer;
import java.util.TimerTask;

public class MainActivity extends AppCompatActivity {

    Timer timer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //Currently just a title screen that auto transitions to the welcome screen

        //NOTE will add an if else statement that checks if the user has inputted their credits
        //before and if that is the case then will go to their respective home screen and not
        //require them to re enter their info

        timer = new Timer();
        timer.schedule(new TimerTask() {
            @Override
            public void run() {
                    Intent intent = new Intent(MainActivity.this, WelcomeScreen.class);
                    startActivity(intent);
                    finish();
            }
        }, 3000);
    }
}