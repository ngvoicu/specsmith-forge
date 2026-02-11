"""Spec, Phase, Task dataclasses."""

from dataclasses import dataclass, field


@dataclass
class Task:
    description: str
    done: bool = False
    is_current: bool = False


@dataclass
class Phase:
    name: str
    status: str  # pending, in-progress, completed, blocked
    tasks: list[Task] = field(default_factory=list)

    @property
    def tasks_done(self) -> int:
        return sum(1 for t in self.tasks if t.done)

    @property
    def tasks_total(self) -> int:
        return len(self.tasks)

    @property
    def current_task(self) -> Task | None:
        for t in self.tasks:
            if t.is_current:
                return t
        return None


@dataclass
class Spec:
    id: str
    title: str
    status: str
    created: str
    updated: str
    priority: str = "medium"
    tags: list[str] = field(default_factory=list)
    phases: list[Phase] = field(default_factory=list)

    @property
    def total_done(self) -> int:
        return sum(p.tasks_done for p in self.phases)

    @property
    def total_tasks(self) -> int:
        return sum(p.tasks_total for p in self.phases)

    @property
    def progress_pct(self) -> float:
        if self.total_tasks == 0:
            return 0.0
        return (self.total_done / self.total_tasks) * 100
