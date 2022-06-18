import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QWidget, QInputDialog, QLineEdit, QFileDialog, QMessageBox
from PyQt5 import uic, QtCore

from PIL import Image 
import glob
import os, sys



Ui_MainWindow, QtBaseClass = uic.loadUiType('window.ui')

class MyApp(QMainWindow):

    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Centrar window
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


        self.rutaFotosOriginales = ''
        self.rutaFotosDestino = ''
        self.rutaSello = ''
        #Botones
        self.ui.seleccionarFotos.clicked.connect(lambda: self.elegirDirectorio('originales'))
        self.ui.carpetaDestino.clicked.connect(lambda: self.elegirDirectorio('destino'))
        self.ui.seleccionarSello.clicked.connect(lambda: self.elegirDirectorio('sello'))
        self.ui.pegarSello.clicked.connect(self.sellar)
        self.ui.cancelar.clicked.connect(self.cancelar)


        # Radio Button
        self._posicionFoto = None
        self.ui.inf_centro.toggled.connect(self.posicionFoto)
        self.ui.inf_izq.toggled.connect(self.posicionFoto)


        self.progreso = self.ui.progreso

    def posicionFoto(self):

        if(self.ui.inf_centro.isChecked()):
            self._posicionFoto = "abajo_centro"
        else:
            self._posicionFoto = "abajo_izquierda"


    def sellar(self):
        if(not self.comprobarRutas()):
            return


        try: 

            self.posicionFoto()



            #Relative Path 
            #Image which we want to paste 
            img2 = Image.open(self.rutaSello)  

            rutaFotosOriginales = self.rutaFotosOriginales+'/*.jpg'
            fotosOriginales = glob.glob(rutaFotosOriginales)
            #Relative Path 
            #Image on which we want to paste 
            i = 1
            porcentaje = 0
            for foto in fotosOriginales:

                try:
                    #print("Foto "+foto)
                    nombreFoto = foto
                    img = Image.open(nombreFoto)  

                    if(self._posicionFoto == 'abajo_izquierda'):

                        img.paste(img2, (50, (img.size[1] - img2.size[1] - 50 )), img2) 
                    elif(self._posicionFoto == 'abajo_centro'):
                        img.paste(img2, ( int((  (img.size[0]/2) - (img2.size[0]/2))   ), (img.size[1] - img2.size[1] - 50 )), img2)
                    
                    
                    nombreFoto = nombreFoto.split('/')
                    ruta = self.rutaFotosDestino+'/'+nombreFoto[-1]
                    img.save(ruta)
                    porcentaje = i*100/len(fotosOriginales)
                    self.progreso.setValue(porcentaje)
                except:
                    print("Error")
                    print(nombreFoto.split('/')[-1])
                finally:

                    i+=1
            else:
                pass

            if(porcentaje == 100):
                QMessageBox.about(self, "Proceso finalizado", "EL proceso ha finalizado correctamente")
                self.progreso.setValue(0)
        except IOError as err: 
            print(err)
            

    def cancelar(self):
        print("Cancelando acciones.")

    def elegirDirectorio(self, tipo):
        mensaje = ''
        if (tipo == 'originales'):
            mensaje = 'Fotos originales'
            self.rutaFotosOriginales = str(QFileDialog.getExistingDirectory(self, mensaje))
            self.ui.labelOriginales.setText(self.rutaFotosOriginales)
        elif (tipo == 'destino'):
            mensaje = 'Carpeta de destino'
            self.rutaFotosDestino = str(QFileDialog.getExistingDirectory(self, mensaje))
            self.ui.labelDestino.setText(self.rutaFotosDestino)
        elif (tipo == 'sello'):
            mensaje = 'Seleccionar sello'
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self,mensaje, "","PNG (*.png);;JPG (*.jpg)", options=options)
            if fileName:
                self.rutaSello = fileName
                self.ui.labelSello.setText(self.rutaSello)
        
    def comprobarRutas(self):
        resultado = False
        if(self.rutaFotosDestino != '' and self.rutaFotosOriginales !='' and self.rutaSello != ''):
            resultado =True
        return resultado
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()


    sys.exit(app.exec_())
