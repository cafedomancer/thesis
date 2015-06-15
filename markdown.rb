require 'github/markup'
require 'json'
require 'pp'

files = Dir.glob('data/merge/*.json') +
        Dir.glob('data/unmerge/*.json')

jsons = files.map { |file| JSON.load(File.read(file)) }
comments = jsons.map { |json| json['body'] }
files_with_comments = files.zip(comments)

files_with_comments.select! { |file, comment| comment.include? 'https' }
files_with_comments.select! { |file, comment| comment.include? 'github' }
files_with_comments.select! { |file, comment| comment.include? 'rails' }
files_with_comments.select! { |file, comment| comment.include? '```' }

files_with_comments.map! { |file, comment| [file, comment.gsub("\r\n", "\n")] }

puts files_with_comments.map { |file, comment| file }

# puts GitHub::Markup.render('README.markdown', comment)
