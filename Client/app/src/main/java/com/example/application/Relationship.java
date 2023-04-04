package com.example.application;

import org.json.JSONException;
import org.json.JSONObject;

public class Relationship{
    int id, partnerId;
    boolean friendType;
    String startDate;


    public Relationship(JSONObject relationshipJSON) throws JSONException {
        id = relationshipJSON.getInt("relationship");
        if(relationshipJSON.getInt("user_id") == SocketFunctions.user.getId()){
            partnerId = relationshipJSON.getInt("user_id_2");
        }else{
            partnerId = relationshipJSON.getInt("user_id");
        }
        friendType = (relationshipJSON.getInt("training_relationship") == 0);
        startDate = relationshipJSON.getString("start_date");
    }

    public int getId() {
        return id;
    }

    public int getPartnerId() {
        return partnerId;
    }

    public boolean isFriendType() {
        return friendType;
    }

    public boolean isTrainerTraineeType() {
        return !friendType;
    }
}
