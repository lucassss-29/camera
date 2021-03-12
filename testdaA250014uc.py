from pypylon import pylon
import cv2

"""
   This is an implementation for Basler daA2500-14uc camera, the 
   program depict how an Basler camera operation when requiring
   an image with prior set parameters.
   Note: By default, they will take only one photo and save it local
   for each shot. The user's just needs to call the 'BaslerdaA250014uc'
   class, set the parameters, call the 'captureImage' function to take 
   the image, and end by closing the camera 'closeCamera'.
   The demonstration end of this program will give you more details.
"""


class BaslerdaA250014uc:
    def __init__(self):
        '''
        Initializing the camera configuration'
        '''
        try:
            self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
            self.camera.Open()
            self.camera.PixelFormat = "RGB8"
            self.camera.BslColorSpaceMode.SetValue("sRGB")
            self.camera.SensorShutterMode.SetValue("Rolling")
            self.camera.GainAuto.SetValue("Off")
            self.camera.ExposureAuto.SetValue("Off")
            self.camera.BalanceWhiteAuto.SetValue("Off")
            self.camera.BslContrastMode.SetValue("Linear")
            self.camera.MaxNumBuffer = 500
            self.originSetting()
            self.converter = pylon.ImageFormatConverter()
            self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
            self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        except Exception as e:
            print('An exception occurred' + str(e))
            print(e.GetDescription())
            raise

    # comment out the function below in order to grab continuous images
    # def numberOfPic(self, num):
    #     '''
    #     WARNING: always set desired number of image before capture
    #     :param num:
    #     :return: None
    #     '''
    #     self.camera.StartGrabbingMax(num)

    def gain(self, gainValue):
        '''
        set GAIN value: 0 to 24 dB (step = 0.000001)
        :param gainValue:
        :return: None
        '''
        self.camera.Gain.SetValue(gainValue)

    def exposure(self, exposureValue):
        '''
        set EXPOSURE value: 10 to 1000000 us (step = 1)
        :param exposureValue:
        :return:
        '''
        self.camera.ExposureTime.SetValue(exposureValue)

    def brightness(self, brightnessValue):
        '''
        set BRIGHTNESS value: -1 to 1 (step = 0.01)
        :param brightnessValue:
        :return:
        '''
        self.camera.BslBrightness.SetValue(brightnessValue)

    def contrast(self, contrastValue):
        '''
        set CONTRAST value: -1 to 1 (step = 0.01)
        :param contrastValue:
        :return:
        '''
        self.camera.BslContrast.SetValue(contrastValue)

    def blackLevel(self, blackLevelValue):
        '''
        set BLACK_LEVEL value: 0 to 32 (step = 0.0001)
        :param blackLevelValue:
        :return:
        '''
        self.camera.BlackLevel.SetValue(blackLevelValue)

    def gamma(self, gammaValue):
        '''
        set GAMMA value: 0.25 to 2 (step = 0.001)
        :param gammaValue:
        :return:
        '''
        self.camera.Gamma.SetValue(gammaValue)

    def RGB(self, redValue=None, greenValue=None, blueValue=None):
        '''
        set RED, GREEN, RED value: 1 to 7.98 (step = 0.000001)
        :param redValue:
        :param greenValue:
        :param blueValue:
        :return: None
        '''
        if redValue:
            self.camera.BalanceRatioSelector.SetValue("Red")
            self.camera.BalanceRatio.SetValue(redValue)
        if greenValue:
            self.camera.BalanceRatioSelector.SetValue("Green")
            self.camera.BalanceRatio.SetValue(greenValue)
        if blueValue:
            self.camera.BalanceRatioSelector.SetValue("Blue")
            self.camera.BalanceRatio.SetValue(blueValue)

    def hue(self, hueValue):
        '''
        set HUE value: -180 to 180 (step = 1)
        :param hueValue:
        :return:
        '''
        self.camera.BslHueValue.SetValue(hueValue)

    def saturation(self, saturationValue):
        '''
        set SATURATION value: 0 to 4 (step = 0.001)
        :param saturationValue:
        :return: None
        '''
        self.camera.BslSaturationValue.SetValue(saturationValue)

    def sharpness(self, sharpnessValue):
        '''
        set SHARPNESS value: 0 to 1 (step = 0.000001)
        :param sharpnessValue:
        :return:
        '''
        self.camera.SharpnessEnhancement.SetValue(sharpnessValue)

    def originSetting(self):
        '''
        The original Basler preset
        :return: None
        '''
        self.camera.Gain.SetValue(1)
        self.camera.BlackLevel.SetValue(0)
        self.camera.Gamma.SetValue(1)
        self.camera.ExposureTime.SetValue(1246)
        self.camera.BalanceRatioSelector.SetValue("Red")
        self.camera.BalanceRatio.SetValue(1.297)
        self.camera.BalanceRatioSelector.SetValue("Green")
        self.camera.BalanceRatio.SetValue(1.063)
        self.camera.BalanceRatioSelector.SetValue("Blue")
        self.camera.BalanceRatio.SetValue(1)
        self.camera.BslHueValue.SetValue(0)
        self.camera.BslSaturationValue.SetValue(1)
        self.camera.BslContrast.SetValue(0)
        self.camera.BslBrightness.SetValue(0)

    def captureImage(self, path, name, format='.jpeg'):
        '''
        Capture image with name and save in path
        :param path:
        :param name:
        :param format:
        :return:
        '''
        self.camera.StartGrabbingMax(1)
        while self.camera.IsGrabbing():
            grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grabResult.GrabSucceeded():
                image = self.converter.Convert(grabResult)
                img = image.GetArray()
                imageName = path + name + format
                cv2.imwrite(imageName, img)
            grabResult.Release()

    def closeCamera(self):
        '''
        Close the camera
        :return:
        '''
        self.camera.Close()

# '''___Demonstration___'''
cam = BaslerdaA250014uc()
cam.exposure(5037)
cam.gamma(1.134)
cam.brightness(-0.1)
cam.contrast(0.14)
cam.sharpness(0.5)
cam.captureImage('/home/fossil/Documents/cameraPi/imageSource/Manual/inkSetting/', 'ink_circle_4')
cam.closeCamera()
