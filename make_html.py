from jinja2 import Environment, FileSystemLoader, select_autoescape
import requests
import json
import datetime
from time import gmtime, strftime

# Jinja2 stuff
def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)


# Declare foldier in which templades are stored
env = Environment(
    loader=FileSystemLoader('templates/'),
    autoescape=select_autoescape(['html', 'xml']),
)

# Gather Data
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)
    rpcuri = 'http://{}:{}'.format(config_data.get('rpchost'), config_data.get('rpcport'))
    raw_data = '{"jsonrpc":"1.0","id":"curltext","method":"getinfo","params":[]}'
    nextsuperblock_request = '{"jsonrpc":"1.0","id":"curltext","method":"getnextsuperblock","params":[]}'
    budgetinfo_request = '{"jsonrpc":"1.0","id":"curltext","method":"getbudgetinfo","params":[]}'
    response = requests.get(rpcuri, headers={'content-type': 'application/json'}, data=raw_data, auth=(config_data.get('rpcusername'), config_data.get('rpcpassword')))
    my_response = response.json().get('result')
    current_block = my_response.get('blocks')
    print(current_block)

    response = requests.get(rpcuri, headers={'content-type': 'application/json'}, data=nextsuperblock_request, auth=(config_data.get('rpcusername'), config_data.get('rpcpassword')))
    next_superblock = response.json().get('result')

    response = requests.get(rpcuri, headers={'content-type': 'application/json'}, data=budgetinfo_request, auth=(config_data.get('rpcusername'), config_data.get('rpcpassword')))
    budgetinfo = response.json().get('result')



time_now = datetime.datetime.utcnow()
delta = next_superblock-current_block
delta = datetime.timedelta(minutes=delta)
time_next_superblock = time_now+delta


fname = "output.html"
context = {
   	'current_block': current_block,
   	'next_superblock': next_superblock,
   	'proposals': budgetinfo,
   	'time_now': time_now.strftime("%Y-%m-%d %H:%M"),
   	'time_next_superblock': time_next_superblock.strftime("%Y-%m-%d %H:%M")
}

print(type(budgetinfo))
with open(fname, 'w') as f:
   	html = env.get_template('template.html').render(context)
   	f.write(html)
