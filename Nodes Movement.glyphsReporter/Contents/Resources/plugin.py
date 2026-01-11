# encoding: utf-8

###########################################################################################################
#
#
# Reporter Plugin
#
# Read the docs:
# https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################


from __future__ import division, print_function, unicode_literals
import objc
import math
from GlyphsApp import Glyphs, GSAnchor
from GlyphsApp.plugins import ReporterPlugin
from AppKit import NSColor, NSPoint, NSBezierPath


class NodesMovement(ReporterPlugin):

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Nodes Movement',
			'de': 'Nodes Movement',
			'fr': 'Nodes Movement',
			'es': 'Nodes Movement',
			'pt': 'Nodes Movement',
		})
		# Visual tuning
		self.minDelta = 0.5  # ignore tiny movements
		
	@objc.python_method
	def foreground(self, layer):
		font = layer.parent.parent
		masters = font.masters

		# Need at least 2 masters
		if len(masters) < 2:
			return

		masterA = masters[0]
		masterB = masters[1]

		layerA = layer.parent.layers[masterA.id]
		layerB = layer.parent.layers[masterB.id]

		if not layerA or not layerB:
			return

		NSColor.systemBlueColor().set()

		for pathIndex, pathA in enumerate(layerA.paths):
			if pathIndex >= len(layerB.paths):
				continue

			pathB = layerB.paths[pathIndex]

			for nodeIndex, nodeA in enumerate(pathA.nodes):
				if nodeIndex >= len(pathB.nodes):
					continue

				nodeB = pathB.nodes[nodeIndex]

				dx = nodeB.position.x - nodeA.position.x
				dy = nodeB.position.y - nodeA.position.y

				if abs(dx) < self.minDelta and abs(dy) < self.minDelta:
					continue

				self.drawArrow(nodeA.position, nodeB.position)

	# ---------- Drawing helpers ----------
	@objc.python_method
	def drawArrow(self, start, end):
		path = NSBezierPath.bezierPath()
		path.moveToPoint_(start)
		path.lineToPoint_(end)
		path.setLineWidth_(1.2)
		path.stroke()

		self.drawArrowHead(start, end)
		
	@objc.python_method
	def drawArrowHead(self, start, end):
		angle = math.atan2(end.y - start.y, end.x - start.x)

		headLength = 6
		headAngle = math.radians(25)

		p1 = NSPoint(
			end.x - headLength * math.cos(angle - headAngle),
			end.y - headLength * math.sin(angle - headAngle)
		)

		p2 = NSPoint(
			end.x - headLength * math.cos(angle + headAngle),
			end.y - headLength * math.sin(angle + headAngle)
		)

		head = NSBezierPath.bezierPath()
		head.moveToPoint_(end)
		head.lineToPoint_(p1)
		head.moveToPoint_(end)
		head.lineToPoint_(p2)
		head.setLineWidth_(1.2)
		head.stroke()

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
