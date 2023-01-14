package com.example.application;

/**Trainer
 */

public class Trainer {

    private int id;
    private String name;
    private String email;

    /**
     * Create an Trainer object without a specified ID
     *
     */
    public Trainer(){

        this(-1);
    }

    /**
     * Create Trainer containing it's info.
     * @param id An integer to identify individual Trainer.
     */
    public Trainer(int id) {

        name = "Unnamed";
        this.id = id;
    }

    // The classes getter function

    /**
     *
     * @return Trainer id integer
     */
    public int getId() {

        return id;
    }

    /**
     *
     * @return Trainer name string
     */
    public String getName() {

        return name;
    }

    /**
     *
     * @return Trainer email string
     */
    public String getEmail() {

        return email;
    }

    //The classes setter function

    /**
     * Set new Trainer id
     * @param id id integer
     */
    public void setId(int id) {

        this.id = id;
    }

    /**
     * Change name of Trainer
     * @param name String containing name of Trainer
     */
    public void setName(String name) {

        this.name = name;
    }

    /**
     * Change name of Trainer
     * @param email String containing name of Trainer
     */
    public void setEmail(String email) {

        this.email = email;
    }

    //Override functions

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Trainer)) return false;
        Trainer trainer = (Trainer) o;
        return id == trainer.id;
    }
}
