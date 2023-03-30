package com.example.application;

import android.content.Intent;

import java.io.Serializable;

//have id, credentials, rating, username, name ,email
public class ObjectTrainer implements Serializable {

    private String credentials;
    private Integer id;
    private String Trainer_username;
    private String Trainer_name;
    private String Trainer_email;
    private float rating;


    public ObjectTrainer(int id, String credentials, float rating, String username, String name, String email) {

        this.id = id;
        this.credentials = credentials;
        this.rating = rating;
        this.Trainer_username = username;
        this.Trainer_name = name;
        this.Trainer_email = email;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }
    public String getTrainer_username() {
        return Trainer_username;
    }

    public void setTrainer_username(String trainer_username) {
        Trainer_username = trainer_username;
    }

    public String getTrainer_name() {
        return Trainer_name;
    }

    public void setTrainer_name(String trainer_name) {
        Trainer_name = trainer_name;
    }

    public String getTrainer_email() {
        return Trainer_email;
    }

    public void setTrainer_email(String trainer_email) {
        Trainer_email = trainer_email;
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
