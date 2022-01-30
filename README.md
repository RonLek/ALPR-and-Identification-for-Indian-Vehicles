# Automatic License Plate Detection and Identification for Indian Vehicles

<p align="center">
  <img  src="/results/result_gif.gif">
</p>

### Video Tutorials for Running the Code

**Part 1 - https://drive.google.com/open?id=1n5qZgEIDQEoyE0VV5S0fuPEHKPWz4Mol**

**Part 2 - https://drive.google.com/open?id=1z2_BK1dVoNp1NRTqmirddaLScGjDdaOc**

### Introduction
Automatic number-plate recognition (ANPR; see also other names below) is a technology that uses optical character recognition on images to read vehicle registration plates to create vehicle location data.

In this repository we build a web application to automatically detect and identify vehicles and vehicle owners based on their number plates. The application is built in Node.js and a MongoDB backend is used. We plan to deploy the application on Docker to make it robust to run any machine. The model is based on [YOLOv3](https://github.com/AlexeyAB/darknet) and is trained to detect number plates in a variety of scenarios including but not limited to - multiple vehicles in a single frame and videos shot in low light.

The model is built taking into consideration the highest accuracy achievable without compromising on speed. It has been trained on more than 2000 images annotated manually.

#### Important

**Since the weight files are too big to bypass the GitHub upload limit (100 MB) we have decided to place the Detection model on Google Drive. Run the `training_sih.ipynb` and `test_sih.ipynb` files for training and testing the model respectively**

Link to Jupyter Notebooks - https://drive.google.com/drive/folders/1JCh9v5bzPIMDWtKUpAaCH3i2glOkW8iu?usp=sharing

#### darknet folder

The video shows you need credentials to the Google Drive to access a folder named `darknet`. This folder is just the darknet folder [here](https://github.com/AlexeyAB/darknet). Clone the contents of this repository into your Drive and you should be good to go. Follow everything else as mentioned in the video. In case of errors refer ipynb cell logs or raise an issue within this GitHub repository.

## Part 1 - Detection

### Training
`training_sih.ipynb` is the Jupyter notebook which contains the code used to train the model. It can be run on [Google Colab](https://colab.research.google.com/) or locally using [Anaconda](https://www.anaconda.com/). (When running using Anaconda make sure you have the `project_sih` folder from the Google Drive placed correctly in the path.)

If you don't wish to train the model from the beginning and are looking for a pretrained model `yolo-obj_best.weights` (Stored in Google Drive/project_sih/darknet/build/darknet/x64/backup - [Direct Link](https://drive.google.com/drive/folders/1C4FuPq-L1jv0S9yAM5Zt-Hquv1yZCJxw?usp=sharing)) contains pretrained weights to initialize the model and test directly. 

### Dataset
The model has been trained on more than 2500 images. About 1000 images were taken for the dataset from the paper - [A Robust Real-Time Automatic License Plate Recognition Based on the YOLO Detector by Laroca *et.al.*](https://ieeexplore.ieee.org/document/8489629) and a lot of images were manually clicked for odd and more difficult cases. We also scraped images from Google, meticulously selecting unique and difficult-to-detect images to make the model more robust to different kinds of vehicles and scenarios.

### Testing
The `yolo-obj_best.weights` is the weights file which `test_sih.ipynb` uses to test our model against images and videos. The following parts show how to test on images and videos.

**Testing on Images**
* Upload your image to `project_sih/darknet/test_videos_images` in the Google Drive.
* Change `image3.jpg` to the name of your image file in the in the following section in the "Test on Image" section.

```python
# At the end of the line, there is image3.jpg which can be replaced by any image of your choice. (Note: The image to be tested must be placed inside /darknet/test_videos_images)~~~
# Image name must not have spaces eg. 'image 1.jpg' is not allowed.

%cd /myDrive
!./darknet detector test /myDrive/build/darknet/x64/data/obj.data  /myDrive/build/darknet/x64/cfg/yolo-obj.cfg  /myDrive/build/darknet/x64/backup/yolo-obj_best.weights   /myDrive/test_videos_images/image3.jpg
```
* The resulting image with the bounding box is stored as `predictions.jpg` in `project_sih/darknet`

**Testing on Videos**
* Upload your test video to `project_sih/darknet/test_videos_images` either manually or on running the Video upload code block in the Test on Video section.
* Rename your video to "video.mp4" before running the block with the following code:
```
# After uploading the video, replace your video file name with 'video.mp4' written in below code. Then, run this cell.
# Video name must not have spaces eg. 'video 1.jpg' is not allowed.

%cd /myDrive
!./darknet detector demo /myDrive/build/darknet/x64/data/obj.data  /myDrive/build/darknet/x64/cfg/yolo-obj.cfg  /myDrive/build/darknet/x64/backup/yolo-obj_best.weights -dont_show  /myDrive/test_videos_images/video.mp4 -i 0 -out_filename res.avi
```

### Detection Results

A insight of the results obtained on the dataset provided by MixORG:

<p align="center">
  <img  src="/results/result_dataset_gif.gif">
</p>

**Additional results of our model**:

![](/results/result1.jpg)
![](/results/result2.jpg)
![](/results/result3.jpg)

## Part 2 - Optical Character Recognition

### Image Preprocessing

Once the number plates have been successfully detected, they are cropped from the image using their bounding box coordinates and saved in the `project_SIH/darknet/result_img` directory. Image processing operations are applied to convert the image to gray scale, sharpen it and enhance it.

![Cropped Plate](/results/croppedplate.jpg)
![Enhanced Plate](/results/enhancedplate.jpg)

### Optical Character Recognition

* Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the path the `gcloudapikey.json` file. For explicit instructions on how to do this follow the steps [here](https://cloud.google.com/vision/docs/quickstart-cli#before-you-begin). 

* Make sure you have the Google Cloud Vision python library installed and added to your PATH. If not, execute the following command:
```
pip install google-cloud-vision
```

* Once this has been achieved run the `ocr.py` file changing the argument of the *detect_text()* method to the path of the cropped number plate image file.

**Our method can efficiently detect number plates in more than 50 different languages as shown below**

![OCR Hindi Result](/results/ocrhindiresult.jpg)

The final result is the trimmed number plate which will be stored in the MongoDB database.

![OCR Final](/results/ocrfinal.png)

## Part 3 - Web Application (TBI)
The number plate detected by the model and recognized by the OCR engine is now stored in the MongoDB database. The appication built would have a Node.js backend and would be deployed using Docker. The `vehicle.py` script located in `scripts/vehicle.py` smartly (it bypasses the captcha on the website ;) ) fetches all the vehicle details such as Vehicle Owner Name, vehicle color, chassis number, PUC, Insurance and other details. 

Make sure you have the dependencies installed and have changed the paths to the webdriver appropriately. Execute the script as follows replacing the "Number_plate_without_spaces" with the entire number plate:

```
python vehicle.py Number_plate_without_spaces
```

We plan to monetize this application by providing premium features to the users (residents of a society). 

The premium features include the following:
* We've all been through the problem when the trash collecting van arrives and we miss it, or when the milkman arrives but you're not prepared with how much milk you need for that day, or when you're expecting a courier and are not home and don't know when the postman would arrive so that you could call your neighbor. We provide a solution to these problems for the premium subscribers to recieve a notification everytime when daily utility services like postman, milkman or trash-collecting van arrives by storing the numbers of their vehicles in our database after detection.

* Ever caught by the traffic police and found the your insurance and PUC have expired? With our app, we provide the solution to this problem! Every time your PUC or Insurance expires, a SMS/Email is sent to the resident to renew it. No need to get scared of the cop anymore (Don't drink and drive though, the application doesn't help in that case.)

Other features include:
* Timing visitors that enter into the society - Any vehicle not stored in the database will be tagged as "Visitor" and would be set with a 24 hour timer unless it leaves, after which the security guard would be alerted along with the details of the vehicle extracted from VAHAN.

* Guest Additions - All residents would have the option to feed in certain vehicles as guest number plates. The application would tag such plates with the "Guest" tag and no timer limit would be set for these vehicles thus distinguishing them from visitors.


