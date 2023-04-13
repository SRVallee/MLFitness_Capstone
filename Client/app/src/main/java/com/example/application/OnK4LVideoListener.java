package com.example.application;

public interface OnK4LVideoListener {
    void onTrimStarted();

    void onError(String message);

    void onVideoPrepared();
}