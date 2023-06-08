'''
Copyright (C)
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)#fulltext. 

For license issues, please contact:

Dr. Bing Ye
Life Sciences Institute
University of Michigan
210 Washtenaw Avenue, Room 5403
Ann Arbor, MI 48109-2216
USA

Email: bingye@umich.edu
'''



from .tools import extract_frames
from .traintestdetectors import TrainTestDetectors
from .detectanimals import DetectAnimals
from pathlib import Path
import wx
import os
import json
import shutil



the_absolute_current_path=str(Path(__file__).resolve().parent)



class WindowLv1_GenerateImages(wx.Frame):

	def __init__(self,title):

		super(WindowLv1_GenerateImages,self).__init__(parent=None,title=title,size=(1000,340))
		self.path_to_videos=None
		self.result_path=None
		self.framewidth=None
		self.t=0
		self.duration=0
		self.skip_redundant=1000

		self.dispaly_window()

	def dispaly_window(self):

		panel=wx.Panel(self)
		boxsizer=wx.BoxSizer(wx.VERTICAL)

		module_inputvideos=wx.BoxSizer(wx.HORIZONTAL)
		button_inputvideos=wx.Button(panel,label='Select the video(s) to generate\nimage examples',size=(300,40))
		button_inputvideos.Bind(wx.EVT_BUTTON,self.select_videos)
		self.text_inputvideos=wx.StaticText(panel,label='Can select multiple videos.',style=wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_END)
		module_inputvideos.Add(button_inputvideos,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		module_inputvideos.Add(self.text_inputvideos,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,10,0)
		boxsizer.Add(module_inputvideos,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,5,0)

		module_outputfolder=wx.BoxSizer(wx.HORIZONTAL)
		button_outputfolder=wx.Button(panel,label='Select a folder to store the\ngenerated image examples',size=(300,40))
		button_outputfolder.Bind(wx.EVT_BUTTON,self.select_outpath)
		self.text_outputfolder=wx.StaticText(panel,label='Will create a subfolder for each video under this folder.',style=wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_END)
		module_outputfolder.Add(button_outputfolder,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		module_outputfolder.Add(self.text_outputfolder,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(module_outputfolder,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,5,0)

		module_startgenerate=wx.BoxSizer(wx.HORIZONTAL)
		button_startgenerate=wx.Button(panel,label='Specify when generating image examples\nshould begin (unit: second)',size=(300,40))
		button_startgenerate.Bind(wx.EVT_BUTTON,self.specify_timing)
		self.text_startgenerate=wx.StaticText(panel,label='Default: at the beginning of the video(s).',style=wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_END)
		module_startgenerate.Add(button_startgenerate,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		module_startgenerate.Add(self.text_startgenerate,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(module_startgenerate,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,5,0)

		module_duration=wx.BoxSizer(wx.HORIZONTAL)
		button_duration=wx.Button(panel,label='Specify how long generating examples\nshould last (unit: second)',size=(300,40))
		button_duration.Bind(wx.EVT_BUTTON,self.input_duration)
		self.text_duration=wx.StaticText(panel,label='Default: lasts until the end of video(s).',style=wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_END)
		module_duration.Add(button_duration,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		module_duration.Add(self.text_duration,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(module_duration,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,5,0)

		module_skipredundant=wx.BoxSizer(wx.HORIZONTAL)
		button_skipredundant=wx.Button(panel,label='Specify how many frames to skip when\ngenerating two consecutive images',size=(300,40))
		button_skipredundant.Bind(wx.EVT_BUTTON,self.specify_redundant)
		self.text_skipredundant=wx.StaticText(panel,label='Default: generate an image example every 1000 frames.',style=wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_END)
		module_skipredundant.Add(button_skipredundant,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		module_skipredundant.Add(self.text_skipredundant,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(module_skipredundant,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,5,0)

		generate=wx.BoxSizer(wx.HORIZONTAL)
		cvat=wx.lib.agw.hyperlink.HyperLinkCtrl(panel,0,'To train Detectors, please annotate images with Roboflow.',URL='https://roboflow.com')
		button_generate=wx.Button(panel,label='Start to generate image examples',size=(300,40))
		button_generate.Bind(wx.EVT_BUTTON,self.generate_images)
		generate.Add(cvat,0,wx.ALIGN_CENTER_VERTICAL|wx.RIGHT,50)
		generate.Add(button_generate,0,wx.LEFT,50)
		boxsizer.Add(generate,0,wx.RIGHT|wx.ALIGN_RIGHT,90)
		boxsizer.Add(0,10,0)

		panel.SetSizer(boxsizer)

		self.Centre()
		self.Show(True)


	def select_videos(self,event):

		wildcard='Video files(*.avi;*.mpg;*.mpeg;*.wmv;*.mp4;*.mkv;*.m4v;*.mov)|*.avi;*.mpg;*.mpeg;*.wmv;*.mp4;*.mkv;*.m4v;*.mov'
		dialog=wx.FileDialog(self,'Select video(s)','','',wildcard,style=wx.FD_MULTIPLE)

		if dialog.ShowModal()==wx.ID_OK:
			self.path_to_videos=dialog.GetPaths()
			path=os.path.dirname(self.path_to_videos[0])
			dialog2=wx.MessageDialog(self,'Proportional resize the video frames?\nSelect "No" if dont know what it is.','(Optional) resize the frames?',wx.YES_NO|wx.ICON_QUESTION)
			if dialog2.ShowModal()==wx.ID_YES:
				dialog3=wx.NumberEntryDialog(self,'Enter the desired frame width','The unit is pixel:','Desired frame width',480,1,10000)
				if dialog3.ShowModal()==wx.ID_OK:
					self.framewidth=int(dialog3.GetValue())
					if self.framewidth<10:
						self.framewidth=10
					self.text_inputvideos.SetLabel('Selected '+str(len(self.path_to_videos))+' video(s) in: '+path+' (proportionally resize framewidth to '+str(self.framewidth)+').')
				else:
					self.framewidth=None
					self.text_inputvideos.SetLabel('Selected '+str(len(self.path_to_videos))+' video(s) in: '+path+' (original framesize).')
				dialog3.Destroy()
			else:
				self.framewidth=None
				self.text_inputvideos.SetLabel('Selected '+str(len(self.path_to_videos))+' video(s) in: '+path+' (original framesize).')
			dialog2.Destroy()

		dialog.Destroy()


	def select_outpath(self,event):

		dialog=wx.DirDialog(self,'Select a directory','',style=wx.DD_DEFAULT_STYLE)
		if dialog.ShowModal()==wx.ID_OK:
			self.result_path=dialog.GetPath()
			self.text_outputfolder.SetLabel('Generate image examples in: '+self.result_path+'.')
		dialog.Destroy()


	def specify_timing(self,event):

		dialog=wx.NumberEntryDialog(self,'Enter beginning time to generate examples','The unit is second:','Beginning time to generate examples',0,0,100000000000000)
		if dialog.ShowModal()==wx.ID_OK:
			self.t=float(dialog.GetValue())
			if self.t<0:
				self.t=0
			self.text_startgenerate.SetLabel('Start to generate image examples at the: '+str(self.t)+' second.')
		dialog.Destroy()


	def input_duration(self,event):

		dialog=wx.NumberEntryDialog(self,'Enter the duration for generating examples','The unit is second:','Duration for generating examples',0,0,100000000000000)
		if dialog.ShowModal()==wx.ID_OK:
			self.duration=int(dialog.GetValue())
			if self.duration!=0:
				self.text_duration.SetLabel('The generation of image examples lasts for '+str(self.duration)+' seconds.')
		dialog.Destroy()


	def specify_redundant(self,event):

		dialog=wx.NumberEntryDialog(self,'How many frames to skip?','Enter a number:','Interval for generating examples',15,0,100000000000000)
		if dialog.ShowModal()==wx.ID_OK:
			self.skip_redundant=int(dialog.GetValue())
			self.text_skipredundant.SetLabel('Generate an image example every '+str(self.skip_redundant)+' frames.')
		else:
			self.skip_redundant=1000
			self.text_skipredundant.SetLabel('Generate an image example every 10000 frames.')
		dialog.Destroy()


	def generate_images(self,event):

		if self.path_to_videos is None or self.result_path is None:

			wx.MessageBox('No input video(s) / output folder selected.','Error',wx.OK|wx.ICON_ERROR)

		else:

			do_nothing=True

			dialog=wx.MessageDialog(self,'Start to generate image examples?','Start to generate examples?',wx.YES_NO|wx.ICON_QUESTION)
			if dialog.ShowModal()==wx.ID_YES:
				do_nothing=False
			else:
				do_nothing=True
			dialog.Destroy()

			if do_nothing is False:
				print('Generating animal / object image examples...')
				for i in self.path_to_videos:
					extract_frames(i,self.result_path,framewidth=self.framewidth,start_t=self.t,duration=self.duration,skip_redundant=self.skip_redundant)
				print('Animal / object image generation completed!')                        



class WindowLv1_TrainDetectors(wx.Frame):

	def __init__(self,title):

		super(WindowLv1_TrainDetectors,self).__init__(parent=None,title=title,size=(1000,290))
		self.path_to_trainingimages=None
		self.path_to_annotation=None
		self.inference_size=640
		self.iteration_num=500
		self.detector_path=os.path.join(the_absolute_current_path,'detectors')
		self.path_to_detector=None

		self.dispaly_window()


	def dispaly_window(self):

		panel=wx.Panel(self)
		boxsizer=wx.BoxSizer(wx.VERTICAL)

		module_selectimages=wx.BoxSizer(wx.HORIZONTAL)
		button_selectimages=wx.Button(panel,label='Select the folder containing\nall the training images',size=(300,40))
		button_selectimages.Bind(wx.EVT_BUTTON,self.select_images)
		self.text_selectimages=wx.StaticText(panel,label='The folder storing all the images that your annotations were done on.',style=wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_END)
		module_selectimages.Add(button_selectimages,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		module_selectimages.Add(self.text_selectimages,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,10,0)
		boxsizer.Add(module_selectimages,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,5,0)

		module_selectannotation=wx.BoxSizer(wx.HORIZONTAL)
		button_selectannotation=wx.Button(panel,label='Select the *.json\nannotation file',size=(300,40))
		button_selectannotation.Bind(wx.EVT_BUTTON,self.select_annotation)
		self.text_selectannotation=wx.StaticText(panel,label='The annotation file should be in COCO instance segmentation format.',style=wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_END)
		module_selectannotation.Add(button_selectannotation,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		module_selectannotation.Add(self.text_selectannotation,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(module_selectannotation,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,5,0)

		module_inferencingsize=wx.BoxSizer(wx.HORIZONTAL)
		button_inferencingsize=wx.Button(panel,label='Specify the inferencing framesize\nfor the Detector to train',size=(300,40))
		button_inferencingsize.Bind(wx.EVT_BUTTON,self.input_inferencingsize)
		self.text_inferencingsize=wx.StaticText(panel,label='Must be divisible by 32. Larger size = higher accuracy but slower speed.',style=wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_END)
		module_inferencingsize.Add(button_inferencingsize,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		module_inferencingsize.Add(self.text_inferencingsize,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(module_inferencingsize,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,5,0)

		module_iterations=wx.BoxSizer(wx.HORIZONTAL)
		button_iterations=wx.Button(panel,label='Specify the iteration number\nfor the Detector training',size=(300,40))
		button_iterations.Bind(wx.EVT_BUTTON,self.input_iterations)
		self.text_iterations=wx.StaticText(panel,label='More iterations may yield higher accuracy but are slower and might also cause overfitting.',style=wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_END)
		module_iterations.Add(button_iterations,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		module_iterations.Add(self.text_iterations,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(module_iterations,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,10,0)

		button_train=wx.Button(panel,label='Start to train the Detector',size=(300,40))
		button_train.Bind(wx.EVT_BUTTON,self.train_detector)
		boxsizer.Add(button_train,0,wx.RIGHT|wx.ALIGN_RIGHT,90)
		boxsizer.Add(0,10,0)

		panel.SetSizer(boxsizer)

		self.Centre()
		self.Show(True)


	def select_images(self,event):

		dialog=wx.DirDialog(self,'Select a directory','',style=wx.DD_DEFAULT_STYLE)
		if dialog.ShowModal()==wx.ID_OK:
			self.path_to_trainingimages=dialog.GetPath()
			self.text_selectimages.SetLabel('Path to training images: '+self.path_to_trainingimages+'.')
		dialog.Destroy()


	def select_annotation(self,event):

		wildcard='Annotation File (*.json)|*.json'
		dialog=wx.FileDialog(self, 'Select the annotation file (.json)','',wildcard=wildcard,style=wx.FD_OPEN)
		if dialog.ShowModal()==wx.ID_OK:
			self.path_to_annotation=dialog.GetPath()
			f=open(self.path_to_annotation)
			info=json.load(f)
			classnames=[]
			for i in info['categories']:
				if i['id']>0:
					classnames.append(i['name'])
			self.text_selectannotation.SetLabel('Animal/object categories in annotation file: '+str(classnames)+'.')
		dialog.Destroy()


	def input_inferencingsize(self,event):

		dialog=wx.NumberEntryDialog(self,'Input the inferencing frame size\nof the Detector to train','Enter a number:','Divisible by 32',480,1,2048)
		if dialog.ShowModal()==wx.ID_OK:
			self.inference_size=int(dialog.GetValue())
			self.text_inferencingsize.SetLabel('Input inferencing frame size: '+str(self.inference_size)+'.')
		dialog.Destroy()
		

	def input_iterations(self,event):

		dialog=wx.NumberEntryDialog(self,'Input the iteration number\nfor the Detector training','Enter a number:','Iterations',200,1,2000)
		if dialog.ShowModal()==wx.ID_OK:
			self.iteration_num=int(dialog.GetValue())
			self.text_iterations.SetLabel('Input iteration number: '+str(self.iteration_num)+'.')
		dialog.Destroy()


	def train_detector(self,event):

		if self.path_to_trainingimages is None or self.path_to_annotation is None:

			wx.MessageBox('No training images / annotation file selected.','Error',wx.OK|wx.ICON_ERROR)

		else:

			do_nothing=False

			stop=False
			while stop is False:
				dialog=wx.TextEntryDialog(self,'Enter a name for the Detector to train','Detector name')
				if dialog.ShowModal()==wx.ID_OK:
					if dialog.GetValue()!='':
						self.path_to_detector=os.path.join(self.detector_path,dialog.GetValue())
						if not os.path.isdir(self.path_to_detector):
							stop=True
						else:
							wx.MessageBox('The name already exists.','Error',wx.OK|wx.ICON_ERROR)
				else:
					do_nothing=True
					stop=True
				dialog.Destroy()

			if do_nothing is False:

				TTD=TrainTestDetectors()
				TTD.train_the_detector(self.path_to_detector,self.path_to_trainingimages,self.path_to_annotation,inference_size=self.inference_size,iteration_num=self.inference_size)



class WindowLv1_TestDetectors(wx.Frame):

	def __init__(self,title):

		super(WindowLv1_TestDetectors,self).__init__(parent=None,title=title,size=(1000,290))
		self.detector_path=os.path.join(the_absolute_current_path,'detectors')
		self.path_to_detector=None
		self.animal_number=1
		self.path_to_video=None
		self.duration=0
		self.out_path=None

		self.dispaly_window()


	def dispaly_window(self):

		panel=wx.Panel(self)
		boxsizer=wx.BoxSizer(wx.VERTICAL)

		module_selectdetector=wx.BoxSizer(wx.HORIZONTAL)
		button_selectdetector=wx.Button(panel,label='Select a Detector\nto test',size=(300,40))
		button_selectdetector.Bind(wx.EVT_BUTTON,self.select_detector)
		self.text_selectdetector=wx.StaticText(panel,label='Select a trained Detector for testing.',style=wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_END)
		module_selectdetector.Add(button_selectdetector,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		module_selectdetector.Add(self.text_selectdetector,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,10,0)
		boxsizer.Add(module_selectdetector,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,5,0)

		module_selectvideo=wx.BoxSizer(wx.HORIZONTAL)
		button_selectvideo=wx.Button(panel,label='Select a\ntesting video',size=(300,40))
		button_selectvideo.Bind(wx.EVT_BUTTON,self.select_video)
		self.text_selectvideo=wx.StaticText(panel,label='Select a video for testing the Detector.',style=wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_END)
		module_selectvideo.Add(button_selectvideo,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		module_selectvideo.Add(self.text_selectvideo,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(module_selectvideo,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,5,0)

		module_duration=wx.BoxSizer(wx.HORIZONTAL)
		button_duration=wx.Button(panel,label='Specify the testing duration\n(unit: second)',size=(300,40))
		button_duration.Bind(wx.EVT_BUTTON,self.input_duration)
		self.text_duration=wx.StaticText(panel,label='Default: entire duration of the testing video.',style=wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_END)
		module_duration.Add(button_duration,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		module_duration.Add(self.text_duration,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(module_duration,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,5,0)

		module_outpath=wx.BoxSizer(wx.HORIZONTAL)
		button_outpath=wx.Button(panel,label='Select a folder to store\nthe annotated video',size=(300,40))
		button_outpath.Bind(wx.EVT_BUTTON,self.select_outpath)
		self.text_outpath=wx.StaticText(panel,label='This is the folder to store the annotated testing video.',style=wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_END)
		module_outpath.Add(button_outpath,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		module_outpath.Add(self.text_outpath,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(module_outpath,0,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
		boxsizer.Add(0,10,0)

		testanddelete=wx.BoxSizer(wx.HORIZONTAL)
		button_test=wx.Button(panel,label='Test the selected Detector',size=(300,40))
		button_test.Bind(wx.EVT_BUTTON,self.test_detector)
		button_delete=wx.Button(panel,label='Delete a Detector',size=(300,40))
		button_delete.Bind(wx.EVT_BUTTON,self.remove_model)
		testanddelete.Add(button_test,0,wx.RIGHT,50)
		testanddelete.Add(button_delete,0,wx.LEFT,50)
		boxsizer.Add(testanddelete,0,wx.RIGHT|wx.ALIGN_RIGHT,90)
		boxsizer.Add(0,10,0)

		panel.SetSizer(boxsizer)

		self.Centre()
		self.Show(True)


	def select_detector(self,event):

		detectors=[i for i in os.listdir(self.detector_path) if os.path.isdir(os.path.join(self.detector_path,i))]
		if '__pycache__' in detectors:
			detectors.remove('__pycache__')
		if '__init__' in detectors:
			detectors.remove('__init__')
		if '__init__.py' in detectors:
			detectors.remove('__init__.py')
		detectors.sort()

		dialog=wx.SingleChoiceDialog(self,message='Select a Detector to test',caption='Detector to test',choices=detectors)
		if dialog.ShowModal()==wx.ID_OK:
			detector=dialog.GetStringSelection()
			self.path_to_detector=os.path.join(self.detector_path,detector)
			self.text_selectdetector.SetLabel('Detector to test: '+detector+'.')
		dialog.Destroy()


	def select_video(self,event):

		wildcard='Video files(*.avi;*.mpg;*.mpeg;*.wmv;*.mp4;*.mkv;*.m4v;*.mov)|*.avi;*.mpg;*.mpeg;*.wmv;*.mp4;*.mkv;*.m4v;*.mov'
		dialog=wx.FileDialog(self,'Select a testing video','','',wildcard,style=wx.FD_OPEN)
		if dialog.ShowModal()==wx.ID_OK:
			self.path_to_video=dialog.GetPath()
			dialog1=wx.NumberEntryDialog(self,'','How many animals / objects in the video?','Animal number',1,1,100)
			if dialog1.ShowModal()==wx.ID_OK:
				self.animal_number=int(dialog1.GetValue())
			dialog1.Destroy()
			self.text_selectvideo.SetLabel('Path to testing video: '+self.path_to_video+' w/ '+str(self.animal_number)+' animals/obejcts.')
		dialog.Destroy()


	def input_duration(self,event):

		dialog=wx.NumberEntryDialog(self,'Enter the duration of testing','The unit is second:','Testing duration',0,0,100000000000000)
		if dialog.ShowModal()==wx.ID_OK:
			self.duration=int(dialog.GetValue())
			if self.duration!=0:
				self.text_duration.SetLabel('The testing duration is '+str(self.duration)+' seconds.')
		dialog.Destroy()


	def select_outpath(self,event):

		dialog=wx.DirDialog(self,'Select a directory','',style=wx.DD_DEFAULT_STYLE)
		if dialog.ShowModal()==wx.ID_OK:
			self.out_path=dialog.GetPath()
			self.text_outpath.SetLabel('Annotated video will be in: '+self.out_path+'.')
		dialog.Destroy()


	def test_detector(self,event):

		if self.path_to_detector is None or self.path_to_video is None or self.out_path is None:
			wx.MessageBox('No Detector / testing video / path to annotated video selected.','Error',wx.OK|wx.ICON_ERROR)
		else:
			TTD=TrainTestDetectors()
			TTD.test_the_detector(self.path_to_detector,self.path_to_video,self.out_path,duration=self.duration,animal_number=self.animal_number)


	def remove_model(self,event):

		detectors=[i for i in os.listdir(self.detector_path) if os.path.isdir(os.path.join(self.detector_path,i))]
		if '__pycache__' in detectors:
			detectors.remove('__pycache__')
		if '__init__' in detectors:
			detectors.remove('__init__')
		if '__init__.py' in detectors:
			detectors.remove('__init__.py')
		detectors.sort()

		dialog=wx.SingleChoiceDialog(self,message='Select a Detector to delete',caption='Delete a Detector',choices=detectors)
		if dialog.ShowModal()==wx.ID_OK:
			detector=dialog.GetStringSelection()
			dialog2=wx.MessageDialog(self,'Delete '+str(detector)+'?','CANNOT be restored!',wx.YES_NO|wx.ICON_QUESTION)
			if dialog2.ShowModal()==wx.ID_YES:
				shutil.rmtree(os.path.join(self.detector_path,detector))
			dialog2.Destroy()
		dialog.Destroy()


