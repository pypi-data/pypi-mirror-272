import argcomplete
import importlib.metadata

from mando import command, main
from datetime import datetime

from ketacli.sdk.base.client import *
from ketacli.sdk.base.search import search_spl
from ketacli.sdk.request.list import list_assets_request, list_admin_request
from ketacli.sdk.request.create import create_asset_request
from ketacli.sdk.request.get import get_asset_by_id_request
from ketacli.sdk.request.update import update_asset_request
from ketacli.sdk.request.delete import delete_asset_request
from ketacli.sdk.request.asset_map import get_resources, get_resource

from ketacli.sdk.output.output import list_output, describe_output, get_asset_output
from ketacli.sdk.output.output import search_result_output
from ketacli.sdk.output.format import format_table
from ketacli.sdk.output.output import rs_output_all, rs_output_one, rs_output_one_example
from ketacli.sdk.util import parse_url_params, template_render
from rich.console import Console

console = Console()


@command
def login(name="keta", endpoint="http://localhost:9000", token=""):
    """Login to ketadb, cache authentication info to ~/.keta/config.yaml

    :param repository: Repository to push to.
    :param -n, --name: The login account name. Defaults to "keta".
    :param -e, --endpoint: The ketadb endpoint. Defaults to "http://localhost:9000".
    :param -t, --token: Your keta api token, create from ketadb webui. Defaults to "".
    """
    do_login(name=name, endpoint=endpoint, token=token)


@command
def logout():
    """Logout from ketadb, clear authentication info"""
    do_logout()


@command
def list(asset_type, groupId=-1, order="desc", pageNo=1, pageSize=10, prefix="", sort="updateTime", fields="",
         format=None, raw=False, lang=None, extra=None):
    """List asset (such as repo,sourcetype,metric...) from ketadb

    :param asset_type: The asset type such as repo, sourcetype, metirc, targets ...
    :param -l, --pageSize: Limit the page size.
    :param --pageNo: Limit the page number.
    :param --prefix: Fuzzy query filter.
    :param --sort: The field used to order by
    :param --order: The sort order, desc|asc
    :param --fields: The fields to display. Separate by comman, such as "id,name,type"
    :param -f, --format: The output format, text|json|csv|html|latex
    :param --groupId: The resource group id.
    :param --raw: Prettify the time field or output the raw timestamp, if specified, output the raw format
    :param --lang: Choose the language preference of return value
    :param -e, --extra: extra query filter, example: include_defaults=true,flat_settings=true
    """
    extra_dict = {}
    if extra is not None:
        # 解析 url 参数为 dict
        extra_dict = parse_url_params(extra)
    req = list_assets_request(
        asset_type, groupId, order, pageNo, pageSize, prefix, sort, lang, **extra_dict)
    resp = request_get(req["path"], req["query_params"],
                       req["custom_headers"]).json()
    output_fields = []
    if len(fields.strip()) > 0:
        output_fields = fields.strip().split(",")
    table = list_output(asset_type, output_fields=output_fields, resp=resp)
    if table is None:
        console.print(f"we cannot find any {asset_type}")
    else:
        console.print(format_table(table, format, not raw), overflow="fold")


@command
def admin(asset_type, format=None, extra=None):
    """List asset (such as repo,sourcetype,metric...) from ketadb

    :param asset_type: The asset type such as repo, sourcetype, metirc, targets ...
    :param -f, --format: The output format, text|json|csv|html|latex
    :param -e, --extra: extra query filter, example: include_defaults=true,flat_settings=true
    """
    extra_dict = {}
    if extra is not None:
        # 解析 url 参数为 dict
        extra_dict = parse_url_params(extra)
    req = list_admin_request(asset_type, **extra_dict)
    resp = request_get(req["path"], req["query_params"], req["custom_headers"]).json()
    output_fields = []
    table = list_output(asset_type, output_fields=output_fields, resp=resp)
    if table is None:
        console.print(f"we cannot find any {asset_type}")
    else:
        console.print(format_table(table, format))


