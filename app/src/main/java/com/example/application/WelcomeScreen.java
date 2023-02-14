package com.example.application;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

public class WelcomeScreen extends AppCompatActivity implements View.OnClickListener{

    Button button1, button2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_welcome_screen);

        button1 = (Button) findViewById(R.id.loginButtonWelcome);
        button1.setOnClickListener(WelcomeScreen.this);

        button2 = (Button) findViewById(R.id.signUpButtonWelcome);
        button2.setOnClickListener(WelcomeScreen.this);

    }

    @Override
    public void onClick(View v) {

        Intent i;

        switch (v.getId()) {
            //Go to login
            case R.id.loginButtonWelcome:
                i = new Intent(getApplicationContext(), Login.class);
                startActivity(i);
                break;
            //Go to signup, goes to role select first but then to signup activity
            case R.id.signUpButtonWelcome:
                i = new Intent(getApplicationContext(), SignUp.class);
                startActivity(i);
                break;
            default:
                break;
        }
    }
}
