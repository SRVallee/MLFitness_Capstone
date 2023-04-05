package com.example.application;

import android.content.Intent;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.VideoView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.view.GravityCompat;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class TrainerFeedback extends AppCompatActivity {

    String feedback;
    private EditText feetBack;

    private TextView workoutTitle, reviewerName;

    private VideoView videoFeedback;
    private ArrayList<Workout> workouts = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_trainer_feetback);

        workoutTitle = findViewById(R.id.feetBackTitle);
        reviewerName = findViewById(R.id.workout_feedback_by);
        feetBack = findViewById(R.id.workout_feedback_text);
        videoFeedback = findViewById(R.id.workout_video);

    }

    public void sentFeetBack(View view){
        feedback = feetBack.getText().toString();
        if (!feedback.isEmpty()){
            //feet givin
            sendFeet(feedback);
        } else {
            //no feet sadge
        }
    }

    public void sendFeet(String feedback) {

        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        String url = "http://162.246.157.128/MLFitness/get_workouts.php";

        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                response -> {
                    Log.d("Response: ", response.toString());
                    try {
                        JSONObject jsonResponse = new JSONObject(response);
                        String status = jsonResponse.getString("status");
                        if (status.equals("success")) {
                            Log.d("Feedback: ", jsonResponse.getString("feedback"));
                            JSONObject feedbackJSON = jsonResponse.getJSONObject("feedback");
                            //feedback.setText(feedbackJSON.getString("feedback"));
                            //reviewerName.setText("Feedback by ");

                        } else {
                            //feedback.setText(status);
                            //reviewerName.setText("");
                        }

                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }, error -> Log.d("User id: ", error.getLocalizedMessage())) {
            protected Map<String, String> getParams() {
                Map<String, String> paramV = new HashMap<>();
                paramV.put("id", String.valueOf(SocketFunctions.user.getId()));
                paramV.put("apiKey", SocketFunctions.apiKey);
                paramV.put("workout_id", String.valueOf(workout_id));
                paramV.put("feedback", feedback);
                return paramV;
            }
        };
        queue.add(stringRequest);

    }

    @Override
    public void onBackPressed() {
        //Go to homepage
        Intent i = new Intent(getApplicationContext(), TrainerHomePage.class);
        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
        startActivity(i);
        finish();
        super.onBackPressed();
    }
}
