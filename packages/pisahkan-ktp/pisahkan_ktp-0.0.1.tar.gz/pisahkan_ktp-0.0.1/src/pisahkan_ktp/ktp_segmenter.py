import cv2
import src.pisahkan_ktp.ktp_helper as ktp_helper

def segmenter(image_path):
    '''
     This function identifies and isolates sections of Indonesian identity cards from images. 
     By detecting text and photo areas, it creates boundaries for province, nik, and personal information.
    '''
    assert isinstance(image_path, str), "Tokens can be str() type only"

    # Original Image
    originalImage, provinsiArea, nikArea, detailArea = ktp_helper.prepareRecognitionArea(image_path)

    # Preprocessed Image
    provinsiAreaPreprocessed = ktp_helper.preprocessRecognitionArea(provinsiArea)
    nikAreaPreprocessed = ktp_helper.preprocessRecognitionArea(nikArea)
    detailAreaPreprocessed = ktp_helper.preprocessRecognitionArea(detailArea)

    # Pattern Image
    provinsiAreaPattern = ktp_helper.findTextPattern(provinsiAreaPreprocessed, "provinsi")
    nikAreaPattern = ktp_helper.findTextPattern(nikAreaPreprocessed, "nik")
    detailAreaPattern = ktp_helper.findTextPattern(detailAreaPreprocessed, "detail")

    # Draw bounding boxes on the original image
    segmented_provinsi = []
    boundingBoxesRowsProvinsi = ktp_helper.provinsiCreateBoudingBox(provinsiAreaPattern, 450)
    for bbox in boundingBoxesRowsProvinsi:
        x1, y1, x2, y2 = bbox
        segmented_provinsi.append(provinsiArea[y1:y2, x1:x2])

    segmented_nik = []
    boundingBoxesRowsNIK = ktp_helper.nikCreateBoudingBox(nikAreaPattern, 450)
    for bbox in boundingBoxesRowsNIK:
        x1, y1, x2, y2 = bbox
        segmented_nik.append(nikArea[y1:y2, x1:x2])

    segmented_detail = []
    boundingBoxesRowsDetail = ktp_helper.detailCreateBoudingBox(detailAreaPattern, 450)
    for bbox in boundingBoxesRowsDetail:
        x1, y1, x2, y2 = bbox
        segmented_detail.append(detailArea[y1:y2, x1:x2])

    return {
        "image": [originalImage],
        "provinsiArea": segmented_provinsi,
        "nikArea": segmented_nik,
        "detailArea": segmented_detail,
    }
        