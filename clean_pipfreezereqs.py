import codecs
import os

class cleanReqs():

	def __init__(self, infile, outfile):
		self.infile = infile
		self.outfile = outfile

	def create(self, encoding='utf-16', spl='='):
		''' Function create allows you to read a pip freeze encoded file (by default utf-16) and split (by default by '=') the
		version number of the different libraries to be installed and creates a new file with the listed libraries versionless.
		'''
		package_list = []
		self.encoding = encoding
		self.spl = spl

		if os.path.exists(self.infile):
			fp = codecs.open(self.infile, 'r', self.encoding)
			installed_packages = fp.readlines()

			for package in installed_packages:
				p = package.split(self.spl)
				package_list.append(p[0])

			with open(self.outfile, 'w') as f:
				for pack in package_list:
					f.write('%s\n' % pack)
			print('new_requirements file creado exitosamente!')
		else:
			print('Por favor ejectue el comando pip freeze y guarde el file requirements.txt en la ruta deseada')