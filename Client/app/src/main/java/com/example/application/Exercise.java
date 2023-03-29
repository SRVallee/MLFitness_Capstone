package com.example.application;

import android.content.Context;
import android.util.Log;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class Exercise {

    int id, trainerId;
    String name, description, trainerName;


    public Exercise(Context context, int id, String name, String description, int trainer){
        this.id = id;
        this.name = name;
        this.description = description;
        this.trainerId = trainer;
        if(trainerId == -1){
            trainerName = "Public";
        }else {
            getTrainerInfo(context);
        }
    }

    public Exercise(Context context, int id, String name, String description){
        this.id = id;
        this.name = name;
        this.description = description;
        this.trainerId = -1;
        this.trainerName = "Kensee";
    }


    private void getTrainerInfo(Context context){
        RequestQueue queue = Volley.newRequestQueue(context);
        String url = "http://162.246.157.128/MLFitness/get_user_info.php";

        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        Log.d("Response: ", response.toString());
                        try {
                            JSONObject jsonResponse = new JSONObject(response);
                            String status = jsonResponse.getString("status");
                            if (status.equals("success")) {
                                Log.d("Array: ", jsonResponse.getString("exercises"));
                            }
                            trainerName = jsonResponse.getString("name");
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
                paramV.put("id", String.valueOf(SocketFunctions.user.getId()));
                paramV.put("apiKey", SocketFunctions.apiKey);
                return paramV;
            }
        };
        queue.add(stringRequest);
    }

    @Override
    public String toString() {
        return name + ": " + trainerName;
    }
}
