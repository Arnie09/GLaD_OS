package com.example.glad_os;

import android.database.Cursor;
import android.graphics.Color;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ListView;
import android.widget.TextView;

import java.util.ArrayList;

public class HistoryActivity extends AppCompatActivity {

    ArrayList<String> messagelist;
    ArrayList<String> datetime;
    ArrayList<Integer> id;
    MyCustomAdapter customAdapter;
    ListView listView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_history);
        listView = findViewById(R.id.ListView);
        DatabaseHandler databaseHandler = new DatabaseHandler(this);
        Cursor result = databaseHandler.getallData();
        if (result.getCount() == 0) {
            Log.i("MAIN_ACTIVITY", "NO DATA");
        } else {
            id = new ArrayList<Integer>();
            messagelist = new ArrayList<String>();
            datetime = new ArrayList<String>();
            while (result.moveToNext()) {

                id.add(Integer.parseInt(result.getString(0)));
                messagelist.add(result.getString(1));
                datetime.add(result.getString(2));
            }

            customAdapter = new MyCustomAdapter();
            listView.setAdapter(customAdapter);
        }
    }
    class MyCustomAdapter extends BaseAdapter {

        @Override
        public int getCount() {
            return id.size();
        }

        @Override
        public Object getItem(int position) {
            return null;
        }

        @Override
        public long getItemId(int position) {
            return 0;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            convertView = getLayoutInflater().inflate(R.layout.list_view_layout,null);
            TextView date = convertView.findViewById(R.id.datetime);
            TextView message = convertView.findViewById(R.id.message);

            date.setText(datetime.get(position));
            date.setTextColor(Color.parseColor("#FFF0E7"));
            message.setText(messagelist.get(position));
            message.setTextColor(Color.parseColor("#FFF0E7"));
            return convertView;
        }
    }
}
