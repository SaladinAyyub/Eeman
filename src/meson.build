pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'eeman'
gnome = import('gnome')

gnome.compile_resources('eeman',
  'eeman.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'eeman.in',
  output: 'eeman',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

eeman_sources = [
  '__init__.py',
  'main.py',
  'configuration.py',
  'config.ini',
]

install_data(eeman_sources, install_dir: moduledir)
install_subdir('libs', install_dir: moduledir)
install_subdir('gui', install_dir: moduledir)