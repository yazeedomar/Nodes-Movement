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
import objc, math
from objc import lookUpClass
from GlyphsApp import Glyphs, GSAnchor
from GlyphsApp.plugins import ReporterPlugin
from Foundation import NSString
from AppKit import NSColor, NSPoint, NSBezierPath


class NodesMovement(ReporterPlugin):

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Nodes Movement',
			'de': 'Knotenbewegung',
			'fr': 'Mouvement des nœuds',
			'es': 'Movimiento de nodos',
			'pt': 'Movimento de nós',
		})
		# Visual tuning
		self.minDelta = 0.5  # ignore tiny movements
		
	@objc.python_method
	def background(self, layer):
		if not self.conditionsAreMetForDrawing():
			return
		font = layer.parent.parent
		masters = font.masters

		if len(masters) < 2:
			return

		activeMaster = layer.master
		activeIndex = masters.index(activeMaster)

		if activeIndex == 0:
			return

		ghostMaster = masters[activeIndex - 1]

		layerA = layer.parent.layers[ghostMaster.id]
		layerB = layer.parent.layers[activeMaster.id]

		if not layerA or not layerB:
			return

		if not self.layersCompatible(layerA, layerB):
			return

		scale = self.getScale()

		# ── Draw Ghost master filled gray ─────────────────────
		NSColor.systemIndigoColor().colorWithAlphaComponent_(0.1).set()
		layerA.completeBezierPath.fill()

		# ── Draw nodes of ghost master ────────────────────────
		NSColor.systemIndigoColor().colorWithAlphaComponent_(0.8).set()
		for path in layerA.paths:
			for node in path.nodes:
				r = 2.0 / scale
				dot = NSBezierPath.bezierPathWithOvalInRect_(
					((node.position.x - r, node.position.y - r), (2*r, 2*r))
				)
				dot.fill()

		# ── Draw delta arrows ─────────────────────────────────
		NSColor.systemIndigoColor().colorWithAlphaComponent_(0.8).set()

		for pA, pB in zip(layerA.paths, layerB.paths):
			for nA, nB in zip(pA.nodes, pB.nodes):

				dx = nB.position.x - nA.position.x
				dy = nB.position.y - nA.position.y

				if abs(dx) < self.minDelta and abs(dy) < self.minDelta:
					continue

				self.drawArrow(nA.position, nB.position, scale)

	# ─────────────────────────────────────────────────────────

	@objc.python_method
	def drawArrow(self, start, end, scale):
		# Main line
		path = NSBezierPath.bezierPath()
		path.moveToPoint_(start)
		path.lineToPoint_(end)
		path.setLineWidth_(1.5 / scale)
		path.stroke()

		self.drawArrowHead(start, end, scale)

	@objc.python_method
	def drawArrowHead(self, start, end, scale):
		angle = math.atan2(end.y - start.y, end.x - start.x)

		length = 8 / scale
		width = 6.0 / scale

		p1 = NSPoint(
			end.x - length * math.cos(angle) + width * math.sin(angle),
			end.y - length * math.sin(angle) - width * math.cos(angle)
		)
		p2 = NSPoint(
			end.x - length * math.cos(angle) - width * math.sin(angle),
			end.y - length * math.sin(angle) + width * math.cos(angle)
		)

		arrow = NSBezierPath.bezierPath()
		arrow.moveToPoint_(end)
		arrow.lineToPoint_(p1)
		arrow.lineToPoint_(p2)
		arrow.closePath()
		arrow.fill()

	# ─────────────────────────────────────────────────────────

	@objc.python_method
	def layersCompatible(self, layerA, layerB):
		if len(layerA.paths) != len(layerB.paths):
			return False

		for pA, pB in zip(layerA.paths, layerB.paths):
			if len(pA.nodes) != len(pB.nodes):
				return False
			for nA, nB in zip(pA.nodes, pB.nodes):
				if nA.type != nB.type:
					return False

		return True

	# ─────────────────────────────────────────────────────────

	@objc.python_method
	def conditionsAreMetForDrawing(self):
			"""Don't activate if text or pan (hand) tool are active."""
			currentController = self.controller.view().window().windowController()
			if currentController:
				tool = currentController.toolDrawDelegate()
				textToolIsActive = tool.isKindOfClass_(lookUpClass("GlyphsToolText"))
				handToolIsActive = tool.isKindOfClass_(lookUpClass("GlyphsToolHand"))
				if not textToolIsActive and not handToolIsActive: 
					return True
			return False

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
