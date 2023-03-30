package com.example.application;

import android.graphics.Bitmap;
import android.media.Image;

import androidx.appcompat.app.AppCompatActivity;

public class User extends AppCompatActivity {

    private int id;
    private String UserName;
    private String name;
    private String email;
    private Bitmap pfp;
    private Boolean isTrainer = false;

    public User(){
        this(-1);
    }

    public User(int id) {

        name = "Unnamed";
        this.id = id;
    }

    public int getId() {
        return id;
    }

    public String getUserName() {
        return UserName;
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
        UserName = userName;
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
