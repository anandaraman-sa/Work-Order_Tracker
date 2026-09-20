from enum import Enum
from typing import List
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


app = FastAPI(
    title="Work Order Tracker API",
    description="API for creating and tracking work orders",
    version="1.0.0"
)


# -------------------------
# Enums
# -------------------------

class WorkOrderStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# -------------------------
# Pydantic Models
# -------------------------

class WorkOrderCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=5, max_length=500)
    assigned_to: str = Field(..., min_length=2, max_length=100)


class WorkOrderStatusUpdate(BaseModel):
    status: WorkOrderStatus


class WorkOrderResponse(BaseModel):
    id: UUID
    title: str
    description: str
    assigned_to: str
    status: WorkOrderStatus


class ErrorResponse(BaseModel):
    error: str
    message: str
    details: list | None = None


# -------------------------
# In-memory database
# -------------------------

work_orders: dict[UUID, WorkOrderResponse] = {}


# -------------------------
# Validation Error Handler
# -------------------------

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "error": "ValidationError",
            "message": "Invalid request data",
            "details": exc.errors()
        }
    )


# -------------------------
# 1. Create Work Order
# -------------------------

@app.post(
    "/work-orders",
    response_model=WorkOrderResponse,
    status_code=status.HTTP_201_CREATED
)
def create_work_order(work_order: WorkOrderCreate):

    work_order_id = uuid4()

    new_work_order = WorkOrderResponse(
        id=work_order_id,
        title=work_order.title,
        description=work_order.description,
        assigned_to=work_order.assigned_to,
        status=WorkOrderStatus.OPEN
    )

    work_orders[work_order_id] = new_work_order

    return new_work_order


# -------------------------
# 2. List All Work Orders
# -------------------------

@app.get(
    "/work-orders",
    response_model=List[WorkOrderResponse]
)
def list_work_orders():

    return list(work_orders.values())


# -------------------------
# 3. Get Work Order By ID
# -------------------------

@app.get(
    "/work-orders/{work_order_id}",
    response_model=WorkOrderResponse
)
def get_work_order(work_order_id: UUID):

    work_order = work_orders.get(work_order_id)

    if work_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "WorkOrderNotFound",
                "message": f"Work order '{work_order_id}' was not found"
            }
        )

    return work_order


# -------------------------
# 4. Update Work Order Status
# -------------------------

@app.patch(
    "/work-orders/{work_order_id}/status",
    response_model=WorkOrderResponse
)
def update_work_order_status(
    work_order_id: UUID,
    status_update: WorkOrderStatusUpdate
):

    work_order = work_orders.get(work_order_id)

    if work_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "WorkOrderNotFound",
                "message": f"Work order '{work_order_id}' was not found"
            }
        )

    updated_work_order = work_order.model_copy(
        update={
            "status": status_update.status
        }
    )

    work_orders[work_order_id] = updated_work_order

    return updated_work_order