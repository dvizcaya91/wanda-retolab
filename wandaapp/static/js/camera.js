const constraints =  { facingMode: 'environment',"video": { width: { exact: 400 }}};
var videoTag = document.getElementById('video-tag');
var imageTag = document.getElementById('image-tag');
var focusSlider = document.getElementById("focus-slider");
var focusSliderValue = document.getElementById("focus-slider-value");
var imageCapturer;

function start() {
  console.log("Start");
  navigator.mediaDevices.getUserMedia({ video: constraints })
    .then(gotMedia)
    .catch(e => { console.error('getUserMedia() failed: ', e); });

}

  function gotMedia(mediastream) {
    var videoTag = document.getElementById('video-tag');
    //var imageTag = document.getElementById('image-tag');
    var focusSlider = document.getElementById("focus-slider");
    var focusSliderValue = document.getElementById("focus-slider-value");

  console.log("got media")
  videoTag.srcObject = mediastream;
  //document.getElementById('start').disabled = true;
  var videoTrack = mediastream.getVideoTracks()[0];
  imageCapturer = new ImageCapture(videoTrack);

  // Timeout needed in Chrome, see https://crbug.com/711524
  setTimeout(() => {
    const capabilities = videoTrack.getCapabilities()
    // Check whether focus distance is supported or not.
    if (!capabilities.focusDistance) {
      return;
    }

    // Map focus distance to a slider element.
    focusSlider.min = capabilities.focusDistance.min;
    focusSlider.max = capabilities.focusDistance.max;
    focusSlider.step = capabilities.focusDistance.step;
    focusSlider.value = videoTrack.getSettings().focusDistance;
    focusSliderValue.value=focusSlider.value;
    focusSlider.oninput = function() {
      focusSliderValue.value = focusSlider.value;
      videoTrack.applyConstraints({
        advanced : [{focusMode: "manual", focusDistance: focusSlider.value}]

      });
    }
 }, 500);
  }

  function takePhoto() {

  imageCapturer.takePhoto()
    .then((blob) => {
      console.log("Photo taken: " + blob.type + ", " + blob.size + "B")
      $("#photo_btn").html("<div class='btn btn-primary'><img class='loading-img' src='static/images/loading.gif' /></div>")

      //var imageTag = document.getElementById('camera-tag');

      $("#camera-tag").html("<img class='loading-img' src='" + URL.createObjectURL(blob) + "' />");

      var form = new FormData();
      form.append("myfile", blob);

      var XHR = new XMLHttpRequest();

     XHR.addEventListener('load', function(event) {
        window.location.replace('crm');
     });

      // Set up our request
      XHR.open('POST', 'new-image');

      // Send our FormData object; HTTP headers are set automatically
      XHR.send(form);


      }
    /*.catch((err) => {
      console.error("takePhoto() failed: ", err);
    });*/
    )

  }
