import sys
import cv2
import numpy as np
import face_recognition
import os
import pandas as pd
import time as t
# from RPLCD.i2c import CharLCD
from datetime import datetime, date, time, timedelta
from test import test
from openpyxl import load_workbook, workbook
# from antispoofing.test import test

a = (0b00000, 0b00000, 0b00001, 0b00011, 0b00111, 0b00110, 0b01100, 0b01100)
b = (0b00000, 0b11111, 0b11111, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000)
c = (0b00000, 0b00000, 0b10000, 0b11000, 0b11100, 0b01100, 0b00110, 0b00110)
d = (0b01100, 0b01100, 0b00110, 0b00111, 0b00011, 0b00001, 0b00000, 0b00000)
e = (0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b11111, 0b11111, 0b00000)
f = (0b00110, 0b00110, 0b01100, 0b11100, 0b11000, 0b10000, 0b00000, 0b00000)

# lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
#               cols=20, rows=4, dotsize=8,
#               charmap='A02',
#               auto_linebreaks=True,
#               backlight_enabled=True)
#
# lcd.create_char(0, a)
# lcd.create_char(1, b)
# lcd.create_char(2, c)
# lcd.create_char(3, d)
# lcd.create_char(4, e)
# lcd.create_char(5, f)
#
#

path = 'img'
images = []
nama = []
# jabatan = []
myList = os.listdir(path)
listnama = []



check = datetime.now().strftime('%H:%M:%S')
tanggal = str(datetime.now().date())

file = pd.read_excel('praga_presensi.xlsx')
nama_file = 'praga_presensi.xlsx'

absenMasuk = time.strftime(time(7, 59, 59), '%H:%M:%S')
absenMasukClosed = time.strftime(time(10, 59, 59), '%H:%M:%S')
absenPulang = time.strftime(time(15, 0, 0), '%H:%M:%S')
absenPulangClosed = time.strftime(time(17, 59, 59), '%H:%M:%S')

for namaImg in myList:
    curImg = cv2.imread(f'{path}/{namaImg}')
    images.append(curImg)
    nama.append(os.path.splitext(namaImg)[0])
    # jabatan.append(os.path.splitext(namaImg)[0].split('-')[1])




# def lcdLoading():
#     lcd.write_string('\x00')
#     t.sleep(.1)
#     lcd.write_string('\x01')
#     t.sleep(.1)
#     lcd.write_string('\x02')
#     t.sleep(.1)
#     lcd.cursor_pos = (1, 2)
#     lcd.write_string('\x05')
#     t.sleep(.1)
#     lcd.cursor_pos = (1, 1)
#     lcd.write_string('\x04')
#     t.sleep(.1)
#     lcd.cursor_pos = (1, 0)
#     lcd.write_string('\x03')
#
#     lcd.cursor_pos = (0, 4)
#     lcd.write_string('MEMULAI')
#     t.sleep(.1)
#     lcd.cursor_pos = (1, 4)
#     lcd.write_string('SISTEM')
#     t.sleep(.2)
#     lcd.write_string('.')
#     t.sleep(.2)
#     lcd.write_string('.')
#     t.sleep(.2)
#     lcd.write_string('.')
#     t.sleep(.4)
#     lcd.clear()

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def gaji(jabatan):
    global denda
    if jabatan == 'SEKRETARIS DESA':
        gaji = 1800000
    elif jabatan == 'KAUR KEUANGAN':
        gaji = 1700000
    elif jabatan == 'KAUR UMUM' or jabatan == 'KASI':
        gaji = 1250000
    elif jabatan == 'KADUS':
        gaji = 1100000

    if datetime.today().weekday() != 4:
        if (check >= '08:00:00') & (check <= '08:30:59'):
            return 0
        elif (check >= '08:31:00') & (check <= '09:00:59'):
            return gaji * 0.5 / 100
        elif (check >= '09:01:00') & (check <= '09:30:59'):
            return gaji * 1 / 100
        elif (check >= '09:31:00') & (check <= '10:00:59'):
            return gaji * 1.5 / 100
        elif (check >= '10:01:00') & (check <= absenMasukClosed):
            return gaji * 2 / 100
        elif (check >= '14:30:00') & (check <= '15:30:00'):
            return 0
        elif (check >= '15:31:00') & (check <= '16:00:59'):
            return gaji * 0.5 / 100
        elif (check >= '16:01:00') & (check <= '16:30:59'):
            return gaji * 1 / 100
        elif (check >= '16:31:00') & (check <= '17:00:59'):
            return gaji * 1.5 / 100
        elif (check >= '17:01:00') & (check <= absenPulangClosed):
            return gaji * 2 / 100

    elif datetime.today().weekday() == 4:
        if (check >= '08:00:00') & (check <= '08:30:59'):
            return 0
        elif (check >= '08:31:00') & (check <= '09:00:59'):
            return gaji * 0.5 / 100
        elif (check >= '09:01:00') & (check <= '09:30:59'):
            return gaji * 1 / 100
        elif (check >= '09:31:00') & (check <= '10:00:59'):
            return gaji * 1.5 / 100
        elif (check >= '10:01:00') & (check <= absenMasukClosed):
            return gaji * 2 / 100
        elif (check >= '11:00:00') & (check <= '12:00:59'):
            return 0
        elif (check >= '12:01:00') & (check <= '12:30:59'):
            return gaji * 0.5 / 100
        elif (check >= '12:31:00') & (check <= '13:00:59'):
            return gaji * 1 / 100
        elif (check >= '13:10:00') & (check <= '13:30:59'):
            return gaji * 1.5 / 100
        elif (check >= '13:31:00') & (check <= absenPulangClosed):
            return gaji * 2 / 100
        elif (check >= absenPulangClosed):
            return gaji * 2 / 100



