import asyncio
import cv2
import pickle
import struct
import websockets

async def webcam_stream(websocket, path):
    print(f"Client connected: {path}")
    cap = cv2.VideoCapture(0)  # Open the default camera

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame. Exiting.")
                break

            # Serialize frame using pickle
            data = pickle.dumps(frame)

            # Send the serialized frame size and frame data
            message = struct.pack("L", len(data)) + data
            await websocket.send(message)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cap.release()
        print("Camera released and server stopped.")

# Start the WebSocket server
start_server = websockets.serve(webcam_stream, "0.0.0.0", 9999)

print("WebSocket server listening on port 9999")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
