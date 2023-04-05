package com.example.application;

import android.content.Intent;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.VideoView;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.view.GravityCompat;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class TraineeWorkoutFeedback extends AppCompatActivity {

    private TextView workoutTitle, reviewerName, feedback;
    private VideoView videoFeedback;
    private Spinner workoutSelect;
    private ArrayList<Workout> workouts = new ArrayList<>();

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.workout_feedback);

        workoutTitle = findViewById(R.id.workout_feedback_title);
        reviewerName = findViewById(R.id.workout_feedback_by);
        feedback = findViewById(R.id.workout_feedback_text);
        videoFeedback = findViewById(R.id.workout_video);
        workoutSelect = findViewById(R.id.workout_feedback_select);

        getWorkouts();

    }

    public void goToUpload(View view){
        Intent intent = new Intent(this, TraineeUpload.class);
        String path = Environment.getExternalStorageDirectory().getPath();
        intent.putExtra("path", path);
        startActivity(intent);
    }

    public void getWorkouts() {

        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        String url = "http://162.246.157.128/MLFitness/get_workouts.php";

        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                response -> {
                    Log.d("Response: ", response.toString());
                    try {
                        JSONObject jsonResponse = new JSONObject(response);
                        String status = jsonResponse.getString("status");
                        if (status.equals("success")) {
                            Log.d("Array: ", jsonResponse.getString("workouts"));
                            for (int i = 0; i < jsonResponse.getJSONArray("workouts").length(); i++) {
                                JSONObject workoutJSON = jsonResponse.getJSONArray("workouts").getJSONObject(i);
                                workouts.add(new Workout(workoutJSON.getInt("workout_id"),
                                        workoutJSON.getInt("user_user_id"),
                                        workoutJSON.getInt("exercise_exercise_id"),
                                        Float.parseFloat( workoutJSON.getString("score")),
                                        workoutJSON.getString("date")));
                            }
                            ArrayAdapter<Workout> adapter = new ArrayAdapter<>(this,
                                    android.R.layout.simple_spinner_item, workouts);
                            adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
                            workoutSelect.setAdapter(adapter);
                            workoutSelect.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() { // Listener for exercise
                                @Override
                                public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                                    getFeedBack(((Workout) workoutSelect.getSelectedItem()).getWorkout_id());
                                }

                                @Override
                                public void onNothingSelected(AdapterView<?> adapterView) {

                                }
                            });

                        }

                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }, error -> Log.d("User id: ", error.getLocalizedMessage())) {
            protected Map<String, String> getParams() {
                Map<String, String> paramV = new HashMap<>();
                paramV.put("id", String.valueOf(SocketFunctions.user.getId()));
                paramV.put("apiKey", SocketFunctions.apiKey);
                paramV.put("user_id", String.valueOf(SocketFunctions.user.getId()));
                return paramV;
            }
        };
        queue.add(stringRequest);

    }

    private void getFeedBack(int workout_id){
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        String url = "http://162.246.157.128/MLFitness/get_feedback.php";

        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                response -> {
                    Log.d("Response: ", response.toString());
                    try {
                        JSONObject jsonResponse = new JSONObject(response);
                        String status = jsonResponse.getString("status");
                        if (status.equals("success")) {
                            Log.d("Feedback: ", jsonResponse.getString("feedback"));
                            JSONObject feedbackJSON = jsonResponse.getJSONObject("feedback");
                            feedback.setText(feedbackJSON.getString("feedback"));
                            reviewerName.setText("Feedback by ");

                        } else {
                            feedback.setText(status);
                            reviewerName.setText("");
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
                return paramV;
            }
        };
        queue.add(stringRequest);
    }

    @Override
    public void onBackPressed() {
        //Go to homepage
        Intent i = new Intent(getApplicationContext(), TraineeHomePage.class);
        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
        startActivity(i);
        finish();
        super.onBackPressed();

    }

}
