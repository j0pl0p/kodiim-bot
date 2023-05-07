from io import BytesIO
import torch
import cv2
from PIL import Image
import numpy as np
import requests


# Загрузка весовой модели
model_path = '/Users/egorurov/Desktop/Kod11m/best.pt'
yolo_path = '/Users/egorurov/Desktop/Kod11m/yolov5'
model = torch.hub.load(yolo_path, 'custom', path=model_path, source='local')

"""# Получение доступа к веб-камере
cap = cv2.VideoCapture(0)

# Обработка каждого кадра видеопотока
while True:
    # Получение кадра видеопотока
    ret, frame = cap.read()

    if frame is None:
        continue
    
    # Преобразование цветового пространства кадра
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Запуск детекции на кадре
    results = model(frame)
    
    # Получение рамок объектов
    boxes = results.xyxy[0].numpy()
    
    # Отрисовка рамок вокруг объектов
    for box in boxes:
        x1, y1, x2, y2, confidence, class_id = box
        
        # Отображение рамки только для объектов с высокой вероятностью
        if confidence > 0.1:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f'{class_id}, {confidence}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
    
    # Отображение результата на экране
    cv2.imshow('frame', frame)
    
    # Прерывание выполнения при нажатии клавиши "q"
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождение ресурсов
cap.release()
cv2.destroyAllWindows()"""



def check(link):
    print(link)
    response = requests.get(link)


    print(response.status_code)

    if response.status_code != 200:
        return [False, []]
        
    frame = Image.open(BytesIO(response.content))

    frame = np.asarray(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    results = model(frame)

    # Получение рамок объектов
    boxes = results.xyxy[0].numpy()

    faces = []
    
    # Отрисовка рамок вокруг объектов
    for box in boxes:
        x1, y1, x2, y2, confidence, class_id = box
        x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
        
        # Отображение рамки только для объектов с высокой вероятностью
        if confidence > 0.6:
            faces.append(frame[y1:y2, x1:x2])
    
    # Отображение результата на экране
    """cv2.imshow('frame', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()"""

    if len(faces) == 0:
        return [False, faces]
    
    else:
        return [True, faces]
    




check("http://localhost:8080")