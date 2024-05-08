# from pprint36 import pprint

# built-in
import os
import re
import base64

import platform
import socket

import click
import requests
import json

# third-party
import chardet
from bs4 import BeautifulSoup

# brew update && brew upgrade openssl
# pip install urllib3==1.26.16


# PATTERN = r'(?<!zzd.one:8000)(/media/)'
# BASE = "http://zzd.one:8000/"
# CODEBASE = "http://code.zzd.one:8000/"
PATTERN = r'(?<!zzd.show)(/media/)'
BASE = "https://zzd.show/"
CODEBASE = "https://code.zzd.show/"

DEBUG = True
# DEBUG = False


ENDPOINTS = {
    'web': 'users/cli/', 
    'tokenverify': 'users/cli/tokenverify/',
    'login': 'users/cli/login/',
    'list': 'shows/cli/list/',
    'clone': 'shows/cli/clone/',
    'info': 'shows/cli/info/',
    'static-upload': 'shows/cli/static/upload/',
    'show-upload': 'shows/cli/upload/',
}

for k, v in ENDPOINTS.items():
    ENDPOINTS[k] = BASE + v


# bs4 support
def has_body_scripts(html_str, css_cdns, js_cdns):
    soup = BeautifulSoup(html_str, 'html.parser')
    has_body = soup.body is not None
    # has_script = any(script.has_attr('src') and not script['src'].startswith('http') for script in soup.find_all('script'))
    has_script = False
    for link in soup.find_all('link'):
        if link.has_attr('href'):
            if link['href'].startswith('http'):
                if link['href'] not in css_cdns:
                    css_cdns.append(link['href'])
    for script in soup.find_all('script'):
        if script.has_attr('src'):
            if script['src'].startswith('http'):
                if script['src'] not in js_cdns:
                    js_cdns.append(script['src'])
            else:
                has_script = True
    return [has_body, has_script]


def soup_html(html_str, extract_body=False, remove_scripts=False):
    soup = BeautifulSoup(html_str, 'html.parser')
    if extract_body:
        body = soup.find('body')
        if body:
            soup = BeautifulSoup(''.join(str(tag) for tag in body.contents), 'html.parser')
    if remove_scripts:
        # for script in soup.find_all('script', src=lambda src: not src.startswith('http')):
        for script in soup.find_all('script'):
            script.decompose()
    return str(soup)


def read_and_convert_to_utf8(file_path):
    # Detect the encoding
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'

    # Read the file with the detected encoding
    with open(file_path, 'r', encoding=encoding) as f:
        content = f.read()

    # Convert to UTF-8 if necessary
    if encoding != 'utf-8':
        content = content.encode('utf-8', errors='ignore').decode('utf-8')

    return content


@click.group(help=f"走之底开发 www.zzd.show 客户端 cli - {ENDPOINTS['web']}")
def zzd():
    pass