@command
def get(asset_type, asset_id, fields="", format=None, lang=None, extra=None):
    """Get asset detail info from ketadb

    :param asset_type: The asset type such as repo, sourcetype, metirc, targets ...
    :param asset_id: The unique id of asset. (such as id or name...)
    :param --fields: The fields to display. Separate by comman, such as "id,name,type"
    :param -f, --format: The output format, text|json|csv|html|latex
    :param --lang: Choose the language preference of return value
    :param -e, --extra: extra args, example:id=1234567890,name=test
    """
    if extra:
        extra_args_map = parse_url_params(extra)
    else:
        extra_args_map = {}
    extra_args_map['name'] = asset_id

    req = get_asset_by_id_request(
        asset_type=asset_type, asset_id=asset_id, lang=lang, **extra_args_map)
    resp = request_get(req["path"], req["query_params"],
                       req["custom_headers"]).json()
    if format == "json":
        console.print(json.dumps(resp, indent=2, ensure_ascii=False))
        return

    output_fields = []
    if len(fields.strip()) > 0:
        output_fields = fields.strip().split(",")
    table = get_asset_output(output_fields=output_fields, resp=resp)
    table.align = "l"
    if table is None:
        console.print(f"we cannot find any {asset_type}")
    else:
        console.print(format_table(table, format), overflow="fold")


@command
def describe(asset_type, format=None):
    """Describe the schema of asset type

    :param asset_type: The asset type such as repo, sourcetype, metirc, targets ...
    :param -f, --format: The output format, text|json|csv|html|latex
    """

    req = list_assets_request(asset_type)
    resp = request_get(req["path"], req["query_params"],
                       req["custom_headers"]).json()
    table = describe_output(asset_type, resp=resp)
    if table is None:
        console.print(f"we cannot find any {asset_type}")
    else:
        console.print(format_table(table, format), overflow="fold")


@command
def search(spl, start=None, end=None, limit=100, format=None, raw=False):
    """Search spl from ketadb

    :param spl: The spl query
    :param --start: The start time. Time format "2024-01-02 10:10:10"
    :param --end: The start time. Time format "2024-01-02 10:10:10"
    :param -l, --limit: The limit size of query result
    :param -f, --format: The output format, text|json|csv|html|latex
    :param --raw: Prettify the time field or output the raw timestamp, if specified, output the raw format
    """
    if start != None:
        start = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    if end != None:
        end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    resp = search_spl(spl=spl, start=start, end=end, limit=limit)
    table = search_result_output(resp)
    if table is None:
        console.print(f"we cannot find any data")
    else:
        console.print(format_table(table, format, not raw), overflow="fold")


@command
def insert(repo="default", data=None, file=None):
    """Upload data to specified repo

    :param --repo: The target repo
    :param --data: The json string data [{"raw":"this is text", "host": "host-1"}]
    :param --file: Upload json text from file path.
    """
    if repo is None:
        console.print(f"Please specify target repo with --repo")
        return
    if data is None and file is None:
        console.print(f"Please use --data or --file to specify data to upload")
        return

    if file is not None:
        f = open(file)
        data = f.read()

    query_params = {
        "repo": repo,
    }
    resp = request_post("data", json.loads(data), query_params).json()
    console.print(resp, overflow="fold")


@command
def create(asset_type, name=None, data=None, file=None, extra=None):
    """Create asset

    :param asset_type: The target asset type, such as repo, sourcetype ...
    :param -n, --name: The target asset name
    :param --data: The json string data {...}
    :param --file: Upload json text from file path.
    :param -e, --extra: extra args, example:id=1234567890,name=test
    """
    if data is None and file is None:
        content = {}
    else:
        content = data
        if file is not None:
            f = open(file)
            content = f.read()
        try:
            content = json.loads(content)
        except json.JSONDecodeError as e:
            console.print("JSON 解析错误:", e)
            return
    if extra:
        extra_args_map = parse_url_params(extra)
    else:
        extra_args_map = {}
    if 'name' in extra_args_map:
        name = extra_args_map.pop('name')
    req = create_asset_request(asset_type, name, content, **extra_args_map)
    resp = request(req["method"], req["path"], data=req['data']).json()
    console.print(resp, overflow="fold")


