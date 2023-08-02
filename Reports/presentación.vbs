Sub CrearPresentacion()
    Dim PPTApp As Object
    Dim PPTPres As Object
    Dim PPTSlide As Object
    
    ' Crear una instancia de PowerPoint
    Set PPTApp = CreateObject("PowerPoint.Application")
    
    ' Crear una presentación nueva
    Set PPTPres = PPTApp.Presentations.Add
    
    ' Agregar la primera diapositiva
    Set PPTSlide = PPTPres.Slides.Add(1, 11) ' 11 representa el tipo de diapositiva en blanco
    
    ' Configurar el contenido de la primera diapositiva
    PPTSlide.Shapes.Title.TextFrame.TextRange.Text = "La Transformación Digital: Su Rol en la Transformación Laboral y la Evolución de las Profesiones Actuales"
    
    ' Agregar la segunda diapositiva
    Set PPTSlide = PPTPres.Slides.Add(2, 11)
    
    ' Configurar el contenido de la segunda diapositiva
    PPTSlide.Shapes.Title.TextFrame.TextRange.Text = "Impacto en la Transformación Laboral"
    ' Agregar puntos clave utilizando PPTSlide.Shapes.AddTextbox
    
    ' Agregar la tercera diapositiva
    Set PPTSlide = PPTPres.Slides.Add(3, 11)
    
    ' Configurar el contenido de la tercera diapositiva
    PPTSlide.Shapes.Title.TextFrame.TextRange.Text = "Evolución de las Profesiones Actuales y Nuevas Profesiones Emergentes"
    ' Agregar puntos clave utilizando PPTSlide.Shapes.AddTextbox
    
    ' Mostrar la aplicación de PowerPoint
    PPTApp.Visible = True
    
    ' Liberar la memoria
    Set PPTSlide = Nothing
    Set PPTPres = Nothing
    Set PPTApp = Nothing
End Sub
