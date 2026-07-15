import strawberry

from rbac.orders.graphql.inputs import CreateOrderInput, OrderIdInput
from rbac.orders.graphql.payloads import OrderMutationPayload
from rbac.core.graphql.payloads import SimpleMutationPayload
from rbac.orders.services import create_order as create_action
from rbac.orders.services import transition_order as transition_action
from rbac.orders.services import delete_order as delete_action
from rbac.orders.models import Order
from rbac.accounts.selectors import get_current_user
from rbac.authorization.decorators import require_permission
from rbac.core.exceptions import ApplicationError, AppPermissionDeniedError
from rbac.core.graphql.errors import format_application_error


@strawberry.type
class OrderMutation:
    @strawberry.mutation
    @require_permission("orders.add_order")
    def create_order(self, info: strawberry.Info, input: CreateOrderInput) -> OrderMutationPayload:
        current = get_current_user(info)
        if not current or not current.company_id:
            raise AppPermissionDeniedError("No company context.")
        try:
            order = create_action(
                company=current.company,
                created_by=current,
                reference=input.reference,
                notes=input.notes,
                line_items=[
                    {"description": li.description, "quantity": li.quantity, "unit_price": li.unit_price}
                    for li in input.line_items
                ],
            )
            return OrderMutationPayload(success=True, order=order)
        except ApplicationError as e:
            return OrderMutationPayload(success=False, errors=[format_application_error(e)])

    @strawberry.mutation
    @require_permission("orders.submit_order")
    def submit_order(self, info: strawberry.Info, input: OrderIdInput) -> OrderMutationPayload:
        try:
            order = transition_action(order_id=input.order_id, new_status=Order.Status.SUBMITTED)
            return OrderMutationPayload(success=True, order=order)
        except ApplicationError as e:
            return OrderMutationPayload(success=False, errors=[format_application_error(e)])

    @strawberry.mutation
    @require_permission("orders.approve_order")
    def approve_order(self, info: strawberry.Info, input: OrderIdInput) -> OrderMutationPayload:
        try:
            order = transition_action(order_id=input.order_id, new_status=Order.Status.APPROVED)
            return OrderMutationPayload(success=True, order=order)
        except ApplicationError as e:
            return OrderMutationPayload(success=False, errors=[format_application_error(e)])

    @strawberry.mutation
    @require_permission("orders.complete_order")
    def complete_order(self, info: strawberry.Info, input: OrderIdInput) -> OrderMutationPayload:
        try:
            order = transition_action(order_id=input.order_id, new_status=Order.Status.COMPLETED)
            return OrderMutationPayload(success=True, order=order)
        except ApplicationError as e:
            return OrderMutationPayload(success=False, errors=[format_application_error(e)])

    @strawberry.mutation
    @require_permission("orders.cancel_order")
    def cancel_order(self, info: strawberry.Info, input: OrderIdInput) -> OrderMutationPayload:
        try:
            order = transition_action(order_id=input.order_id, new_status=Order.Status.CANCELLED)
            return OrderMutationPayload(success=True, order=order)
        except ApplicationError as e:
            return OrderMutationPayload(success=False, errors=[format_application_error(e)])

    @strawberry.mutation
    @require_permission("orders.delete_order")
    def delete_order(self, info: strawberry.Info, input: OrderIdInput) -> SimpleMutationPayload:
        try:
            delete_action(order_id=input.order_id)
            return SimpleMutationPayload(success=True)
        except ApplicationError as e:
            return SimpleMutationPayload(success=False, errors=[format_application_error(e)])