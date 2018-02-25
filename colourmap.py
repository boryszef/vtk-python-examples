#!/usr/bin/python

import vtk
density = vtk.vtkGaussianCubeReader()
density.SetFileName("crown.den.cube")

density.Update()

grid = density.GetGridOutput()
bound  = grid.GetBounds()

plane = vtk.vtkPlaneSource()
plane.SetResolution(100, 100)

t = vtk.vtkTransform()
t.Scale(bound[1]-bound[0], bound[3]-bound[2], bound[5]-bound[4])
t.Translate(0.5, 0.5, 0.5)

trans = vtk.vtkTransformPolyDataFilter()
trans.SetTransform(t)
trans.SetInputConnection(plane.GetOutputPort())

probe = vtk.vtkProbeFilter()
probe.SetInputConnection(trans.GetOutputPort())
probe.SetSourceData(grid)

# Update probe filter to get valid scalar range
probe.Update()
srange = probe.GetOutput().GetScalarRange()

lut = vtk.vtkLookupTable()
lut.SetTableRange(srange)
lut.SetNumberOfTableValues(255)
for i in range(255):
	lut.SetTableValue(i, i/255.0, 0.0, 1 - i/255.0, 1.0)
lut.SetScaleToLog10()

outline = vtk.vtkOutlineFilter()
outline.SetInputData(grid)

planeMapper = vtk.vtkPolyDataMapper()
planeMapper.SetInputConnection(probe.GetOutputPort())
planeMapper.UseLookupTableScalarRangeOn()
planeMapper.SetLookupTable(lut)

outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(outline.GetOutputPort())

planeActor = vtk.vtkActor()
planeActor.SetMapper(planeMapper)

outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)

renderer = vtk.vtkRenderer()
renderer.ResetCamera()
renderer.AddActor(planeActor)
renderer.AddActor(outlineActor)

window = vtk.vtkRenderWindow()
window.AddRenderer(renderer)
window.SetSize(800,800)

istyle = vtk.vtkInteractorStyleSwitch()
istyle.SetCurrentStyleToTrackballCamera()

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)
interactor.SetInteractorStyle(istyle)

interactor.Initialize()
interactor.Start()

