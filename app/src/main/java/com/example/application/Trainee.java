package com.example.application;

import android.util.Log;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Objects;

/**Trainee
 */

public class Trainee {

    private int id;
    private String name;
    private String email;
    private int trainerId;

    /**
     * Create an Trainee object without a specified ID
     *
     */
    public Trainee(){

        this(-1);
    }

    /**
     * Create Trainee containing it's info.
     * @param id An integer to identify individual Trainee.
     */
    public Trainee(int id) {

        name = "Unnamed";
        this.id = id;
    }

    // The classes getter function

    /**
     *
     * @return Trainee id integer
     */
    public int getId() {

        return id;
    }

    /**
     *
     * @return Trainee name string
     */
    public String getName() {

        return name;
    }

    /**
     *
     * @return Trainee email string
     */
    public String getEmail() {

        return email;
    }

    /**
     *
     * @return Trainee personal trainer id int
     */
    public int getPersonalTrainerId() {

        return trainerId;
    }

    //The classes setter function

    /**
     * Set new Trainee id
     * @param id id integer
     */
    public void setId(int id) {

        this.id = id;
    }

    /**
     * Change name of Trainee
     * @param name String containing name of Trainee
     */
    public void setName(String name) {

        this.name = name;
    }

    /**
     * Change name of Trainee
     * @param email String containing name of Trainee
     */
    public void setEmail(String email) {

        this.email = email;
    }

    /**
     * Change personal trainer assigned to Trainee
     * @param trainerId Trainee personal trainer id int
     */
    public void setPersonalTrainerId(int trainerId) {

        this.trainerId = trainerId;
    }

    //Override functions

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Trainee)) return false;
        Trainee trainee = (Trainee) o;
        return id == trainee.id;
    }
}