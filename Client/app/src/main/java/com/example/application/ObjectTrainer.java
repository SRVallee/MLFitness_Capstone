package com.example.application;

import java.io.Serializable;

//have id, credentials, rating, username, name ,email
public class ObjectTrainer extends User implements Serializable {

    private String credentials;

    private float rating;


    public ObjectTrainer(int id, String credentials, float rating, String username, String name, String email) {
        super(id);
        super.setName(name);
        super.setUserName(username);
        super.setEmail(email);
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
