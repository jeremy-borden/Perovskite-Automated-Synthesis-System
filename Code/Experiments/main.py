

'''
System outputs
    - Gantry (3d printer commands)
    - gui (images, number data)
    - hotplate (temperature control)
    - spectrometer (access measurements)

System inputs
    - gui (buttons, sliders)
    - camera (images)
    - spectrometer (measurements)
    - gantry (printer feedback, access gantry position)




// linign up grabber to hotplate for example
take picture of scene
for each aruco marker
    get corners
    get centers
    
if marker matches id for hotplate 
    find closest mathcihng aruco marker 
    calculate center of camera (plus some arbitray offset) to the distance of the aruco marker
    move gantry by the offset

'''