@command
def update(asset_type, name=None, operation="update", data=None, file=None, extra=None):
    """Create asset

    :param asset_type: The target asset type, such as repo, sourcetype ...
    :param -n, --name: The target asset name
    :param -d, --data: The json string data {...}
    :param -f, --file: Upload json text from file path.
    :param -o, --operation: operation type, such as open, close, update, delete
    :param -e, --extra: extra args, example:id=1234567890,name=test
    """
    if data is None and file is None:
        data = {}
    else:
        content = data
        if file is not None:
            f = open(file)
            content = f.read()

        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            console.print("JSON 解析错误:", e)
            return
    if extra:
        extra_args_map = parse_url_params(extra)
    else:
        extra_args_map = {}
    if 'name' in extra_args_map:
        name = extra_args_map.pop('name')
    req = update_asset_request(asset_type, operation, name, data, **extra_args_map)
    resp = request(req["method"], req["path"], data=req['data']).json()
    console.print(resp, overflow="fold")


@command
def delete(asset_type, name=None, data=None, file=None, extra=None):
    """Delete asset

    :param --asset_type: The target asset type, such as repo, sourcetype ...
    :param -n, --name: The target asset name or id
    :param -d, --data: The json string data {...}
    :param -f, --file: Upload json text from file path.
    :param -e, --extra: extra args, example:id=1234567890,name=test
    """
    if data is None and file is None:
        data = {}
    else:
        content = data
        if file is not None:
            f = open(file)
            content = f.read()

        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            console.print("JSON 解析错误:", e)
            return

    if extra:
        extra_args_map = parse_url_params(extra)
    else:
        extra_args_map = {}
    if 'name' in extra_args_map:
        name = extra_args_map.pop('name')
    req = delete_asset_request(asset_type, name, data, **extra_args_map)
    resp = request(req["method"], req["path"], data=req['data']).json()
    console.print(resp, overflow="fold")


@command
def rs(type=None, format="table"):
    """Show resource info

    :param -t, --type: The target asset type, such as repo, sourcetype ...
    :param -f, --format: The output format, text, json ...
    """
    resources = get_resources()
    if type is None:
        table = rs_output_all(resources)
    else:
        table = rs_output_one(type, resources.get(type))
    console.print(format_table(table, format=format), overflow="fold")


@command
def mock_data(repo="default", data=None, file=None, number=1):
    """Mock data to specified repo
    :param --repo: The target repo, default: "default"
    :param --data: The json string data default: {"raw":"{{ faker.sentence() }}", "host": "{{ faker.ipv4_private() }}"}
    :param --file: Upload json text from file path.
    :param --number,-n: Number of data, default 1
    """
    if repo is None:
        console.print(f"Please specify target repo with --repo")
        return
    if data is None and file is None:
        console.print(f"Please use --data or --file to specify data to upload")
        return
    if file is not None:
        f = open(file)
        data = f.read()
    query_params = {
        "repo": repo,
    }

    datas = []
    resps = []
    for i in range(number):
        text = template_render(data)
        datas.append(json.loads(text))
        if len(datas) == 100 or i == number - 1:  # 发送条件：达到100条数据或到达最后一个数据
            chunk = datas[:100] if len(datas) > 100 else datas
            resps.append(request_post("data", chunk, query_params).json())
            console.print(f'sent {i + 1} data')
            datas = datas[100:] if len(datas) > 100 else []
    console.print(resps, overflow="fold")


@command
def version():
    _version = importlib.metadata.version('ketacli')
    console.print(_version, overflow="fold")


def start():
    try:
        argcomplete.autocomplete(main.parser)
        main()
    except Exception:
        console.print_exception()


if __name__ == "__main__":
    start()
