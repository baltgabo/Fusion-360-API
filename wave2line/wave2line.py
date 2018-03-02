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
    
    
    Width = 20 # wave total width
    Stepnr = 20 #How many steps to go through
    stepln = Width / float(Stepnr)
    ampli = 1
    
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
    
    
    #create second sketch
    planes = rootComp.constructionPlanes
            
    ####        # Create construction plane input
    
    planeInput = planes.createInput()
            
            # Add construction plane by offset
    offsetValue = adsk.core.ValueInput.createByReal(30.0)
    planeInput.setByOffset(rootComp.xYConstructionPlane, offsetValue)
    planeOne = planes.add(planeInput)
    
    sketch2 = rootComp.sketches
    offsetplane = planeOne
    sketch = sketch2.add(offsetplane)
    
    lines = sketch.sketchCurves.sketchLines;
    line1 = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(int(Width), 0, 0))
    
    
    ########LOFT
    
    openProfile1 = adsk.fusion.Path.create(spline1, adsk.fusion.ChainedCurveOptions.noChainedCurves)
    openProfile2 = adsk.fusion.Path.create(line1, adsk.fusion.ChainedCurveOptions.noChainedCurves)
    
    
     # Create loft feature input
    loftFeats = rootComp.features.loftFeatures
    loftInput = loftFeats.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    loftSectionsObj = loftInput.loftSections
    section1 = loftSectionsObj.add(openProfile1)
    section1.setDirectionEndCondition(adsk.core.ValueInput.createByString('0.0 deg'), adsk.core.ValueInput.createByReal(1.0))
    loftSectionsObj.add(openProfile2)
    loftInput.isSolid = False
    
    # Create loft feature
    loftFeats.add(loftInput)
    
    
  except:
    if ui:
      ui.messageBox('Failed:\n{}'.format(traceback.format_exc())) 