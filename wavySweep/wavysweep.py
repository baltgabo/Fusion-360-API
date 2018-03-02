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
    Stepnr = 7 #How many steps to go through on the first wave
    Stepnr2 = 7 #How many steps to go through on the second wave
    stepln = Width / float(Stepnr) #wavelegth1
    stepln2 = Width / float(Stepnr2) #wavelegth2
    
    ampli = 2 #wave1 amplitude
    ampli2 = 2 # wave2 amplitude
    
    sweeptaper = '0.0 deg'
    sweeptwist = '0.0 deg'
    
    ### WAVE1
    
    # Create a new sketch on the xy plane.
    sketches = rootComp.sketches
    xyPlane = rootComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)
    
    # Create an object collection for the points.
    points = adsk.core.ObjectCollection.create()  
    
    points.add(adsk.core.Point3D.create(0, 0, 0)) # This plots the origin
    
    #This part creates the wave coordinates for wave1
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
    
    ### WAVE 2

    yzPlane = rootComp.yZConstructionPlane
    
    sketch2 = rootComp.sketches
    sketch = sketch2.add(yzPlane)
    
    # Create an object collection for the points.
    points2 = adsk.core.ObjectCollection.create()
         
    
    Bin3 = range(0, Stepnr2, 2)
    Bin4 = range(1, Stepnr2, 2)
    
    xCoord2 = 0
    yCoord2 = 0
    
    points2.add(adsk.core.Point3D.create(0, yCoord2, 0)) #first point
    
    for i in range(Stepnr2):
    
        if i in Bin3:
            xCoord2 = xCoord2 + stepln2
            yCoord2 = yCoord2 + ampli2
            points2.add(adsk.core.Point3D.create(xCoord2, yCoord2, 0))
    
        if i in Bin4:
            xCoord2 = xCoord2 + stepln2
            yCoord2 = yCoord2 - ampli2
            points2.add(adsk.core.Point3D.create(xCoord2, yCoord2, 0))
    
    
    # Create the spline.
    spline2 = sketch.sketchCurves.sketchFittedSplines.add(points2)
    
    ###SWEEP
    
    openProfile1 = adsk.fusion.Path.create(spline1, adsk.fusion.ChainedCurveOptions.noChainedCurves)
    openProfile2 = adsk.fusion.Path.create(spline2, adsk.fusion.ChainedCurveOptions.noChainedCurves)
    
    # Create a sweep input
    sweeps = rootComp.features.sweepFeatures
    sweepInput = sweeps.createInput(openProfile1, openProfile2, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    sweepInput.taperAngle = adsk.core.ValueInput.createByString(sweeptaper)
    sweepInput.twistAngle = adsk.core.ValueInput.createByString(sweeptwist)
    sweepInput.isSolid = False

    # Create the sweep.
    sweeps.add(sweepInput)
    
  except:
    if ui:
      ui.messageBox('Failed:\n{}'.format(traceback.format_exc())) 