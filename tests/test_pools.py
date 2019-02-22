from tsuruclient import client

import json
import unittest
import httpretty


class PoolsTestCase(unittest.TestCase):
    def setUp(self):
        self.target = "https://target.example.com"
        self.token = "example-of-token"
        self.client = client.Client(self.target, self.token)
        httpretty.enable()

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def test_list_when_server_return_no_content_status(self):
        url = "{}/pools".format(self.target)
        httpretty.register_uri(httpretty.GET, url, status=204)

        pools = self.client.pools.list()
        
        expected_pools = []
        self.assertListEqual(pools, expected_pools)

    def test_list(self):
        expected_pools = [
            {
                "allowed": {
                    "plans": ["medium"],
                    "router": ["hipache"],
                    "service": ["healthcheck"],
                    "team": ["theoneteam"]
                },
                "default": False,
                "public": True,
                "name": "theonepool",
                "teams": ["theoneteam"]
            }
        ]

        url = "{}/pools".format(self.target)
        httpretty.register_uri(httpretty.GET, url, status=200, body=json.dumps(expected_pools))

        pools = self.client.pools.list()
        
        self.assertListEqual(pools, expected_pools)

    def test_rebalance(self):
        url = "{}/node/rebalance".format(self.target)
        httpretty.register_uri(
            httpretty.POST,
            url,
            body="",
            status=200
        )

        self.client.pools.rebalance("dev")

        result = httpretty.last_request().body.decode('utf-8')
        expected = "MetadataFilter.pool=dev"
        self.assertEqual(expected, result)
