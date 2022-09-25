package com.example.connectiontosql_java;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    TextView textview;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Connection connection;
        textview = findViewById(R.id.textView);
        List<String> names = new ArrayList<String>();
        try {
            ConSQL c = new ConSQL();
            connection = c.conclass();
            String sqlstatement = "SELECT store_name FROM store_info";
            Statement smt = connection.createStatement();
            ResultSet set = smt.executeQuery(sqlstatement);
            while (set.next()){
                names.add(set.getString(1));
            }
            textview.setText(names.toString());

            connection.close();
        }catch (Exception e){
            Log.d("SqlCon1",e.toString());
        }


    }
}