def pulang(nameDetect, check, frame):
    pulang = check
    nama = nameDetect.split('-')[0]
    jabatan = nameDetect.split('-')[1]

    label = test(image=frame,
                 model_dir='antispoofing/resources/anti_spoof_models/',
                 device_id=0)

    if label == 1:
        if nama not in listnama:
            listnama.append(nama)
            cek_datang = file.loc[(file.Nama == nama) & (file.Tanggal == tanggal) & file.Datang.isnull()]
            cek_nama = file.loc[(file.Nama==nama) & (file.Tanggal == tanggal)]
            if cek_nama.empty is True :
                if cek_datang.empty is True :
                    df_pulang = pd.DataFrame([[nama, jabatan, tanggal, '', pulang, gaji(jabatan)]],columns=['Nama', 'Jabatan', 'Tanggal', 'Datang', 'Pulang', 'Denda'])
                    res = pd.concat([file, df_pulang], ignore_index=True)
                    res.to_excel(nama_file, index=False)
                    # print(file)
                    # print(res)
                    # print('nama kosong & datang kosong')
            else:
                if cek_datang.empty is False:
                    file.loc[(file.Nama == nama) & (file.Tanggal == tanggal) & file.Datang.isnull() & file.Pulang.isnull(), ['Pulang','Denda']] = [pulang, gaji(jabatan)]
                    file.to_excel(nama_file, index=False)
                    # print(file)
                    # print('nama ada & datang kosong')
                    # ok
                else:
                    file.loc[(file.Nama == nama) & (file.Tanggal == tanggal) & file.Datang.notnull() & file.Pulang.isnull(), ['Pulang','Denda']] = [pulang,gaji(jabatan)]
                    file.to_excel(nama_file, index=False)
                    # print(file)
                    # print('nama ada & datang ada')
                    # ok



        cv2.rectangle(img, (150, 50), (510, 100), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, 'ABSEN PULANG', (200, 85),cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 2)
        print('absensi (wajah asli)')

    else:
        print('absensi (wajah palsu)')




def datang(nameDetect, check, frame):
    datang = check
    pulang = None
    nama = nameDetect.split('-')[0]
    jabatan = nameDetect.split('-')[1]

    label = test(image=frame,
                 model_dir='antispoofing/resources/anti_spoof_models/',
                 device_id=0)

    if label == 1:
        if nama not in listnama:
            listnama.append(nameDetect)

            df_datang = pd.DataFrame([[nama,jabatan, tanggal, datang, pulang, gaji(jabatan)]],
                               columns=['Nama','Jabatan', 'Tanggal', 'Datang', 'Pulang','Denda'])

            res = pd.concat([file, df_datang], ignore_index=True)

            res.to_excel(nama_file,  index=False)

        cv2.rectangle(img, (150, 50), (510, 100), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, 'ABSEN DATANG', (200, 85),
                    cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 2)
        print('absensi (wajah asli)')

    else:
        print('absensi (wajah palsu)')

encodeListKnown = findEncodings(images)


# print("Loading:")
# # animation = ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]
# animation = ["[■□□□□□□□□□]", "[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
# for i in range(len(animation)):
#     t.sleep(0.2)
#     sys.stdout.write("\r" + animation[i % len(animation)])
#     sys.stdout.flush()
# print("\n")
#
# print("Status:")
# # lcdLoading()
# print("[Encoding Selesai]")

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)




while True:
    # lcd.clear()
    success, img = cap.read()
    frame = img
    frameRe = cv2.resize(img, (800, 600))
    imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgSmall)
    encodeCurFrame = face_recognition.face_encodings(imgSmall, faceCurFrame)

    w, h, c = img.shape
    new_w = int(w * 1.5)
    new_h = int(h * 1.5)

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            nameDetect = nama[matchIndex].upper()

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, nameDetect, (x1 + 6, y2 - 6),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)

            jabatan = nameDetect.split('-')[1]

            if absenMasuk <= check <= absenMasukClosed:
                datang(nameDetect, check, frame)

            elif absenPulang <= check <= absenPulangClosed:
                pulang(nameDetect, check, frame)

    cv2.imshow('webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if check >= absenPulangClosed:
        for n in nama:
            alpha_nama = n.split('-')[0].upper()
            alpha_jabatan = n.split('-')[1].upper()
            cek_nama = file.loc[(file.Nama == alpha_nama) & (file.Tanggal == tanggal)]
            #
            if cek_nama.empty is True:
                df_alpha = pd.DataFrame([[alpha_nama, alpha_jabatan, tanggal, '', '', gaji(alpha_jabatan)*2]],columns=['Nama', 'Jabatan', 'Tanggal', 'Datang', 'Pulang', 'Denda'])
                res_alpha = pd.concat([file, df_alpha], ignore_index=True)
                res_alpha.to_excel(nama_file, index=False)



