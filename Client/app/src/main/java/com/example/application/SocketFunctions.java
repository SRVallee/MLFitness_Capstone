package com.example.application;
import android.content.Context;
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

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class SocketFunctions {

    static public User user = new User();
    static public String apiKey = null;
    static public ArrayList<Exercise> exercises = new ArrayList<>();
    static public Exercise selectedExercise;
    static public ArrayList<Relationship> relationships;

    /**
     * upload profile picture
     * @param context given context
     * @param pfp a bitmap of the image
     */
    public static void uploadPfp(Context context, Bitmap pfp){
        Log.d("uploadPfp ", "initiated");
        ByteArrayOutputStream byteArrayOutputStream;
        byteArrayOutputStream = new ByteArrayOutputStream();
        Log.d("uploadPfp ", "checking if pfp is null");
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

    public static void addExercise(Context context, JSONObject exerciseInfo) throws JSONException {
        Exercise exercise = new Exercise(context, exerciseInfo.getInt("exercise_id"),
                exerciseInfo.getString("exercise"),
                exerciseInfo.getString("notes"));

        exercises.add(exercise);
    }
}

