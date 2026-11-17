class OperationService:

    def __init__(self, cirrus_page):

        self.cirrus_page = cirrus_page

    async def execute(
            self,
            operation_name):

        await self.cirrus_page.select_operation(
            operation_name
        )

        await self.cirrus_page.deploy_operation()