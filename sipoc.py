
import FreeCAD
App=FreeCAD





#-------------------------------
import FreeCAD
import PySide
from PySide import QtCore, QtGui, QtSvg
from PySide.QtGui import * 


def say(s):
		FreeCAD.Console.PrintMessage(str(s)+"\n")
def saye(s):
		FreeCAD.Console.PrintError(str(s)+"\n")
		
vers='0.1'
saye("mycomp 4")
saye(vers)


def dlge(msg):
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Critical,u"Error Message",msg )
    diag.setWindowFlags(PySide.QtCore.Qt.WindowStaysOnTopHint)
    diag.exec_()


import os
import re,numpy

try:
	__dir__ = os.path.dirname(__file__)
	say(__dir__)
	say(__file__)
except:
	__dir__='/usr/lib/freecad/Mod/mylib'

import PySide
from PySide import QtCore, QtGui, QtSvg
from PySide.QtGui import * 
from PySide.QtCore import * 

class MyWidget(QtGui.QWidget):
	def __init__(self, *args):
		QtGui.QWidget.__init__(self, *args)

		self.vollabel = QtGui.QLabel('Volume')
		self.volvalue = QtGui.QLineEdit()
		self.checkBox = QtGui.QCheckBox()

		self.pushButton02 = QtGui.QPushButton()
		self.pushButton02.clicked.connect(self.on_pushButton02_clicked) 
		self.pushButton02.setText("Hide me")

		self.listWidget = QListWidget() 
		for i in range(10):
			item = QListWidgetItem("List Item %i" % i)
			self.listWidget.addItem(item)

		self.combo = QtGui.QComboBox(self)
		for i in range(10):
			self.combo.addItem("Combo Item %i" % i)

		layout = QtGui.QGridLayout()
		layout.addWidget(self.vollabel, 0, 0)
		layout.addWidget(self.volvalue, 0, 1)
		layout.addWidget(self.checkBox, 0, 2)
		layout.addWidget(self.pushButton02, 5, 0,1,4)
		layout.addWidget(self.listWidget, 3, 0,1,4)
		layout.addWidget(self.combo, 4, 0,1,4)

		self.setLayout(layout)
		self.setWindowTitle("Comp Dialog")

	def on_pushButton02_clicked(self):
		pass
		self.hide()





def createComp(name='MyComp', objlinks=[],liste=[]):
	obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython",name)
	
	
	_Comp(obj)
	_ViewProviderComp(obj.ViewObject)
	#obj.execute2=updater
	
	c3=obj
	c3.addProperty("App::PropertyStringList","execute3","2 MyCTL","")
	c3.execute3=['say("hallo")']
	c3.Proxy.updater=True
	c3.addProperty("App::PropertyStringList","propliste","2 MyCTL","")
	c3.propliste=[]
	 
	#c3.addProperty("App::PropertyLink",'link',"MyProps","")
	#c3.link=FreeCAD.getDocument("comp2").getObject("Box")
	while objlinks.__len__() > 1: 
		key=objlinks.pop(0)
		val=objlinks.pop(0)
		say(key)
		say(val)
		c3.addProperty("App::PropertyLink",key,"3 MyParts","")
		s='c3.'+key+'=FreeCAD.ActiveDocument.getObject(val)'
		say(s)
		exec(s)
	propliste=[]
	while liste.__len__() > 1: 
		key=liste.pop(0)
		val=liste.pop(0)
		say(key)
		say(val)
		propliste.append(key)
		say(propliste)
		#say(val.__class__)
		if val.__class__ == int:
			c3.addProperty("App::PropertyInteger",key,"1 MyProps","")
			s='c3.'+key + '=' + str(val) 
			exec(s)
		elif val.__class__ ==  str:
			c3.addProperty("App::PropertyString",key,"1 MyProps","")
			s='c3.'+key + '="' + val + '"'
			exec(s)
		elif val.__class__ ==  float:
			c3.addProperty("App::PropertyFloat",key,"1 MyProps","")
			s='c3.'+key + '=' + str(val) 
			#say(s)
			exec(s)
		else:
			say("nicht bearbeiteit")
			say(val.__class__)
	c3.propliste=propliste
	return obj


class _Comp():
	def __init__(self,obj):
		obj.Proxy = self
		self.Type = "_Comp"
		self.obj2 = obj 
		self.Lock=False
	def execute(self,obj):
		
		if not self.Lock:
			say("exec self=" +str(self) +' obj.Lab:' +str(obj.Label) + " lock: " + str(self.Lock))
			say("set Lock---------------------------------------------")
			try:
				if not hasattr(self,"updater"):
					say("erzeuge updater")
					self.updater=True
					
				if self.updater:
					self.updater=False
					say("updater true!")
					return
				else:
					self.updater=True
			except:
				pass
			
			self.Lock=True
			
			try:
#				say("try 4")
#				say(self)
#				say(obj)
				FreeCAD.z=obj
				#obj.execute2()

				for line in obj.execute3:
					if re.match('^\s*#',line) or re.match('^\s*$',line):
						say("ueberspringe -->" + line +'<--')
						continue
					say("****************")
					say(line)
					try:
						m = re.match("^\s*(\S*)\s*=\s*(.*)\s*$",line)
						l=m.group(1)
						r=m.group(2)
						say(l)
						say(r)
						#say("weiter")
						# alle parameter
