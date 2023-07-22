public class Salarm extends BroadcastReceiver{
  MediaPlayer mediaPlayer;
  // This function is run when the BroadcastReceiver is fired
   @Override
   public void onReceive(Context context, Intent sintent) {
       super.onDestroy();
       if (mediaPlayer != null) mediaPlayer.release();
   }

}