package com.example.application;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.SwitchCompat;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity implements View.OnClickListener{

    //TEMP STUFF JUST TO TEST AND WORK ON BOTH ROLES UI
    Button button1, button2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        button1 = (Button) findViewById(R.id.tempTraineeHomePage);
        button1.setOnClickListener(MainActivity.this);

        button2 = (Button) findViewById(R.id.tempTrainerHomePage);
        button2.setOnClickListener(MainActivity.this);

    }

    @Override
    public void onClick(View v) {

        Intent i;

        switch (v.getId()) {
            case R.id.tempTraineeHomePage:
                i = new Intent(getApplicationContext(), TraineeHomePage.class);
                startActivity(i);
                break;
            case R.id.tempTrainerHomePage:
                i = new Intent(getApplicationContext(), TrainerHomePage.class);
                startActivity(i);
                break;

            default:
                break;
        }
    }
}