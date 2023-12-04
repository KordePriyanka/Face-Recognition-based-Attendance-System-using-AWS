import boto3
import requests
import datetime
import time
import cv2



#Credentials----------------------------------------------------------------------------------
client = boto3.client('rekognition',
                    aws_access_key_id="YOUR_ACCESS_KEY",
                    aws_secret_access_key="YOUR_SECRET_ACCESS_KEY",
                    #aws_session_token="FwoGZXIvYXdzECEaDIYUDFobtJnX2oDJVCLBAYop3p7T11dVZL/rjE4nmQQNBQEgYMSXua9XMWaiSGT1v1Giv0j4Txt0883Mrmz4zAlN2RAfXPk4QK6MxHEuEamQ3U4AgrZ4qA4AVv+uvMuGLWmVPwqUk/uK61R/kE3cNN5Bs3qzWYOzZ22z1RB8IT8YDxS81Wz5tZT/rRBXEGODdV6oIR8LIYixYoyBfl3hPWxTpqS/IrOzTcFnFbuoLYZQvLH2IGzf087tsV2bL56CoX62V9eAbv8VORF1RlGowgIouvqB/AUyLXdmJoVk+HOLePDbLDlYvDU3e7po7lEVq9DW+Aa3vDoqnjqqCEy3WjQtPj8N5Q==",
                      region_name='ap-south-1')



#Capture images for every 1 hour and store the image with current date and time -----------------------------------------------------------------------------------
for j in range(0, 6):
    current_time = datetime.datetime.now().strftime("%d-%m-%y  %H-%M-%S ")
    print(current_time)
    camera = cv2.VideoCapture(0)
    

        
    while True:
        # Capture the video frame by frame
        ret, frame = camera.read()

        # Display the resulting frame
        cv2.imshow('frame', frame)
        # Check if the image needs to be captured
        if cv2.waitKey(1) & 0xFF == ord(' '):
            # Save the captured frame as an image
            cv2.imwrite('img/' + current_time + '.jpg', frame)
            print("Image captured!")
            # Reset the flag
            break

        # Check if the 'q' button is pressed to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()

   
    del (camera) 

#Send the captured image to AWS S3 Bucket--------------------------------------------------------------------------------------
    clients3 = boto3.client('s3', aws_access_key_id="YOUR_ACCESS_KEY",
                      aws_secret_access_key="YOUR_SECRET_ACCESS_KEY", region_name='ap-south-1')
    # clients3.upload_file("Hourly Class Images/"+current_time+'.jpg', 'add your S3 bucket name', current_time+'.jpg')

    clients3.upload_file("img/" + current_time + '.jpg', 'attendance-management-system', current_time + '.jpg')


    #Recoginze students in captured image ---------------------------------------------------------------------------------------
    image_path = 'img/' + current_time + '.jpg'
    with open(image_path,'rb') as source_image:
        source_bytes = source_image.read()
    print(type(source_bytes))

    print("Recognition Service")
    response = client.detect_custom_labels(
    
    #Update the Rokognition ARN with yours   
        
        ProjectVersionArn='arn:aws:rekognition:ap-south-1:413313710573:project/AttendancesManagement/version/AttendancesManagement.2023-11-07T14.29.14/1699347559923',


        Image={
            'Bytes': source_bytes
        },

    )

    print(response)
    if not len(response['CustomLabels']):
         print('Not identified')

    else:
        str = response['CustomLabels'][0]['Name']
        print(str)
        
        # Update the attendance of recognized student in DynamoDB by calling the API

        url = "https://62ct6a3ad3.execute-api.ap-south-1.amazonaws.com/Name/Attendfunction2" + str
        
        resp = requests.get(url)
        print("Attendence Mark Sucesssful")
        if resp.status_code==200:
            print("Success")

    time.sleep(3600)
