#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import bpy
import math

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *
from utilities_math import *
 
shape_file = sys.argv[-2]
basename = os.path.splitext(os.path.split(shape_file)[-1])[0]
lfd_images_folder = sys.argv[-1]
if not os.path.exists(lfd_images_folder):
    os.makedirs(lfd_images_folder)

#http://sarvanz.blogspot.co.il/2013/07/sphere-triangulation-using-icosahedron.html
vertices = []
theta = 26.56505117707799 * math.pi / 180.0 # refer paper for theta value
sin_theta = math.sin(theta)
cos_theta = math.cos(theta)
# the lower vertex
vertices.append([0.0, 0.0, -1.0]) 
# the lower pentagon
phi = math.pi / 5.0;
for i in range(1,6):
    vertices.append([cos_theta * math.cos(phi), cos_theta * math.sin(phi), -sin_theta]);
    phi = phi + 2.0 * math.pi / 5.0;
# the upper pentagon
phi = 0.0;
for i in range(6,11):
    vertices.append([cos_theta * math.cos(phi), cos_theta * math.sin(phi), sin_theta]);
    phi = phi + 2.0 * math.pi / 5.0;
# the upper vertex
vertices.append([0.0, 0.0, 1.0])

render_task_finished = True
for i in range(len(vertices)):
    lfd_image_file= '%s_%02d.png' % (basename, i)
    if not os.path.isfile(os.path.join(lfd_images_folder, lfd_image_file)):
        render_task_finished = False
        break
if render_task_finished:
    exit()

bpy.ops.import_scene.obj(filepath=shape_file) 

bpy.context.scene.render.alpha_mode = 'TRANSPARENT'
bpy.context.scene.render.use_textures = False
#bpy.context.scene.render.use_shadows = False
#bpy.context.scene.render.use_raytrace = False

# disable material transparency and raytrace
for material_idx in range(len(bpy.data.materials)):
    bpy.data.materials[material_idx].use_transparency = False
    bpy.data.materials[material_idx].use_raytrace = False
    bpy.data.materials[material_idx].use_mist = False
    bpy.data.materials[material_idx].diffuse_color = (0.6, 0.6, 0.6)
    bpy.data.materials[material_idx].diffuse_intensity = 0.8
    bpy.data.materials[material_idx].diffuse_shader = 'LAMBERT'
    bpy.data.materials[material_idx].specular_color = (0.2, 0.2, 0.2)
    bpy.data.materials[material_idx].specular_intensity = 0.6
    bpy.data.materials[material_idx].specular_hardness = 32
    bpy.data.materials[material_idx].specular_shader = 'PHONG'
    bpy.data.materials[material_idx].emit = 0.0
    bpy.data.materials[material_idx].ambient = 1.0
    bpy.data.materials[material_idx].translucency = 0.0

camObj = bpy.data.objects['Camera']
# camObj.data.lens_unit = 'FOV'
# camObj.data.angle = 0.2

bpy.ops.object.shade_smooth()
# YOUR CODE START HERE

# clear default lights
bpy.ops.object.select_by_type(type='LAMP')
bpy.ops.object.delete(use_global=False)

# set environment lighting
#bpy.context.space_data.context = 'WORLD'
bpy.context.scene.world.light_settings.use_environment_light = True
bpy.context.scene.world.light_settings.environment_energy = 0.35
bpy.context.scene.world.light_settings.environment_color = 'PLAIN'

# set point lights
light_elevation_degs = [-60, 0, 60]
for i in range(g_lfd_light_num):
    light_azimuth_deg = 360.0/g_lfd_light_num*i
    for light_elevation_deg in light_elevation_degs:
        lx, ly, lz = obj_centened_camera_pos(g_lfd_light_dist, light_azimuth_deg, light_elevation_deg)
        bpy.ops.object.lamp_add(type='POINT', location=(lx, ly, lz))
for lamp_idx in range(len(bpy.data.lamps)):
    bpy.data.lamps[lamp_idx].energy = 2.0

for i in range(len(vertices)):
    azimuth_deg = math.degrees(math.atan(z, x))
    elevation_deg = math.degrees(math.atan(y, abs(x)))
    theta_deg = 0
    
    lfd_image_file= '%s_%02d.png' % (basename, i)
    if os.path.isfile(os.path.join(lfd_images_folder, lfd_image_file)):
      continue
  
    cx, cy, cz = obj_centened_camera_pos(g_lfd_camera_dist, azimuth_deg, elevation_deg)
    q1 = camPosToQuaternion(cx, cy, cz)
    q2 = camRotQuaternion(cx, cy, cz, theta_deg)
    q = quaternionProduct(q2, q1)
    camObj.location[0] = cx
    camObj.location[1] = cy 
    camObj.location[2] = cz
    camObj.rotation_mode = 'QUATERNION'
    camObj.rotation_quaternion[0] = q[0]
    camObj.rotation_quaternion[1] = q[1]
    camObj.rotation_quaternion[2] = q[2]
    camObj.rotation_quaternion[3] = q[3]
    
    bpy.data.scenes['Scene'].render.filepath = os.path.join(lfd_images_folder, lfd_image_file)
    bpy.ops.render.render( write_still=True )