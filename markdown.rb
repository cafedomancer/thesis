require 'github/markup'
require 'json'
require 'pp'

json = JSON.load(File.read(ARGV.first))
comment = json['body']
puts GitHub::Markup.render('README.markdown', comment)
