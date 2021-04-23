/*var callOptions={'iceServers': [
    {url: 'stun:95.xxx.xx.x9:3479',		
    username: "user",
    credential: "xxxxxxxxxx"},
    { url: "turn:95.xxx.xx.x9:3478",		
    username: "user",
    credential: "xxxxxxxx"}]
}; 
peer= new Peer({config: callOptions});*/
peer= new Peer(); 
peer.on('open', function(peerID) {
        document.getElementById('myid').innerHTML=peerID;			
    });
var peercall;
var datacall;
var media_stream;
peer.on('call', function(call) {
      // Answer the call, providing our mediaStream
        peercall=call;
        document.getElementById('callinfo').innerHTML="Входящий звонок <button onclick='callanswer()' >Принять</button><button onclick='callcancel()' >Отклонить</button>";
});
peer.on('connection', function(conn) {
    datacall = conn;
    datacall.on('close', onCallClose);
});
async function callanswer() {
  media_stream = await navigator.mediaDevices.getUserMedia({ audio: { autoGainControl: false, channelCount: 1, echoCancellation: false, latency: 0, noiseSuppression: false, sampleRate: 48000, sampleSize: 16, volume: 1.0 } });;
  try {
    peercall.answer(media_stream); // отвечаем на звонок и передаем свой медиапоток собеседнику
    document.getElementById('callinfo').innerHTML="Звонок начат... <button onclick='callclose()' >Завершить звонок</button>"; //информируем, что звонок начат, и выводим кнопку Завершить
    setTimeout(function() {
    //входящий стрим помещаем в объект видео для отображения
      document.getElementById('remAudio').srcObject = peercall.remoteStream; 
      document.getElementById('remAudio').onloadedmetadata= function(e) {
  // и запускаем воспроизведение когда объект загружен
        document.getElementById('remAudio').play();
        };
        },1500);			  
          
          
    }
    catch(err) { console.log(err.name + ": " + err.message); };
}
async function callToNode(peerId) { //вызов
media_stream = await navigator.mediaDevices.getUserMedia ({ audio: true, video: false});
  try {
    var audio = document.getElementById('myAudio');				  
    peercall = peer.call(peerId,media_stream); 
    peercall.on('stream', function (stream) { //нам ответили, получим стрим
            setTimeout(function() {
            document.getElementById('callinfo').innerHTML="Звонок начат... <button onclick='callclose()' >Завершить звонок</button>";
            document.getElementById('remAudio').srcObject = peercall.remoteStream;
                document.getElementById('remAudio').onloadedmetadata= function(e) {
                  document.getElementById('remAudio').play();
                };
                },1500);	
            });
    datacall = peer.connect(peerId);
    datacall.on('close', onCallClose);
    audio.srcObject = media_stream;
    audio.onloadedmetadata = function(e) {
      audio.play();
    };}
      
    catch(err) { console.log(err.name + ": " + err.message); };
}
function callclose() {
    datacall.close();
    peercall.close();
}

function onCallClose() {
    console.log(document.getElementById('callinfo').innerHTML)
    document.getElementById('callinfo').innerHTML="";
    media_stream.getTracks().forEach(track => track.stop())
}
