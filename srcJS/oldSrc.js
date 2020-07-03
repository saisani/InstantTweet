<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/0.4.5/p5.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/0.4.5/addons/p5.dom.js"></script>
<script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
<script src="/s/p5speech-m3lc.js"></script>
<srcipt src="/s/Queue.js"></script>
<script>
  // eventually add to environment variables:
  AUTOMATION_URL = "https://n8up.herokuapp.com/webhook/1/webhook/listen";
  SENTENCE_BLOCK = "#block-yui_3_17_2_1_1593335120037_4492";
  BUTTON_BLOCK = "block-yui_3_17_2_1_1593586139183_4823"
  TWEET_CHAR_LIMIT = 280;

  // create queue to store phrases
  // var phraseQueue = new Queue();
  
  var myRec = new p5.SpeechRec();
  myRec.continuous = true;

  // attach callback to button press

  // changes the header with the argument text
  function changeText(newText)
  {
    $(document).ready(function(){
        $(SENTENCE_BLOCK).find("h3")
          .text(newText);
    });
  }

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

  function restartMic() {
    console.log("Mic failed");
    myRec.start();
  }
  
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
    
    myRec.onResult = showResult;
    // myRec.onEnd = restartMic;
    myRec.onError = restartMic;
    myRec.start();
  }
</script>