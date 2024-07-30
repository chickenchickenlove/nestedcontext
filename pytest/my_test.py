import aiohttp
import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'request_url, expected_status, expected_body',
    [

        ('/api/a1/b1/svc1', 200, 'svc1'),
        ('/api/a2/b1/svc1', 200, 'svc1'),

        ('/api/a1/b1/c1/d1/svc2', 200, 'svc2'),
        ('/api/a2/b1/c1/d1/svc2', 200, 'svc2'),

        ('/api/a1/b1/c1/d1/e1/svc3', 200, 'svc3'),
        ('/api/a1/b1/c1/d1/e2/svc3', 200, 'svc3'),
        ('/api/a2/b1/c1/d1/e1/svc3', 200, 'svc3'),
        ('/api/a2/b1/c1/d1/e2/svc3', 200, 'svc3'),

        ('/api/a1/b1/c1/d1/e1/svc4', 200, 'svc4'),
        ('/api/a1/b1/c1/d1/e2/svc4', 200, 'svc4'),
        ('/api/a2/b1/c1/d1/e1/svc4', 200, 'svc4'),
        ('/api/a2/b1/c1/d1/e2/svc4', 200, 'svc4'),


        ('/api/a1/b1/c1/d1/e1/f1/g1/h1/svc5', 200, 'svc5'),
        ('/api/a1/b1/c1/d1/e2/f1/g1/h1/svc5', 200, 'svc5'),
        ('/api/a2/b1/c1/d1/e1/f1/g1/h1/svc5', 200, 'svc5'),
        ('/api/a2/b1/c1/d1/e2/f1/g1/h1/svc5', 200, 'svc5'),

        # Test Before
        ('/api/a1/b1/c1/d1/e1/f1/g1/i1/svc6', 200, 'svc6'),
        ('/api/a1/b1/c1/d1/e2/f1/g1/i1/svc6', 200, 'svc6'),
        ('/api/a2/b1/c1/d1/e1/f1/g1/i1/svc6', 200, 'svc6'),
        ('/api/a2/b1/c1/d1/e2/f1/g1/i1/svc6', 200, 'svc6'),

        # Test and
        ('/api/second/svc7', 200, 'svc7'),
    ]
)
async def test_nested_context_paths(
        request_url,
        expected_status,
        expected_body):

    async with aiohttp.ClientSession() as s:
        host = 'http://localhost:8080'
        url = host + request_url

        r = await s.get(url=url)

        res_text = await r.text()
        assert r.status ==  expected_status
        assert res_text.startswith(expected_body)
