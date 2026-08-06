"""
database/models.py
"""

from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)


from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

from datetime import datetime


class Base(DeclarativeBase):
    pass



# ---------------------------------------------------------
# TestRun Model
# ---------------------------------------------------------

class TestRun(Base):

    __tablename__ = "test_runs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    run_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="Pending",
        nullable=False
    )

    stage: Mapped[str] = mapped_column(
        String(100),
        default="Waiting"
    )

    progress: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    start_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    end_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )

    duration: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    bottleneck: Mapped[str] = mapped_column(
        String(200),
        nullable=True
    )

    confidence: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )

    html_report: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    json_report: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    error_message: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    logs: Mapped[list["ExecutionLog"]] = relationship(
        back_populates="test_run",
        cascade="all, delete-orphan"
    )

    def __repr__(self):

        return (
            f"<TestRun("
            f"id={self.id}, "
            f"run_name='{self.run_name}', "
            f"status='{self.status}'"
            f")>"
        )





class ExecutionLog(Base):

    __tablename__ = "execution_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    run_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("test_runs.id"),
        nullable=False
    )

    level: Mapped[str] = mapped_column(
        String(20),
        default="INFO"
    )

    stage: Mapped[str] = mapped_column(
        String(100)
    )

    message: Mapped[str] = mapped_column(
        String(1000)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )

    test_run: Mapped["TestRun"] = relationship(
        "TestRun",
        back_populates="logs"
    )

    def __repr__(self):

        return (
            f"<ExecutionLog("
            f"id={self.id}, "
            f"run_id={self.run_id}, "
            f"stage='{self.stage}'"
            f")>"
        )