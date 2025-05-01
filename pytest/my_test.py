import aiohttp
import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'request_url, virtual_host, expected_status, expected_body',
    [

        # Depth-1 annotatedService() test
        ('/api/context-path/a1/b1/svc1', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/svc1'),
        ('/api/context-path/a1/b2/svc1', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/svc1'),
        ('/api/context-path/a2/b1/svc1', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/svc1'),
        ('/api/context-path/a2/b2/svc1', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/svc1'),

        # Depth-1 annotatedService() test
        ('/api/context-path/a1/b1/svc2', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/svc2'),
        ('/api/context-path/a1/b2/svc2', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/svc2'),
        ('/api/context-path/a2/b1/svc2', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/svc2'),
        ('/api/context-path/a2/b2/svc2', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/svc2'),

        # Depth-1 service() test
        ('/api/context-path/a1/b1/my-service', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/my-service'),
        ('/api/context-path/a1/b2/my-service', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/my-service'),
        ('/api/context-path/a2/b1/my-service', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/my-service'),
        ('/api/context-path/a2/b2/my-service', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/my-service'),

        # Depth-2 service() test
        ('/api/context-path/a1/b1/c1/my-service1', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/[c1|c2]/my-service1'),
        ('/api/context-path/a1/b1/c2/my-service1', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/[c1|c2]/my-service1'),
        ('/api/context-path/a1/b2/c1/my-service1', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/[c1|c2]/my-service1'),
        ('/api/context-path/a1/b2/c2/my-service1', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/[c1|c2]/my-service1'),
        ('/api/context-path/a2/b1/c1/my-service1', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/[c1|c2]/my-service1'),
        ('/api/context-path/a2/b1/c2/my-service1', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/[c1|c2]/my-service1'),
        ('/api/context-path/a2/b2/c1/my-service1', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/[c1|c2]/my-service1'),
        ('/api/context-path/a2/b2/c2/my-service1', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/[c1|c2]/my-service1'),

        # Depth-2 service() test
        ('/api/context-path/a1/b1/c1/my-service2', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/[c1|c2]/my-service2'),
        ('/api/context-path/a1/b1/c2/my-service2', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/[c1|c2]/my-service2'),
        ('/api/context-path/a1/b2/c1/my-service2', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/[c1|c2]/my-service2'),
        ('/api/context-path/a1/b2/c2/my-service2', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/[c1|c2]/my-service2'),
        ('/api/context-path/a2/b1/c1/my-service2', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/[c1|c2]/my-service2'),
        ('/api/context-path/a2/b1/c2/my-service2', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/[c1|c2]/my-service2'),
        ('/api/context-path/a2/b2/c1/my-service2', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/[c1|c2]/my-service2'),
        ('/api/context-path/a2/b2/c2/my-service2', '', 200, '/api/context-path/[a1|a2]/[b1|b2]/[c1|c2]/my-service2'),

        # Depth-1 another context paths test()
        ('/api/context-path/a1/b3/my-service', '', 200, '/api/context-path/[a1|a2]/[b3|b4]/my-service'),
        ('/api/context-path/a1/b4/my-service', '', 200, '/api/context-path/[a1|a2]/[b3|b4]/my-service'),
        ('/api/context-path/a2/b3/my-service', '', 200, '/api/context-path/[a1|a2]/[b3|b4]/my-service'),
        ('/api/context-path/a2/b4/my-service', '', 200, '/api/context-path/[a1|a2]/[b3|b4]/my-service'),

        # VirtualHost foo.com and Depth-1 service() test
        ('/virtual-foo/a1/my-service1', 'foo.com', 200, 'foo.com /virtual-foo/[a1|a2]/my-service1'),
        ('/virtual-foo/a2/my-service1', 'foo.com', 200, 'foo.com /virtual-foo/[a1|a2]/my-service1'),

        ('/virtual-foo/a1/my-service2', 'foo.com', 200, 'foo.com /virtual-foo/[a1|a2]/my-service2'),
        ('/virtual-foo/a2/my-service2', 'foo.com', 200, 'foo.com /virtual-foo/[a1|a2]/my-service2'),

        # VirtualHost foo.com and Depth-1 annotatedService() test
        ('/virtual-foo/a1/svc1', 'foo.com', 200, 'foo.com /virtual-foo/[a1|a2]/svc1'),
        ('/virtual-foo/a2/svc1', 'foo.com', 200, 'foo.com /virtual-foo/[a1|a2]/svc1'),

        ('/virtual-foo/a1/svc2', 'foo.com', 200, 'foo.com /virtual-foo/[a1|a2]/svc2'),
        ('/virtual-foo/a2/svc2', 'foo.com', 200, 'foo.com /virtual-foo/[a1|a2]/svc2'),

        # VirtualHost foo.com and Depth-2 annotatedService() test
        ('/virtual-foo/a1/b1/my-service', 'foo.com', 200, 'foo.com /virtual-foo/[a1|a2]/[b1|b2]/my-service'),
        ('/virtual-foo/a1/b2/my-service', 'foo.com', 200, 'foo.com /virtual-foo/[a1|a2]/[b1|b2]/my-service'),
        ('/virtual-foo/a2/b1/my-service', 'foo.com', 200, 'foo.com /virtual-foo/[a1|a2]/[b1|b2]/my-service'),
        ('/virtual-foo/a2/b2/my-service', 'foo.com', 200, 'foo.com /virtual-foo/[a1|a2]/[b1|b2]/my-service'),



        # VirtualHost foo.com and Depth-1 service() test
        ('/virtual-foooo/a1/my-service1', 'foooo.com', 200, 'foooo.com /virtual-foooo/[a1|a2]/my-service1'),
        ('/virtual-foooo/a2/my-service1', 'foooo.com', 200, 'foooo.com /virtual-foooo/[a1|a2]/my-service1'),

        ('/virtual-foooo/a1/my-service2', 'foooo.com', 200, 'foooo.com /virtual-foooo/[a1|a2]/my-service2'),
        ('/virtual-foooo/a2/my-service2', 'foooo.com', 200, 'foooo.com /virtual-foooo/[a1|a2]/my-service2'),

        # VirtualHost foo.com and Depth-1 annotatedService() test
        ('/virtual-foooo/a1/svc1', 'foooo.com', 200, 'foooo.com /virtual-foooo/[a1|a2]/svc1'),
        ('/virtual-foooo/a2/svc1', 'foooo.com', 200, 'foooo.com /virtual-foooo/[a1|a2]/svc1'),

        ('/virtual-foooo/a1/svc2', 'foooo.com', 200, 'foooo.com /virtual-foooo/[a1|a2]/svc2'),
        ('/virtual-foooo/a2/svc2', 'foooo.com', 200, 'foooo.com /virtual-foooo/[a1|a2]/svc2'),

        # VirtualHost foo.com and Depth-2 annotatedService() test
        ('/virtual-foooo/a1/b1/my-service', 'foooo.com', 200, 'foooo.com /virtual-foooo/[a1|a2]/[b1|b2]/my-service'),
        ('/virtual-foooo/a1/b2/my-service', 'foooo.com', 200, 'foooo.com /virtual-foooo/[a1|a2]/[b1|b2]/my-service'),
        ('/virtual-foooo/a2/b1/my-service', 'foooo.com', 200, 'foooo.com /virtual-foooo/[a1|a2]/[b1|b2]/my-service'),
        ('/virtual-foooo/a2/b2/my-service', 'foooo.com', 200, 'foooo.com /virtual-foooo/[a1|a2]/[b1|b2]/my-service'),



        # Other - Depth1
        ('/api/context-path1000/a1/svc1000', '', 200, "/api/context-path1000/[a1|a2]/svc1000"),
        ('/api/context-path1000/a2/svc1000', '', 200, "/api/context-path1000/[a1|a2]/svc1000"),

        ### Other - Depth2
        ('/api/context-path1000/a1/b1/svc2000', '', 200, "/api/context-path1000/[a1|a2]/[b1|b2]/svc2000"),
        ('/api/context-path1000/a1/b2/svc2000', '', 200, "/api/context-path1000/[a1|a2]/[b1|b2]/svc2000"),
        ('/api/context-path1000/a2/b1/svc2000', '', 200, "/api/context-path1000/[a1|a2]/[b1|b2]/svc2000"),
        ('/api/context-path1000/a2/b2/svc2000', '', 200, "/api/context-path1000/[a1|a2]/[b1|b2]/svc2000"),

        ('/api/context-path1000/a1/b3/svc2001', '', 200, "/api/context-path1000/[a1|a2]/[b3|b4]/svc2001"),
        ('/api/context-path1000/a1/b4/svc2001', '', 200, "/api/context-path1000/[a1|a2]/[b3|b4]/svc2001"),
        ('/api/context-path1000/a2/b3/svc2001', '', 200, "/api/context-path1000/[a1|a2]/[b3|b4]/svc2001"),
        ('/api/context-path1000/a2/b4/svc2001', '', 200, "/api/context-path1000/[a1|a2]/[b3|b4]/svc2001"),

        ('/api/context-path1000/a1/b5/svc1', '', 200, "/api/context-path1000/[a1|a2]/[b5|b6]/svc1"),
        ('/api/context-path1000/a1/b6/svc1', '', 200, "/api/context-path1000/[a1|a2]/[b5|b6]/svc1"),
        ('/api/context-path1000/a2/b5/svc1', '', 200, "/api/context-path1000/[a1|a2]/[b5|b6]/svc1"),
        ('/api/context-path1000/a2/b6/svc1', '', 200, "/api/context-path1000/[a1|a2]/[b5|b6]/svc1"),

        ('/api/context-path1000/a1/b5/svc2', '', 200, "/api/context-path1000/[a1|a2]/[b5|b6]/svc2"),
        ('/api/context-path1000/a1/b6/svc2', '', 200, "/api/context-path1000/[a1|a2]/[b5|b6]/svc2"),
        ('/api/context-path1000/a2/b5/svc2', '', 200, "/api/context-path1000/[a1|a2]/[b5|b6]/svc2"),
        ('/api/context-path1000/a2/b6/svc2', '', 200, "/api/context-path1000/[a1|a2]/[b5|b6]/svc2"),

    ]
)
async def test_nested_context_paths(
        request_url,
        virtual_host,
        expected_status,
        expected_body):

    async with aiohttp.ClientSession() as s:
        # Given
        host = 'http://localhost:8080'
        url = host + request_url

        headers = {}
        if virtual_host:
            headers = {
                'Host': virtual_host
            }

        # When
        r = await s.get(url=url, headers=headers)

        # Then
        res_text = await r.text()
        assert r.status ==  expected_status
        assert res_text.startswith(expected_body)
