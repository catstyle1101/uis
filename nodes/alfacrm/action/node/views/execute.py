from uc_flow_schemas.flow import RunState
from uc_flow_nodes.views import execute

from nodes.alfacrm.action.node.provider.alfacrm import Action
from nodes.alfacrm.action.node.schemas.enums import ActionEnum
from nodes.alfacrm.action.node.schemas.node import NodeRunContext


class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        result: dict = {}
        try:
            action: Action = json.node.data.properties
            request = action.get_request()
            response = await request.execute()
            validated_response = action.validate_response(response)
            content = action.process_content(validated_response)
            result.update(content)

            await json.save_result(result)
            json.state = RunState.complete

        except Exception as e:
            self.log.warning(f'Error {e}')
            await json.save_error(str(e))
            json.state = RunState.error

        return json
