package com.example.application;

import static androidx.core.content.ContextCompat.startActivity;

import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.material.chip.Chip;
import com.sendbird.uikit.SendBirdUIKit;
import com.sendbird.uikit.adapter.SendBirdUIKitAdapter;
import com.sendbird.uikit.interfaces.UserInfo;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class SignUp extends AppCompatActivity {

    String USER_ID;
    String USER_NICKNAME;
    String USER_PROFILE_URL;
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
        passwordTwoSignup = findViewById(R.id.passwordReEditText);

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

        if (!isTrainee && !isTrainer) {
            //Non selected
            alertDialog.setTitle("No role selected");
            alertDialog.setMessage("Selected desired role");
            alertDialog.show();
            return;
        }

        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        String url = "http://162.246.157.128/MLFitness/register.php";

        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        try {
                            JSONObject jsonResponse = new JSONObject(response);
                            if (jsonResponse.getString("status").equals("success")) { //or email already exists if when implemented
                                //Log.d("Response: ", response);
                                SocketFunctions.user.setId(Integer.parseInt(jsonResponse.getString("user_id")));
                                SocketFunctions.user.setUserName(username);
                                SocketFunctions.user.setEmail(email);
                                SocketFunctions.user.setName(name);
                                SocketFunctions.user.setTrainer(isTrainer);
                                SocketFunctions.apiKey = jsonResponse.getString("api_key");
                                Log.d("User id: ", "was returned");
                                Intent i;
                                int tempInt = SocketFunctions.user.getId();
                                USER_ID = String.valueOf(tempInt);
                                USER_NICKNAME = SocketFunctions.user.getName();
                                //Once profile pictures are implemented change this
                                USER_PROFILE_URL = "";
                                if (isTrainer) {
                                    //User has entered all inputs and has indicated to signup as trainee
                                    //First connects to sendbird and makes account
                                    SendBirdUIKit.init(new SendBirdUIKitAdapter() {
                                        @Override
                                        public String getAppId() {
                                            return "011F57DA-BA7D-4DCF-96AC-12217F169139";  // The ID of the Sendbird application
                                        }

                                        @Override
                                        public String getAccessToken() {
                                            return "";
                                        }

                                        @Override
                                        public UserInfo getUserInfo() {
                                            return new UserInfo() {
                                                @Override
                                                public String getUserId() {
                                                    return USER_ID; // The userID of the user you wish to log in as
                                                }

                                                @Override
                                                public String getNickname() {
                                                    return USER_NICKNAME; // The nickname of the user you wish to log in as
                                                }

                                                @Override
                                                public String getProfileUrl() {
                                                    return USER_PROFILE_URL;
                                                }
                                            };
                                        }
                                    }, getApplicationContext());// If errors use this and move
                                    //Goes to homepage
                                    i = new Intent(getApplicationContext(), TrainerHomePage.class);
                                    startActivity(i);
                                    finish();
                                } else{
                                    //User has entered all inputs and has indicated to signup as trainee
                                    //First connects to sendbird and makes account
                                    SendBirdUIKit.init(new SendBirdUIKitAdapter() {
                                        @Override
                                        public String getAppId() {
                                            return "011F57DA-BA7D-4DCF-96AC-12217F169139";  // The ID of the Sendbird application
                                        }

                                        @Override
                                        public String getAccessToken() {
                                            return "";
                                        }

                                        @Override
                                        public UserInfo getUserInfo() {
                                            return new UserInfo() {
                                                @Override
                                                public String getUserId() {
                                                    return USER_ID; // The userID of the user you wish to log in as
                                                }

                                                @Override
                                                public String getNickname() {
                                                    return USER_NICKNAME; // The nickname of the user you wish to log in as
                                                }

                                                @Override
                                                public String getProfileUrl() {
                                                    return USER_PROFILE_URL;
                                                }
                                            };
                                        }
                                    }, getApplicationContext());// If errors use this and move
                                    //Goes to homepage
                                    i = new Intent(getApplicationContext(), TraineeHomePage.class);
                                    startActivity(i);
                                    finish();
                                }
                            }
                            else{
                                alertDialog.setTitle("Error!");
                                alertDialog.setMessage(jsonResponse.getString("status"));
                                alertDialog.show();
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                    }, new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {
                            Log.d("User id: ", error.getLocalizedMessage());
                        }
                    }) {
                        protected Map<String, String> getParams() {
                            Map<String, String> paramV = new HashMap<>();
                            paramV.put("username", username);
                            paramV.put("name", name);
                            paramV.put("email", email);
                            paramV.put("password", passwordOne);
                            if(isTrainer) {
                                paramV.put("isTrainer", "1");
                            }else{
                                paramV.put("isTrainer", "0");
                            }
                            return paramV;
                        }
        };
        queue.add(stringRequest);

    }

    private boolean emailIsValid(String email){
        return (email.matches("([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\\.[a-zA-Z0-9_-]+)"));
    }
}