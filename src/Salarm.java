package coffersmart.com.healthysleep;
//The package name of your android app

import android.content.BroadcastReceiver;
import android.content.Intent;
import android.content.Context;
import android.media.MediaPlayer;
import coffersmart.com.healthysleep.R;

public class Salarm extends BroadcastReceiver{
  MediaPlayer mediaPlayer;
  // This function is run when the BroadcastReceiver is fired
   @Override
   public void onReceive(Context context, Intent sintent) {
       super.onReceive();
       if (mediaPlayer != null) mediaPlayer.release();
   }

}