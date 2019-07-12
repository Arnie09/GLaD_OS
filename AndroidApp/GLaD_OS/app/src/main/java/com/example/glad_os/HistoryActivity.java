package com.example.glad_os;

import android.database.Cursor;
import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.BaseAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import java.util.ArrayList;


public class HistoryActivity extends AppCompatActivity {

    ArrayList<String> messagelist;
    ArrayList<String> datetime;
    ArrayList<Integer> id;
    MyCustomAdapter customAdapter;
    ListView listView;
    View previous_view;
    int ID_TO_BE_DELETED = -1;
    View currentselectedrow;
    DatabaseHandler databaseHandler;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_history);

        Toolbar toolbar = findViewById(R.id.toolbar_history);
        setSupportActionBar(toolbar);
        getSupportActionBar().setDisplayShowTitleEnabled(false);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        listView = findViewById(R.id.ListView);
        databaseHandler = new DatabaseHandler(this);

        refreshListView();

        listView.setOnItemLongClickListener(new AdapterView.OnItemLongClickListener() {
            @Override
            public boolean onItemLongClick(AdapterView<?> parent, View view, int position, long idno) {
                ID_TO_BE_DELETED = id.get(position);
                currentselectedrow = view;
                highlightCurrentRow(currentselectedrow);
                return false;
            }
        });
    }
    private  void refreshListView(){
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

    private void highlightCurrentRow(View currentselectedview) {
        if(previous_view == null) {
            currentselectedview.setBackgroundColor(Color.GRAY);
            previous_view = currentselectedview;
        }
        else{
            previous_view.setBackgroundColor(Color.parseColor("#00000000"));
            currentselectedview.setBackgroundColor(Color.GRAY);
            previous_view = currentselectedview;
        }
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater menuInflater = getMenuInflater();
        menuInflater.inflate(R.menu.history_options_menu,menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        if(id == R.id.action_delete){
            //delete database entry
            Integer res = databaseHandler.deleteData(String.valueOf(ID_TO_BE_DELETED));
            if (res != 0) {
                refreshListView();
                Toast.makeText(this, "Item Deleted", Toast.LENGTH_SHORT).show();
                ID_TO_BE_DELETED = -1;
            } else {
                refreshListView();
                Toast.makeText(this, "Select something before trying to delete", Toast.LENGTH_LONG).show();
            }
        }
        return super.onOptionsItemSelected(item);
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
