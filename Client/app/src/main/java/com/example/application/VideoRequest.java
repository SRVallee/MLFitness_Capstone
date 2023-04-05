package com.example.application;

import com.sendbird.android.shadow.com.google.gson.annotations.SerializedName;

public class VideoRequest {
    @SerializedName("apiKey")
    private String authToken;

    @SerializedName("id")
    private int userId;

    @SerializedName("exercise_id")
    private int exercise_id;

    @SerializedName("workout_id")
    private int workout_id;

    // Constructor
    public VideoRequest(String authToken, int userId) {
        this.authToken = authToken;
        this.userId = userId;
    }

    public void setWorkout_id(int workout_id) {
        this.workout_id = workout_id;
    }

    public void setExercise_id(int exercise_id) {
        this.exercise_id = exercise_id;
    }
}
