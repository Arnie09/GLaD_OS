package com.example.glad_os;

import android.Manifest;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.constraintlayout.widget.ConstraintLayout;
import androidx.core.app.ActivityCompat;
import android.text.InputType;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import androidx.core.view.GravityCompat;
import android.view.MenuItem;
import androidx.drawerlayout.widget.DrawerLayout;
import android.view.Menu;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.navigation.NavigationView;
import com.google.android.material.snackbar.Snackbar;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.EventListener;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.FirebaseFirestoreException;
import com.google.firebase.firestore.QueryDocumentSnapshot;
import com.google.firebase.firestore.QuerySnapshot;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.io.InputStream;
import java.io.UnsupportedEncodingException;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

import javax.annotation.Nullable;

public class MainActivity extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener ,RecognitionListener {

    private static final int REQUEST_RECORD_PERMISSION = 100;
    private TextView returnedText;
    private String currentPartialText;
    private String currentConfirmedText;
    private SpeechRecognizer speech = null;
    private Intent recognizerIntent;
    private String LOG_TAG = "SpeechRecognizer";
    ConstraintLayout parent_layout;
    Boolean recordButtonStatus;
    FloatingActionButton fab;
    MqttAndroidClient client;
    DatabaseHandler databaseHandler;
    TextView text_input;
    String user_id;
    FirebaseFirestore db;
    int error;
    IMqttToken token;
    public static  int no_users;
    String email;
    String password;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        fab = findViewById(R.id.fab);
        db = FirebaseFirestore.getInstance();
        fab.hide();
        parent_layout = findViewById(R.id.constraintlayout);
        parent_layout.setVisibility(View.INVISIBLE);

        error = 0;
        text_input = findViewById(R.id.inputText);


        databaseHandler = new DatabaseHandler(this);

        returnedText = (TextView) findViewById(R.id.resultText);
        recordButtonStatus = false;
        currentPartialText = "";
        currentConfirmedText = "";
        user_id = "";