#						params=['height','position']
#						params=obj.PropertiesList
						#say(ps)
						#alle parameter lang fuer uebergabe
						params=[]
						paraml=[]
						#for p in obj.PropertiesList:
						#say(obj.Proxy)
						FreeCAD.pp=obj
						#say(obj.Proxy.propliste)
						#say("aaa--------------------------------------------------------------------------aaa")
						for p in obj.propliste:
						#for p in obj.PropertiesList:
							ss=str(p)
							#say(p)
#							ss=p
#							if ss<>'execute3' and ss<>'Group' and ss<>'Proxy':
							# paraml.append('self.obj2.'+str(p))
							paraml.append('obj.'+str(p))
							params.append(str(p))
						
						ps= ', '.join(params)
						pl= ', '.join(paraml)
						#say(pl)
						#say(ps)
						kv="k=lambda " +ps +" : " + r
						say(kv)
						exec(kv) 
						#say(k)
#						say(l)

# ablaug ohne zuweisung - ist term berechen bar?
						yy="zz=k("+pl+")"
						#say(yy)
						#say("exec yy")
						exec(yy)
						say("berechnet:" +str(zz))

						# say("constraints sucher ..")
						mc = re.match("(.+)\.(.+)\.(.+)",l)
						if mc and mc.group(2)=="Constraints":
							s1=mc.group(1)
							s2=mc.group(2)
							s3=mc.group(3)
							#say("sketcher constraint " +s1 + " " + s3)
							#say(s3)
							#say("und---------------------")
							#cmd="self.obj2."+s1+".setDatum('"+s3+"',"+"k("+pl+"))"
							if re.match('^\d+$',s3):
								cmd="obj."+s1+".setDatum("+s3+","+str(zz)+")"
							else:
								cmd="obj."+s1+".setDatum('"+s3+"',"+str(zz)+")"
							
							#cmd="self.obj2."+s1+".setDatum('"+s3+"',FreeCAD.Units.Quantity('"+str(zz)+" deg'))"
							#FreeCAD.uu=self.obj2.triangle
							#say(cmd)
							#say(self.obj2)
							#say(self.obj2.triangle)
							#FreeCADGui.getDocument('comp2').resetEdit()
							#FreeCAD.uu.ViewObject.startEditing()
							exec(cmd)
							say("exec constraint done")
							s='obj.'+s1+ '.touch()'
							exec(s)
							App.activeDocument().recompute()
							exec(s)
							App.activeDocument().recompute()
							
							# say("recompute constraint done")

							# t=FreeCAD.getDocument("comp2").getObject("Sketch")



						else:
							#say("# zuweisung")
							#cmd="self.obj2."+l+"="+"k("+pl+")"
							cmd="obj."+l+"="+"k("+pl+")"
							#cmd="self.obj2."+l+"="+str(zz)
							say(cmd)
							#say(self.obj2)
							#say(self.obj2.table)
							exec(cmd)
						#say(res)
						
						
						
						
						
						say("done zuweisung")
					except:
						saye("Fehler bei exec Zeile")

				# say("done")
			except:
				say("except Fehler beim execute")
			self.Lock=False
			say("unset Lock +++++++++++++++++++++++++++++++++++++++")

	def __getstate__(self):
		say("getstate " + str(self))
		return None

	def __setstate__(self,state):
		say("setstate " + str(self) + str(state))
		return None
		
	def addComponent(self,name='object'):
		say(name)
		self.obj2.addProperty("App::PropertyLink",name,"3 MyParts","")
	def addProperty(self,key,val):
		say(key)
		#propliste.append(key)
		#say(propliste)
		say(val.__class__)
		c3=self.obj2
		if val.__class__ == int:
			c3.addProperty("App::PropertyInteger",key,"1 MyProps","")
			s='c3.'+key + '=' + str(val) 
			exec(s)
		elif val.__class__ ==  str:
			c3.addProperty("App::PropertyString",key,"1 MyProps","")
			s='c3.'+key + '="' + val + '"'
			exec(s)
		elif val.__class__ ==  float:
			c3.addProperty("App::PropertyFloat",key,"1 MyProps","")
			s='c3.'+key + '=' + str(val) 
			#say(s)
			exec(s)
		else:
			say("nicht bearbeiteit")
			say(val.__class__)
		say(c3.propliste)
		t=c3.propliste
		t.append(key)
		c3.propliste=t
		say(c3.propliste)


class _ViewProviderComp(object):
 
	def getIcon(self):
		return __dir__ +'/icons/master.png'
   
	def __init__(self,vobj):
		say("__init__" + str(self) + str(vobj))
		vobj.Proxy = self

	def attach(self,vobj):
		say("attach 2" + str(self) + str(vobj))
		self.Object = vobj.Object
		FreeCAD.t=self
		if not hasattr(self.Object,"Lock"):
				self.Object.Proxy.Lock=False
				say("lock gesetzt")
		say("fertig")
		return	
	
	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		say("getstate " + str(self))
		return None

	def __setstate__(self,state):
		say("setstate " + str(self) + str(state))
		return None
		
	def setEdit(self,vobj,mode=0):
		s=MyWidget()
		self.s=s
		s.show()
		return True

	def unsetEdit(self,vobj,mode=0):
		return False

	def doubleClicked(self,vobj):
		say("Double CLicked 3")
		self.setEdit(vobj)
		pass



#----------------------------
# end of mycomp4
#----------------------------
