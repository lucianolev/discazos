package 
{
    
    import flash.errors.IOError;
    import flash.events.Event;
    import flash.events.EventDispatcher;
    import flash.events.IOErrorEvent;
    import flash.events.ProgressEvent;
    import flash.events.TimerEvent;
    import flash.media.Sound;
    import flash.media.SoundChannel;
    import flash.media.SoundLoaderContext;
    import flash.media.SoundMixer;
    import flash.media.SoundTransform;
    import flash.net.URLRequest;
    import flash.utils.Timer;
    
    /* Discazos Minimal Player */
    /* Debe ser lo mas minimal posible. Todo la logica que se pueda hacer via JS 
    * debe hacerse ahi y no en acá en AS.
    * Se debe encargar de cargar un archivo de audio, reproducirlo, pausarlo, pararlo, 
    * adelantar y cambiar el volumen.
    * Se usa como unidad de medida de posicion y tamaño los milisegundos.
    * Debe tambien informar su estado (position actual, estado de reproduccion, ms cargados 
    * del archivo y volumen actual de 0 a 100) para ser accedido via JS.
    */
    public class DiscazosPlayer extends EventDispatcher
    {        
        private var track:Sound;
        private var channel:SoundChannel;
        private var pausedPosition:Number;
        private var positionTimer:Timer;
        private var isPlaying:Boolean = false;
        
        private const bufferTime:int = 8000;
        
        /* Events */
        public static const BUFFER_PROGRESS:String = "bufferProgress"; 
        public static const PLAY_PROGRESS:String = "playProgress";
        
        /* Public interfaces */
        public var startVolume:Number;
        public var trackLength:Number;
        
        public function DiscazosPlayer() {
            this.pausedPosition = 0;
            this.startVolume = SoundMixer.soundTransform.volume * 100;
        }
        
        public function load(url:String):void {
            var trackUrl:URLRequest = new URLRequest(url);
            this.track = new Sound();
            try {
                var context:SoundLoaderContext = new SoundLoaderContext(this.bufferTime); 
                this.track.load(trackUrl, context);
                
                this.channel = new SoundChannel();
                this.positionTimer = new Timer(50);
                this.positionTimer.addEventListener(TimerEvent.TIMER, updatePositionHandler);
                
                this.track.addEventListener(Event.OPEN, bufferLoadingStartedHandler);
                this.track.addEventListener(ProgressEvent.PROGRESS, bufferProgressHandler);
                this.track.addEventListener(Event.COMPLETE, bufferLoadingFinishHandler);
            }
            catch (err:Error) {
                trace(err.message);
            }
            this.track.addEventListener(IOErrorEvent.IO_ERROR, bufferErrorHandler);
        }
        
        public function play(position:Number = 0):void {
            if(!this.track.isBuffering && !this.isPlaying) {
                if(position == 0 && this.pausedPosition > 0) {
                    position = this.pausedPosition;
                }
                this.channel = this.track.play(position, 0, this.channel.soundTransform);
                this.isPlaying = true;
                this.positionTimer.start();
            }
        }
        
        public function pause():void {
            this.pausedPosition = this.channel.position;
            this.channel.stop();
            this.positionTimer.stop();
            this.isPlaying = false;
        }
        
        public function seek(position:Number):void {
            if(position > 0 && position < this.trackLength) {
                if(this.isPlaying) {
                    this.pause();
                }
                this.play(position);
            }
        }
        
        public function stop():void {
            this.pause();
            this.pausedPosition = 0;
        }
        
        public function setVolume(volumePercent:int):void {
            if(volumePercent >= 0 && volumePercent <= 100) {
                var newTransform:SoundTransform = this.channel.soundTransform;
                newTransform.volume = volumePercent / 100;
                this.channel.soundTransform = newTransform;
            }
        }
        
        /* Event Handlers */
        
        private function bufferErrorHandler(errorEvent:IOErrorEvent):void {
            this.dispatchEvent(errorEvent.clone());
        }
        
        private function bufferLoadingStartedHandler(event:Event):void {
            this.dispatchEvent(event.clone());
        }
        
        private function bufferLoadingFinishHandler(event:Event):void {
            this.dispatchEvent(event.clone());
        }
        
        private function bufferProgressHandler(event:ProgressEvent):void {
            this.trackLength = this.track.length;
            var bufferMsLoaded:Number = Math.round(event.bytesLoaded * this.trackLength / event.bytesTotal);
            var bufferProgressEvent:ProgressEvent = 
                new ProgressEvent(BUFFER_PROGRESS, false, false, bufferMsLoaded, this.trackLength);
            this.dispatchEvent(bufferProgressEvent);
        }
        
        private function updatePositionHandler(event:TimerEvent):void {
            var playProgressEvent:ProgressEvent = 
                new ProgressEvent(PLAY_PROGRESS, false, false, Math.round(this.channel.position), this.trackLength);
            this.dispatchEvent(playProgressEvent);
        }
        
    }
}