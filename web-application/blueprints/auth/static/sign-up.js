const video = document.getElementById('video')
const snap = document.getElementById('snap')
const errorMshElement = document.getElementById('errormsg')

const constraints = {
  audio: false,
  video: {
    width: 480,
    height: 320
  }
}

function init(){
  navigator.mediaDevices.getUserMedia(constraints)
    .then(stream => {
      handleSuccess(stream)
    })
    .catch(e => {
      errorMshElement.innerHTML = `navigator.getUserMedia.error ${e.toString()}`
    })
}

function handleSuccess(stream){
  window.stream = stream
  video.srcObject = stream
}

init()

function snapHandler(e){
    e.preventDefault()

    const faceScreenshooter = document.getElementById('face-screenshooter')
    faceScreenshooter.innerHTML = ''
  
    const canvas = document.createElement('canvas')
    canvas.id = 'canvas'
    canvas.width = 480
    canvas.height = 320
  
    faceScreenshooter.appendChild(canvas)
  
    canvas.getContext('2d').drawImage(video, 0, 0, 480, 320)
    const imgData = canvas.toDataURL('image/jpeg'); 
    const imageInput = document.getElementById('imgdata')
    imageInput.value = imgData
  
    window.stream = null
    video.srcObject = null
    snap.removeEventListener('click', snapHandler)
  
}

snap.addEventListener('click', snapHandler)
