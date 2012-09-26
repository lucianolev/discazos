//Interfaz JS para DiscazosPlayer

package
{
    import flash.display.Sprite;
    import flash.events.Event;
    import flash.events.ProgressEvent;
    import flash.events.IOErrorEvent;
    import flash.external.ExternalInterface;

    public class DiscazosPlayerJS extends Sprite
    {
        private var player:DiscazosPlayer;
        
        public function DiscazosPlayerJS()
        {
            this.player = new DiscazosPlayer();
            
            if(ExternalInterface.available) {
                this.player.addEventListener(Event.OPEN, bufferLoadingStarted);
                this.player.addEventListener(IOErrorEvent.IO_ERROR, bufferError);
                this.player.addEventListener(DiscazosPlayer.BUFFER_PROGRESS, updateBufferProgress);
                //this.player.addEventListener(Event.COMPLETE, bufferLoadingFinish);
                ExternalInterface.addCallback("load", this.player.load);
                ExternalInterface.addCallback("play", this.player.play);
                ExternalInterface.addCallback("pause", this.player.pause);
                ExternalInterface.addCallback("seek", this.player.seek);
                
                this.player.addEventListener(DiscazosPlayer.PLAY_PROGRESS, updateCurrentPosition);
            }
        }

        private function bufferLoadingStarted(event:Event):void {
            ExternalInterface.call("DiscazosPlayer.bufferLoadingStarted");
        }
        
        private function bufferError(errorEvent:IOErrorEvent):void {
            ExternalInterface.call("DiscazosPlayer.bufferError", errorEvent.text);
        }
        
        private function updateBufferProgress(event:ProgressEvent):void {
            ExternalInterface.call("DiscazosPlayer.updateBufferProgress", event.bytesLoaded, event.bytesTotal);
        }
        
        private function bufferLoadingFinish(event:Event):void {
            ExternalInterface.call("DiscazosPlayer.bufferLoadingFinish");
        }
        
        private function updateCurrentPosition(event:ProgressEvent):void {
            ExternalInterface.call("DiscazosPlayer.currentPlaybackPositionChanged", event.bytesLoaded);
        }
    }
}