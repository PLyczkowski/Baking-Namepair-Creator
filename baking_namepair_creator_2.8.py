# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Select the lowpoly and highpoly objects, and press the Create Baking Namepair button in the Relations tab. The suffixes _high and _low are added automatically based on the vertex count. The name of the low poly object is used as the new name's base.

bl_info = {
	'name': "Baking Namepair Creator",
	'author': "Paweł Łyczkowski",
	'version': (1, 0, 3),
	'blender': (2, 80, 0),
	'location': "View3D > Toolbar > Relations Tab",
	'description': "Set's up a baking namepair.",
	'warning': "",
	'wiki_url': "",
	'tracker_url': "",
	'category': 'Object'
}

import bpy, bmesh
import string
import random

class BakingNamepair(bpy.types.Operator):
	'''Tooltip'''
	bl_description = "BakingNamepair"
	bl_idname = "object.baking_namepair"
	bl_label = "BakingNamepair"
	bl_options = { 'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		
		selected = bpy.context.selected_objects
		depsgraph = context.depsgraph

		high_poly = None
		low_poly = None

		def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
			return ''.join(random.choice(chars) for _ in range(size))

		if len(selected) == 2:

			tempmesh1 = bmesh.new()
			tempmesh1.from_object(selected[0], depsgraph, deform=True, cage=False, face_normals=True)
			vertex_count1 = len(tempmesh1.verts)

			tempmesh2 = bmesh.new()
			tempmesh2.from_object(selected[1], depsgraph, deform=True, cage=False, face_normals=True)
			vertex_count2 = len(tempmesh2.verts)

			if vertex_count1 != vertex_count2:

				#The meshes are not the same, set up which is which.

				if vertex_count1 > vertex_count2:
					high_poly = selected[0]
					low_poly= selected[1]
				else:
					high_poly = selected[1]
					low_poly= selected[0]

				#Set up a random name, if option toggled.

				if bpy.context.scene.r_generate_random_name:
					low_poly.name = id_generator()
					if bpy.context.scene.r_also_rename_datablock:
						low_poly.data.name = low_poly.name

				else:

				#Check if lowpoly doesn't already end in "_low".

					low_poly_name_len = len(low_poly.name)

					if low_poly.name[low_poly_name_len - 1] == "w" and low_poly.name[low_poly_name_len - 2] == "o" and low_poly.name[low_poly_name_len - 3] == "l" and low_poly.name[low_poly_name_len - 4] == "_":

						#It does, remove the "_low".

						low_poly.name = low_poly.name[:low_poly_name_len - 4]

				#Check if the names are not yet occupied.

				high_poly_check = bpy.data.objects.get(low_poly.name + "_high")

				low_poly_check = bpy.data.objects.get(low_poly.name + "_low")

				if high_poly_check == None and low_poly_check == None:

					#They are not, add suffixes.

					high_poly.name = low_poly.name + "_high"

					if bpy.context.scene.r_also_rename_datablock:
						high_poly.data.name = high_poly.name

					low_poly.name = low_poly.name + "_low"

					if bpy.context.scene.r_also_rename_datablock:
						low_poly.data.name = low_poly.name

					#Hide, if option toggled.

					if bpy.context.scene.r_hide_after_renaming:
						selected[0].hide_viewport = True
						selected[1].hide_viewport = True

				elif low_poly_check == None and high_poly.name == low_poly.name + "_high":

					#Only the highpoly is, so add suffix only to the lowpoly.

					low_poly.name = low_poly.name + "_low"

					if bpy.context.scene.r_also_rename_datablock:
						low_poly.data.name = low_poly.name

					#Hide, if option toggled.

					if bpy.context.scene.r_hide_after_renaming:
						selected[0].hide_viewport = True
						selected[1].hide_viewport = True

				else:


					#Low poly name occupied.

					self.report({'ERROR'}, "One of the names already occupied. Please rename the low poly object.")

			else:

				self.report({'ERROR'}, "Same vertex count.")

			tempmesh1.free
			tempmesh2.free

		else:

			self.report({'ERROR'}, "Invalid number of objects selected.")

		return {'FINISHED'}

class OpToggleRenamed(bpy.types.Operator):
	bl_idname = "object.toggle_viewport_renamed_objects"
	bl_label = "Hide(/Unhide) all renamed High/Low poly objects"
	bl_description = "Hide/Unhide all renamed High/Low poly objects in selected collections"
	bl_options = {'INTERNAL', 'UNDO'}

	group : bpy.props.EnumProperty(items = {
		('HIGH', "High polys", "High"),
		('LOW', "Low polys", "Low"),
		('ALL', "All renamed", "All"),
	})
	action : bpy.props.EnumProperty(items = {
		('SHOW', "Show", "Show"),
		('HIDE', "Hide", "Hide")
	})

	def execute(self, context):
		if self.group == 'HIGH':
			suffixes = "_high"
		elif self.group == 'LOW':
			suffixes = "_low"
		else:
			suffixes = ("_low", "_high")

		for obj in bpy.data.objects:
			if not obj.name.endswith(suffixes):
				continue
			if self.action == 'SHOW':
				obj.hide_viewport = False
			else:
				obj.hide_viewport = True
		return {'FINISHED'}

class addButtonsInObjectMode(bpy.types.Panel):
	bl_idname = "RELATIONS_PT_baking_namepair_objectmode"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'

	bl_label = "Baking Namepair"
	bl_context = "objectmode"

	def draw(self, context):
		layout = self.layout

		# col = layout.column(align=True)

		layout.operator("object.baking_namepair", text="Create Baking Namepair")

		layout.prop(context.scene, "r_generate_random_name", text="Generate Random Name")
		layout.prop(context.scene, "r_hide_after_renaming", text="Hide After Renaming")
		layout.prop(context.scene, "r_also_rename_datablock", text="Also Rename Datablock")

		self._draw_toggle_viewport(context, 'HIGH', layout)
		self._draw_toggle_viewport(context, 'LOW', layout)
		self._draw_toggle_viewport(context, 'ALL', layout)
	
	def _draw_toggle_viewport(self, context, group, layout):
		row = layout.row()
		row.label(text=group.lower())
		op = row.operator("object.toggle_viewport_renamed_objects", text="SHOW")
		op.group = group
		op.action = 'SHOW'
		op = row.operator("object.toggle_viewport_renamed_objects", text="HIDE")
		op.group = group
		op.action = 'HIDE'
		

def register():
	bpy.types.Scene.r_generate_random_name = bpy.props.BoolProperty(default= False)
	bpy.types.Scene.r_hide_after_renaming = bpy.props.BoolProperty(default= False)
	bpy.types.Scene.r_also_rename_datablock = bpy.props.BoolProperty(default= True)

	bpy.utils.register_class(BakingNamepair)
	bpy.utils.register_class(OpToggleRenamed)
	bpy.utils.register_class(addButtonsInObjectMode)

def unregister():
	bpy.utils.unregister_class(BakingNamepair)
	bpy.utils.unregister_class(OpToggleRenamed)
	bpy.utils.unregister_class(addButtonsInObjectMode)

if __name__ == "__main__":
	register()