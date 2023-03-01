package com.example.application;

public class SocketFunctions {
    private String ServerIP;
    private String Port;

    public SocketFunctions(){

        /**
         * Used for login. This will only be called if there is both user inputted username and
         * password. Returns a boolean based on if the username and password are valid.
         * Parameters:
         *  - username (String): username that the user inputted
         *  - password (String): password that the user inputted
         * Returns:
         *  - boolean where true if the username and password are valid, and returns false if the
         *    inputs don't match what is present in the database
         * **/
        //verifyLogin(String username,String password)

        /**
         *  Used for login. This will only be called if the user is verified. Given a valid username
         *  returns a boolean if the user is a trainer.
         * Parameters:
         *  - username (String): username that is user inputted
         * Returns:
         *  - boolean where true if the user is a trainer, and returns false if the user is not a
         *    trainer
         * **/
        //userIsTrainer(String username)

        /**
         * Used for signup. Expects valid info
         * Parameters:
         *  - username (String):
         *  - name (String):
         *  - email (String):
         *  - password (String):
         *  - isTrainer (boolean):
         * Returns:
         *  -
         * **/
        //makeUser(String username, String name, String email, String password, boolean isTrainer)

    }
}
