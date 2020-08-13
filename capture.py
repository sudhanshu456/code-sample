def capture():
	import cv2 
	import os
	key = cv2. waitKey(1)
	webcam = cv2.VideoCapture(0)
	while True:
	    try:
	        check, frame = webcam.read()
	        #print(check) #prints true as long as the webcam is running
	        #print(frame) #prints matrix values of each framecd 
	        cv2.imshow("Capturing", frame)
	        key = cv2.waitKey(1)
	        if key == ord('s'): 
	            cv2.imwrite('saved_img.jpg', img=frame)
	            webcam.release()
	            img_new = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
	            img_new = cv2.imshow("Captured Image", img_new)
	            cv2.waitKey(1650)
	            cv2.destroyAllWindows()
	            #print("Processing image...")
	            #img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
	            #print("Converting RGB image to grayscale...")
	            #gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
	            #print("Converted RGB image to grayscale...")
	            #print("Resizing image to 28x28 scale...")
	            #img_ = cv2.resize(gray,(28,28))
	            #print("Resized...")
	            #img_resized = cv2.imwrite(filename='saved_img-final.jpg', img=gray)
	            #img_resized = cv2.imwrite(filename='saved_img-final.jpg', img=img_)
	            print("Image saved!")
	            p=os.getcwd()
	            path_file=os.sep.join([p,'saved_img.jpg'])
	            return path_file
	        elif key == ord('q'):
	            print("Turning off camera.")
	            webcam.release()
	            print("Camera off.")
	            print("Program ended.")
	            cv2.destroyAllWindows()
	            break
	        
	    except(KeyboardInterrupt):
	        print("Turning off camera.")
	        webcam.release()
	        print("Camera off.")
	        print("Program ended.")
	        cv2.destroyAllWindows()
	        break
	return 0
