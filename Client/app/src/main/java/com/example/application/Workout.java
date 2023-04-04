package com.example.application;

import static com.example.application.SocketFunctions.exercises;

public class Workout {
    private int workout_id;
    private int user_id;
    private int exercise_id;
    private String exercise_name;
    private float score;
    private String date;

    public Workout(int workout_id, int user_id, int exercise_id, float score, String date) {
        this.workout_id = workout_id;
        this.user_id = user_id;
        this.exercise_id = exercise_id;
        this.score = score;
        this.date = date;
    }

    public Workout(int workout_id, int user_id, String exercise_name, float score, String date) {
        this.workout_id = workout_id;
        this.user_id = user_id;
        this.exercise_name = exercise_name;
        this.score = score;
        this.date = date;
    }

    private void findExerciseName(int id){
        for (Exercise currExercise: exercises) {
            if (currExercise.getId() == id){
                this.exercise_name = currExercise.getName();
            }
        }
    }

    private void findExerciseID(String name){
        for (Exercise currExercise: exercises) {
            if (currExercise.getName().equals(name)){
                this.exercise_id = currExercise.getId();
            }
        }
    }

    public int getWorkout_id() {
        return workout_id;
    }

    public void setWorkout_id(int workout_id) {
        this.workout_id = workout_id;
    }

    public int getUser_id() {
        return user_id;
    }

    public void setUser_id(int user_id) {
        this.user_id = user_id;
    }

    public int getExercise_id() {
        return exercise_id;
    }

    public void setExercise_id(int exercise_id) {
        this.exercise_id = exercise_id;
    }

    public String getExercise_name() {
        return exercise_name;
    }

    public void setExercise_name(String exercise_name) {
        this.exercise_name = exercise_name;
    }

    public float getScore() {
        return score;
    }

    public void setScore(float score) {
        this.score = score;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }
}