@zzd.command()
def list():
    """查看我的demo"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, 'data.json')
    token = None
    if os.path.isfile(data_file_path):
        try:
            data = json.loads(read_and_convert_to_utf8(data_file_path))
            token = data['token']
        except Exception as e:
            if DEBUG:
                raise e
    if not token:
        click.echo('您尚未登录，请先通过\nzzd login\n登录')
        return
    try:
        response = requests.post(ENDPOINTS['list'], data={
            'token': token, 
        })
        if response.status_code == 200:
            data = response.json()['data']
            click.echo(data)
        elif response.status_code == 402 and data['username']:
            click.echo(f'API冷却当中，我们暂时无法核验该操作。\n若您需要核验登录状态，请在30秒后重试')
            return
    except Exception as e:
        if DEBUG:
            raise e   
        click.echo("抱歉，您的网络不稳定或者服务器流量过大，请稍后重试")
        return


@zzd.command(help="唯一参数，可以是一个序号或者一个链接")
@click.argument('demo', type=str)
def info(demo):
    """调取demo基本信息"""
    def extractPk(inp):
        try:
            if str(int(inp)) == str(inp):
                return int(inp)
        except Exception as e:
            if DEBUG:
                raise e
        match = re.search(r'/(?P<int>\d+)', inp)
        if match:
            return int(match.group('int'))
        else:
            return None

    pk = extractPk(demo)
    if not pk:
        click.echo('参数不合法，请带上一个序号或者一个链接')
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, 'data.json')
    token = None
    if os.path.isfile(data_file_path):
        try:
            data = json.loads(read_and_convert_to_utf8(data_file_path))
            token = data['token']
        except Exception as e:
            if DEBUG:
                raise e
    if not token:
        click.echo('您尚未登录，请先通过\nzzd login\n登录')
        return

    """ error messages
    400 internal server error
    401 auth failed id or passcode
    402 exceed auth token rate limit 
    403 show not allow user
    """

    try:
        response = requests.post(ENDPOINTS['info'], data={
            'token': token, 
            'pk': pk, 
        })
        if response.status_code == 200:
            # click.echo("正在尝试访问...")
            click.echo(response.json()['data'])
            return
        elif response.status_code == 402:
            click.echo('API冷却当中，请过30秒再进行操作')
        else:
            click.echo('抱歉API调用失败，可能是登录密匙已过期')
    except Exception as e:
        if DEBUG:
            raise e
        click.echo("抱歉，您的网络不稳定或者服务器流量过大，请稍后重试")
        return


@zzd.command()
def login():
    """登录您的账号, 请前往官网查询id以及passcode"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, 'data.json')
    still_working = False
    username = ''
    if os.path.isfile(data_file_path):
        try:
            data = json.loads(read_and_convert_to_utf8(data_file_path))
            token = data['token']
            # tries to check if the current token still works
            try:
                # also implemented rate limit
                response = requests.post(ENDPOINTS['tokenverify'], data={
                    'token': token, 
                })
                if response.status_code == 200:
                    still_working = True
                    username = response.json()['username']
                elif response.status_code == 402 and data['username']:
                    click.echo(f'API冷却当中，我们暂时无法核验该操作。\n若您需要核验登录状态，请在30秒后重试')
                    return
            except Exception as e:
                if DEBUG:
                    raise e
        except Exception as e:
            if DEBUG:
                raise e
            click.echo("抱歉，您的网络不稳定或者服务器流量过大，请稍后重试")
            return
    if still_working and username:
        click.echo(f'您已以{username}登录, 若需要切换账号或者重新登录，请先使用\nzzd logout\n退出当前账号')
        return
    click.echo('登录您的账号, 使用id以及passcode')
    tut_site = ENDPOINTS['web']
    click.echo(f'若不清楚，请前往\n{tut_site}\n查看详细操作步骤\n')
    _id = click.prompt('id', type=int)
    passcode = click.prompt('密钥', type=str)
    # response = requests.post('https://www.zzd.show/users/cli/login/', data={'id': _id, 'passcode': passcode})
    try:
        response = requests.post(ENDPOINTS['login'], data={
            'id': _id, 
            'passcode': passcode, 
            'device': json.dumps({
                'ip': socket.gethostbyname(socket.gethostname()), 
                'system': platform.system(),
                'node': platform.node(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
            }, ensure_ascii=False)
        })
        if response.status_code == 200:
            # click.echo("正在尝试访问...")
            data = response.json()
            # click.echo(data)
            # [status, msg]
            if data['status'] == 200:
                # local storage
                username = data['username']
                with open(data_file_path, 'w', encoding="utf-8") as file:
                    json.dump({'token': data['msg'], 'username': username}, file)
                click.echo(f"\n登陆成功，欢迎{username}\n您可以使用 \nzzd --help\n 查看命令帮助")
            else:
                st = '抱歉登录失败，可能是由于API冷却中，可能是您的登录信息错误'
                try:
                    st = data['msg']
                except Exception as e:
                    if DEBUG:
                        raise e
                click.echo(st)
                return
    except Exception as e:
        if DEBUG:
            raise e
        click.echo("抱歉，您的网络不稳定或者服务器流量过大，请稍后重试")
        return

@zzd.command()
def logout():
    """退出您的账号本地登录"""
    # Assuming you're using a token that needs to be invalidated
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, 'data.json')
    if os.path.isfile(data_file_path):
        os.remove(data_file_path)
    click.echo("退出登录成功")


def get_compiled_name(rawname, generic):
    sld = rawname.split('.')
    ext = sld.pop()
    nm = '.'.join(sld) + '_' + ext + '.' + generic
    return nm


