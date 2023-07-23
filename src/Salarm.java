package coffersmart.com.healthysleep;
//The package name of your android app

import android.content.BroadcastReceiver;
import android.content.Intent;
import android.content.Context;
import coffersmart.com.healthysleep.Notify;
import coffersmart.com.healthysleep.R;

public class Salarm extends BroadcastReceiver{
  // This function is run when the BroadcastReceiver is fired
   @Override
   public void onReceive(Context context, Intent sintent) {
    Notify.stopAlarm(context);
   }

}