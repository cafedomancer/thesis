import json
import os


DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "data")

CHART_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "charts")

for d in [DATA_DIR, CHART_DIR]:
    if not os.path.exists(d):
        os.mkdir(d)

filename = os.path.join(DATA_DIR, 'projects.json')
with open(filename) as input:
    PROJECT_LIST = json.load(input)


'''
def clean_email_reply(text):
    return email_reply_parser.EmailReplyParser.parse_reply(text)


def clean_nltk_stopwords(words):
    return [word for word in words if word not in nltk.corpus.stopwords.words('english')]


def clean_user_stopwords(words):
    return [word for word in words if word not in ["``", "n't", "'s", "''", "--", "'m", "...", "'ll", "'ve", "'d", "'re", "ca", "wo", "http", "https", "+1", "-1", "`ruby", "`python", "pr", "pull", "request", "1", "2", "3", "/cc"]]


def clean_mysql_stopwords(words):
    return [word for word in words if word not in ["a's", 'able', 'about', 'above', 'according', 'accordingly', 'across', 'actually', 'after', 'afterwards', 'again', 'against', "ain't", 'all', 'allow', 'allows', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'an', 'and', 'another', 'any', 'anybody', 'anyhow', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apart', 'appear', 'appreciate', 'appropriate', 'are', "aren't", 'around', 'as', 'aside', 'ask', 'asking', 'associated', 'at', 'available', 'away', 'awfully', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'best', 'better', 'between', 'beyond', 'both', 'brief', 'but', 'by', "c'mon", "c's", 'came', 'can', "can't", 'cannot', 'cant', 'cause', 'causes', 'certain', 'certainly', 'changes', 'clearly', 'co', 'com', 'come', 'comes', 'concerning', 'consequently', 'consider', 'considering', 'contain', 'containing', 'contains', 'corresponding', 'could', "couldn't", 'course', 'currently', 'definitely', 'described', 'despite', 'did', "didn't", 'different', 'do', 'does', "doesn't", 'doing', "don't", 'done', 'down', 'downwards', 'during', 'each', 'ed', 'eg', 'eight', 'either', 'else', 'elsewhere', 'enough', 'entirely', 'especially', 'et', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'ex', 'exactly', 'example', 'except', 'far', 'few', 'fifth', 'first', 'five', 'followed', 'following', 'follows', 'for', 'former', 'formerly', 'forth', 'four', 'from', 'further', 'furthermore', 'get', 'gets', 'getting', 'given', 'gives', 'go', 'goes', 'going', 'gone', 'got', 'gotten', 'greetings', 'had', "hadn't", 'happens', 'hardly', 'has', "hasn't", 'have', "haven't", 'having', 'he', "he's", 'hello', 'help', 'hence', 'her', 'here', "here's", 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'hi', 'him', 'himself', 'his', 'hither', 'hopefully', 'how', 'howbeit', 'however', "i'd", "i'll", "i'm", "i've", 'ie', 'if', 'ignored', 'immediate', 'in', 'inasmuch', 'inc', 'indeed', 'indicate', 'indicated', 'indicates', 'inner', 'insofar', 'instead', 'into', 'inward', 'is', "isn't", 'it', "it'd", "it'll", "it's", 'its', 'itself', 'just', 'keep', 'keeps', 'kept', 'know', 'knows', 'known', 'last', 'lately', 'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let', "let's", 'like', 'liked', 'likely', 'little', 'look', 'looking', 'looks', 'ltd', 'mainly', 'many', 'may', 'maybe', 'me', 'mean', 'meanwhile', 'merely', 'might', 'more', 'moreover', 'most', 'mostly', 'much', 'must', 'my', 'myself', 'name', 'namely', 'nd', 'near', 'nearly', 'necessary', 'need', 'needs', 'neither', 'never', 'nevertheless', 'new', 'next', 'nine', 'no', 'nobody', 'non', 'none', 'noone', 'nor', 'normally', 'not', 'nothing', 'novel', 'now', 'nowhere', 'obviously', 'of', 'off', 'often', 'oh', 'ok', 'okay', 'old', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'ought', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'own', 'particular', 'particularly', 'per', 'perhaps', 'placed', 'please', 'plus', 'possible', 'presumably', 'probably', 'provides', 'que', 'quite', 'qv', 'rather', 'rd', 're', 'really', 'reasonably', 'regarding', 'regardless', 'regards', 'relatively', 'respectively', 'right', 'said', 'same', 'saw', 'say', 'saying', 'says', 'second', 'secondly', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'selves', 'sensible', 'sent', 'serious', 'seriously', 'seven', 'several', 'shall', 'she', 'should', "shouldn't", 'since', 'six', 'so', 'some', 'somebody', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry', 'specified', 'specify', 'specifying', 'still', 'sub', 'such', 'sup', 'sure', "t's", 'take', 'taken', 'tell', 'tends', 'th', 'than', 'thank', 'thanks', 'thanx', 'that', "that's", 'thats', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence', 'there', "there's", 'thereafter', 'thereby', 'therefore', 'therein', 'theres', 'thereupon', 'these', 'they', "they'd", "they'll", "they're", "they've", 'think', 'third', 'this', 'thorough', 'thoroughly', 'those', 'though', 'three', 'through', 'throughout', 'thr', 'thus', 'to', 'together', 'too', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying', 'twice', 'two', 'un', 'under', 'unfortunately', 'unless', 'unlikely', 'until', 'unto', 'up', 'upon', 'us', 'use', 'used', 'useful', 'uses', 'using', 'usually', 'value', 'various', 'very', 'via', 'viz', 'vs', 'want', 'wants', 'was', "wasn't", 'way', 'we', "we'd", "we'll", "we're", "we've", 'welcome', 'well', 'went', 'were', "weren't", 'what', "what's", 'whatever', 'when', 'whence', 'whenever', 'where', "where's", 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', "who's", 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'willing', 'wish', 'with', 'within', 'without', "won't", 'wonder', 'would', "wouldn't", 'yes', 'yet', 'yo', "yo'd", "yo'll", "yo're", "yo've", 'your', 'yours', 'yourself', 'yourselves', 'zero']]


def clean_punctuations(words):
    return [word for word in words if word not in string.punctuation]


def clean_projects(words):
    return [word for word in words if word not in ['akka', 'akka', 'hadley', 'devtools', 'johnmyleswhite', 'ProjectTemplate', 'mavam', 'stat-cookbook', 'facebook', 'hiphop-php', 'yihui', 'knitr', 'rstudio', 'shiny', 'facebook', 'folly', 'mongodb', 'mongo', 'TTimo', 'doom3.gpl', 'ariya', 'phantomjs', 'TrinityCore', 'TrinityCore', 'mangos', 'MaNGOS', 'bitcoin', 'bitcoin', 'keithw', 'mosh', 'xbmc', 'xbmc', 'joyent', 'http-parser', 'kr', 'beanstalkd', 'antirez', 'redis', 'liuli', 'ccv', 'memcached', 'memcached', 'openframeworks', 'openFrameworks', 'libgit2', 'libgit2', 'vmg', 'redcarpet', 'joyent', 'libuv', 'SignalR', 'SignalR', 'hbons', 'SparkleShare', 'moxiecode', 'plupload', 'mono', 'mono', 'NancyFx', 'Nancy', 'ServiceStack', 'ServiceStack', 'AutoMapper', 'AutoMapper', 'restsharp', 'RestSharp', 'ravendb', 'ravendb', 'SamSaffron', 'MiniProfiler', 'nathanmarz', 'storm', 'elasticsearch', 'elasticsearch', 'JakeWharton', 'ActionBarSherlock', 'facebook', 'facebook-android-sdk', 'clojure', 'clojure', 'Bukkit', 'CraftBukkit', 'netty', 'netty', 'github', 'android', 'joyent', 'node', 'jquery', 'jquery', 'h5bp', 'html5-boilerplate', 'bartaz', 'impress.js', 'mbostock', 'd3', 'harvesthq', 'chosen', 'FortAwesome', 'Font-Awesome', 'mrdoob', 'three.js', 'zurb', 'foundation', 'symfony', 'symfony', 'EllisLab', 'CodeIgniter', 'facebook', 'php-sdk', 'zendframework', 'zf2', 'cakephp', 'cakephp', 'ginatrapani', 'ThinkUp', 'sebastianbergmann', 'phpunit', 'codeguy', 'Slim', 'django', 'django', 'facebook', 'tornado', 'jkbr', 'httpie', 'mitsuhiko', 'flask', 'kennethreitz', 'requests', 'xphere-forks', 'symfony', 'reddit', 'reddit', 'boto', 'boto', 'django-debug-toolbar', 'django-debug-toolbar', 'midgetspy', 'Sick-Beard', 'divio', 'django-cms', 'rails', 'rails', 'mxcl', 'homebrew', 'mojombo', 'jekyll', 'gitlabhq', 'gitlabhq', 'diaspora', 'diaspora', 'plataformatec', 'devise', 'joshuaclayton', 'blueprint-css', 'imathis', 'octopress', 'vinc', 'vinc.cc', 'thoughtbot', 'paperclip', 'chriseppstein', 'compass', 'twitter', 'finagle', 'robey', 'kestrel', 'twitter', 'flockdb', 'twitter', 'gizzard', 'sbt', 'sbt', 'scala', 'scala', 'scalatra', 'scalatra', 'twitter', 'zipkin']]


def clean_git_commands(words):
    return [word for word in words if word not in ["init", "add", "rm", "mv", "status", "commit", "log", "diff", "show", "branch", "checkout", "merge", "tag", "close", "fetch", "pull", "push", "remote", "reset", "rebase", "bisect", "grep"]]


def line_tokenize(sents):
    sents = [nltk.tokenize.LineTokenizer().tokenize(sent) for sent in sents]
    return nltk.util.flatten(sents)


def sent_tokenize(sents):
    return nltk.tokenize.sent_tokenize(sents)


def word_tokenize(sent):
    return nltk.tokenize.word_tokenize(sent)


def flatten(lists):
    return nltk.util.flatten(lists)


def comment_sent_tokenize(sents):
    sents = clean_email_reply(sents)
    sents = nltk.tokenize.sent_tokenize(sents)
    sents = line_tokenize(sents)
    return sents


def comment_word_tokenize(sent):
    sent = sent.lower()
    words = word_tokenize(sent)
    words = clean_nltk_stopwords(words)
    words = clean_user_stopwords(words)
    words = clean_mysql_stopwords(words)
    words = clean_punctuations(words)
    words = clean_projects(words)
    return words


def parse_topic_model(topic):
    topic = topic.split(' + ')
    topic = [[term[:term.index('*')], term[term.index('*')+1:]] for term in topic]
    topic = [[float(norm), word.strip('"')] for norm, word in topic]
    return topic
'''
