from tsuruclient.base import Manager as Base


class Manager(Base):
    """
    Manage pool resources.
    """
    def list(self):
        """
        List pools.
        """
        return self.request("get", "/pools",
            handle_response=lambda response: [] if response.status_code == 204 else response.json())

    def rebalance(self, pool):
        """
        Rebalance a pool.
        """
        data = {"MetadataFilter.pool": pool}
        return self.request("post", "/node/rebalance",
                            data=data, stream=True)
