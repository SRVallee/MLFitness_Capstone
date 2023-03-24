package com.example.application;

import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;

public interface ApiService {
    @Multipart
    @POST("upload_video.php")
    Call<String> uploadVideo(@Part("video\"; filename=\"video.mp4\"") RequestBody video,
                             @Part("id") String id,
                             @Part("apiKey") String apiKey,
                             @Part("trainer_id") String trainerId);
}