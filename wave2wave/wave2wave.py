# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 13:14:19 2018

@author: balintgabor
"""

import adsk.core, adsk.fusion, traceback

def run(context):
  ui = None
  try:
    app = adsk.core.Application.get()
    ui  = app.userInterface
            
    design = app.activeProduct
    
    # Get the root component of the active design.
    rootComp = design.rootComponent
    

    ###### PARAMETERS
    
    Width = 20 #How wide the loft will be
    Stepnr = 10 #How many steps to go through on the first wave
    Stepnr2 = 15 #How many steps to go through on the second wave
    stepln = Width / float(Stepnr) #wavelegth1
    stepln2 = Width / float(Stepnr2) #wavelegth2
    height = 15 #loft distance
    
    ampli = 1 #wave1 amplitude
    ampli2 = 1 # wave2 amplitude
 
    ### WAVE1
    
    # Create a new sketch on the xy plane.
    sketches = rootComp.sketches
    xyPlane = rootComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)
    
    # Create an object collection for the points.
    points = adsk.core.ObjectCollection.create()  

    
 
    points.add(adsk.core.Point3D.create(0, 0, 0)) # This plots the origin
    
    
    Bin1 = range(0, Stepnr, 2)
    Bin2 = range(1, Stepnr, 2)
    
    xCoord = 0
    yCoord = 0
    
    for i in range(Stepnr):
    
        if i in Bin1:
            xCoord = xCoord + stepln
            yCoord = 0 + ampli
            points.add(adsk.core.Point3D.create(xCoord, yCoord, 0))
    
        if i in Bin2:
            xCoord = xCoord + stepln
            yCoord = 0 - ampli
            points.add(adsk.core.Point3D.create(xCoord, yCoord, 0))
    
    
    # Create the spline.
    spline1 = sketch.sketchCurves.sketchFittedSplines.add(points)
    
    ### Wave 2
    
    #create second sketch
    planes = rootComp.constructionPlanes
            
    ####        # Create construction plane input
    
    planeInput = planes.createInput()
            
            # Add construction plane by offset
    offsetValue = adsk.core.ValueInput.createByReal(float(height))
    planeInput.setByOffset(rootComp.xYConstructionPlane, offsetValue)
    planeOne = planes.add(planeInput)
    
    sketch2 = rootComp.sketches
    offsetplane = planeOne
    sketch = sketch2.add(offsetplane)
    
 # Create an object collection for the points.
    points2 = adsk.core.ObjectCollection.create()

    points2.add(adsk.core.Point3D.create(0, 0, 0))     
    
    Bin3 = range(0, Stepnr2, 2)
    Bin4 = range(1, Stepnr2, 2)
    
    xCoord2 = 0
    yCoord2 = 0
    
    for i in range(Stepnr2):
    
        if i in Bin3:
            xCoord2 = xCoord2 + stepln2
            yCoord2 = 0 + ampli2
            points2.add(adsk.core.Point3D.create(xCoord2, yCoord2, 0))
    
        if i in Bin4:
            xCoord2 = xCoord2 + stepln2
            yCoord2 = 0 - ampli2
            points2.add(adsk.core.Point3D.create(xCoord2, yCoord2, 0))
    
    
    # Create the spline.
    spline2 = sketch.sketchCurves.sketchFittedSplines.add(points2)
    
    ########LOFT
    
    openProfile1 = adsk.fusion.Path.create(spline1, adsk.fusion.ChainedCurveOptions.noChainedCurves)
    openProfile2 = adsk.fusion.Path.create(spline2, adsk.fusion.ChainedCurveOptions.noChainedCurves)
    
    
     # Create loft feature input
    loftFeats = rootComp.features.loftFeatures
    loftInput = loftFeats.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    loftSectionsObj = loftInput.loftSections
    section1 = loftSectionsObj.add(openProfile1)
    section1.setDirectionEndCondition(adsk.core.ValueInput.createByString('0.0 deg'), adsk.core.ValueInput.createByReal(1.0))
    section2 = loftSectionsObj.add(openProfile2)
    section2.setDirectionEndCondition(adsk.core.ValueInput.createByString('0.0 deg'), adsk.core.ValueInput.createByReal(1.0))
    loftInput.isSolid = False
    
    # Create loft feature
    loftFeats.add(loftInput)
    
    
  except:
    if ui:
      ui.messageBox('Failed:\n{}'.format(traceback.format_exc())) 