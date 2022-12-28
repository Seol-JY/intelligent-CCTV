isDetect = 0;

const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const context = canvas.getContext("2d");
const checkbox = document.getElementById("flexSwitchCheckDefault")
const img = document.getElementById("img");
const detect_info = document.getElementById("detect-info");
const detect_sensitivity_slider = document.getElementById("range");
const mention = document.getElementById("mention");

cocoSsd.load().then((model) => {
  predict();
  function predict() {
    context.drawImage(video, 0, 0);
    model.detect(canvas).then((predictions) => {
    
      predictions = predictions.filter((det) => det.class === "person" && det.score >= detect_sensitivity_slider.value);
      
      canvas.width = 640;
      canvas.height = 480;

      if (predictions.length) { isDetect++ }
      else {
        isDetect = 0;
        detect_info.innerText = "사람이 감지되지 않음";
        detect_info.setAttribute('class', 'alert alert-success');
      }

      if (isDetect ==  35) {
        detect_info.innerText = "사람이 감지됨!";
        detect_info.setAttribute('class', 'alert alert-danger');
        console.log("/detect/"+parseInt(predictions[0].score * 100)+"/"+mention.value);
        if (checkbox.checked) { fetch("/detect/"+parseInt(predictions[0].score * 100)+"/"+encodeURIComponent(mention.value)); }
      } 

      for (let i = 0; i < predictions.length; i++) {
        context.beginPath();
        context.lineWidth = 2;
        //party mode
        context.strokeStyle = "#00ff00";
        context.rect(...predictions[i].bbox);
        context.stroke();
        context.font = "24px Arial";
        context.fillStyle = "#00ff00";
        context.fillText(
          predictions[i].class +
            " " +
            parseInt(predictions[i].score * 100) +
            "%",
          predictions[i].bbox[0],
          predictions[i].bbox[1]
        );
      }
    });
    requestAnimationFrame(predict);
  }
});