        speech = SpeechRecognizer.createSpeechRecognizer(this);
        Log.i(LOG_TAG, "isRecognitionAvailable: " + SpeechRecognizer.isRecognitionAvailable(this));
        speech.setRecognitionListener(this);
        recognizerIntent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        recognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE,
                "en");
        recognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        recognizerIntent.putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 3);

        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                /* Trigger voice
                recording here
                 */

                if (recordButtonStatus) {
                    recordButtonStatus = false;
                    speech.stopListening();
                    fab.setBackground(getDrawable(R.drawable.microphone_button_off));
                } else {
                    ActivityCompat.requestPermissions
                            (MainActivity.this,
                                    new String[]{Manifest.permission.RECORD_AUDIO},
                                    REQUEST_RECORD_PERMISSION);
                    recordButtonStatus = true;
                    fab.setBackground(getDrawable(R.drawable.microphone_button_on));
                }
                Snackbar.make(view, "Recording audio", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
                }
        });

        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        NavigationView navigationView = findViewById(R.id.nav_view);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.addDrawerListener(toggle);
        toggle.syncState();
        navigationView.setNavigationItemSelectedListener(this);

        /* Establishing Mqtt client connection*/

        connectToMQTT();

        //sending the username or making one for first time use
            final String userid = PreferenceManager.getDefaultSharedPreferences(getApplicationContext()).getString("userid", "defaultStringIfNothingFound");

            Log.i("Userid",userid);
            if (userid.equals("defaultStringIfNothingFound")){
                //showpopup();
                AlertDialog.Builder builder = new AlertDialog.Builder(this);
                builder.setTitle("Pick an unique username");

                    // Set up the input
                final EditText input = new EditText(this);
                input.setTextColor(Color.BLACK);
                // Specify the type of input expected; this, for example, sets the input as a password, and will mask the text
                input.setInputType(InputType.TYPE_CLASS_TEXT);
                builder.setView(input);

                // Set up the buttons

                builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        final String m_Text = input.getText().toString();
                        Log.i("User", m_Text);
                        user_id = m_Text;

                        db.collection("userids")
                                .addSnapshotListener(new EventListener<QuerySnapshot>() {
                                    @Override
                                    public void onEvent(@Nullable QuerySnapshot queryDocumentSnapshots, @Nullable FirebaseFirestoreException e) {
                                        if (e != null) {
                                            Log.w("MainActivity", "Listen failed.", e);
                                            return;
                                        }


                                        for (QueryDocumentSnapshot document : queryDocumentSnapshots) {
                                            String name = document.get("name").toString();
                                            if (name.equals(m_Text)) {
                                                error = 1;
                                                Toast.makeText(MainActivity.this, "Name aldready taken try something else", Toast.LENGTH_SHORT).show();
                                                break;
                                            }
                                        }
                                        if (error == 0) {

                                            db.collection("no_of_user").document("Number")
                                                    .get().addOnCompleteListener(new OnCompleteListener<DocumentSnapshot>() {
                                                @Override
                                                public void onComplete(@androidx.annotation.NonNull Task<DocumentSnapshot> task) {
                                                    if (task.isSuccessful()) {
                                                        DocumentSnapshot documentSnapshot = task.getResult();
                                                        no_users = Integer.parseInt(documentSnapshot.get("total_users").toString());
                                                        Log.i("Number of users: ",String.valueOf(no_users));
                                                        no_users = no_users+1;
                                                        Log.i("Users:",String.valueOf(no_users));
                                                        Map<String,Integer> no = new HashMap<>();
                                                        no.put("total_users",no_users);
                                                        Map<String,String> name = new HashMap<>();
                                                        name.put("name",m_Text);
                                                        db.collection("no_of_user").document("Number").set(no);
                                                        db.collection("userids").document(String.valueOf(no_users)).set(name);
                                                        PreferenceManager.getDefaultSharedPreferences(MainActivity.this).edit().putString("userid", m_Text).apply();
                                                        sendMessageMQTT(m_Text,"GladOs/userid");
                                                    }
                                                }
                                            });

                                        }
                                    }
                                });

                    }
                });
                builder.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.cancel();
                    }
                });

                AlertDialog alert1 = builder.create();
                alert1.show();

                Button cancel = alert1.getButton(DialogInterface.BUTTON_NEGATIVE);
                cancel.setTextColor(Color.BLUE);

                Button ok = alert1.getButton(DialogInterface.BUTTON_POSITIVE);
                ok.setTextColor(Color.BLUE);
            }
            else{
                user_id = userid;
            }
            email = PreferenceManager.getDefaultSharedPreferences(getApplicationContext()).getString("email", "defaultStringIfNothingFound");
            password = PreferenceManager.getDefaultSharedPreferences(getApplicationContext()).getString("password", "defaultStringIfNothingFound");



    }

    private void parseMqttMessage(String s) {
        if (s.equals("Enter the password")) {
            if (email.equals("defaultStringIfNothingFound")) {

                AlertDialog.Builder builder = new AlertDialog.Builder(this);
                // Get the layout inflater
                LayoutInflater inflater = this.getLayoutInflater();
                // Inflate and set the layout for the dialog
                // Pass null as the parent view because its going in the dialog layout
                builder.setView(inflater.inflate(R.layout.alertlayout, null))
                        // Add action buttons
                        .setPositiveButton("Ok", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int id) {
                                // sign in the user ...
                                EditText input_email = (EditText) ((AlertDialog) dialog).findViewById(R.id.Email);
                                EditText input_password = (EditText) ((AlertDialog) dialog).findViewById(R.id.Password);
                                String entered_email = input_email.getText().toString();
                                String entered_password = input_password.getText().toString();
                                PreferenceManager.getDefaultSharedPreferences(MainActivity.this).edit().putString("email", entered_email).apply();
                                PreferenceManager.getDefaultSharedPreferences(MainActivity.this).edit().putString("password", entered_password).apply();
                                sendMessageMQTT("Password:" + entered_email + "," + entered_password, "GladOs/messages/" + user_id);

                            }
                        })
                        .setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int id) {
                                dialog.cancel();
                            }
                        });
                AlertDialog alert2 = builder.create();
                builder.show();

                Button Ok_button = alert2.getButton(DialogInterface.BUTTON_POSITIVE);
                Ok_button.setTextColor(Color.BLUE);

                Button Cancel_button = alert2.getButton(DialogInterface.BUTTON_NEGATIVE);
                Cancel_button.setTextColor(Color.BLUE);
            } else {
                sendMessageMQTT("Password:" + email + "," + password, "GladOs/messages/" + user_id);
                Toast.makeText(this, "Please wait while Glados cooks up the magic!", Toast.LENGTH_LONG).show();
            }
        } else if (s.equals("Everything OK")){
            parent_layout.setVisibility(View.VISIBLE);
            fab.show();
        }
    }


    private void connectToMQTT() {
        String clientId = MqttClient.generateClientId();
        client =
                new MqttAndroidClient(this.getApplicationContext(), "tcp://broker.hivemq.com:1883",
                        clientId);

        try {
            token = client.connect();
            token.setActionCallback(new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {
                    // We are connected
                    Toast.makeText(MainActivity.this, "Connected to server!", Toast.LENGTH_SHORT).show();
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                    // Something went wrong e.g. connection timeout or firewall problems
                    Toast.makeText(MainActivity.this, "Failed to connect to server!", Toast.LENGTH_SHORT).show();

                }
            });
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }


    public void TextSend(View view){

        String text = text_input.getText().toString();
        if(text.length()>0 && user_id.length()>0){
            sendMessageMQTT(text,"GladOs/messages/"+user_id);
        }
        else if(user_id.length() == 0){
            Toast.makeText(this, "Please make sure you have a valid user id before proceeding", Toast.LENGTH_SHORT).show();
        }
        else if(text.length()>0){
            Toast.makeText(this, "Please enter some text before hitting send button", Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_exit) {
            finish();
            return true;
        }
        else if(id == R.id.action_connect){
            sendMessageMQTT("CALLING ALPHABASE","GladOs/messages/" + user_id);
            Log.i("GLADOS",String.valueOf(client.isConnected()));
            if(client.isConnected()) {
                Log.i("GLADOS","HERE");
                try {
                    int qos = 1;
                    client.subscribe("GladOs/messages/raspberry2phone" + user_id, qos);
                    client.setCallback(new MqttCallback() {
                        @Override
                        public void connectionLost(Throwable cause) {

                        }

                        @Override
                        public void messageArrived(String topic, MqttMessage message) throws Exception {
                            Log.i("GLADOS",new String(message.getPayload()));

                            parseMqttMessage(new String(message.getPayload()));

                        }

                        @Override
                        public void deliveryComplete(IMqttDeliveryToken token) {

                        }
                    });
                }
                catch (MqttException e){
                    e.printStackTrace();
                }
            }
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();

        if (id == R.id.nav_about) {
            // Handle the camera action
        } else if (id == R.id.nav_history) {
            startActivity(new Intent(getApplicationContext(), HistoryActivity.class));
        }

        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }
    /*functions of the
    Speech Recogniser class
     */

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions,@NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        switch (requestCode) {
            case REQUEST_RECORD_PERMISSION:
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    speech.startListening(recognizerIntent);
                } else {
                    Toast.makeText(MainActivity.this, "Permission Denied!", Toast
                            .LENGTH_SHORT).show();
                }
        }
    }

    @Override
    public void onResume() {
        super.onResume();
    }

    @Override
    protected void onPause() {
        super.onPause();

    }

    @Override
    protected void onStop() {
        super.onStop();
        if (speech != null) {
            recordButtonStatus = false;
            fab.setBackground(getDrawable(R.drawable.microphone_button_off));
            Log.i(LOG_TAG, "destroy");
        }
    }


    @Override
    public void onBeginningOfSpeech() {
        Log.i(LOG_TAG, "onBeginningOfSpeech");
    }

    @Override
    public void onBufferReceived(byte[] buffer) {
        Log.i(LOG_TAG, "onBufferReceived: " + buffer);
    }

    @Override
    public void onEndOfSpeech() {
        Log.i(LOG_TAG, "onEndOfSpeech");

        recordButtonStatus = false;
        fab.setBackground(getDrawable(R.drawable.microphone_button_off));
    }

    @Override
    public void onError(int errorCode) {
        String errorMessage = getErrorText(errorCode);
        Log.d(LOG_TAG, "FAILED " + errorMessage);
        Toast.makeText(this, errorMessage, Toast.LENGTH_SHORT).show();
        recordButtonStatus = false;
        fab.setBackground(getDrawable(R.drawable.microphone_button_off));
    }

    @Override
    public void onEvent(int arg0, Bundle arg1) {
        Log.i(LOG_TAG, "onEvent");

    }

    @Override
    public void onPartialResults(Bundle arg0) {
        Log.i(LOG_TAG, "Results");

    }

    @Override
    public void onReadyForSpeech(Bundle arg0) {
        Log.i(LOG_TAG, "Ready For Speech");
    }

    @Override
    public void onResults(Bundle results) {
        Log.i(LOG_TAG, "Results");
        returnedText.setText("");
        ArrayList<String> matches = results
                .getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);


        String text = matches.get(0);
        returnedText.setText(text);

        sendMessageMQTT(text,"GladOs/messages/"+user_id);

        recordButtonStatus = false;
        fab.setBackground(getDrawable(R.drawable.microphone_button_off));
    }

    public void sendMessageMQTT(String text,String channel){
        if(user_id.length()>0) {

            if(client.isConnected()!= true) {
                connectToMQTT();
                try {
                    Thread.sleep(1000);
                }
                catch (Exception e){
                    e.printStackTrace();
                }
            }
            String payload = text;
            byte[] encodedPayload = new byte[0];
            try {
                encodedPayload = payload.getBytes("UTF-8");
                MqttMessage message = new MqttMessage(encodedPayload);
                client.publish(channel, message);
            } catch (UnsupportedEncodingException | MqttException e) {
                e.printStackTrace();
            }

            //making database entry for the new command
            DateFormat df = new SimpleDateFormat("dd/MM/yy HH:mm:ss");
            Date dateobj = new Date();
            String currDate = df.format(dateobj);
            databaseHandler.insertData(payload, currDate);
        }
        else{
            Toast.makeText(this, "Please make a valid username first!", Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    public void onRmsChanged(float rmsdB) {
        Log.i(LOG_TAG, "RMS Changed: " + rmsdB);

    }

    public static String getErrorText(int errorCode) {
        String message;
        switch (errorCode) {
            case SpeechRecognizer.ERROR_AUDIO:
                message = "ERROR: There was an error recording audio.";
                break;
            case SpeechRecognizer.ERROR_CLIENT:
                message = "ERROR: There was an error with the Client.";
                break;
            case SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS:
                message = "ERROR:  You need to accept permissions first.  Please go to your phone Settings -> Apps -> Speech to Text and accept.";
                break;
            case SpeechRecognizer.ERROR_NETWORK:
                message = "ERROR:  There was a Network error";
                break;
            case SpeechRecognizer.ERROR_NETWORK_TIMEOUT:
                message = "ERROR: There was a Network timeout";
                break;
            case SpeechRecognizer.ERROR_NO_MATCH:
                message = "ERROR: I didn't quite catch that.";
                break;
            case SpeechRecognizer.ERROR_RECOGNIZER_BUSY:
                message = "ERROR: RecognitionService busy";
                break;
            case SpeechRecognizer.ERROR_SERVER:
                message = "ERROR:  A Server error occurred";
                break;
            case SpeechRecognizer.ERROR_SPEECH_TIMEOUT:
                message = "ERROR: I didn't quite catch that";
                break;
            default:
                message = "Hmm, I'm not sure I understand, please try again.";
                break;
        }
        return message;
    }
}
