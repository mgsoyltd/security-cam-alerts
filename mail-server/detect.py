import cv2
from imutils import resize
from os import path
import sys

def detect_people(imagePath, file=False, test=False):

    # Initializing the HOG person detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # Reading the Image
    image = cv2.imread(imagePath)

    # Resizing the Image
    image = resize(image, width=min(400, image.shape[1]))

    img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detecting all the regions in the
    # Image that has a pedestrians inside it
    (regions, weights) = hog.detectMultiScale(img_grey,
                                        winStride=(4, 4),
                                        padding=(4, 4),
                                        scale=1.05)

    count = len(regions)
    print("Found {0} people!".format(count))
    result = count > 0 
    confidence = 0 if len(weights) == 0 else max(weights)
    print("Confidence {}".format(confidence))

    if result and ( test or file ):
        # Drawing the regions in the Image
        for i, (x, y, w, h) in enumerate(regions):
            if weights[i] < 0.13:
                continue
            elif weights[i] > 0.13 and weights[i] <= 0.3:
                # Low confidence
                cv2.rectangle(image, (x, y),
                            (x + w, y + h),
                            (0, 0, 255), 2)     # Blue
            elif weights[i] > 0.3 and weights[i] <= 0.7:
                # Medium confidence
                cv2.rectangle(image, (x, y),
                            (x + w, y + h),
                            (50, 122, 255), 2)  # Light Blue
            else:   # > 0.7
                # High confidence
                cv2.rectangle(image, (x, y),
                            (x + w, y + h),
                            (0, 255, 0), 2)     # Green

        if file:
            # Write w/ regions back to file
            cv2.imwrite(imagePath, image)

        if test:
            # Showing the output Image
            cv2.imshow("Image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    # Return True on medium confidence detection
    return( result and confidence > 0.3 )


if __name__ == '__main__':
    argv = sys.argv
    file = len(argv) >= 3 and argv[2].lower() == "true"
    test = len(argv) == 4 and argv[3].lower() == "true"
    print(argv, file, test)
    detect_people(argv[1], file, test)
