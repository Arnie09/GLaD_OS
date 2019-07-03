package com.example.glad_os;

import android.content.Context;
import android.content.SharedPreferences;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.os.AsyncTask;
import android.text.format.Formatter;
import android.util.Log;
import android.widget.Toast;

import java.io.DataOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.math.BigInteger;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.nio.ByteOrder;
import java.util.ArrayList;

import static android.content.Context.MODE_WORLD_WRITEABLE;
import static android.content.Context.WIFI_SERVICE;
import static android.provider.Settings.System.getString;
import static android.support.v4.content.ContextCompat.getSystemService;

public class MessageSender extends AsyncTask<String,Void,Void> {

    Socket s;
    DataOutputStream dos;
    PrintWriter pw;

    public static ArrayList<String> ipList = new ArrayList<>();


    @Override
    protected Void doInBackground(String... voids) {


        String message = voids[0];
        if(ipList.size()==0) {
            String ip_ = voids[1];
            String ip_frstPart = ip_.substring(0, ip_.lastIndexOf("."));
            String ip_lastPart = ip_.substring(ip_.lastIndexOf(".") + 1);
            Log.i("IPADDRESS", ip_frstPart);
            Log.i("IPADDRESS", ip_lastPart);
            for (int i = 1; i < 3; i++) {

                String ip = ip_frstPart + "." + String.valueOf(Integer.parseInt(ip_lastPart) + i);
                ipList.add(ip);
                ip = ip_frstPart + "." + String.valueOf(Integer.parseInt(ip_lastPart) - i);
                ipList.add(ip);
            }
        }
        for (int i = 0;i<ipList.size();i++){

            Log.i("Pinging", ipList.get(i));
            try {

                s = new Socket(ipList.get(i), 12345);
                pw = new PrintWriter(s.getOutputStream());
                pw.write(message);
                pw.flush();
                pw.close();
                s.close();
            } catch (IOException e) {
                e.printStackTrace();
                ipList.remove(i);
            }

        }

        return null;
    }
}
