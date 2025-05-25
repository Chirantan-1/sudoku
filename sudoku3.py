from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import base64
from selenium.webdriver.common.keys import Keys
import time
import keyboard
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

def s(p, a=0, b=0):
        global st
        if a == 9:
            return True
        elif b == 9:
            return s(p, a+1, 0)
        elif p[a][b] != 0:
            return s(p, a, b+1)
        else:
            for k in range(1, 10):
                if (k not in p[a]) and (k not in [p[x][b] for x in range(0, 9)]) and (k not in [p[i][j] for i in range(a // 3 * 3, a // 3 * 3 + 3) for j in range(b // 3 * 3, b // 3 * 3 + 3)]):
                    p[a][b] = k
                    st += str(k)
                    if s(p, a, b+1):
                        return True
                    p[a][b] = 0
                    st = st[:-1]
            return False

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://sudoku.com') 

print(1)
time.sleep(5)
canvas = driver.find_element(By.CSS_SELECTOR, '#game canvas')

data_url = driver.execute_script("return arguments[0].toDataURL('image/png');", canvas)
image_data = base64.b64decode(data_url.split(',')[1])

with open('canvas_image.png', 'wb') as f:
    f.write(image_data)

img = cv2.imread("C:/Users/*****/Documents/python/canvas_image.png")
img = cv2.resize(img, (630, 630))

p = []
for i in range(9):
    row = []
    for j in range(9):
        cell = img[i*70:(i+1)*70, j*70:(j+1)*70]
        cell = cell[10:60, 10:60]
        gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (100, 100))
        blur = cv2.GaussianBlur(resized, (3, 3), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)


        denoised = cv2.fastNlMeansDenoising(thresh, None, 30, 7, 21)
        cv2.imshow("IMage", denoised)
        cv2.waitKey(100)
        cv2.destroyAllWindows()
        config = '--psm 13 --oem 3 -c tessedit_char_whitelist=123456789'
        digit = pytesseract.image_to_string(denoised, config=config).strip()
        row.append(int(digit[0]) if digit.isdigit() else 0)
    p.append(row)


print(p)
ans = p
st = ""

s(ans)
print(ans)

ans = [j for i in ans for j in i]
print(ans)

for i, num in enumerate(ans):
    keyboard.press_and_release(str(num))
    time.sleep(0.05)
    keyboard.press_and_release('right')
    time.sleep(0.05)
    
    
    if (i + 1) % 9 == 0:
        keyboard.press_and_release('down')
        time.sleep(0.05)
        for _ in range(9):
            keyboard.press_and_release('left')
            time.sleep(0.05)

time.sleep(100)
driver.quit()

