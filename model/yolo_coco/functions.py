import cv2 #opencv
import numpy as np

# Load Yolo
net = cv2.dnn.readNet("./model/yolo_coco/yolov3.weights", "./model/yolo_coco/yolov3.cfg")
classes = []
with open("./model/yolo_coco/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

def detect(image_name):
    # Loading image
    img = cv2.imread(image_name)
    #img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)
    

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []

    #file = open('outs.txt',"w")

    for out in outs:
        
        # file.write("out\n")
        # file.write("len(out): " + str(len(out)) + " \n")

                
        for detection in out:
            # file.write("detection\n")
            # file.write(str(detection) + "\n")
            
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

        # file.write("\n")

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
            cv2.putText(img, label, (x, y + 30), font, 1, color, 2)

    # Save image after detecting objects
    cv2.imwrite("./static/img/detection.jpg",img)
    #cv2.imwrite("./readouts.jpg",img)
    