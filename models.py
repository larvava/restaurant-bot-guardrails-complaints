from pydantic import BaseModel


class HandoffData(BaseModel):
    to_agent_name: str
    issue_type: str
    issue_description: str
    reason: str


class InputGuardRailOutput(BaseModel):
    is_off_topic: bool
    is_inappropriate: bool
    reason: str


class MenuOutputGuardRailOutput(BaseModel):
    contains_order_taking: bool
    contains_reservation_details: bool
    contains_internal_info: bool
    reason: str


class OrderOutputGuardRailOutput(BaseModel):
    contains_reservation_details: bool
    contains_complaint_handling: bool
    contains_internal_info: bool
    reason: str


class ReservationOutputGuardRailOutput(BaseModel):
    contains_order_taking: bool
    contains_complaint_handling: bool
    contains_internal_info: bool
    reason: str


class ComplaintsOutputGuardRailOutput(BaseModel):
    contains_order_taking: bool
    contains_reservation_details: bool
    contains_internal_info: bool
    reason: str
