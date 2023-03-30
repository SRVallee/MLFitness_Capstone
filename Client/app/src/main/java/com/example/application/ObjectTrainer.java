package com.example.application;
//have id, credentials, rating, username, name ,email
public class ObjectTrainer {
    private int id;

    private String credentials;

    private float rating;

    private String username;

    private String name;

    private String email;

    public ObjectTrainer(int id, String credentials, float rating, String username, String name, String email) {
        this.credentials = credentials;
        this.rating = rating;
    }


    public String getCredentials() {
        return credentials;
    }

    public void setCredentials(String credentials) {
        this.credentials = credentials;
    }

    public float getRating() {
        return rating;
    }

    public void setRating(float rating) {
        this.rating = rating;
    }

}
