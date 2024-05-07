# **PISAHKAN KTP: Indonesian ID Card (KTP) Information Segmentation**

![Image](./assets/OIG1.jpg)

## **About**
`pisahkan_ktp` is a Python function that extracts province, NIK, and personal information from an image of an Indonesian National Identity Card (KTP). It utilizes image processing techniques to locate and isolate relevant sections of the KTP image, then extracts text data accurately. The extracted information is returned in a structured format, facilitating further processing or integration into other applications.

## **Requirements**
- Python 3.7 or Higher
- numpy
- opencv-python
- opencv-contrib-python
- pythonRLSA

## **Key Features**
- Extracts province, NIK, and personal information from Indonesian National Identity Card (KTP) images.
- Utilizes image processing techniques to locate and isolate relevant sections accurately.
- Returns extracted information in a structured format for easy integration and further processing.

## Usage
### Manual Installation via Github
1. Clone Repository
    ```
    git clone https://github.com/hanifabd/pisahkan-ktp
    ```
2. Installation
    ```
    cd pisahkan-ktp && pip install .
    ```
### Installation Using Pip
1. Installation
    ```sh
    pip install pisahkan-ktp
    ```
### Inference
1. Usage
    ```py
    from pisahkan_ktp.ktp_segmenter import segmenter

    image_path = "./tests/sample.jpg"
    result = segmenter(image_path)
    print(result)
    ```

3. Result
    ```json
    {
        "image": [originalImage],
        "provinsiArea": [segmented_provinsi_img_matrix_list],
        "nikArea": [segmented_nik_img_matrix_list],
        "detailArea": [segmented_detail_img_matrix_list],
    }
    ```

4. Preview
    - Provinsi Area Cropped
        
        ![provinsi](./assets/8-5-provinsi.jpg)
    
    - NIK Area Cropped
        
        ![nik](./assets/8-6-nik.jpg)

    - Detail Area Cropped
        
        ![detail](./assets/8-7-detail.jpg)