from flask import Flask, Response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)  # 0 for default webcam; replace with 1 for external webcam

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Encode frame to JPEG format
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield frame as part of a multipart HTTP response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    # Video streaming route
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    # Simple homepage
    return "<h1>Webcam Stream</h1><p>Go to <a href='/video_feed'>/video_feed</a> to view the stream.</p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
