package com.example.application;

import android.content.Intent;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;
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
import com.sendbird.android.shadow.com.google.gson.annotations.SerializedName;

import org.apache.commons.io.IOUtils;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Retrofit;
import retrofit2.converter.scalars.ScalarsConverterFactory;

public class TraineeWorkoutFeedback extends AppCompatActivity {

    private static final String BASE_URL = "http://162.246.157.128/MLFitness/";
    private TextView workoutTitle, reviewerName, feedback;
    private VideoView videoFeedback;
    private Spinner workoutSelect;

    private int workoutID;
    private ArrayList<Workout> workouts = new ArrayList<>();

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.workout_feedback);

        Intent intent = getIntent();
        Bundle bundle = intent.getExtras();
        if (bundle!=null){
            workoutID = (int) bundle.get("workout_id");
        }

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
                            int index = 0;
                            for (int i = 0; i < workouts.size(); i++) {
                                if (workouts.get(i).getWorkout_id() == workoutID){
                                    index = i;
                                    break;
                                }
                            }
                            workoutSelect.setSelection(index);
                            workoutSelect.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() { // Listener for exercise
                                @Override
                                public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                                    getFeedBack(((Workout) workoutSelect.getSelectedItem()).getWorkout_id());
                                    getVideo(((Workout) workoutSelect.getSelectedItem()).getWorkout_id());
                                }

                                @Override
                                public void onNothingSelected(AdapterView<?> adapterView) {

                                }
                            });

                        }

                        getVideo(((Workout) workoutSelect.getSelectedItem()).getWorkout_id());

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

    private void getVideo(int workout_id){ //I know anyone with the link can see the video, but I couldn't make it work
        int workoutId = ((Workout) workoutSelect.getSelectedItem()).getWorkout_id();
        int userId = ((Workout) workoutSelect.getSelectedItem()).getUser_id();
        String exerciseName = ((Workout) workoutSelect.getSelectedItem()).getExercise_name();
        String videoUrl = BASE_URL + "PostProcessedVideos/Users/"+ userId +"/"+exerciseName+"/"+workoutId+".mp4";

        Uri videoUri = Uri.parse(videoUrl);

        videoFeedback.stopPlayback();

        videoFeedback.setZOrderOnTop(true);
        videoFeedback.setVideoURI(videoUri);

        videoFeedback.start();

        // loop video
        videoFeedback.setOnCompletionListener(mp -> videoFeedback.start());
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
