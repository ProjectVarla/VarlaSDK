from __future__ import annotations

from functools import cached_property
from typing import Generic, TypeVar

from pydantic import BaseModel, computed_field

from . import VarlaPolicy

VarlaPolicyType = TypeVar("VarlaPolicyType", bound=VarlaPolicy)


class VarlaPolicyBundle(BaseModel, Generic[VarlaPolicyType]):
    policies: set[VarlaPolicyType]

    @computed_field
    @cached_property
    def policies_bundle(self) -> int:
        value = 0
        for policy in self.policies:
            value |= policy.value
        return value

    @computed_field
    def type(self) -> str:
        return self.__class__.__name__.split("[")[1].split("]")[0]

    def __str__(self) -> str:

        return (
            super().__repr__()
            + "\n╔═╡ Varla Debug ╞════════════════════════════════════════════╡\n"
            + "║\n"
            + f"╚═╡[{self.__class__.__base__.__name__}] of type [{self.type}] \n\tPolicies:\n\t- "
            + "\n\t- ".join([policy.type for policy in self.policies])
        )

    def __add__(
        self, other: VarlaPolicyBundle[VarlaPolicyType]
    ) -> VarlaPolicyBundle[VarlaPolicyType]:
        return VarlaPolicyBundle[self.type](
            policies=[*(self.policies | other.policies)]
        )

    def hasAccessTo(self, policy: VarlaPolicyType) -> bool:
        return (self.policies_bundle & policy.value) == policy.value
