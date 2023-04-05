package com.example.application;

import okhttp3.RequestBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;
import retrofit2.http.Path;
import retrofit2.http.Streaming;

public interface ApiService {
    @Multipart
    @POST("upload_video.php")
    Call<String> uploadVideo(@Part("video\"; filename=\"video.mp4\"") RequestBody video,
                             @Part("id") String id,
                             @Part("apiKey") String apiKey,
                             @Part("exercise_id") String exercise_id);

    @Multipart
    @POST("get_video.php")
    @Streaming
    Call<ResponseBody> getVideoStreamExercise(@Part("info") String info);

    @Multipart
    @POST("get_video.php")
    @Streaming
    Call<ResponseBody> getVideoStreamWorkout(@Part("info") String info);
}