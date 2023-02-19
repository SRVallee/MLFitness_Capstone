package com.example.application;

import android.media.Image;

public class User {

    private int id;
    private String name;
    private String email;
    private int trainerId = -1;
    private int traineeId = -1;
    private Image pfp;

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

    public int getTraineeId() {
        return traineeId;
    }

    public int getTrainerId() {
        return trainerId;
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

    public void setName(String name) {
        this.name = name;
    }

    public void setTraineeId(int traineeId) {
        this.traineeId = traineeId;
    }

    public void setTrainerId(int trainerId) {
        this.trainerId = trainerId;
    }

    public boolean isTrainer(){
        return (trainerId != -1);
    }

    public Image getPfp() {
        return pfp;
    }

    public void setPfp(Image pfp) {
        this.pfp = pfp;
    }
}
