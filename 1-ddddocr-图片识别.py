import ddddocr

with open("code2.png", 'rb') as f:
    img_bytes = f.read()

ocr = ddddocr.DdddOcr(show_ad=False)
code = ocr.classification(img_bytes)

print(code)