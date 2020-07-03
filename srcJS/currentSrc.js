<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/0.4.5/p5.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/0.4.5/addons/p5.dom.js"></script>
<script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
<script src="/s/p5speech-m3lc.js"></script>
<srcipt src="/s/Queue.js"></script>
<script>
  // eventually add to environment variables:
  AUTOMATION_URL = "https://n8up.herokuapp.com/webhook/1/webhook/listen";
  SENTENCE_ID = "block-yui_3_17_2_1_1593335120037_4492";
  TWEET_CHAR_LIMIT = 280;

  // create queue to store phrases
  // var phraseQueue = new Queue();
  
  var myRec = new p5.SpeechRec();
  myRec.continuous = false;

  // changes the header with the text in the argument
  function changeText(newText)
  {
    completeText = newText + "... (Click Me Again?)"
    $(document).ready(function(){
        $("#" + SENTENCE_ID).find("h3")
          .text(completeText);
    });
  }

  // sends text to automation in n8n
  // content needs to be plain text to avoids preflight CORS
  function sendText(text)
  {
    $.ajax({
      type: 'POST',
      url: AUTOMATION_URL,
      data: text,
      contentType: "text/plain",
      success: function(result) {
        console.log("Received: ", result);
      },
      headers: {
        Accept: "application/json; charset=utf-8",
      }
    })
  }

  // starts mic again for new recording
  function restartMic() {
    console.log("Starting mic again");
    myRec.start();
  }
  
  // callback for when recording is done
  function showResult()
  {
    if(myRec.resultValue==false)
      return;

    if(myRec.resultString.length > TWEET_CHAR_LIMIT) {
      changeText("You said too much!");
    }
    else {
      sendText(myRec.resultString);
      changeText(myRec.resultString);
    }
  }
  
  function setup()
  {
    // graphics stuff DO NOT DO:
    // createCanvas(800, 400);
    // background(255, 255, 255);
    // fill(0, 0, 0, 255);
    
    // instructions:
    // textSize(32);
    // textAlign(CENTER);
    // text("say something", width/2, height/2);
    
    document.getElementById(SENTENCE_ID).onclick = restartMic;
    
    myRec.onResult = showResult;
    // myRec.onEnd = restartMic;
    // myRec.onError = restartMic;
    // myRec.start();
  }
</script>
