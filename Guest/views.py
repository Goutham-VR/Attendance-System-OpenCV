from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from Guest.models import*
from django.utils.timezone import now
from datetime import datetime, date
from .models import Attendance
import cv2
import os
import numpy as np
import face_recognition
import base64
from django.core.files.base import ContentFile
# Create your views here.

def Registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('mail')
        contact = request.POST.get('cont')
        address = request.POST.get('address')
        password = request.POST.get('password')
        photo_data = request.POST.get('file_photo')  # Captured photo in base64

        # Decode the base64 image and save it
        format, imgstr = photo_data.split(';base64,')
        ext = format.split('/')[-1]
        photo_file = ContentFile(base64.b64decode(imgstr), name=f"{name}.{ext}")

        # Save to database
        tbl_student.objects.create(
            student_name=name,
            student_email=email,
            student_contact=contact,
            student_address=address,
            student_password=password,
            student_photo=photo_file
        )

        return render(request, 'Guest/StudentReg.html', {'message': 'Registration successful!'})
    return render(request, 'Guest/StudentReg.html')


# def name(request):
#     if request.method == "POST":
#         name1 = request.POST['name1']
        
#         cam = cv2.VideoCapture('http://192.168.1.7:4747/video')

#         while True:
#             ret, frame = cam.read()
#             if not ret:
#                 print("Failed to grab frame")
#                 break
#             cv2.imshow("Press Space to capture image", frame)

#             k = cv2.waitKey(1)
#             if k % 256 == 27:  # ESC pressed
#                 print("Escape hit, closing...")
#                 break
#             elif k % 256 == 32:  # SPACE pressed
#                 img_name = f"{name1}.png"
#                 path = os.path.join("media", "Assets", "train")
#                 os.makedirs(path, exist_ok=True)
#                 cv2.imwrite(os.path.join(path, img_name), frame)
#                 print(f"{img_name} written!")
#         cam.release()
#         cv2.destroyAllWindows()
#         return render(request, 'Guest/image.html')
#     return render(request ,'Guest/image.html')

def recognize(request):
    if request.method == "POST":
        path = os.path.join("media", "Assets", "train")
        images = []
        classNames = []
        myList = os.listdir(path)
        for cl in myList:
            curImg = cv2.imread(os.path.join(path, cl))
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])

        def findEncodings(images):
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList

        def markAttendance(name):
            current_time = datetime.now().strftime('%H:%M:%S')
            today_date = date.today()
            Attendance.objects.create(name=name, time=current_time, date=today_date)

        encodeListKnown = findEncodings(images)
        cap = cv2.VideoCapture(0)
        while True:
            success, img = cap.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)

                if faceDis[matchIndex] < 0.50:
                    name = classNames[matchIndex].upper()
                    markAttendance(name)
                else:
                    name = "Unknown"

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            cv2.imshow('Punch your Attendance', img)
            if cv2.waitKey(1) == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
        return render(request, 'Guest/first.html')
    return render(request, 'Guest/main.html')

def data(request):
    if request.method == "POST":
        today_date = date.today()
        attendance_data = Attendance.objects.filter(date=today_date)
        return render(request, 'Guest/form2.html', {'rows': attendance_data})
    return render(request, 'Guest/form1.html')

def whole(request):
    attendance_data = Attendance.objects.all()
    return render(request, 'Guest/form3.html', {'rows': attendance_data})

def dashboard(request):
    return render(request, 'Guest/dashboard.html')