def process_media_links(raw_text):
    # Regular expression to target /media/ that appears at the start of the path or after a space or quote,
    # and not part of a full URL (by checking it's not immediately following ':' or a slash)
    pattern = r'(?<![:/.\w])(/media/)'
    # Replacement string with the desired URL prefix
    replacement = 'https://code.zzd.show/media/'
    # Using re.sub() to replace the matched patterns in the string
    return re.sub(pattern, replacement, raw_text)


# print(process_media_links('''
# <div class="content">
# <img src="https://cdn.io/media/portray/ksenia.jpg"/>
# </div>

# <div class="content">
# <img src="/media/portray/ksenia.jpg"/>
# </div>

# div{
#     background: url('/media/portray/ksenia.jpg');
# }
# '''))
# exit()

def html_embrace(compiled: bool, cdndt, title, _html, css_refs, js_all):
    html = process_media_links(_html)
    css_blocks = '\n'
    js_blocks = '\n'
    if cdndt:
        cdn_css = cdndt.get('css')
        cdn_js = cdndt.get('js')
        if cdn_css:
            for cdn in cdn_css:
                css_blocks += f'<link rel="stylesheet" href="{cdn}" />\n'
                if cdn == cdn_css[-1]:
                    css_blocks += '\n'
        if cdn_js:
            for cdn in cdn_js:
                js_blocks += f'<script src="{cdn}"></script>\n'
                if cdn == cdn_js[-1]:
                    js_blocks += '\n'
    if css_refs:
        for i, href in enumerate(css_refs):
            href = '../' + href
            if compiled:
                href = '../' + href
            css_blocks += f'<link rel="stylesheet" href="{href}" />'
            if i != len(css_refs) - 1:
                css_blocks += '\n'
    if js_all:
        for i, dt in enumerate(js_all):
            src = '../' + dt['path']
            if compiled:
                src = '../' + src
            js_blocks += f'<script src="{src}"'
            if dt.get('is_module', None):
                js_blocks +=  ' type="module"'
            js_blocks += '></script>'
            if i != len(js_all) - 1:
                js_blocks += '\n'
    if ('</head>' in html) and ('</body>' in html):
        sld = html.split('</head>')
        sld[0] += css_blocks
        t1 = '</head>'.join(sld)

        sld2 = t1.split('</body>')
        sld2[0] += js_blocks
        t2 = '</body>'.join(sld2)
        return t2
    else:
        sld = [
            '<!DOCTYPE html>', 
            '<html lang="en">', 
            '<head>', 
            '   <meta charset="UTF-8">', 
            '   <meta name="viewport" content="width=device-width, initial-scale=1.0">', 
            f'   <title>{title}</title>', 
            '</head>',
            css_blocks,  
            '<body>',
            html, 
            js_blocks, 
            '</body>', 
            '</html>', 
        ]
        return '\n'.join(sld)


def writeLog(data, baselevel=True):
    # if baselevel, we are not in the directory
    if not data: return
    if baselevel:
        log_path = os.path.join(data['title'], 'log.json')
    else:
        log_path = 'log.json'
    with open(log_path, 'w', encoding="utf-8") as f:
        rdt = {
            'pk': data['pk'], 
            'title': data['title'], 
            'createTime': data['createTime'], 
            'author': data['author'], 
            'detailLink': data['detailLink'], 
            'tags': data['tags'], 
            'cdns': data['cdns'], 
        }
        if data.get('project'):
            rdt['project'] = data['project']
        if data.get('pack'):
            rdt['pack'] = data['pack']
        json.dump(rdt, f, indent='\t', ensure_ascii=False)


