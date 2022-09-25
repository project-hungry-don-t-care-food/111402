package com.example.connectiontosql

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Toast
import kotlinx.android.synthetic.main.activity_main.*
import java.sql.*

class MainActivity : AppCompatActivity() {
    lateinit var connection : Connection
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        button.setOnClickListener {
            var list = mutableListOf<String>()
            try {
                val c : ConSQL = ConSQL()
                connection = c.conclass()
                var sqlstatement : String = "SELECT store_name FROM store_info"
                var smt : Statement = connection.createStatement()
                var set : ResultSet = smt.executeQuery(sqlstatement)
                while (set.next()){
                    textView.text = set.getString(1)
                    list+=set.getString(1)
                }
                connection.close()
            }catch (e : Exception){
                textView.text = e.toString()
            }

            Toast.makeText(this,list.toString(),Toast.LENGTH_LONG).show()
        }

        button2.setOnClickListener {
            try {
                val c : ConSQL = ConSQL()
                connection = c.conclass()
                var sqlstatement : String = "Insert Into restaurant_list (id, 餐廳名稱, 餐廳評價, 餐廳地址, 餐廳連結)Values (9999, 'A', 5.0, 'AA', 'AAA')"
                var smt : Statement = connection.createStatement()
                var set : Int = smt.executeUpdate(sqlstatement)
                textView.text = set.toString()

                connection.close()
            }catch (e : Exception){
                textView.text = e.toString()
            }
        }

        button3.setOnClickListener {
            try {
                val c : ConSQL = ConSQL()
                connection = c.conclass()
                var sqlstatement : String = "UPDATE restaurant_list SET 餐廳名稱= 'B' WHERE id = 9999;"
                var smt : Statement = connection.createStatement()
                var set : Int = smt.executeUpdate(sqlstatement)
                textView.text = set.toString()

                connection.close()
            }catch (e : Exception){
                textView.text = e.toString()
            }
        }

        button4.setOnClickListener {
            try {
                val c : ConSQL = ConSQL()
                connection = c.conclass()
                var sqlstatement : String = "Delete from restaurant_list"
                var smt : Statement = connection.createStatement()
                var set : Int = smt.executeUpdate(sqlstatement)
                textView.text = set.toString()

                connection.close()
            }catch (e : Exception){
                textView.text = e.toString()
            }
        }
    }
}