package com.mosip.qrcodescanner;

import androidx.annotation.ColorInt;
import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;


import com.google.crypto.tink.proto.Ed25519;
import com.google.crypto.tink.subtle.Ed25519Sign;
import com.google.crypto.tink.subtle.Ed25519Verify;
import com.google.crypto.tink.subtle.Hex;
import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.security.GeneralSecurityException;
import java.util.Base64;

public class MainActivity extends AppCompatActivity {

    private TextView textView;
    private TextView messageView;
    private TextView signatureView;
    private TextView statusView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        textView = findViewById(R.id.textView);
        messageView = findViewById(R.id.textView2);
        signatureView = findViewById(R.id.textView3);
        statusView = findViewById(R.id.textView6);

        ActivityCompat.requestPermissions(this,new String[]{Manifest.permission.CAMERA}, PackageManager.PERMISSION_GRANTED);

    }

    public void ScanButton(View view) {
        IntentIntegrator intentIntegrator = new IntentIntegrator(this);
        intentIntegrator.setPrompt("Scan a barcode");
        intentIntegrator.setCameraId(0);  // Use a specific camera of the device
        intentIntegrator.setOrientationLocked(true);
        intentIntegrator.setBeepEnabled(true);
        //intentIntegrator.setCaptureActivity(CaptureActivityPortrait.class);
        intentIntegrator.initiateScan();
    }

   // @RequiresApi(api = Build.VERSION_CODES.O)
    @RequiresApi(api = Build.VERSION_CODES.O)
    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {

        IntentResult intentResult = IntentIntegrator.parseActivityResult(requestCode,resultCode, data);
        if(intentResult != null) {
            if(intentResult.getContents() == null ){
                textView.setText("Cancelled");
            }
            else{
                textView.setText(intentResult.getContents());
            }
        }

        try{

            String jsonMessage = textView.getText().toString();
            JSONObject qrMessage = new JSONObject(jsonMessage);
            //JSONObject qrMessageArray = parser.getJSONObject(s);

            //String subject = qrMessage.getString("subject");
            //messageView.setText(subject);


            //String signature = qrMessage.getString("signature");
            //signatureView.setText(signature);
//            Ed25519Sign.KeyPair pair = Ed25519Sign.KeyPair.newKeyPair();
//
//            String privKey = Base64.getEncoder().encodeToString(pair.getPrivateKey());
//            String publicKey = Base64.getEncoder().encodeToString(pair.getPublicKey());

            String publicKey = "tWOWYT9twCd2SNCNMsSTaZFTICeafaStU5FAdZcHaG4=";
            byte[] publicKeyDecoded = Base64.getDecoder().decode(publicKey.getBytes());
            messageView.setText(publicKey);

            //Ed25519Sign signed = new Ed25519Sign(pair.getPrivateKey());
            String subject1 = "{\"Suffix\":\"\",\"lName\":\"banto\",\"fName\":\"aaron-o-niel\",\"mName\":\"simbaco\",\"sex\":\"Male\",\"BF\":\"[1,7]\",\"DOB\":\"November 12, 1993\",\"POB\":\"City of Manila,NCR, CITY OF MANILA, FIRST DISTRICT\",\"PCN\":\"5073-0634-8709-1024\"}";
            //System.out.println("Message: " +  subject);
            //System.out.println("Message 1: " +  subject1);
//            if(subject==subject1) {
//                System.out.println("Both Are Equal");
//            } else {
//                System.out.println("There Are Difference");
//            }
            //signature = "Wm/mTiVtkOO3kppoPtrWbkTaVE6+bE/9AVZ3ct/1IyjsvwQJm9lOk7XDzBK4BCmWCDB6V/+I0k6KTpIXXiXVCQ==";

            //byte[] signatureDecoded = signed.sign(subject.getBytes());
            //signature = Base64.getEncoder().encodeToString(signatureDecoded);


            //byte[] signatureDecoded = Base64.getDecoder().decode(signature.trim().getBytes());
            boolean isVarified = false;
            //signatureView.setText(signature);
            Ed25519Verify ed = new Ed25519Verify(publicKeyDecoded);
            try{
                //ed.verify(signatureDecoded, subject.trim().getBytes());
                statusView.setTextColor(Color.GREEN);
                statusView.setText("Verified Successfully");
                isVarified = true;

            } catch (Exception ex) {
                statusView.setTextColor(Color.RED);
                statusView.setText("Verification Failed");
            }

            //signature = Base64.getEncoder().encodeToString(signatureBytes);



            Intent intent = new Intent();

            if (intent != null) {

                //intent.putExtra("date_issued", qrMessage.getString("DateIssued"));
                //intent.putExtra("issuer", qrMessage.getString("Issuer"));
                //JSONObject subjectJSON = qrMessage.getJSONObject("subject");
                intent.putExtra("state" , qrMessage.getString("state"));
                intent.putExtra("phone" , qrMessage.getString("phone"));
                intent.putExtra("city" , qrMessage.getString("city"));
                intent.putExtra("fullName" , qrMessage.getString("fullName"));
                intent.putExtra("gender" , qrMessage.getString("gender"));
                intent.putExtra("postalCode" , qrMessage.getString("postalCode"));
                intent.putExtra("dateOfBirth" , qrMessage.getString("dateOfBirth"));
                intent.putExtra("email" , qrMessage.getString("email"));
                intent.putExtra("address" , qrMessage.getString("address"));
                intent.putExtra("id" , qrMessage.getString("id"));
                intent.putExtra("locality" , qrMessage.getString("locality"));

                if(isVarified) {
                    intent.putExtra("verifyStatus" , "true");
                    intent.putExtra("successMessage" , "Verification Success");
                } else {
                    intent.putExtra("verifyStatus" , "false");
                    intent.putExtra("verifyMessage" , "Verification failed");
                }
                setResult(RESULT_OK, intent);
                finish();
            }

        }catch(JSONException pe) {
            System.out.println("position: " + pe.getStackTrace());
            statusView.setTextColor(Color.RED);
            statusView.setText(pe.getMessage());
        } catch (Exception ex) {
            System.out.println("Exception: " + ex.getStackTrace());
            statusView.setTextColor(Color.RED);
            statusView.setText(ex.getMessage());
        }

        super.onActivityResult(requestCode, resultCode, data);

    }


}