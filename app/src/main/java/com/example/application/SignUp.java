package com.example.application;

import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import com.google.android.material.chip.Chip;

public class SignUp extends AppCompatActivity {

    String username, name, email, passwordOne, passwordTwo;
    EditText usernameSignup, nameSignup, emailSignup, passwordOneSignup, passwordTwoSignup;

    boolean isTrainee, isTrainer;
    Chip traineeChipSignup, trainerChipSignup;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup);

        //Init fields in xml
        usernameSignup = findViewById(R.id.userNameSignUpEditText);
        nameSignup = findViewById(R.id.nameSignUpEditText);
        emailSignup = findViewById(R.id.emailEditText);
        passwordOneSignup = findViewById(R.id.passwordEditText);
        passwordOneSignup.setTransformationMethod(new AsteriskPasswordTransformationMethod());
        passwordTwoSignup = findViewById(R.id.passwordReEditText);
        passwordTwoSignup.setTransformationMethod(new AsteriskPasswordTransformationMethod());

        traineeChipSignup = findViewById(R.id.traineeChip);
        trainerChipSignup = findViewById(R.id.trainerChip);

    }

    /***
     * Attempts to signup using the user inputted data
     * ***/
    public void attemptSignUp (View view) {

        //Check fields have input
        AlertDialog alertDialog = new AlertDialog.Builder(this).create();
        alertDialog.setButton(AlertDialog.BUTTON_NEUTRAL, "OK",
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                    }
                });

        //Check username input
        username = usernameSignup.getText().toString();
        if(username.isEmpty()){
            alertDialog.setTitle("No Username");
            alertDialog.setMessage("Username is required");
            alertDialog.show();
            return;
        }

        //Check name input
        name = nameSignup.getText().toString();
        if(name.isEmpty()){
            alertDialog.setTitle("No Name");
            alertDialog.setMessage("Name is required");
            alertDialog.show();
            return;
        }

        //Check email input is entered and valid
        email = emailSignup.getText().toString();
        if(email.isEmpty()){
            alertDialog.setTitle("No Email");
            alertDialog.setMessage("Email is Required");
            alertDialog.show();
            return;
        }
        if(!email.isEmpty() && !emailIsValid(email)){
            alertDialog.setTitle("Invalid email: " + email);
            alertDialog.setMessage("Please enter a valid email");
            alertDialog.show();
            return;
        }

        //Check password one input
        passwordOne = passwordOneSignup.getText().toString();
        if(passwordOne.isEmpty()){
            alertDialog.setTitle("Error with password");
            alertDialog.setMessage("Password is required");
            alertDialog.show();
            return;
        }

        //Check password two input
        passwordTwo = passwordTwoSignup.getText().toString();
        if(passwordTwo.isEmpty()){
            alertDialog.setTitle("Error with password");
            alertDialog.setMessage("Password is required");
            alertDialog.show();
            return;
        }

        //Check if passwords are the same
        if(!passwordOne.equals(passwordTwo)){
            //Passwords different
            alertDialog.setTitle("Error with password");
            alertDialog.setMessage("Passwords are different");
            alertDialog.show();
            return;
        }

        //Get role selected
        isTrainee = traineeChipSignup.isChecked();
        isTrainer = trainerChipSignup.isChecked();

        Intent i;

        if (isTrainee) {
            //User has entered all inputs and has indicated to signup as trainee
            //makeUser(username, name, email, passwordOne, isTrainer);
            i = new Intent(getApplicationContext(), TraineeHomePage.class);
            startActivity(i);
            this.finish();
        }
        if (isTrainer) {
            //User has entered all inputs and has indicated to signup as trainee
            //makeUser(username, name, email, passwordOne, isTrainer);
            i = new Intent(getApplicationContext(), TrainerHomePage.class);
            startActivity(i);
            this.finish();
        }
        if (!isTrainee && !isTrainer) {
            //Non selected
            alertDialog.setTitle("No role selected");
            alertDialog.setMessage("Selected desired role");
            alertDialog.show();
            return;
        }
    }

    private boolean emailIsValid(String email){
        return (email.matches("([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\\.[a-zA-Z0-9_-]+)"));
    }
}