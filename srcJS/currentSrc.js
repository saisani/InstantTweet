<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/0.4.5/p5.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/0.4.5/addons/p5.dom.js"></script>
<script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
<script src="/s/p5speech-m3lc.js"></script>
<srcipt src="/s/Queue.js"></script>
<script>
  // eventually add to environment variables:
  AUTOMATION_URL = "https://n8up.herokuapp.com/webhook/1/webhook/listen";
  SENTENCE_ID = "block-yui_3_17_2_1_1593335120037_4492";
  IMAGE_ID = "block-yui_3_17_2_1_1593243056431_3681";
  TWEET_CHAR_LIMIT = 280;
  
  var myRec = new p5.SpeechRec();
  myRec.continuous = false;

  // changes the header with the text in the argument
  function changeText(newText)
  {
    completeText = newText;
    $(document).ready(function(){
        $("#" + SENTENCE_ID).find("h3")
          .text(completeText);
    });

    setTimeout(clearText, 3*1000);
  }

  // removes text in the header
  function clearText()
  {
    $(document).ready(function(){
        $("#" + SENTENCE_ID).find("h3")
          .text("");
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

  // changes cursor when hovering over image
  function changeImage()
  {
    img = document.getElementById(IMAGE_ID).getElementsByTagName("img");

    // cursor is hosted in google drive
    img[0].style.cursor = "url('https://drive.google.com/uc?export=view&id=1hDk7a0P7pDODQuAsYKpH8KIx8J8ii_01'), auto";
  }
  
  function setup()
  {
    // NOT NEEDED:
    // graphics stuff 
    // createCanvas(800, 400);
    // background(255, 255, 255);
    // fill(0, 0, 0, 255);
    // textSize(32);
    // textAlign(CENTER);
    // text("say something", width/2, height/2);

    // change style of img block
    changeImage();
    
    // set callback to restart mic
    document.getElementById(IMAGE_ID).onclick = restartMic;

    myRec.onResult = showResult;
  }
</script>