def filespawn(data, commit=True):
    '''
    pk, title, detailLink, tags, 
    cdns {path_str: author_pk}
    textcode {
        html: {index.pug: {
            unplug: 0, 
            raw, 
            compiled,     
        }}, 
        css ...
    }
    '''         
    # click.echo(data)  
    # return
    if commit: os.makedirs(data['title'], exist_ok=True)
    dirpath = os.path.join(data['title'])
    # narrative
    writeLog(data, True)
    # file parse 
    css_refs = []
    js_refs = []
    js_all = []
    for generic, ddt in data['textcode'].items():
        if generic == 'html': continue
        generic_dir = os.path.join(dirpath, generic)
        if commit: os.makedirs(generic_dir, exist_ok=True)
        for filename, dt in ddt.items():
            unplug = dt.get('unplug')
            raw = dt.get('raw')
            compiled = dt.get('compiled')
            filepath = os.path.join(generic_dir, filename)
            if commit:
                with open(filepath, 'w', encoding="utf-8") as f:
                    f.write(process_media_links(raw))
            if compiled:
                compiled_dir = os.path.join(generic_dir, 'compiled')
                compiled_name = get_compiled_name(filename, generic)
                compiled_path = os.path.join(compiled_dir, compiled_name)
                if commit:
                    os.makedirs(compiled_dir, exist_ok=True)
                    with open(compiled_path, 'w', encoding="utf-8") as f:
                        f.write(process_media_links(compiled))
                _sld = compiled_path.split('/')
                _sld.pop(0)
                relative_path = '/'.join(_sld)
                if generic == 'css':
                    css_refs.append(relative_path)
                elif generic == 'js':
                    js_refs.append(relative_path)
                    js_all.append({
                        'path': relative_path,
                        'is_module': dt.get('is_module', 0), 
                    })
            else:
                _sld = filepath.split('/')
                _sld.pop(0)
                relative_path = '/'.join(_sld)
                if generic == 'css':
                    css_refs.append(relative_path)
                elif generic == 'js':
                    js_refs.append(relative_path)
                    js_all.append({
                        'path': relative_path,
                        'is_module': dt.get('is_module', 0), 
                    })
            # print(generic, filename, unplug, raw, compiled)
    html = data['textcode'].get('html')
    if not html:
        html = {'index.html': {'raw': '', 'compiled': '', 'unplug': 0}}
    generic = 'html'
    generic_dir = os.path.join(dirpath, generic)
    if commit: os.makedirs(generic_dir, exist_ok=True)
    for filename, dt in html.items():
        unplug = dt.get('unplug')
        raw = dt.get('raw')
        compiled = dt.get('compiled')
        filepath = os.path.join(generic_dir, filename)
        if compiled:
            compiled_dir = os.path.join(generic_dir, 'compiled')
            compiled_name = get_compiled_name(filename, generic)
            compiled_path = os.path.join(compiled_dir, compiled_name)
            if commit:
                    os.makedirs(compiled_dir, exist_ok=True)
                    with open(compiled_path, 'w', encoding="utf-8") as f:
                        f.write(html_embrace(True, data['cdns'], data['title'], compiled, css_refs, js_all))
        if commit:
            with open(filepath, 'w', encoding="utf-8") as f:
                if not compiled:
                    # html
                    f.write(html_embrace(False, data['cdns'], data['title'], raw, css_refs, js_all))
                else:
                    # pug, etc (handled in previous condition, only compiled parsed)
                    f.write(process_media_links(raw))


# exit()

@zzd.command(help="唯一参数，可以是一个序号或者一个链接")
@click.argument('demo', type=str)
def clone(demo):
    """将demo复制到本地"""
    def extractPk(inp):
        try:
            if str(int(inp)) == str(inp):
                return int(inp)
        except Exception as e:
            if DEBUG:
                raise e
        match = re.search(r'/(?P<int>\d+)', inp)
        if match:
            return int(match.group('int'))
        else:
            return None

    pk = extractPk(demo)
    if not pk:
        click.echo('参数不合法，请带上一个序号或者一个链接')
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, 'data.json')
    token = None
    if os.path.isfile(data_file_path):
        try:
            data = json.loads(read_and_convert_to_utf8(data_file_path))
            token = data['token']
        except Exception as e:
            if DEBUG:
                raise e
    if not token:
        click.echo('您尚未登录，请先通过\nzzd login\n登录')
        return

    """ error messages
    400 internal server error
    401 auth failed id or passcode
    402 exceed auth token rate limit 
    403 show not allow user
    """

    try:
        response = requests.post(ENDPOINTS['clone'], data={
            'token': token, 
            'pk': pk, 
        })
        if response.status_code == 200:
            # click.echo("正在尝试访问...")
            data = json.loads(response.json()['data'])
            title = data['title']
            current_dir = os.getcwd()
            clone_dir = os.path.join(current_dir, title)
            if os.path.isdir(clone_dir):
                click.echo(f'操作失败-检测到重名文件夹已存在\n{clone_dir}:')
                return
            filespawn(data) 
            click.echo(f'成功复刻{title}到\n{clone_dir}')
            return
        elif response.status_code == 402:
            click.echo('API冷却当中，请过30秒再进行操作')
        else:
            msg = '抱歉API调用失败，可能是登录密匙已过期'
            try:
                msg = response.json()['msg']
            except Exception as e:
                if DEBUG:
                    raise e
            click.echo(msg)
    except Exception as e:
        if DEBUG:
            raise e
        click.echo("抱歉，您的网络不稳定或者服务器流量过大，请稍后重试")
        return

