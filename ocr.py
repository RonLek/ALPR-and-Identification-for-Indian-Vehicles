states = ['AP', 'AR', 'AS', 'BR', 'CG', 'GA',
          'GJ', 'HR', 'HP', 'JH', 'KA', 'KL',
          'MP', 'MH', 'MN', 'ML', 'MZ', 'NL',
          'OD', 'PB', 'RJ', 'SK', 'TN', 'TS',
          'TR', 'UP', 'UK', 'WB', 'AN', 'CH',
          'DD', 'DL', 'JK', 'LA', 'LD', 'PY']

def resultplate(plate):
    result=""
    j=0
    for character in plate:
        if character.isalnum():
            result+=character
        if character.isdigit():
            j+=1
        else:
            j=0
        if j==4:
            break
    if j!=4:
        print('Couldn\'t extract number')
    else:
        while result[0:2] not in states and result!="":
            result=result[2:]
        if result=="":
            print('Couldn\'t Recognize Plate. Try with a different plate')
        else:
            return result

def preprocess(plate):
    plate = plate.replace('\n', '')
    plate = plate.replace('INDIA', '')
    plate = plate.replace('IND', '')
    plate = plate.replace('IN', '')
    return plate
    
def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    #with open('results.txt', 'w', encoding='utf8') as f:
        #result=""
        #for text in texts:
        #    result+=text.description
         #   result+='\n"{}"'.format(text.description)

            #vertices = (['({},{})'.format(vertex.x, vertex.y)
             #           for vertex in text.bounding_poly.vertices])

            #result+='bounds: {}'.format(','.join(vertices))
        #f.write(result)
    plate = preprocess(texts[0].description)
    plate = resultplate(plate)
    print(plate)
        

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

detect_text('numberplate.jpg')
