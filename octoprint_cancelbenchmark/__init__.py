# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import time


class CancelbenchmarkPlugin(octoprint.plugin.StartupPlugin,
							octoprint.plugin.TemplatePlugin,
							octoprint.plugin.AssetPlugin,
							octoprint.plugin.SettingsPlugin,
							octoprint.plugin.SimpleApiPlugin):


	def __init__(self):
		self.cancelTime = 0
		self.stopTime = 0
		self.printCanceled = False



	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			# put your plugin's default settings here
		)

	##~~ AssetPlugin mixin

	def hook_gcode_queuing(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
		if gcode:

			if (gcode in ["G80"]):
				self._printer.commands("M114")
				self.cancelTime = time.mktime(time.gmtime())
				self.printCanceled = True
				self._logger.info("Print cancelled via G80 in file; cancelTime: "+str(self.cancelTime))
				self._printer.cancel_print()


	def detect_firmware_response(self, comm_instance, line, *args, **kwargs):
		if "Count" not in line:
			return line

		if not self.printCanceled:
			return line

		self.stopTime = time.mktime(time.gmtime())
		self.delayLength = self.stopTime - self.cancelTime
		self._logger.info("It took this long to get the Position read response after canceling: "+str(self.delayLength))
		self.printCanceled = False

		return line





	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/cancelbenchmark.js"],
			css=["css/cancelbenchmark.css"],
			less=["less/cancelbenchmark.less"]
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			cancelbenchmark=dict(
				displayName="Cancelbenchmark Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="you",
				repo="OctoPrint-Cancelbenchmark",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/you/OctoPrint-Cancelbenchmark/archive/{target_version}.zip"
			)
		)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Cancelbenchmark Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = CancelbenchmarkPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.hook_gcode_queuing,
		"octoprint.comm.protocol.gcode.received": __plugin_implementation__.detect_firmware_response
	}

