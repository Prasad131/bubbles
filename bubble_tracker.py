import re, csv
import cv2, sys

tracker = cv2.TrackerMIL_create()
tracker_bubble = cv2.TrackerMIL_create()
video = cv2.VideoCapture('_DSC0196.MOV')

start_frame, end_frame, ct = 0, 137, 0

cv2.namedWindow('Tracking', cv2.WINDOW_NORMAL)

if not video.isOpened():
    print("Could not open video")
    sys.exit()

print('Getting you to the start frame...')
while ct <= start_frame:
    ok, frame = video.read()
    if ok:
        ct += 1
    else:
        break
print('Done!')

if not ok:
    print("Cannot read video file")
    sys.exit()


bbox = cv2.selectROI('Tracking',frame, False)
bbox_bubble = cv2.selectROI('Tracking', frame, False)
ok = tracker.init(frame, bbox)
okB = tracker_bubble.init(frame, bbox_bubble)
data = []
data.append(['rise (in pixel)', 'rise of bubble(in pixel)'])

while True:
    ok, frame = video.read()
    if not ok:
        break

    timer = cv2.getTickCount()

    ok, bbox = tracker.update(frame)
    okB, bbox_bubble = tracker_bubble.update(frame)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
 
    # Draw bounding box
    if ok:
        # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        p1B = (int(bbox_bubble[0]), int(bbox_bubble[1]))
        p2B = (int(bbox_bubble[0]+bbox_bubble[2]), int(bbox_bubble[1]+bbox_bubble[3]))
        h = int(bbox[1])+float(bbox[3]/2)
        hB = int(bbox_bubble[1])+float(bbox_bubble[3]/2)
        data.append([h, hB])
        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        cv2.rectangle(frame, p1B, p2B, (0, 0, 255), 2, 1)
    else :
        # Tracking failure
        cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

    # Display result
    cv2.imshow('Tracking', frame)

    # Exit if ESC pressed
    k = cv2.waitKey(30) & 0xff
    if k == 27 :
        print('Frame no. ', ct)
        break
    ct += 1
    if ct >= end_frame:
        break

video.release()
cv2.destroyAllWindows()

myFile = open('data.csv', 'w')
with myFile:
    writer = csv.writer(myFile)
    writer.writerows(data)
