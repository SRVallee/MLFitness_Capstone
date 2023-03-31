package com.example.application;

import android.graphics.Bitmap;
import android.media.Image;

import androidx.appcompat.app.AppCompatActivity;

import java.io.Serializable;

public class User extends AppCompatActivity implements Serializable {


    private int id;
    private String userName;
    private String name;
    private String email;
    private Bitmap pfp;
    private Boolean isTrainer = false;

    public User(){
        this(-1,null,null,null);
    }

    public User(int id, String userName, String name, String email ) {


        this.id = id;
        this.userName = userName;
        this.name = name;
        this.email = email;
    }

    public int getId() {
        return id;
    }

    public String getUserName() {
        return userName;
    }

    public String getEmail() {
        return email;
    }

    public String getName() {
        return name;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setUserName(String userName) {
        userName = userName;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Bitmap getPfp() {
        return pfp;
    }

    public void setPfp(Bitmap pfp) {
        this.pfp = pfp;
    }

    public boolean isTrainer(){
        return isTrainer;
    }

    public void setTrainer(Boolean trainer) {
        isTrainer = trainer;
    }

    public boolean hasPfp() {
        return (pfp != null);
    }
}
