import cv2
import numpy as np
import speech_recognition as sr


punkty = []
processed_image = None

r=sr.Recognizer()

def getText():
    with sr.Microphone() as source:
        try:
            
            audio=r.listen(source)
            text=r.recognize_google(audio, language='pl-PL')
            if text!="":
                return text
            return 0
        except:
            return 0

def mouse_handler(event, x, y, flags, param):
    global processed_image
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(punkty) < 4:
            punkty.append((x, y))
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow("Image", image)
        if len(punkty) == 4:
            processed_image = process_image()

def process_image():
    width, height = 1400, 2000
    dst_punkty = np.array([[0, 0], [width-1, 0], [width-1, height-1], [0, height-1]], dtype=np.float32)
    src_punkty = np.array(punkty, dtype=np.float32)
    matrix = cv2.getPerspectiveTransform(src_punkty, dst_punkty)
    warped = cv2.warpPerspective(orig_image, matrix, (width, height))
    cv2.namedWindow("Warped Image", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Warped Image", 800, 600)
    cv2.imshow("Warped Image", warped)
    
    return warped

print("Aby rozpoczac powiedz 'start' aby przerwa powiedz 'stop' ")
while True:
    txt=getText()
    if not txt==0:
        print(txt)
        
        break
    else:
        print("nie udalo sie rozpoczac, wlacz program jescze raz")  
        continue

if txt=="start":
    print("Powiedz nazwe zdjecia")
    while True:
        txt=getText()
        if not txt==0:
            print(txt)
        
            break
        else:
            print("nie udalo sie pobrac nazwy zdjecia")  
            continue
    nazwazdjecia="D:/pobrane/studia/zdjeciawma/"+txt+".jpg"
    image = cv2.imread(nazwazdjecia)
    if image is None:
        print("nie pobrano zdjecia, zresetuj program")
    else:
        orig_image = image.copy()

        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Image", 800, 600)

        cv2.imshow("Image", image)
        cv2.setMouseCallback("Image", mouse_handler)

        
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        

        zdjecie = processed_image if processed_image is not None else image
        zdjecie2 = zdjecie.copy()
        ##################################################################

        hsv = cv2.cvtColor(zdjecie, cv2.COLOR_BGR2HSV)
        cv2.namedWindow("hsv", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("hsv", 800, 600)
        cv2.imshow("hsv", hsv)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        jasnyczer_zakres1 = (0, 120, 80)
        ciemnyczerowny_zakres1 = (3, 255, 255)

        maska1 = cv2.inRange(hsv, jasnyczer_zakres1, ciemnyczerowny_zakres1)

        jasnyczer_zakres2 = (170, 120, 80)
        ciemnyczerowny_zakres2 = (180, 255, 230)

        maska2 = cv2.inRange(hsv, jasnyczer_zakres2, ciemnyczerowny_zakres2)

        maska = maska1 + maska2
        czerwone = cv2.bitwise_and(zdjecie, zdjecie, mask=maska)

        cv2.namedWindow("Czerwone", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Czerwone", 800, 600)
        cv2.imshow("Czerwone", czerwone)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        mask_morph = cv2.morphologyEx(maska, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        mask_morph = cv2.morphologyEx(mask_morph, cv2.MORPH_DILATE, np.ones((5, 5), np.uint8))
        mask_morph = cv2.morphologyEx(mask_morph, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

        wynik_morph = cv2.bitwise_and(zdjecie, zdjecie, mask=mask_morph)

        cv2.namedWindow("Wynik Morph", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Wynik Morph", 800, 600)
        cv2.imshow("Wynik Morph", wynik_morph)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        krawedzie = cv2.Canny(wynik_morph, 200, 300)
        kontury, _ = cv2.findContours(krawedzie, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        min_obaszar = 25000
        limit_proporcji_dol = 0.7
        limit_proporcji_gora= 1.3

        kontury_duze = []
        for elementy in kontury:
            if cv2.contourArea(elementy) > min_obaszar:
        
                x, y, width, height = cv2.boundingRect(elementy)
                if height != 0:
                    proporcja = width / height
                    if (proporcja >= limit_proporcji_dol and proporcja<= limit_proporcji_gora):
                        kontury_duze.append(elementy)
        #cv2.drawContours(zdjecie, kontury_duze, -1, (255, 0, 0), 3)
        kier = False
        karo = False

        for kontur_pom in kontury_duze:
            approx = cv2.approxPolyDP(kontur_pom, 0.03 * cv2.arcLength(kontur_pom, True), True)
            if len(approx) == 6:
                cv2.drawContours(zdjecie, [approx], 0, (255, 0, 0), 4)
                kier = True
            elif len(approx) == 4:
                cv2.drawContours(zdjecie, [approx], 0, (255, 0, 0), 4)
                karo = True
            print(len(approx))

        cv2.namedWindow("Znalezione kontury", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Znalezione kontury", 800, 600)
        cv2.imshow("Znalezione kontury", zdjecie)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        if kier:
            print("Na zdjeciu znaleziono kiera")
        if karo:
            print("Na zdjeciu znaleziono karo")
    

        hsv=cv2.cvtColor(zdjecie2,cv2.COLOR_BGR2HSV)

        czarny_dol = (0, 0, 0)
        czarny_gora = (180, 255, 100)

        maska1_cz = cv2.inRange(hsv, czarny_dol, czarny_gora)


        maska_cz = maska1_cz
        czarne = cv2.bitwise_and(zdjecie2, zdjecie2, mask=maska_cz)

        cv2.namedWindow("Czarne", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Czarne", 800, 600)
        cv2.imshow("Czarne", czarne)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        mask_morph_cz = cv2.morphologyEx(maska_cz, cv2.MORPH_OPEN, np.ones((5,5),np.uint8))
        mask_morph_cz = cv2.morphologyEx(mask_morph_cz, cv2.MORPH_DILATE, np.ones((9,9),np.uint8))
        mask_morph_cz = cv2.morphologyEx(mask_morph_cz, cv2.MORPH_CLOSE, np.ones((5,5),np.uint8))

        wynik_morph_cz = cv2.bitwise_and(zdjecie2, zdjecie2, mask=mask_morph_cz)

        cv2.namedWindow("Wynik Morph czarnej", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Wynik Morph czarnej", 800, 600)
        cv2.imshow("Wynik Morph czarnej", wynik_morph_cz)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        krawendzie_cz = cv2.Canny(wynik_morph_cz, 200, 300)

        kontury_cz, _ = cv2.findContours(krawendzie_cz, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        min_obaszar_cz = 25000
        kontury_duze_cz = []
        for elementy in kontury_cz:
            if cv2.contourArea(elementy) > min_obaszar_cz:
        
                x, y, width, height = cv2.boundingRect(elementy)
                if height != 0:
                    proporcja = width / height
                    proporcja = abs(proporcja)
                    if (proporcja >= limit_proporcji_dol and proporcja<= limit_proporcji_gora):
                        kontury_duze_cz.append(elementy)

        #cv2.drawContours(zdjecie2, kontury_duze_cz, -1, (255, 0, 0), 3)


        # cv2.drawContours(zdjecie2, contury_duze_cz, -1, (0, 255, 0), 3)
        # cv2_imshow (zdjecie2)

        pik=False
        trefl=False

        for kontury_pom in kontury_duze_cz:

            approx = cv2.approxPolyDP(kontury_pom, 0.02*cv2.arcLength(kontury_pom, True), True)
            if len(approx) == 9:
              cv2.drawContours(zdjecie2, [approx], 0, (255, 0, 0), 4)
              pik=True
            if len(approx) ==14:
              cv2.drawContours(zdjecie2, [approx], 0, (255, 0, 0), 4)
              trefl=True
            # print(len(approx))

        cv2.namedWindow("Znalezione kontury czarne", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Znalezione kontury czarne", 800, 600)
        cv2.imshow("Znalezione kontury czarne", zdjecie2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        if pik==True:
          print("na zdjeciu znaleziono pika")
        if trefl==True:
          print("na zdjeciu znaleziono trefla")
if txt=="stop":
    print ("koniec programu")
