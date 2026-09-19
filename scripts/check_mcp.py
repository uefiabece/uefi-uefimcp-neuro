"""Exercise a real MCP stdio connection without requiring academic content."""
import json
import sys
import tempfile
from pathlib import Path

import anyio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]

async def check():
    config = json.loads((ROOT / 'config/subject.json').read_text(encoding='utf-8'))
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / 'run.py')], cwd=tempfile.gettempdir())
    with anyio.fail_after(30):
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                initialized = await session.initialize()
                assert initialized.serverInfo.name == config['server_name']
                tools = (await session.list_tools()).tools
                assert len(tools) == 11, [tool.name for tool in tools]
                prompts = (await session.list_prompts()).prompts
                assert {prompt.name for prompt in prompts} == {'teach', 'solve'}
                resources = (await session.list_resources()).resources
                for name, args in [('get_syllabus', {}), ('search_content', {'query': 'teste'})]:
                    response = await session.call_tool(name, args)
                    assert not response.isError, response
                    assert response.content
                prompt = await session.get_prompt('teach', {'topic': 'teste'})
                assert config['subject_name'] in prompt.messages[0].content.text
                print(json.dumps({'server': initialized.serverInfo.name, 'protocol': initialized.protocolVersion, 'tools': len(tools), 'prompts': len(prompts), 'resources': len(resources), 'status': 'PASS'}, ensure_ascii=False))

if __name__ == '__main__':
    anyio.run(check)