@zzd.command()
def push():
    # """将本地更改同步到服务器数据库"""
    # # inspect: dirs check
    annotations = {
        'html': '可以包含html, pug, haml文件', 
        'css': '可以包含css, scss, less, pcss, styl文件', 
        'js': '可以包含js, ts, coffee, ls文件', 
        # image, font, audio, video
        'static': '静态媒体文件，如图片，字体，声音，视频', 
    }

    # ===== auth =====
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file_path = os.path.join(script_dir, 'data.json')
    token = None
    if os.path.isfile(data_file_path):
        try:
            data = json.loads(read_and_convert_to_utf8(data_file_path))
            token = data['token']
        except Exception as e:
            if DEBUG:
                raise e
    if not token:
        click.echo('您尚未登录，请先通过\nzzd login\n登录')
        return

    # ===== inspect =====
    supported_exts = {
        'html': {
            'html', 'pug', 'haml', 
        }, 
        'css': {
            'css', 'scss', 'less', 'pcss', 'styl', 
        }, 
        'js': {
            'js', 'ts', 'coffee', 'ls', 
        }, 
    }
    current_dir = os.getcwd()
    current_dir_name = os.path.basename(current_dir)
    current_items = os.listdir(current_dir)

    static_dir = os.path.join(current_dir, 'static')    
    css_dir = os.path.join(current_dir, 'css')    
    js_dir = os.path.join(current_dir, 'js')    
    html_dir = os.path.join(current_dir, 'html')

    c = f'若您的页面运用了第三方cdn链接，请在{current_dir_name}文件夹中必要添加log.json注明cdn，如：\n'
    c += '\n{"cdns": {'
    c += '\n\t"css": ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"],'
    c += '\n\t"js": []'
    c += '\n}}\n'
    c += '否则cdn无法被记录\n\n'

    h = f'zzd push 会将当前文件夹{current_dir_name}作为前端静态页面上传到服务器\n'
    h += '通常包括以下文件\n'
    h += '\n  log.json: 对于更改下载推进，log.json是走之底自动生成的记录文档，它让我们知道您想更新哪个页面。它不是必要的，若没有该文件，则默认为新建页面。'
    h += '\n  ' + '由于未检测到html文件, ' + c
    h += f'目前在{current_dir_name}中仅支持以下子文件夹：\n\n'
    for k, v in annotations.items():
        h += f'  {k}: {v}\n'
    h += '\n且上述支持读取的文件夹，必须只包含一维文件，而不涵盖更多子文件夹等更复杂结构'
    h += '\n我们检测到您的文件夹构架有一些问题：'

    errors = []
    dirs = set()
    fns = set()
    compiled_warn = False
    for item in current_items:
        p = os.path.join(current_dir, item)
        if os.path.isdir(p) and len(os.listdir(p)):
            dirs.add(item)
            for _item in os.listdir(p):
                _p = os.path.join(p, _item)
                if os.path.isdir(_p) and len(os.listdir(_p)):
                    if _item != 'compiled':
                        errors.append(f'{item}文件夹包含了子文件夹{_item}，该子文件夹中内容无法被读取，它应只包含文件')
                    else:
                        if not compiled_warn:
                            compiled_warn = True
                            errors.append(f'html, css或者js文件夹中的compiled文件夹，不会参与上传。若运用预处理技术，请在源代码文件上传成功后，前往编辑器页面手动保存，否则沙盒嵌入式可能为空白无法展示')
        elif os.path.isfile(p):
            fns.add(item)
    usual = {'html', 'css', 'js'}
    lack = usual - dirs
    supported = {'static'}
    extra = dirs - (usual | supported)
    if len(lack) > 1:
        for l in lack:
            errors.append(f'没有{l}文件夹，这是正常的若您的项目没运用{l}文件')
    if len(extra):
        for l in extra:
            errors.append(f'文件夹{l}暂不支持，上传操作中其会被忽略')
    md = ''
    hasHtml = False
    if os.path.isdir(html_dir):
        for item in os.listdir(html_dir):
            html_path = os.path.join(html_dir, item)
            if os.path.isfile(html_path) and html_path.endswith('.html'):
                hasHtml = True
                break

    log_path = os.path.join(current_dir, 'log.json')
    dt = {}
    if os.path.isfile(log_path):
        if os.path.getsize(log_path) != 0:
            try:
                dt = json.loads(read_and_convert_to_utf8(log_path))
            except json.JSONDecodeError:
                click.echo('您的 log.json 格式存在一些错误，请修正后重试')
                return

    if not hasHtml:
        errors.append(f'html文件夹下未检测到html文件，很抱歉我们无法读取其他类型如haml, pug中的三方cdn，因此若您的项目使用了cdn，请在log.json中叙述，未使用cdn则不用担心')
    if len(errors):
        md = '忽略上述问题'
        e = '\n\n'
        for i, l in enumerate(errors):
            e += f'  {i + 1}. {l}\n'
        e += '\n或许您应该修改文件内容或目录结构\n'
        click.echo(h + e)
        yn = click.prompt(f'请问是否{md}继续上传？(y/n)(默认为是)', type=bool, default=True)
    else:
        if not dt.get('cdns'):
            click.echo(c)
            yn = click.prompt(f'请问是否{md}继续上传？(y/n)(默认为是)', type=bool, default=True)
        else:
            yn = True
    
    if yn:
    # if 1:
        # ===== summerize =====

        sizeRes = []
        sizers = []
        def sizeOk(ext, directory, limit, res, sizers, sizer):
            sexts = supported_exts.get(ext)
            if not os.path.isdir(directory): return
            if not len(os.listdir(directory)): return
            total_size = 0
            # for dirpath, _, filenames in os.walk(directory):
            for item in os.listdir(directory):
                filepath = os.path.join(directory, item)
                if os.path.isfile(filepath):
                    if sexts and item.split('.')[-1] not in sexts:
                        jn = ', '.join(sexts)
                        if item == '.DS_Store':
                            yn = True
                        else:
                            yn = click.prompt(f'{ext}文件夹下{item}不支持，目前仅支持{sexts}，因此会被忽略不上传，是否继续上传操作？(y/n)（默认为是）', type=bool, default=True)
                        if yn:
                            continue
                        else:
                            exit()
                    total_size += os.path.getsize(filepath)
            # total_size_mb = round(total_size, 1)
            total_size_mb = round(total_size / (1024 * 1024), 1)
            dirname = os.path.basename(directory)
            if total_size_mb > limit:
                res.append(f'{dirname}文件夹 超出大小限制 限制为{limit}mb 该文件夹为{total_size_mb}mb')
                return False
            sizers.append(sizer)

        sizeOk('', static_dir, 48, sizeRes, sizers, 'static')
        sizeOk('html', html_dir, 16, sizeRes, sizers, 'html')
        sizeOk('css', css_dir, 16, sizeRes, sizers, 'css')
        sizeOk('js', js_dir, 16, sizeRes, sizers, 'js')

        if sizeRes:
            click.echo('\n'.join(sizeRes))
            return 

        if not dt.get('title'):
            dt['title'] = click.prompt(f'将该页面命名为(默认{current_dir_name})', type=str, default=current_dir_name)
        '''
        html: {index.pug: {
            unplug: 0, 
            raw, 
            compiled,     
        }}, 
        '''

        html = {}
        css = {}
        js = {}
        dt['code'] = {
            'html': html, 
            'css': css, 
            'js': js, 
        }
        # this is not cdn, it is files to upload (share)

        static_uploaded = False
        # mapper generated during static upload
        # used in relative path switch
        relative_paths = {}

        def static_upload(relative_paths, file_paths, overwrites=[], force=False):
            """
            {'e': '小学徒无法静态文件哦，只有魔法师有1GB文件上传资格'}
            {'done': [{'pk': 1, 'path': 'http://zzd.one:8000/media/uploaded/1/1.jpg', 'route': 'media/uploaded/1/1.jpg', 'size': 192893, 'date': '2024年03月03日'}]}
            """
            files = []
            fileData = {}
            for f in file_paths:
                endname = os.path.basename(f)
                files.append(('files', (endname, open(f, 'rb'))))
                fileData[endname] = f
            headers = {'Authorization': f'Bearer {token}'}
            try:
                response = requests.post(ENDPOINTS['static-upload'], headers=headers, data={
                    'action': 'force' if force else '', 
                    'overwrites': json.dumps(overwrites, ensure_ascii=False), 
                }, files=files)
            except Exception as e:
                if DEBUG:
                    raise e
                click.echo("抱歉，您的网络不稳定或者服务器流量过大，请稍后重试")
                exit()
            if response.status_code == 201:
                # ok but has dups
                dups = response.json()['dups']
                # print(dups)
                ignore_files = []
                click.echo('\n文件存在重名，最好避免上传相同文件，接下来为您展示重名文件以及存在路径，请判断是否继续上传（继续上传将自动重命名）')
                _overwrites = []
                for endname, url in dups.items():
                    yn = click.prompt(f'{endname}存在路径：{url}，1.跳过 2.内容覆盖 3. 重命名后上传', type=int, default=1)
                    # yn = click.prompt(f'{endname}存在路径：{url}，继续上传？(y/n)（默认为否）', type=bool, default=False)
                    # if not yn:
                    if yn == 1:
                        ignore_files.append(endname)
                        relative_paths[endname] = url
                    if yn == 2:
                        _overwrites.append(endname)
                nfiles = []
                for f in file_paths:
                    if os.path.basename(f) not in ignore_files:
                        nfiles.append(f)
                if not nfiles:
                    return
                return static_upload(relative_paths, nfiles, _overwrites, force=True)
            elif response.status_code == 200:
                # succeed
                # print(response.json())
                '''
                {'done': [{
                    'pk': 3, 
                    'path': 'http://zzd.one:8000/media/uploaded/1/1_alnqNVq.jpg', 
                    'route': 'media/uploaded/1/1_alnqNVq.jpg', 
                    'size': 192893, 
                    'date': '2024年03月03日', 
                    'name': '1.jpg'
                }]}
                '''
                res = response.json()
                done = res['done']
                wmsgs = res.get('wmsgs')
                if wmsgs:
                    click.echo(wmsgs)
                for di in done:
                    click.echo(f'static成功上传静态文件{di["name"]}到{di["path"]}')
                    endname = di['name']
                    for f in file_paths:
                        if os.path.basename(f) == di['name']:
                            relative_paths[di['name']] = di['path']
            else:
                try:
                    mdt = response.json()
                    msg = mdt.get('msg') or mdt.get('e')
                    click.echo(msg)
                    # show feed back in api, where to go to fix the issue
                    link = mdt.get('link')
                    if link:
                        click.echo(f'请前往{link}\n查看解决方案')
                    exit()
                except Exception as e:
                    if DEBUG:
                        raise e
                    click.echo('static静态文件上传失败')

        # upload static first
        static_paths = []
        if os.path.isdir(static_dir):
            for static_name in os.listdir(static_dir):
                static_path = os.path.join(static_dir, static_name)
                if os.path.isfile(static_path):
                    static_paths.append(static_path)

        static_upload(relative_paths, static_paths)
        # testonly below
        # relative_paths = {'1.jpg': 'http://zzd.one:8000/media/uploaded/1/1_alnqNVq.jpg'}

        soup_warned = {"v": False}
        relative_switches = {}

        def soup_prewarn(soup_warned):
            if soup_warned['v']: return
            soup_warned['v'] = True
            click.echo('\n\n上传到云的html页面应该只包含body标签里面的内容，最好省略DOCTYPE，title等前置')
            click.echo('不必担心该操作会导致页面中资源链接被删除')
            click.echo('若未使用html文件，您需要确保外部cdn已在log.json中叙述')
            click.echo('我们会帮助你替换所有本地静态文件的路径关联')
            click.echo('(以下操作 只上传body内部内容与移除相对路径script 最好全部选择是)')

        css_cdns = []
        js_cdns = []
        def iterLoad(data, supported_exts, _dir, ishtml=False):
            for filename in os.listdir(_dir):
                filepath = os.path.join(_dir, filename)
                if os.path.isfile(filepath):
                    ext = filename.split('.')[-1]
                    if filename == '.DS_Store':
                        continue
                    if ext not in supported_exts:
                        yn = click.prompt(f'{filename}文件类型不支持，上传过程将会忽略它，是否继续?(y/n)（默认为是）', type=bool, default=True)
                        if not yn:
                            exit()
                    try:
                        raw = read_and_convert_to_utf8(filepath)
                        # html bs4 support
                        if ishtml and filename.endswith('html'):
                            [has_body, has_script] = has_body_scripts(raw, css_cdns, js_cdns)
                            extract_body = False
                            remove_scripts = False
                            if has_body:
                                soup_prewarn(soup_warned)
                                extract_body = click.prompt(f'{filename}上传前是否进行简化处理，只上传body内部内容？(y/n)（默认为是）', type=bool, default=True)
                            if has_script:
                                soup_prewarn(soup_warned)
                                remove_scripts = click.prompt(f'{filename}上传前是否将所有相对路径的script移除？(y/n)（默认为是）', type=bool, default=True)
                            raw = soup_html(raw, extract_body, remove_scripts)
                    except Exception as e:
                        if DEBUG:
                            raise e
                        click.echo(f'此文件无法被读取，请确保编码为utf-8或者其他可读取的类型 {filepath}')
                        exit()
                    if relative_switches and len(relative_switches):
                        for endname, url in relative_switches.items():
                            data[filename] = raw.replace(endname, url)
                    else:
                        data[filename] = raw

        if relative_paths and len(relative_paths):
            yn = click.prompt('\n由于此次push包含static静态文件，您是否希望我们对文件内部路径进行批量修改？\n这不会改变您的本地文件，但可以在线上版本帮您同步到上传后的路径，避免图片，字体文件等加载缺失？(y/n)（默认为是）', type=bool, default=True)
            if yn:
                for endname, url in relative_paths.items():
                    # ask then assign to relative_switches
                    rpath = f'../static/{endname}'
                    yn = click.prompt(f'将所有 {rpath} 替换为 {url}?(y/n)（默认为是）', type=bool, default=True)
                    if yn:
                        relative_switches[rpath] = url

        if 'html' in sizers:
            iterLoad(html, supported_exts['html'], html_dir, True)
        if 'css' in sizers:
            iterLoad(css, supported_exts['css'], css_dir)
        if 'js' in sizers:
            iterLoad(js, supported_exts['js'], js_dir)

        # assign cdn result to dt 
        if js_cdns or css_cdns:
            dt['cdns'] = {'css': css_cdns, 'js': js_cdns}

        # pprint(dt['code']['html']['index.html'])

        ''' dt interface {
            pk: int, 
            tags: [str, str, ...], 
            "cdns": {
                "css": [],
                "js": []
            },
            code: {
                "html": {index.pug: sometext, ...},
                "css": ..., 
            },
        } '''
        # ===== finish load =====
        try:
            response = requests.post(ENDPOINTS['show-upload'], data={
                'token': token, 
                'dt': json.dumps(dt, ensure_ascii=False), 
            })
            if response.ok:
                res = response.json()
                click.echo(res['msg'])
                # summerize message is generated in backend api
                # make modification to log.json
                sdt = res.get('data')
                if sdt:
                    writeLog(json.loads(sdt), False)
                return
            else:
                msg = '抱歉API调用失败，可能是登录密匙已过期'
                try:
                    msg = response.json()['msg']
                except:
                    pass
                click.echo(msg)
                return        
        except Exception as e:
            if DEBUG:
                raise e
            click.echo("抱歉，您的网络不稳定或者服务器流量过大，请稍后重试")
        return


if __name__ == '__main__':
    zzd()



