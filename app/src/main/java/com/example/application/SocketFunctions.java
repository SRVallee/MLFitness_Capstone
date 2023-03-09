package com.example.application;
import static androidx.core.content.ContextCompat.startActivity;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.util.Base64;
import android.util.Log;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.util.HashMap;
import java.util.Map;

public class SocketFunctions {
    private String ServerIP;
    private String Port;
    private String username;
    private String name;
    private String email;
    private String password;
    private boolean isTrainer;

    static public User user = new User();
    static public String apiKey = null;

    /**
     * Used for login. This will only be called if there is both user inputted username and
     * password. Returns a boolean based on if the username and password are valid.
     * Parameters:
     *  - username (String): username that the user inputted
     *  - password (String): password that the user inputted
     * Returns:
     *  - boolean where true if the username and password are valid, and returns false if the
     *    inputs don't match what is present in the database
     * **/
    //verifyLogin(String username,String password)

    /**
     *  Used for login. This will only be called if the user is verified. Given a valid username
     *  returns a boolean if the user is a trainer!
     * Parameters:
     *  - username (String): username that is user inputted
     * Returns:
     *  - boolean where true if the user is a trainer, and returns false if the user is not a
     *    trainer
     * **/
    //userIsTrainer(String username)

    /**
     * Used for signup. Expects valid info
     * Parameters:
     * - username (String):
     * - name (String):
     * - email (String):
     * - password (String):
     * - isTrainer (boolean):
     * Returns:
     * -
     **/
//    public static User makeUser(Context context, String username, String name, String email, String password, boolean isTrainer) {
//        RequestQueue queue = Volley.newRequestQueue(context);
//        String url = "https://192.168.56.1/ml_fitness"; //local network for now
//
//
//        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
//                new Response.Listener<String>() {
//                    @Override
//                    public void onResponse(String response) {
//                        if (!response.equals("Connection to database failed")) { //or email already exists if when implemented
//                            user.setId(Integer.parseInt(response));
//                            user.setEmail(email);
//                            user.setName(name);
//                            user.setTrainer(isTrainer);
//                            Log.d("User id: ", "was returned");
//                            Intent i;
//                            if (!isTrainer) {
//                                //User has entered all inputs and has indicated to signup as trainee
//                                i = new Intent(context, TraineeHomePage.class);
//                                startActivity(i);
//                                SignUp.finish();
//                            }
//                            if (isTrainer) {
//                                //User has entered all inputs and has indicated to signup as trainee
//                                //makeUser(username, name, email, passwordOne, isTrainer);
//                                i = new Intent(getApplicationContext(), TrainerHomePage.class);
//                                startActivity(i);
//                                this.finish();
//                        }
//                        else{
//                            Log.d("User id: ", "was not returned");
//                        }
//                    }
//                }, new Response.ErrorListener() {
//            @Override
//            public void onErrorResponse(VolleyError error) {
//                Log.d("User id: ", "Error!!!");
//            }
//        }) {
//            protected Map<String, String> getParams() {
//                Map<String, String> paramV = new HashMap<>();
//                paramV.put("username", username);
//                paramV.put("name", name);
//                paramV.put("email", email);
//                paramV.put("password", password);
//                paramV.put("is_trainer", String.valueOf(isTrainer));
//                return paramV;
//            }
//        };
//        queue.add(stringRequest);
//        Log.d("User id: ", "returning user");
//        return user;
//
//    }

    public static void uploadPfp(Context context, Bitmap pfp){
        Log.d("uploadPfp ", "initiated");
        ByteArrayOutputStream byteArrayOutputStream;
        byteArrayOutputStream = new ByteArrayOutputStream();
        Log.d("uploadPfp ", "checking w if pfp is null");
        if(pfp != null){
            pfp.compress(Bitmap.CompressFormat.JPEG, 100, byteArrayOutputStream);
            byte[] bytes = byteArrayOutputStream.toByteArray();
            final String image = Base64.encodeToString(bytes, Base64.DEFAULT);
            Log.d("uploadPfp ", "Ready to send");
            RequestQueue queue = Volley.newRequestQueue(context);
            String url = "http://162.246.157.128/MLFitness/upload_pfp.php";
            StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                    new Response.Listener<String>() {
                        @Override
                        public void onResponse(String response){
                            Log.d("Response: ", response);
                        }
                    }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {
                    Log.d("User id: ", error.getLocalizedMessage());
                }
            }) {
                protected Map<String, String> getParams() {
                    Map<String, String> paramV = new HashMap<>();
                    paramV.put("id", String.valueOf(user.getId()));
                    paramV.put("apiKey", apiKey);
                    paramV.put("image", image);
                    return paramV;
                }
            };
            queue.add(stringRequest);
        }else{
            Log.d("User id: ", "pfp missing");
        }
    }
}

