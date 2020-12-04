# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 21:16:37 2020

@author: DINGMAN
"""

from tflite_runtime.interpreter import Interpreter
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont

class CrackDectectorLite:
    def __init__(self, filename):
        '''build tensorflow graph, load model'''        
        # Load TFLite model and allocate tensors.
        self.filename = filename
        self.interpreter = Interpreter(model_path='model.tflite')
        self.interpreter.allocate_tensors()
        # Get input and output tensors.
        self.input_index = self.interpreter.get_input_details()[0]["index"]
        self.output_index = self.interpreter.get_output_details()[0]["index"]

    #predict a single image using tf.lite interpreter
    def predict(self, img, print_class=False):
        '''predict the test image
        input: model, test_image(raw image), print_class(boolean)
        output: the predicted class(str)'''
        input_data = np.array(img, dtype=np.float32)
        self.interpreter.set_tensor(self.input_index, input_data)
        self.interpreter.invoke()
        classes = self.interpreter.get_tensor(self.output_index)
        print(classes)
        if classes[0]>0.5:
            class_name = 'P'
        else:
            class_name = 'N'
        if print_class:
            print(class_name)
        return class_name

    def crop_color_draw(self, a, predicted_class, positive_no):
    ## Put predicted class on the cropped image and label the image using different color
        if predicted_class == 'P':
            positive_no += 1
            color = (255,0, 0) #label crack crop as red
        else:
            color = (0, 255, 0) #otherwise green
        pil_a = Image.fromarray(a.astype(np.uint8)).convert('RGB')    
        b = np.zeros_like(a)
        b[:] = color
        pil_b = Image.fromarray(b.astype(np.uint8)).convert('RGB')
        add_img = Image.blend(pil_a, pil_b, alpha=0.2)
        draw = ImageDraw.Draw(add_img)
        font = ImageFont.truetype('Roboto-Regular.ttf', 30)
        draw.text((70,100), predicted_class, font=font, fill=color)
        add_img.save('test_a.jpg')
        return np.array(add_img), positive_no

    def predict_margin_h(self, img, margin_h, img_height, img_width, slide_w, positive_no):  
        if margin_h < 113:
            return None
        
        add_margin_h = np.zeros_like(img[(img_height-227):, :, :])
        for i in range(0, img_width, slide_w):
            a = img[(img_height-227):, i:i+227]
            h, w, c = a.shape
            if h == 227 and w == 227:                
                a_input = np.expand_dims(a, axis=0)
                a_input = a_input/255.
                predicted_class = self.predict(a_input)
            # save image
                add_img, positive_no = self.crop_color_draw(a, predicted_class, positive_no)
                add_margin_h[:, i:i+227, :] = add_img
                    
        return add_margin_h, positive_no

    def predict_margin_w(self, img, margin_w, img_height, img_width, slide_h, positive_no):
        if margin_w < 113:
            return None
        
        add_margin_w = np.zeros_like(img[:, (img_width-227):,:])
        for i in range(0, img_height, slide_h):
            a = img[i:i+227, (img_width-227):]
            h, w, c = a.shape
            if h == 227 and w == 227:                
                a_input = np.expand_dims(a, axis=0)
                a_input = a_input/255.
                predicted_class = self.predict(a_input)
                add_img, positive_no = self.crop_color_draw(a, predicted_class, positive_no)
                add_margin_w[i:i+227, :, :] = add_img
                
        return add_margin_w, positive_no
    

    def predict_tlite_real(self, filename, height=227, width=227, save_crops = False):
        img = Image.open(filename).convert('RGB')
        img = np.array(img, dtype=np.float32)
        img_height, img_width, channels = img.shape
        output_image = np.zeros_like(img)
        positive_no = 0
        condition = False
        k=0
        if img_height > 1500:
            slide_h = height
        else:
            slide_h = 150
        if img_width > 1500:
            slide_w = width
        else:
            slide_w = 150
            
        for i in range(0,img_height,slide_h):
            for j in range(0,img_width,slide_w):
                a = img[i:i+height, j:j+width]
                h, w, c = a.shape
                if h == 227 and w == 227:                
                    a_input = np.expand_dims(a, axis=0)
                    a_input = a_input/255.
                    predicted_class = self.predict(a_input)
                    add_img, positive_no = self.crop_color_draw(a, predicted_class, positive_no)
                    
                    file, ext = os.path.splitext(filename)
                    image_name = file.split('/')[-1]
                    folder_name = 'out_' + image_name
                    if save_crops:
                        if not os.path.exists(os.path.join('real_images', folder_name)):
                            os.makedirs(os.path.join('real_images', folder_name))
                        filename = os.path.join('real_images', folder_name,'img_{}.png'.format(k))
                        add_img = add_img.save(filename)
                
                    output_image[i:i+height, j:j+width,:] = add_img
                    k+=1
        margin_h = (img_height-227) % slide_h
        margin_w = (img_width-227) % slide_w
        call_margin_h = False
        call_margin_w = False

        if self.predict_margin_w(img, margin_w, img_height, img_width, slide_h, positive_no) != None:
            add_margin_w, positive_no = self.predict_margin_w(img, margin_w, img_height, img_width, slide_h, positive_no)        
            output_image[:, (img_width-227):,:] = add_margin_w
            call_margin_w = True
        else:
            add_margin_w = img[:,(img_width-margin_w):, :]
            output_image[:,(img_width-margin_w):, :] = add_margin_w
            
        if self.predict_margin_h(img, margin_h, img_height, img_width, slide_w, positive_no) != None:
            add_margin_h, positive_no = self.predict_margin_h(img, margin_h, img_height, img_width, slide_w, positive_no)        
            output_image[(img_height-227):,:,:] = add_margin_h
            call_margin_h = True
        else:
            add_margin_h = img[(img_height-margin_h):, :, :]
            output_image[(img_height-margin_h):,:,:] = add_margin_h
        if call_margin_w and call_margin_h:
            a = img[(img_height-227):, (img_width-227):,:]
            a_input = np.expand_dims(a, axis=0)
            a_input = a_input/255.
            predicted_class = self.predict(a_input)
            add_img, positive_no = self.crop_color_draw(a, predicted_class, positive_no)
            output_image[(img_height-227):, (img_width-227):,:] = add_img
                 
        ## Save output image
        if positive_no > 0:
            condition = True
        output_image = Image.fromarray(output_image.astype(np.uint8)).convert('RGB')
        output_image = output_image.save(os.path.join('static','scan_image', folder_name+ '.png'))
        return output_image, (condition, positive_no)

    def close(self):
        pass
