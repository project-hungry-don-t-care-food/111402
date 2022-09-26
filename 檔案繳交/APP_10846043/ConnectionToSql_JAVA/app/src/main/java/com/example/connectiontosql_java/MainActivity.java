package com.example.connectiontosql_java;

import androidx.appcompat.app.AppCompatActivity;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.sql.Blob;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    TextView textview;
    ImageView imageView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textview = findViewById(R.id.textView);
        imageView = findViewById(R.id.imageView);

        List<String> names = new ArrayList<String>();
        Connection connection;
        try {
            ConSQL c = new ConSQL();
            connection = c.conclass();
            String sqlstatement = "SELECT store_name FROM store_info";
            Statement smt = connection.createStatement();
            ResultSet set = smt.executeQuery(sqlstatement);
            while (set.next()){
                //names.add(set.getString(1));
            }
            textview.setText(names.toString());

            connection.close();
        }catch (Exception e){
            Log.d("SqlCon1",e.toString());
        }

        try {
            ConSQL c = new ConSQL();
            connection = c.conclass();
            String sqlstatement = "SELECT image FROM store_image where store_info_id = 155";
            Statement smt = connection.createStatement();
            ResultSet set = smt.executeQuery(sqlstatement);
            while (set.next()){
                //names.add(set.getString(1));
                String image = set.getString(1);

                byte[] bytes = Base64.decode(image,Base64.NO_CLOSE);
                Bitmap bitmap = BitmapFactory.decodeByteArray(bytes,0,bytes.length);


                imageView.setImageBitmap(bitmap);
                Toast.makeText(this,"Finish",Toast.LENGTH_LONG).show();
            }
            textview.setText(names.toString());

            connection.close();
        }catch (Exception e){
            Log.d("SqlCon1",e.toString());
        }

    }
}