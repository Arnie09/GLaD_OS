package com.example.glad_os;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

public class DatabaseHandler extends SQLiteOpenHelper {

    public static final String DATABASE_NAME = "User_commands.db";
    public static final String TABLE_NAME = "Commands";
    public static final String COLUMN_1 = "SERIAL";
    public static final String COLUMN_2 = "Message";
    public static final String COLUMN_3 = "Time";

    public DatabaseHandler(Context context) {
        super(context, DATABASE_NAME, null, 1);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL("CREATE TABLE "+TABLE_NAME+" (SERIAL INTEGER PRIMARY KEY AUTOINCREMENT,Message TEXT,Time TEXT)");
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS "+TABLE_NAME);
        onCreate(db);
    }

    public long insertData(String message,String time){
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues contentValues = new ContentValues();
        contentValues.put(COLUMN_2,message);
        contentValues.put(COLUMN_3,time);

        long result = db.insert(TABLE_NAME,null,contentValues);
        if(result == -1)
           return -1;
        else
            return result;
    }

    public Cursor getallData(){
        SQLiteDatabase db = this.getWritableDatabase();
        Cursor res = db.rawQuery("SELECT * FROM "+TABLE_NAME,null);
        return res;
    }

    public Integer deleteData(String id){
        SQLiteDatabase db = this.getWritableDatabase();
        return db.delete(TABLE_NAME,"SERIAL = ?",new String[]{id});
    }
}

